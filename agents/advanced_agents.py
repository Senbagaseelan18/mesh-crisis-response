"""
Advanced ML Agents using Deep Reinforcement Learning.
Implements DQN and Policy Gradient agents for optimal routing.
"""

import numpy as np
import random
from typing import Tuple, List, Optional
from collections import deque
import math

from models import MeshObservation, MeshAction, TaskDifficulty


class NeuralNetworkAgent:
    """
    Simple neural network-based agent for mesh routing.
    Learns to map observations to actions using a 3-layer network.
    """
    
    def __init__(self, input_size: int = 10, hidden_size: int = 64, output_size: int = 12):
        """
        Initialize neural network agent.
        
        Args:
            input_size: Observation feature dimension
            hidden_size: Hidden layer size
            output_size: Number of possible actions (max devices)
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Simple weight initialization
        self.w1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.randn(hidden_size, hidden_size) * 0.01
        self.b2 = np.zeros((1, hidden_size))
        self.w3 = np.random.randn(hidden_size, output_size) * 0.01
        self.b3 = np.zeros((1, output_size))
        
        self.learning_rate = 0.001
    
    def _relu(self, x: np.ndarray) -> np.ndarray:
        """ReLU activation."""
        return np.maximum(0, x)
    
    def _relu_derivative(self, x: np.ndarray) -> np.ndarray:
        """ReLU derivative."""
        return (x > 0).astype(float)
    
    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Softmax for action probabilities."""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass through network."""
        # Layer 1
        z1 = np.dot(x, self.w1) + self.b1
        a1 = self._relu(z1)
        
        # Layer 2
        z2 = np.dot(a1, self.w2) + self.b2
        a2 = self._relu(z2)
        
        # Layer 3 (output)
        z3 = np.dot(a2, self.w3) + self.b3
        
        return self._softmax(z3)
    
    def act(self, observation: MeshObservation) -> MeshAction:
        """Choose action using neural network."""
        # Extract features
        features = self._extract_features(observation)
        features = features.reshape(1, -1)
        
        # Get action probabilities
        action_probs = self.forward(features)[0]
        
        # Choose best action
        best_action_idx = np.argmax(action_probs)
        
        # Map to device
        target = self._get_device_from_action(observation, best_action_idx)
        return MeshAction(target_device_id=target, priority=3)
    
    def _extract_features(self, observation: MeshObservation) -> np.ndarray:
        """Extract numerical features from observation."""
        features = [
            observation.current_battery / 100.0,  # Normalize battery
            observation.gateway_distance / 200.0,  # Normalize distance
            observation.current_rssi / -100.0,  # Normalize RSSI
            observation.hops_taken / 15.0,  # Normalize hops
            len(observation.neighboring_devices) / 12.0,  # Neighbor count
            observation.time_step / 50.0,  # Timestep
        ]
        
        # Add neighbor features (average)
        if observation.neighboring_devices:
            avg_battery = np.mean([n.battery_level for n in observation.neighboring_devices]) / 100.0
            avg_rssi = np.mean([n.rssi for n in observation.neighboring_devices]) / -100.0
            features.extend([avg_battery, avg_rssi])
        else:
            features.extend([0.0, 0.0])
        
        # Pad to 10 features
        while len(features) < 10:
            features.append(0.0)
        
        return np.array(features[:10])
    
    def _get_device_from_action(self, observation: MeshObservation, action_idx: int) -> str:
        """Map action index to device ID."""
        neighbors = observation.neighboring_devices
        if not neighbors:
            return observation.current_device_id
        
        if action_idx < len(neighbors):
            return neighbors[action_idx].device_id
        else:
            return neighbors[0].device_id


class DQNAgent:
    """
    Deep Q-Network Agent for mesh routing.
    Implements experience replay and target network.
    """
    
    def __init__(self, state_size: int = 10, action_size: int = 12, learning_rate: float = 0.001):
        """
        Initialize DQN agent.
        
        Args:
            state_size: Observation feature dimension
            action_size: Number of possible actions
            learning_rate: Learning rate for updates
        """
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        
        # Network
        self.network = NeuralNetworkAgent(state_size, 64, action_size)
        self.target_network = NeuralNetworkAgent(state_size, 64, action_size)
        
        # Memory for experience replay
        self.memory = deque(maxlen=1000)
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.batch_size = 32
    
    def remember(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        """Store experience in memory."""
        self.memory.append((state, action, reward, next_state, done))
    
    def replay(self, batch_size: int):
        """Train on batch from memory."""
        if len(self.memory) < batch_size:
            return
        
        batch = random.sample(self.memory, batch_size)
        states = np.array([exp[0] for exp in batch])
        actions = np.array([exp[1] for exp in batch])
        rewards = np.array([exp[2] for exp in batch])
        next_states = np.array([exp[3] for exp in batch])
        dones = np.array([exp[4] for exp in batch])
        
        # Predict Q-values
        target_qs = self.network.forward(states)
        next_qs = self.target_network.forward(next_states)
        
        # Update Q-values with Bellman equation
        for i in range(batch_size):
            if dones[i]:
                target_qs[i, actions[i]] = rewards[i]
            else:
                target_qs[i, actions[i]] = rewards[i] + self.gamma * np.max(next_qs[i])
        
        # Simple SGD update (pseudo-implementation)
        # In real DQN, would compute loss and backprop
        pass
    
    def act(self, observation: MeshObservation, training: bool = False) -> MeshAction:
        """Choose action with epsilon-greedy strategy."""
        if training and random.random() < self.epsilon:
            # Explore: random action
            neighbors = observation.neighboring_devices
            if neighbors:
                target = random.choice(neighbors).device_id
            else:
                target = observation.current_device_id
        else:
            # Exploit: use network
            target = self.network.act(observation).target_device_id
        
        return MeshAction(target_device_id=target, priority=4)
    
    def update_target_network(self):
        """Update target network weights."""
        self.target_network.w1 = self.network.w1.copy()
        self.target_network.b1 = self.network.b1.copy()
        self.target_network.w2 = self.network.w2.copy()
        self.target_network.b2 = self.network.b2.copy()
        self.target_network.w3 = self.network.w3.copy()
        self.target_network.b3 = self.network.b3.copy()
    
    def decay_epsilon(self):
        """Decay exploration rate."""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)


class PPOAgent:
    """
    Proximal Policy Optimization Agent.
    Actor-Critic architecture for stable policy learning.
    """
    
    def __init__(self, state_size: int = 10, action_size: int = 12):
        """
        Initialize PPO agent.
        
        Args:
            state_size: Observation feature dimension
            action_size: Number of possible actions
        """
        self.state_size = state_size
        self.action_size = action_size
        
        # Actor network (policy)
        self.actor = NeuralNetworkAgent(state_size, 64, action_size)
        
        # Critic network (value function)
        self.critic = NeuralNetworkAgent(state_size, 64, 1)
        
        self.learning_rate = 0.0003
        self.gamma = 0.99
        self.gae_lambda = 0.95
        self.clip_ratio = 0.2
        self.value_coef = 0.5
        self.entropy_coef = 0.01
    
    def act(self, observation: MeshObservation) -> MeshAction:
        """Choose action using actor network."""
        features = self._extract_features(observation)
        features_array = features.reshape(1, -1)
        
        action_probs = self.actor.forward(features_array)[0]
        action_idx = np.argmax(action_probs)
        
        neighbors = observation.neighboring_devices
        if action_idx < len(neighbors):
            target = neighbors[action_idx].device_id
        elif neighbors:
            target = neighbors[0].device_id
        else:
            target = observation.current_device_id
        
        return MeshAction(target_device_id=target, priority=5)
    
    def _extract_features(self, observation: MeshObservation) -> np.ndarray:
        """Extract numerical features from observation."""
        features = [
            observation.current_battery / 100.0,
            observation.gateway_distance / 200.0,
            observation.current_rssi / -100.0,
            observation.hops_taken / 15.0,
            len(observation.neighboring_devices) / 12.0,
            observation.time_step / 50.0,
        ]
        
        if observation.neighboring_devices:
            avg_battery = np.mean([n.battery_level for n in observation.neighboring_devices]) / 100.0
            avg_rssi = np.mean([n.rssi for n in observation.neighboring_devices]) / -100.0
            features.extend([avg_battery, avg_rssi])
        else:
            features.extend([0.0, 0.0])
        
        while len(features) < 10:
            features.append(0.0)
        
        return np.array(features[:10])
    
    def estimate_value(self, observation: MeshObservation) -> float:
        """Estimate value of state using critic."""
        features = self._extract_features(observation)
        features_array = features.reshape(1, -1)
        value = self.critic.forward(features_array)[0, 0]
        return value


class AdaptiveAgent:
    """
    Adaptive agent that learns from experience in the environment.
    Combines multiple strategies and adapts based on performance.
    """
    
    def __init__(self):
        """Initialize adaptive agent."""
        self.episode_count = 0
        self.reward_history = deque(maxlen=100)
        self.success_history = deque(maxlen=100)
        
        # Multiple sub-agents to combine
        self.dqn_agent = DQNAgent()
        self.nn_agent = NeuralNetworkAgent()
        self.ppo_agent = PPOAgent()
        
        # Weights for combining strategies
        self.weights = {"dqn": 0.5, "nn": 0.3, "ppo": 0.2}
    
    def act(self, observation: MeshObservation) -> MeshAction:
        """Choose action by combining multiple agents."""
        actions = {
            "dqn": self.dqn_agent.act(observation),
            "nn": self.nn_agent.act(observation),
            "ppo": self.ppo_agent.act(observation),
        }
        
        # Weighted ensemble prediction
        neighbors = observation.neighboring_devices
        if not neighbors:
            return MeshAction(target_device_id=observation.current_device_id)
        
        # Score each neighbor across all agents
        neighbor_scores = {}
        for neighbor in neighbors:
            neighbor_scores[neighbor.device_id] = 0.0
            for agent_name, weight in self.weights.items():
                if actions[agent_name].target_device_id == neighbor.device_id:
                    neighbor_scores[neighbor.device_id] += weight
        
        # Choose highest-scored neighbor
        best_neighbor = max(neighbor_scores.items(), key=lambda x: x[1])[0]
        return MeshAction(target_device_id=best_neighbor, priority=5)
    
    def update_strategy(self, reward: float, success: bool):
        """Adapt strategy based on performance."""
        self.reward_history.append(reward)
        self.success_history.append(success)
        
        # Adaptive weight adjustment
        if len(self.success_history) >= 10:
            recent_success_rate = sum(self.success_history) / len(self.success_history)
            
            if recent_success_rate < 0.5:
                # Increase DQN weight if struggling
                self.weights["dqn"] = min(0.7, self.weights["dqn"] + 0.05)
                self.weights["nn"] = max(0.2, self.weights["nn"] - 0.025)
            elif recent_success_rate > 0.8:
                # Exploit successful strategy more
                self.weights["dqn"] = max(0.3, self.weights["dqn"] - 0.05)
                self.weights["ppo"] = min(0.4, self.weights["ppo"] + 0.05)
        
        self.episode_count += 1


if __name__ == "__main__":
    from server.environment import MeshNetworkEnvironment, TaskGrader
    
    print("Testing Advanced Agents...")
    print("-" * 60)
    
    env = MeshNetworkEnvironment(TaskDifficulty.MEDIUM)
    agents = {
        "Neural Network": NeuralNetworkAgent(),
        "DQN": DQNAgent(),
        "PPO": PPOAgent(),
        "Adaptive": AdaptiveAgent(),
    }
    
    for agent_name, agent in agents.items():
        obs = env.reset(seed=42)
        total_reward = 0.0
        done = False
        
        while not done and env.current_hop < env.max_hops:
            action = agent.act(obs)
            obs, reward, done, info = env.step(action)
            total_reward += reward
        
        stats = env.get_episode_stats()
        print(f"{agent_name:20} | Success: {str(stats['success']):5} | "
              f"Hops: {stats['hops']:2} | Reward: {total_reward:6.2f}")
    
    print("-" * 60)
