import math
import random
import sys
import os
from typing import Tuple, Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import (
    MeshObservation, MeshAction, MeshState, DeviceNode, 
    TaskDifficulty, RewardInfo, TaskGradeResult
)


class MeshNetworkEnvironment:
    """
    OpenEnv-compatible Mesh Network Environment for emergency alert routing.
    Simulates RSSI signal strength and battery drain for each hop.
    """
    
    def __init__(self, task_difficulty: TaskDifficulty = TaskDifficulty.EASY):
        """
        Initialize the mesh network environment.
        
        Args:
            task_difficulty: EASY, MEDIUM, or HARD
        """
        self.task_difficulty = task_difficulty
        self.device_map: Dict[str, DeviceNode] = {}
        self.alert_location: str = ""
        self.gateway_location: str = ""
        self.current_hop: int = 0
        self.max_hops: int = self._get_max_hops()
        self.timestep: int = 0
        self.episode_reward: float = 0.0
        self.success: bool = False
        self.done: bool = False
        self.history: List[Dict] = []
        
        # RSSI Configuration
        self.rssi_reference_power = -50  # dBm at 1 meter
        self.path_loss_exponent = 2.5
        self.rssi_noise = 2.0
        
        # Battery drain rates (percentage per hop)
        self.base_battery_drain = 5.0
        self.rssi_penalty_factor = 0.5  # Additional drain based on poor RSSI
        
    def _get_max_hops(self) -> int:
        """Get maximum hops allowed based on difficulty."""
        if self.task_difficulty == TaskDifficulty.EASY:
            return 5
        elif self.task_difficulty == TaskDifficulty.MEDIUM:
            return 10
        else:  # HARD
            return 15
    
    def _calculate_distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two positions."""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def _calculate_rssi(self, distance: float, noise: bool = True) -> float:
        """
        Calculate RSSI (signal strength) based on distance using path loss model.
        
        RSSI = RefPower - 10*n*log10(distance) + noise
        where n is the path loss exponent
        """
        if distance < 1:
            distance = 1
        
        rssi = self.rssi_reference_power - 10 * self.path_loss_exponent * math.log10(distance)
        
        if noise:
            rssi += random.gauss(0, self.rssi_noise)
        
        # Clamp between realistic RSSI bounds (-100 to -30 dBm)
        rssi = max(-100, min(-30, rssi))
        return rssi
    
    def _get_neighboring_devices(self, device_id: str, max_distance: float = 50.0) -> List[DeviceNode]:
        """
        Get devices in communication range.
        Devices are in range if they have good RSSI and are active.
        """
        device = self.device_map[device_id]
        neighbors = []
        
        for other_id, other_device in self.device_map.items():
            if other_id == device_id or not other_device.is_active:
                continue
            
            distance = self._calculate_distance(device.position, other_device.position)
            
            # Calculate RSSI to determine if in range
            rssi = self._calculate_rssi(distance)
            
            # In-range threshold: RSSI better than -90 dBm
            if rssi > -90:
                neighbors.append(other_device)
        
        return neighbors
    
    def _apply_battery_drain(self, device_id: str, hop_quality: float = 1.0) -> bool:
        """
        Apply battery drain when forwarding an alert.
        
        Args:
            device_id: Device losing battery
            hop_quality: Signal quality factor (0.0-1.0), affects drain rate
            
        Returns:
            True if device survives, False if battery dies
        """
        device = self.device_map[device_id]
        
        # Base drain + penalty for poor signal quality
        drain = self.base_battery_drain + (1.0 - hop_quality) * self.rssi_penalty_factor * 10
        device.battery_level = max(0, device.battery_level - drain)
        
        # Device dies if battery reaches 0
        if device.battery_level <= 0:
            device.is_active = False
            return False
        
        return True
    
    def reset(self, seed: Optional[int] = None) -> MeshObservation:
        """
        Reset the environment to initial state.
        
        Returns:
            Initial observation
        """
        if seed is not None:
            random.seed(seed)
        
        self.device_map = self._generate_network()
        self.alert_location = "node_0"
        self.gateway_location = self._place_gateway()
        self.current_hop = 0
        self.timestep = 0
        self.episode_reward = 0.0
        self.success = False
        self.done = False
        self.history = []
        
        return self.state()
    
    def _generate_network(self) -> Dict[str, DeviceNode]:
        """Generate mesh network topology based on difficulty."""
        devices = {}
        
        if self.task_difficulty == TaskDifficulty.EASY:
            # 5 devices in a line, gateway 1 hop away
            for i in range(5):
                devices[f"node_{i}"] = DeviceNode(
                    device_id=f"node_{i}",
                    position=(i * 15, 0),
                    battery_level=100.0,
                    rssi=-50,
                    is_gateway=False,
                    is_active=True,
                    hop_count=0
                )
        
        elif self.task_difficulty == TaskDifficulty.MEDIUM:
            # 8 devices scattered, gateway ~3 hops away
            positions = [
                (0, 0), (20, 10), (40, 5), (60, 15),
                (15, 30), (45, 35), (75, 20), (50, 0)
            ]
            for i, pos in enumerate(positions):
                battery = random.uniform(60, 100)  # Some devices have lower battery
                devices[f"node_{i}"] = DeviceNode(
                    device_id=f"node_{i}",
                    position=pos,
                    battery_level=battery,
                    rssi=-60,
                    is_gateway=False,
                    is_active=True,
                    hop_count=0
                )
        
        else:  # HARD
            # 12 devices with random positions, gateway far away, high variability
            for i in range(12):
                x = random.uniform(0, 150)
                y = random.uniform(0, 100)
                battery = random.uniform(30, 100)
                rssi = random.uniform(-90, -40)
                
                devices[f"node_{i}"] = DeviceNode(
                    device_id=f"node_{i}",
                    position=(x, y),
                    battery_level=battery,
                    rssi=rssi,
                    is_gateway=False,
                    is_active=True,
                    hop_count=0
                )
        
        return devices
    
    def _place_gateway(self) -> str:
        """Place gateway device based on difficulty."""
        if self.task_difficulty == TaskDifficulty.EASY:
            gateway_pos = (60, 0)
        elif self.task_difficulty == TaskDifficulty.MEDIUM:
            gateway_pos = (80, 40)
        else:  # HARD
            gateway_pos = (random.uniform(100, 200), random.uniform(50, 150))
        
        gateway_id = "gateway_0"
        self.device_map[gateway_id] = DeviceNode(
            device_id=gateway_id,
            position=gateway_pos,
            battery_level=100.0,  # Gateway never dies
            rssi=-30,
            is_gateway=True,
            is_active=True,
            hop_count=0
        )
        
        return gateway_id
    
    def step(self, action: MeshAction) -> Tuple[MeshObservation, float, bool, Dict]:
        """
        Execute one step of the environment.
        
        Args:
            action: MeshAction specifying target device
            
        Returns:
            observation, reward, done, info
        """
        self.timestep += 1
        reward_info = RewardInfo()
        
        # Get current device and target device
        current_device = self.device_map.get(self.alert_location)
        target_device = self.device_map.get(action.target_device_id)
        
        # Validation
        if not current_device or not target_device or not target_device.is_active:
            reward_info.total_reward = -1.0
            self.done = True
            return self.state(), reward_info.total_reward, self.done, {"error": "Invalid target"}
        
        # Check if target is reachable (in neighbor list)
        neighbors = self._get_neighboring_devices(self.alert_location)
        if target_device not in neighbors:
            reward_info.total_reward = -0.2
            return self.state(), reward_info.total_reward, self.done, {"error": "Target not reachable"}
        
        # Calculate reward components
        gateway = self.device_map[self.gateway_location]
        old_distance = self._calculate_distance(current_device.position, gateway.position)
        new_distance = self._calculate_distance(target_device.position, gateway.position)
        
        # Reward for moving closer to gateway
        if new_distance < old_distance:
            reward_info.distance_reward = 0.1
        
        # Penalty for taking a hop
        reward_info.hop_penalty = -0.05
        
        # Check for successful delivery
        if action.target_device_id == self.gateway_location:
            reward_info.delivery_reward = 1.0
            self.success = True
            self.done = True
        
        # Apply battery drain to current device
        hop_quality = 1.0 / (1.0 + abs(new_distance - old_distance) / 10.0)  # Better quality if close
        if not self._apply_battery_drain(self.alert_location, hop_quality):
            # Device battery died during transmission
            if not self.success:  # Don't penalize if already delivered
                reward_info.battery_penalty = -1.0
                self.done = True
        
        # Move alert to new device
        self.alert_location = action.target_device_id
        self.current_hop += 1
        target_device.hop_count = self.current_hop
        
        # Calculate total reward
        reward_info.total_reward = (
            reward_info.distance_reward +
            reward_info.hop_penalty +
            reward_info.delivery_reward +
            reward_info.battery_penalty
        )
        
        # Check termination conditions
        if self.current_hop >= self.max_hops and not self.success:
            self.done = True
            reward_info.total_reward -= 1.0  # Penalty for exceeding max hops
        
        # Store history for analysis
        self.history.append({
            "timestep": self.timestep,
            "hop": self.current_hop,
            "current_device": self.alert_location,
            "target_device": action.target_device_id,
            "reward": reward_info.total_reward,
            "success": self.success,
            "done": self.done
        })
        
        self.episode_reward += reward_info.total_reward
        
        return self.state(), reward_info.total_reward, self.done, {
            "reward_info": reward_info,
            "hop": self.current_hop,
            "success": self.success
        }
    
    def state(self) -> MeshObservation:
        """
        Get current observation of the environment.
        
        Returns:
            MeshObservation representing current state
        """
        current_device = self.device_map[self.alert_location]
        neighbors = self._get_neighboring_devices(self.alert_location)
        gateway = self.device_map[self.gateway_location]
        
        gateway_distance = self._calculate_distance(
            current_device.position,
            gateway.position
        )
        
        return MeshObservation(
            current_device_id=self.alert_location,
            current_rssi=current_device.rssi,
            current_battery=current_device.battery_level,
            neighboring_devices=neighbors,
            gateway_distance=gateway_distance,
            hops_taken=self.current_hop,
            time_step=self.timestep,
            task_difficulty=self.task_difficulty,
            alert_payload={"priority": "emergency", "origin": "node_0"}
        )
    
    def render(self, mode: str = "text") -> str:
        """Render environment state for visualization."""
        output = f"\n--- Mesh Network State (Step {self.timestep}) ---\n"
        output += f"Alert Location: {self.alert_location}\n"
        output += f"Hops Taken: {self.current_hop} / {self.max_hops}\n"
        output += f"Episode Reward: {self.episode_reward:.2f}\n"
        output += f"Success: {self.success}\n"
        output += f"Done: {self.done}\n"
        return output
    
    def get_episode_stats(self) -> Dict:
        """Get statistics about the completed episode."""
        return {
            "success": self.success,
            "hops": self.current_hop,
            "reward": self.episode_reward,
            "timesteps": self.timestep,
            "difficulty": self.task_difficulty.value
        }


class TaskGrader:
    """
    Programmatic grader for evaluating agent performance on mesh network tasks.
    """
    
    def __init__(self, n_episodes: int = 10):
        """
        Initialize grader.
        
        Args:
            n_episodes: Number of episodes to evaluate
        """
        self.n_episodes = n_episodes
    
    def grade_task(self, agent, difficulty: TaskDifficulty) -> TaskGradeResult:
        """
        Grade an agent on a specific task difficulty.
        
        Args:
            agent: Agent function that takes MeshObservation and returns MeshAction
            difficulty: Task difficulty to grade on
            
        Returns:
            TaskGradeResult with score and metrics
        """
        env = MeshNetworkEnvironment(difficulty)
        
        total_reward = 0.0
        successes = 0
        total_hops = 0
        
        for episode in range(self.n_episodes):
            obs = env.reset(seed=episode)
            done = False
            
            while not done and env.current_hop < env.max_hops:
                # Get action from agent
                action = agent(obs)
                obs, reward, done, info = env.step(action)
            
            total_reward += env.episode_reward
            if env.success:
                successes += 1
            total_hops += env.current_hop
        
        success_rate = successes / self.n_episodes
        avg_hops = total_hops / self.n_episodes if successes > 0 else 0
        avg_reward = total_reward / self.n_episodes
        
        # Calculate score: 0.6 * success_rate + 0.3 * hop_efficiency + 0.1 * reward
        hop_efficiency = max(0, 1.0 - (avg_hops / env.max_hops)) if avg_hops > 0 else 0
        score = 0.6 * success_rate + 0.3 * hop_efficiency + 0.1 * max(0, avg_reward / 10.0)
        score = max(0.0, min(1.0, score))  # Clamp to [0, 1]
        
        return TaskGradeResult(
            difficulty=difficulty,
            score=score,
            success_rate=success_rate,
            average_hops=avg_hops,
            average_reward=avg_reward,
            details=f"Success: {successes}/{self.n_episodes}, Avg Hops: {avg_hops:.1f}"
        )
