#!/usr/bin/env python3
"""
Inference script for Emergency Mesh-Network Router.
Demonstrates agent evaluation on the environment using OpenEnv standards.

Required format for hackathon:
[START] task=... env=... model=...
[STEP] step=1 action=... reward=0.00 done=false error=null
[END] success=true steps=3 score=1.00 rewards=...
"""

import json
import argparse
import time
from typing import Optional

from server.environment import MeshNetworkEnvironment, TaskGrader
from agents.agents import RandomAgent, GreedyAgent, IntelligentAgent, ConservativeAgent, ExplorativeAgent
from models import TaskDifficulty, MeshAction


def run_inference(
    task: str = "easy",
    agent_name: str = "greedy",
    n_episodes: int = 1,
    max_steps: int = 50,
    seed: Optional[int] = None,
    verbose: bool = True
) -> dict:
    """
    Run inference with specified agent on task.
    
    Args:
        task: "easy", "medium", or "hard"
        agent_name: "random", "greedy", "intelligent", "conservative", "explorative"
        n_episodes: Number of episodes to run
        max_steps: Max steps per episode
        seed: Random seed for reproducibility
        verbose: Print [START], [STEP], [END] format
        
    Returns:
        Results dictionary with stats
    """
    # Map task to difficulty
    difficulty_map = {
        "easy": TaskDifficulty.EASY,
        "medium": TaskDifficulty.MEDIUM,
        "hard": TaskDifficulty.HARD,
    }
    
    if task not in difficulty_map:
        print(f"[ERROR] Unknown task: {task}")
        return {}
    
    difficulty = difficulty_map[task]
    
    # Create environment
    env = MeshNetworkEnvironment(difficulty)
    
    # Create agent
    agents_map = {
        "random": RandomAgent(),
        "greedy": GreedyAgent(),
        "intelligent": IntelligentAgent(),
        "conservative": ConservativeAgent(),
        "explorative": ExplorativeAgent(),
    }
    
    if agent_name not in agents_map:
        print(f"[ERROR] Unknown agent: {agent_name}")
        return {}
    
    agent = agents_map[agent_name]
    
    # Print start
    if verbose:
        print(f"[START] task={task} env=emergency-mesh-router model={agent_name}")
    
    # Run episodes
    total_reward = 0.0
    total_steps = 0
    successes = 0
    episode_rewards = []
    
    for episode in range(n_episodes):
        obs = env.reset(seed=seed)
        episode_reward = 0.0
        step_count = 0
        done = False
        error = None
        
        for step in range(max_steps):
            step_count += 1
            
            try:
                # Agent decides action
                action = agent.act(obs)
                
                # Take step
                obs, reward, done, info = env.step(action)
                episode_reward += reward
                
                if verbose and step < 5:  # Print first 5 steps
                    print(f"[STEP] step={step + 1} action={action.target_device_id} reward={reward:.2f} done={done} error=null")
                
                if done:
                    break
                    
            except Exception as e:
                error = str(e)
                if verbose:
                    print(f"[STEP] step={step + 1} action=null reward=0.00 done=true error={error}")
                break
        
        # Track results
        total_reward += episode_reward
        total_steps += step_count
        episode_rewards.append(episode_reward)
        
        if env.success:
            successes += 1
    
    # Calculate stats
    success_rate = successes / n_episodes if n_episodes > 0 else 0.0
    avg_reward = total_reward / n_episodes if n_episodes > 0 else 0.0
    avg_steps = total_steps / n_episodes if n_episodes > 0 else 0.0
    
    # Normalize score to [0, 1]
    score = min(1.0, max(0.0, success_rate + (avg_reward / 10.0)))
    
    # Print end
    if verbose:
        print(f"[END] success={successes > 0} steps={total_steps} score={score:.2f} rewards={total_reward:.2f}")
    
    return {
        "task": task,
        "agent": agent_name,
        "episodes": n_episodes,
        "successes": successes,
        "success_rate": success_rate,
        "total_reward": total_reward,
        "average_reward": avg_reward,
        "average_steps": avg_steps,
        "score": score,
        "episode_rewards": episode_rewards,
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run inference on Emergency Mesh-Network Router environment"
    )
    parser.add_argument("--task", default="easy", choices=["easy", "medium", "hard"])
    parser.add_argument("--agent", default="greedy", 
                       choices=["random", "greedy", "intelligent", "conservative", "explorative"])
    parser.add_argument("--episodes", type=int, default=5)
    parser.add_argument("--max-steps", type=int, default=50)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--verbose", action="store_true", default=True)
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Run inference
    results = run_inference(
        task=args.task,
        agent_name=args.agent,
        n_episodes=args.episodes,
        max_steps=args.max_steps,
        seed=args.seed,
        verbose=not args.json
    )
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("\n" + "="*60)
        print("INFERENCE RESULTS")
        print("="*60)
        print(f"Task:             {results['task']}")
        print(f"Agent:            {results['agent']}")
        print(f"Episodes:         {results['episodes']}")
        print(f"Successes:        {results['successes']}/{results['episodes']}")
        print(f"Success Rate:     {results['success_rate']:.2%}")
        print(f"Average Reward:   {results['average_reward']:.2f}")
        print(f"Average Steps:    {results['average_steps']:.2f}")
        print(f"Total Reward:     {results['total_reward']:.2f}")
        print(f"Score:            {results['score']:.2f}")
        print("="*60)


if __name__ == "__main__":
    main()
