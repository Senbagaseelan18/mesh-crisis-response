"""
Performance benchmarking suite for Emergency Mesh-Network Router.
Measures latency, throughput, memory usage, and scalability.
"""

import time
import sys
import os
import psutil
import json
from datetime import datetime
from typing import Dict, List
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.environment import MeshNetworkEnvironment, TaskGrader
from models import TaskDifficulty, MeshAction
from agents.agents import RandomAgent, GreedyAgent, IntelligentAgent
from agents.advanced_agents import NeuralNetworkAgent, DQNAgent, PPOAgent, AdaptiveAgent


class BenchmarkResult:
    """Stores benchmark metrics."""
    
    def __init__(self, name: str, task: str, iterations: int):
        self.name = name
        self.task = task
        self.iterations = iterations
        self.execution_times = []
        self.memory_usage = []
        self.success_rate = 0.0
        self.avg_reward = 0.0
        self.throughput_eps = 0.0


class PerformanceBenchmark:
    """Comprehensive performance benchmarking suite."""
    
    def __init__(self):
        """Initialize benchmarking suite."""
        self.results: List[BenchmarkResult] = []
        self.start_time = None
    
    def benchmark_environment_creation(self, iterations: int = 100) -> BenchmarkResult:
        """Benchmark environment initialization speed."""
        result = BenchmarkResult("Environment Creation", "all", iterations)
        
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            env = MeshNetworkEnvironment(TaskDifficulty.MEDIUM)
            obs = env.reset()
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms
        
        result.execution_times = times
        result.throughput_eps = 1000 / np.mean(times)  # Episodes per second
        
        print(f"✅ Environment Creation Benchmark:")
        print(f"   Mean:    {np.mean(times):.2f} ms")
        print(f"   Std:     {np.std(times):.2f} ms")
        print(f"   Min:     {np.min(times):.2f} ms")
        print(f"   Max:     {np.max(times):.2f} ms")
        print(f"   Throughput: {result.throughput_eps:.1f} environments/sec")
        
        return result
    
    def benchmark_agent_action(self, agent_name: str, agent, iterations: int = 100) -> BenchmarkResult:
        """Benchmark agent action selection."""
        result = BenchmarkResult(f"Agent: {agent_name}", "all", iterations)
        
        env = MeshNetworkEnvironment(TaskDifficulty.MEDIUM)
        obs = env.reset(seed=42)
        
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            action = agent.act(obs)
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms
        
        result.execution_times = times
        result.throughput_eps = 1000 / np.mean(times)  # Actions per second
        
        print(f"✅ Agent {agent_name} Benchmark:")
        print(f"   Mean:    {np.mean(times):.4f} ms")
        print(f"   Std:     {np.std(times):.4f} ms")
        print(f"   Min:     {np.min(times):.4f} ms")
        print(f"   Max:     {np.max(times):.4f} ms")
        print(f"   Throughput: {result.throughput_eps:.0f} actions/sec")
        
        return result
    
    def benchmark_episode(self, agent_name: str, agent, difficulty: str, 
                         iterations: int = 10) -> BenchmarkResult:
        """Benchmark full episode execution."""
        result = BenchmarkResult(f"Episode: {agent_name}", difficulty, iterations)
        
        task_difficulty = TaskDifficulty(difficulty)
        successes = 0
        total_reward = 0.0
        times = []
        
        for i in range(iterations):
            env = MeshNetworkEnvironment(task_difficulty)
            obs = env.reset(seed=i)
            done = False
            
            start = time.perf_counter()
            
            while not done and env.current_hop < env.max_hops:
                action = agent.act(obs)
                obs, reward, done, info = env.step(action)
                total_reward += reward
            
            end = time.perf_counter()
            times.append((end - start) * 1000)
            
            if env.success:
                successes += 1
        
        result.execution_times = times
        result.success_rate = successes / iterations
        result.avg_reward = total_reward / iterations
        result.throughput_eps = iterations / (sum(times) / 1000)
        
        print(f"✅ Episode {agent_name} ({difficulty}):")
        print(f"   Mean Duration:  {np.mean(times):.2f} ms")
        print(f"   Total Time:     {sum(times)/1000:.2f} sec")
        print(f"   Success Rate:   {result.success_rate:.1%}")
        print(f"   Avg Reward:     {result.avg_reward:.4f}")
        print(f"   Throughput:     {result.throughput_eps:.1f} episodes/sec")
        
        return result
    
    def benchmark_memory_usage(self, agent_name: str, agent, episodes: int = 100) -> Dict:
        """Benchmark memory usage during episodes."""
        process = psutil.Process()
        
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        env = MeshNetworkEnvironment(TaskDifficulty.HARD)
        
        for i in range(episodes):
            obs = env.reset(seed=i)
            done = False
            
            while not done:
                action = agent.act(obs)
                obs, reward, done, info = env.step(action)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        peak_memory = process.memory_info().rss / 1024 / 1024  # Would need tracemalloc for true peak
        
        memory_increase = final_memory - initial_memory
        
        print(f"✅ Memory Usage {agent_name} ({episodes} episodes):")
        print(f"   Initial:    {initial_memory:.2f} MB")
        print(f"   Final:      {final_memory:.2f} MB")
        print(f"   Increase:   {memory_increase:.2f} MB")
        print(f"   Per Episode: {memory_increase/max(1, episodes):.4f} MB")
        
        return {
            "initial_mb": initial_memory,
            "final_mb": final_memory,
            "increase_mb": memory_increase,
            "per_episode_mb": memory_increase / max(1, episodes),
        }
    
    def benchmark_scalability(self) -> Dict:
        """Benchmark scalability across different network sizes."""
        results = {}
        
        for difficulty in [TaskDifficulty.EASY, TaskDifficulty.MEDIUM, TaskDifficulty.HARD]:
            env = MeshNetworkEnvironment(difficulty)
            agent = GreedyAgent()
            
            times = []
            rewards = []
            
            for _ in range(5):
                obs = env.reset()
                done = False
                episode_reward = 0.0
                
                start = time.perf_counter()
                
                while not done and env.current_hop < env.max_hops:
                    action = agent.act(obs)
                    obs, reward, done, info = env.step(action)
                    episode_reward += reward
                
                end = time.perf_counter()
                times.append(end - start)
                rewards.append(episode_reward)
            
            results[difficulty.value] = {
                "avg_time_sec": np.mean(times),
                "avg_reward": np.mean(rewards),
                "num_devices": len(env.device_map),
                "max_hops": env.max_hops,
            }
            
            print(f"✅ Scalability {difficulty.value}:")
            print(f"   Devices: {len(env.device_map)}")
            print(f"   Avg Time: {np.mean(times):.3f} sec")
            print(f"   Avg Reward: {np.mean(rewards):.4f}")
        
        return results
    
    def run_full_benchmark(self):
        """Run complete benchmark suite."""
        print("\n" + "="*70)
        print("🏁 PERFORMANCE BENCHMARK SUITE - Emergency Mesh-Network Router")
        print("="*70 + "\n")
        
        self.start_time = time.time()
        
        # 1. Environment Creation
        print("📊 1. Environment Creation Benchmark")
        print("-" * 70)
        self.benchmark_environment_creation(iterations=100)
        
        # 2. Agent Performance
        print("\n📊 2. Agent Performance Benchmarks")
        print("-" * 70)
        
        agents = {
            "Random": RandomAgent(),
            "Greedy": GreedyAgent(),
            "Intelligent": IntelligentAgent(),
            "Neural Network": NeuralNetworkAgent(),
            "DQN": DQNAgent(),
            "PPO": PPOAgent(),
        }
        
        for agent_name, agent in agents.items():
            self.benchmark_agent_action(agent_name, agent, iterations=100)
        
        # 3. Full Episode Benchmarks
        print("\n📊 3. Full Episode Benchmarks")
        print("-" * 70)
        
        for difficulty in ["easy", "medium", "hard"]:
            for agent_name, agent in list(agents.items())[:3]:  # Top 3 agents
                self.benchmark_episode(agent_name, agent, difficulty, iterations=5)
        
        # 4. Memory Usage
        print("\n📊 4. Memory Usage Benchmarks")
        print("-" * 70)
        
        for agent_name in ["Greedy", "Intelligent"]:
            self.benchmark_memory_usage(agent_name, agents[agent_name], episodes=50)
        
        # 5. Scalability
        print("\n📊 5. Scalability Analysis")
        print("-" * 70)
        
        scalability_results = self.benchmark_scalability()
        
        # Summary
        elapsed = time.time() - self.start_time
        print("\n" + "="*70)
        print(f"✅ BENCHMARK COMPLETE (Total time: {elapsed:.1f}sec)")
        print("="*70 + "\n")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_time_sec": elapsed,
            "scalability_results": scalability_results,
        }


def main():
    """Main entry point for benchmarking."""
    benchmark = PerformanceBenchmark()
    results = benchmark.run_full_benchmark()
    
    # Save results
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("📁 Results saved to: benchmark_results.json")


if __name__ == "__main__":
    main()
