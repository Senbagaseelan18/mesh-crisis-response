"""
Example agents demonstrating different strategies for the mesh network router.
These can be used as baselines or templates for your own RL agents.
"""

from models import MeshObservation, MeshAction
import random
import math


class RandomAgent:
    """
    Baseline agent: Randomly chooses a neighboring device.
    Good for establishing a lower bound on performance.
    """
    
    def act(self, observation: MeshObservation) -> MeshAction:
        """Choose randomly among available neighbors."""
        if observation.neighboring_devices:
            target = random.choice(observation.neighboring_devices)
            return MeshAction(target_device_id=target.device_id)
        
        # Fallback: stay in place (shouldn't happen in practice)
        return MeshAction(target_device_id=observation.current_device_id)


class GreedyAgent:
    """
    Greedy agent: Always moves to the neighbor closest to the gateway.
    Implements a simple "greedy nearest to goal" strategy.
    """
    
    def act(self, observation: MeshObservation) -> MeshAction:
        """Choose neighbor closest to gateway."""
        if not observation.neighboring_devices:
            return MeshAction(target_device_id=observation.current_device_id)
        
        # Gateway position is implicit - use observation.gateway_distance as reference
        # Select neighbor with best combination of distance and battery
        best_neighbor = None
        best_score = float('inf')
        
        for neighbor in observation.neighboring_devices:
            # Simple heuristic: prefer neighbors that are alive
            if not neighbor.is_active:
                continue
            
            # Use battery level as proxy for desirability
            # Also prefer devices with good RSSI
            score = (
                neighbor.hop_count +  # Prefer devices not yet used
                (100 - neighbor.battery_level) * 0.1  # Slight preference for high battery
            )
            
            if score < best_score:
                best_score = score
                best_neighbor = neighbor
        
        if best_neighbor:
            return MeshAction(target_device_id=best_neighbor.device_id)
        
        return MeshAction(target_device_id=observation.neighboring_devices[0].device_id)


class IntelligentAgent:
    """
    Intelligent agent: Uses multiple heuristics to make routing decisions.
    Considers:
    - Distance to gateway
    - Battery level (avoid low-battery devices)
    - Signal strength (RSSI)
    - Device freshness (not recently used)
    """
    
    def __init__(self, distance_weight=0.4, battery_weight=0.3, rssi_weight=0.2, freshness_weight=0.1):
        """
        Initialize with configurable weights.
        
        Args:
            distance_weight: How much to optimize for moving closer to gateway
            battery_weight: Preference for high-battery devices
            rssi_weight: Preference for strong signal (high RSSI)
            freshness_weight: Preference for devices not yet used
        """
        self.weights = {
            'distance': distance_weight,
            'battery': battery_weight,
            'rssi': rssi_weight,
            'freshness': freshness_weight
        }
    
    def _score_neighbor(self, neighbor, gateway_position, current_position):
        """
        Calculate score for a neighbor based on multiple factors.
        Lower score is better.
        """
        # Distance component: how much closer to gateway
        neighbor_to_gateway = math.sqrt(
            (neighbor.position[0] - gateway_position[0])**2 +
            (neighbor.position[1] - gateway_position[1])**2
        )
        current_to_gateway = math.sqrt(
            (current_position[0] - gateway_position[0])**2 +
            (current_position[1] - gateway_position[1])**2
        )
        distance_delta = neighbor_to_gateway - current_to_gateway
        distance_score = max(0, distance_delta) / (current_to_gateway + 1)
        
        # Battery component: prefer high-battery devices
        battery_score = (100 - neighbor.battery_level) / 100.0
        
        # RSSI component: prefer strong signals (higher RSSI is less negative)
        rssi_normalized = (neighbor.rssi + 100) / 70.0  # Normalize to 0-1
        rssi_score = 1.0 - max(0, min(1.0, rssi_normalized))
        
        # Freshness component: prefer devices with fewer hops
        freshness_score = neighbor.hop_count / 10.0
        
        # Weighted combination
        total_score = (
            self.weights['distance'] * distance_score +
            self.weights['battery'] * battery_score +
            self.weights['rssi'] * rssi_score +
            self.weights['freshness'] * freshness_score
        )
        
        return total_score
    
    def act(self, observation: MeshObservation) -> MeshAction:
        """Choose best neighbor based on weighted heuristics."""
        if not observation.neighboring_devices:
            return MeshAction(target_device_id=observation.current_device_id)
        
        # Get gateway position (approximate based on distance)
        # In a real scenario, this could be obtained from observation
        gateway_pos = (observation.gateway_distance, 0)  # Simplified
        current_pos = (0, 0)  # Current device position relative
        
        # Score all active neighbors
        best_neighbor = None
        best_score = float('inf')
        
        for neighbor in observation.neighboring_devices:
            if not neighbor.is_active:
                continue
            
            score = self._score_neighbor(neighbor, gateway_pos, current_pos)
            
            if score < best_score:
                best_score = score
                best_neighbor = neighbor
        
        if best_neighbor:
            return MeshAction(target_device_id=best_neighbor.device_id)
        
        # Fallback to first available
        return MeshAction(target_device_id=observation.neighboring_devices[0].device_id)


class ConservativeAgent:
    """
    Conservative agent: Prioritizes device survival and battery health.
    Useful for scenarios where network stability is critical.
    """
    
    def act(self, observation: MeshObservation) -> MeshAction:
        """Choose neighbor that maximizes network longevity."""
        if not observation.neighboring_devices:
            return MeshAction(target_device_id=observation.current_device_id)
        
        # Filter out low-battery devices (below 20%)
        viable_neighbors = [
            n for n in observation.neighboring_devices
            if n.is_active and n.battery_level > 20
        ]
        
        if not viable_neighbors:
            # If no good options, choose highest battery available
            viable_neighbors = [n for n in observation.neighboring_devices if n.is_active]
        
        if not viable_neighbors:
            return MeshAction(target_device_id=observation.current_device_id)
        
        # Among viable neighbors, choose based on:
        # 1. Battery level (prefer higher)
        # 2. Signal strength (prefer stronger)
        best_neighbor = max(
            viable_neighbors,
            key=lambda n: (n.battery_level, n.rssi)
        )
        
        return MeshAction(target_device_id=best_neighbor.device_id)


class ExplorativeAgent:
    """
    Explorative agent: Balances between exploitation (going to gateway)
    and exploration (discovering new routes).
    """
    
    def __init__(self, exploration_rate=0.2):
        """
        Initialize with exploration rate.
        
        Args:
            exploration_rate: Probability of random choice (0.0-1.0)
        """
        self.exploration_rate = exploration_rate
    
    def act(self, observation: MeshObservation) -> MeshAction:
        """Choose between exploitation and exploration."""
        if not observation.neighboring_devices:
            return MeshAction(target_device_id=observation.current_device_id)
        
        # Epsilon-greedy strategy
        if random.random() < self.exploration_rate:
            # Explore: random choice
            target = random.choice(observation.neighboring_devices)
            return MeshAction(target_device_id=target.device_id)
        else:
            # Exploit: greedy choice toward gateway
            best_neighbor = min(
                observation.neighboring_devices,
                key=lambda n: (
                    n.hop_count,  # Prefer fresh devices
                    -n.battery_level  # Prefer high battery (negative for min)
                )
            )
            return MeshAction(target_device_id=best_neighbor.device_id)


# Example usage demonstrating how to use agents
if __name__ == "__main__":
    from server.environment import MeshNetworkEnvironment, TaskGrader
    from models import TaskDifficulty
    
    # Create environment
    env = MeshNetworkEnvironment(TaskDifficulty.MEDIUM)
    obs = env.reset(seed=42)
    
    # Create different agents
    agents = {
        "random": RandomAgent(),
        "greedy": GreedyAgent(),
        "intelligent": IntelligentAgent(),
        "conservative": ConservativeAgent(),
        "explorative": ExplorativeAgent(exploration_rate=0.1),
    }
    
    # Test each agent
    print("Testing agents on MEDIUM difficulty...")
    print("-" * 60)
    
    for agent_name, agent in agents.items():
        env.reset(seed=42)
        obs = env.state()
        done = False
        total_reward = 0
        
        while not done and env.current_hop < env.max_hops:
            action = agent.act(obs)
            obs, reward, done, info = env.step(action)
            total_reward += reward
        
        stats = env.get_episode_stats()
        print(f"{agent_name:15} | Success: {str(stats['success']):5} | "
              f"Hops: {stats['hops']:2} | Reward: {total_reward:6.2f}")
    
    print("-" * 60)
    
    # Grade agents formally
    print("\nFormal grading (5 episodes each)...")
    grader = TaskGrader(n_episodes=5)
    
    for agent_name, agent in agents.items():
        def agent_wrapper(observation):
            return agent.act(observation)
        
        result = grader.grade_task(agent_wrapper, TaskDifficulty.HARD)
        print(f"{agent_name:15} | Score: {result.score:.2f} | "
              f"Success Rate: {result.success_rate:.1%} | "
              f"Avg Hops: {result.average_hops:.1f}")
