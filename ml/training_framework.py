"""
Advanced training and evaluation framework for Emergency Mesh-Network Router.
Supports multiple agents, curriculum learning, and comprehensive evaluation.
"""

import sys
import os
import json
import time
from typing import Dict, List, Tuple
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.environment import MeshNetworkEnvironment, TaskGrader
from models import TaskDifficulty, MeshAction
from agents.agents import RandomAgent, GreedyAgent, IntelligentAgent, ConservativeAgent, ExplorativeAgent
from agents.advanced_agents import NeuralNetworkAgent, DQNAgent, PPOAgent, AdaptiveAgent
from ml.enhanced_environment import DynamicNetworkEnvironment, EnvironmentFeature
from ml.metrics_dashboard import MetricsCollector, VisualizationGenerator


class TrainingFramework:
    """Advanced training and hyperparameter optimization framework."""
    
    def __init__(self, output_dir: str = "training_results"):
        """Initialize training framework."""
        self.output_dir = output_dir
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def train_agent_curriculum(self, agent, max_episodes: int = 100,
                              difficulties: List[str] = None) -> Dict:
        """
        Train agent using curriculum learning.
        Start easy, progressively increase difficulty.
        
        Args:
            agent: Agent to train
            max_episodes: Total episodes across all difficulties
            difficulties: Order of difficulties (easy -> medium -> hard)
            
        Returns:
            Training results and metrics
        """
        if difficulties is None:
            difficulties = ["easy", "medium", "hard"]
        
        results = {
            "agent_name": agent.__class__.__name__,
            "training_type": "curriculum",
            "total_episodes": max_episodes,
            "difficulties": difficulties,
            "episodes_per_difficulty": max_episodes // len(difficulties),
            "results": {}
        }
        
        episodes_per_diff = max_episodes // len(difficulties)
        
        print(f"\n🎓 Curriculum Learning for {agent.__class__.__name__}")
        print(f"   Total: {max_episodes} episodes")
        print(f"   Per difficulty: {episodes_per_diff}")
        print(f"   Sequence: {' → '.join(difficulties)}\n")
        
        for difficulty_str in difficulties:
            difficulty = TaskDifficulty(difficulty_str)
            env = MeshNetworkEnvironment(difficulty)
            
            successes = 0
            total_reward = 0.0
            total_hops = 0
            episode_times = []
            
            print(f"   Training on {difficulty_str.upper()}...")
            
            for episode in range(episodes_per_diff):
                obs = env.reset(seed=episode)
                done = False
                episode_reward = 0.0
                
                start_time = time.time()
                
                while not done and env.current_hop < env.max_hops:
                    action = agent.act(obs)
                    obs, reward, done, info = env.step(action)
                    episode_reward += reward
                
                elapsed = time.time() - start_time
                episode_times.append(elapsed)
                
                total_reward += episode_reward
                total_hops += env.current_hop
                if env.success:
                    successes += 1
            
            difficulty_results = {
                "episodes": episodes_per_diff,
                "successes": successes,
                "success_rate": successes / episodes_per_diff,
                "average_reward": total_reward / episodes_per_diff,
                "average_hops": total_hops / episodes_per_diff,
                "average_time_sec": sum(episode_times) / len(episode_times),
            }
            
            results["results"][difficulty_str] = difficulty_results
            
            print(f"      ✅ Success Rate: {difficulty_results['success_rate']:.1%}")
            print(f"      📊 Avg Reward: {difficulty_results['average_reward']:.4f}")
            print(f"      ⏱️  Avg Time: {difficulty_results['average_time_sec']:.3f}s")
        
        return results
    
    def evaluate_agent_suite(self, agents: Dict, n_episodes: int = 10) -> Dict:
        """
        Comprehensive evaluation of multiple agents.
        
        Args:
            agents: Dict of {name: agent} pairs
            n_episodes: Episodes per task
            
        Returns:
            Detailed comparison results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "n_episodes": n_episodes,
            "agents": {}
        }
        
        print("\n" + "="*70)
        print("🏆 COMPREHENSIVE AGENT EVALUATION SUITE")
        print("="*70)
        
        for agent_name, agent in agents.items():
            print(f"\n📊 Evaluating: {agent_name}")
            print("-" * 70)
            
            agent_results = {
                "name": agent_name,
                "class": agent.__class__.__name__,
                "difficulties": {}
            }
            
            for difficulty in ["easy", "medium", "hard"]:
                env = MeshNetworkEnvironment(TaskDifficulty(difficulty))
                grader = TaskGrader(n_episodes=n_episodes)
                
                # Create wrapper function for grader
                def agent_wrapper(obs):
                    return agent.act(obs)
                
                grade_result = grader.grade_task(agent_wrapper, TaskDifficulty(difficulty))
                
                agent_results["difficulties"][difficulty] = {
                    "score": grade_result.score,
                    "success_rate": grade_result.success_rate,
                    "average_hops": grade_result.average_hops,
                    "average_reward": grade_result.average_reward,
                }
                
                print(f"   {difficulty.upper():8} | "
                      f"Score: {grade_result.score:.2f} | "
                      f"Success: {grade_result.success_rate:.1%} | "
                      f"Reward: {grade_result.average_reward:.4f}")
            
            # Calculate aggregate metrics
            all_scores = [v["score"] for v in agent_results["difficulties"].values()]
            all_success = [v["success_rate"] for v in agent_results["difficulties"].values()]
            
            agent_results["aggregate"] = {
                "average_score": sum(all_scores) / len(all_scores),
                "average_success_rate": sum(all_success) / len(all_success),
            }
            
            results["agents"][agent_name] = agent_results
        
        # Ranking
        print("\n" + "="*70)
        print("🏅 FINAL RANKINGS")
        print("="*70)
        
        ranked = sorted(
            results["agents"].items(),
            key=lambda x: x[1]["aggregate"]["average_score"],
            reverse=True
        )
        
        for rank, (name, data) in enumerate(ranked, 1):
            print(f"{rank}. {name:20} | "
                  f"Score: {data['aggregate']['average_score']:.3f} | "
                  f"Avg Success: {data['aggregate']['average_success_rate']:.1%}")
        
        return results
    
    def evaluate_with_dynamic_features(self, agent, features: List[str],
                                      n_episodes: int = 5) -> Dict:
        """
        Evaluate agent performance with dynamic environment features.
        
        Args:
            agent: Agent to evaluate
            features: List of features to enable
            n_episodes: Episodes to run
            
        Returns:
            Performance metrics with each feature combination
        """
        results = {
            "agent": agent.__class__.__name__,
            "features": features,
            "episodes": n_episodes,
            "results": {}
        }
        
        print(f"\n🌐 Dynamic Environment Evaluation")
        print(f"   Agent: {agent.__class__.__name__}")
        print(f"   Features: {', '.join(features)}")
        
        # Convert string features to EnvironmentFeature enums
        feature_enums = [EnvironmentFeature(f) for f in features]
        
        env = DynamicNetworkEnvironment(TaskDifficulty.HARD, features=feature_enums)
        
        successes = 0
        total_reward = 0.0
        
        for episode in range(n_episodes):
            obs = env.reset(seed=episode)
            done = False
            episode_reward = 0.0
            
            while not done and env.step_count < 50:
                action = agent.act(obs)
                obs, reward, done, info = env.step(action)
                episode_reward += reward
            
            total_reward += episode_reward
            if env.success:
                successes += 1
        
        results["results"] = {
            "success_rate": successes / n_episodes,
            "average_reward": total_reward / n_episodes,
            "successes": successes,
        }
        
        print(f"   Success Rate: {results['results']['success_rate']:.1%}")
        print(f"   Avg Reward: {results['results']['average_reward']:.4f}")
        
        return results
    
    def save_results(self, results: Dict, filename: str = None):
        """Save results to JSON file."""
        if filename is None:
            filename = f"evaluation_{self.timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {filepath}")


def main():
    """Main entry point for training and evaluation."""
    
    print("\n" + "="*70)
    print("🚀 Advanced Training and Evaluation Framework")
    print("="*70)
    
    # Initialize framework
    framework = TrainingFramework()
    
    # Create agent suite
    agents = {
        "Random": RandomAgent(),
        "Greedy": GreedyAgent(),
        "Intelligent": IntelligentAgent(),
        "Conservative": ConservativeAgent(),
        "Explorative": ExplorativeAgent(),
        "Neural Network": NeuralNetworkAgent(),
        "DQN": DQNAgent(),
        "PPO": PPOAgent(),
        "Adaptive": AdaptiveAgent(),
    }
    
    # 1. Comprehensive Evaluation
    print("\n1️⃣  Running Comprehensive Agent Evaluation...")
    eval_results = framework.evaluate_agent_suite(agents, n_episodes=3)
    framework.save_results(eval_results, f"evaluation_{framework.timestamp}.json")
    
    # 2. Curriculum Learning
    print("\n2️⃣  Running Curriculum Learning for Top Agents...")
    for agent_name in ["Greedy", "Intelligent", "Adaptive"]:
        curriculum_results = framework.train_agent_curriculum(
            agents[agent_name],
            max_episodes=30,
            difficulties=["easy", "medium", "hard"]
        )
        framework.save_results(curriculum_results, f"curriculum_{agent_name}_{framework.timestamp}.json")
    
    # 3. Dynamic Features Evaluation
    print("\n3️⃣  Running Dynamic Features Evaluation...")
    dynamic_features = ["dynamic_obstacles", "rf_interference", "node_failures"]
    dynamic_results = framework.evaluate_with_dynamic_features(
        agents["Adaptive"],
        features=dynamic_features,
        n_episodes=5
    )
    framework.save_results(dynamic_results, f"dynamic_{framework.timestamp}.json")
    
    print("\n" + "="*70)
    print("✅ Training and Evaluation Complete!")
    print("="*70)
    print(f"\n📁 Results folder: {framework.output_dir}/")


if __name__ == "__main__":
    main()
