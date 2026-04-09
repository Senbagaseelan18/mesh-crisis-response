"""
Grader implementations for Emergency Mesh-Network Router environment
Provides concrete grader classes for task evaluation
"""

from abc import ABC, abstractmethod
from typing import Callable, Dict, Any
from models import MeshObservation, MeshAction, TaskDifficulty, TaskGradeResult


class BaseGrader(ABC):
    """Base class for all graders"""
    
    @abstractmethod
    def grade(self, agent_fn: Callable, environment, n_episodes: int = 10) -> Dict[str, Any]:
        """
        Grade an agent on the environment
        
        Args:
            agent_fn: Function that takes observation and returns action
            environment: Environment to grade on
            n_episodes: Number of episodes to run
            
        Returns:
            Dictionary with grading results
        """
        pass


class RewardThresholdGrader(BaseGrader):
    """
    Grades agents based on reward thresholds.
    Evaluates if agents can reach minimum reward targets.
    """
    
    def __init__(self, min_reward: float = 0.0, max_reward: float = 1.0, success_threshold: float = 0.5):
        """
        Initialize reward threshold grader
        
        Args:
            min_reward: Minimum possible reward
            max_reward: Maximum possible reward
            success_threshold: Threshold for task success (0.0-1.0)
        """
        self.min_reward = min_reward
        self.max_reward = max_reward
        self.success_threshold = success_threshold
    
    def grade(self, agent_fn: Callable, environment, n_episodes: int = 10) -> Dict[str, Any]:
        """Grade agent based on reward thresholds"""
        total_reward = 0.0
        successes = 0
        total_hops = 0
        
        for episode in range(n_episodes):
            obs = environment.reset(seed=episode)
            done = False
            
            while not done and environment.current_hop < environment.max_hops:
                action = agent_fn(obs)
                obs, reward, done, info = environment.step(action)
            
            total_reward += environment.episode_reward
            if environment.success:
                successes += 1
            total_hops += environment.current_hop
        
        success_rate = successes / n_episodes
        avg_reward = total_reward / n_episodes
        
        # Normalize reward to [0, 1]
        if self.max_reward > self.min_reward:
            normalized_reward = (avg_reward - self.min_reward) / (self.max_reward - self.min_reward)
        else:
            normalized_reward = 0.0
        
        # Score = 70% success rate + 30% reward achievement
        score = 0.7 * success_rate + 0.3 * max(0, min(1, normalized_reward))
        score = max(0.0, min(1.0, score))
        
        # Success = score meets threshold
        is_success = score >= self.success_threshold
        
        return {
            "score": score,
            "success": is_success,
            "success_rate": success_rate,
            "average_reward": avg_reward,
            "average_hops": total_hops / n_episodes if successes > 0 else 0,
            "details": f"Score: {score:.2f}, Success: {successes}/{n_episodes}, AvgReward: {avg_reward:.2f}"
        }


class EfficientGrader(BaseGrader):
    """
    Grades agents on efficiency metrics.
    Focuses on minimizing hops while achieving success.
    """
    
    def __init__(self, success_threshold: float = 0.6):
        self.success_threshold = success_threshold
    
    def grade(self, agent_fn: Callable, environment, n_episodes: int = 10) -> Dict[str, Any]:
        """Grade agent on efficiency"""
        total_reward = 0.0
        successes = 0
        total_hops = 0
        
        for episode in range(n_episodes):
            obs = environment.reset(seed=episode)
            done = False
            
            while not done and environment.current_hop < environment.max_hops:
                action = agent_fn(obs)
                obs, reward, done, info = environment.step(action)
            
            total_reward += environment.episode_reward
            if environment.success:
                successes += 1
            total_hops += environment.current_hop
        
        success_rate = successes / n_episodes
        avg_hops = total_hops / n_episodes if successes > 0 else environment.max_hops
        hop_efficiency = 1.0 - (avg_hops / environment.max_hops)
        
        # Score = 60% success + 40% hop efficiency
        score = 0.6 * success_rate + 0.4 * max(0, hop_efficiency)
        score = max(0.0, min(1.0, score))
        
        is_success = score >= self.success_threshold
        
        return {
            "score": score,
            "success": is_success,
            "success_rate": success_rate,
            "average_hops": avg_hops,
            "hop_efficiency": hop_efficiency,
            "details": f"Score: {score:.2f}, Efficiency: {hop_efficiency:.1%}, Success: {successes}/{n_episodes}"
        }


class RobustnessGrader(BaseGrader):
    """
    Grades agents on robustness across varying conditions.
    Tests on multiple difficulty levels.
    """
    
    def __init__(self, success_threshold: float = 0.5):
        self.success_threshold = success_threshold
    
    def grade(self, agent_fn: Callable, environment, n_episodes: int = 10) -> Dict[str, Any]:
        """Grade agent on robustness"""
        # For now, just grade on current difficulty
        total_reward = 0.0
        successes = 0
        
        for episode in range(n_episodes):
            obs = environment.reset(seed=episode)
            done = False
            
            while not done and environment.current_hop < environment.max_hops:
                action = agent_fn(obs)
                obs, reward, done, info = environment.step(action)
            
            total_reward += environment.episode_reward
            if environment.success:
                successes += 1
        
        success_rate = successes / n_episodes
        avg_reward = total_reward / n_episodes
        
        # Score based on consistent success
        score = success_rate
        is_success = score >= self.success_threshold
        
        return {
            "score": score,
            "success": is_success,
            "success_rate": success_rate,
            "average_reward": avg_reward,
            "details": f"Robustness Score: {score:.2f}, Consistent Success: {successes}/{n_episodes}"
        }


# Grader registry - maps grader type names to classes
GRADER_REGISTRY = {
    "default": RewardThresholdGrader,
    "reward_threshold": RewardThresholdGrader,
    "efficient": EfficientGrader,
    "robustness": RobustnessGrader,
}


def get_grader(grader_type: str, **kwargs) -> BaseGrader:
    """
    Factory function to get a grader instance
    
    Args:
        grader_type: Type of grader ("default", "efficient", "robustness")
        **kwargs: Arguments to pass to grader constructor
        
    Returns:
        Grader instance
    """
    if grader_type not in GRADER_REGISTRY:
        raise ValueError(f"Unknown grader type: {grader_type}. Available: {list(GRADER_REGISTRY.keys())}")
    
    grader_class = GRADER_REGISTRY[grader_type]
    return grader_class(**kwargs)
