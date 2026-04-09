"""
Enhanced environment with dynamic features like obstacles, interference, and node failures.
Provides realistic complexity layers for advanced RL training.
"""

import random
import math
from typing import Dict, List, Optional, Tuple
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import TaskDifficulty, MeshObservation, MeshAction, DeviceNode


class EnvironmentFeature(str, Enum):
    """Available environment complexity features."""
    DYNAMIC_OBSTACLES = "dynamic_obstacles"
    RF_INTERFERENCE = "rf_interference"
    NODE_FAILURES = "node_failures"
    CONGESTION = "congestion"
    ADAPTIVE_TOPOLOGY = "adaptive_topology"


class Obstacle:
    """Represents a physical obstacle affecting signal propagation."""
    
    def __init__(self, x: float, y: float, radius: float, attenuation_dbm: float = 10.0):
        """
        Initialize obstacle.
        
        Args:
            x, y: Center position
            radius: Obstacle size
            attenuation_dbm: Signal attenuation caused (dBm)
        """
        self.position = (x, y)
        self.radius = radius
        self.attenuation = attenuation_dbm
    
    def calculate_blockage(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calculate how much this obstacle blocks the signal path."""
        # Simple line-circle intersection
        x1, y1 = pos1
        x2, y2 = pos2
        ox, oy = self.position
        
        # Vector from pos1 to pos2
        dx = x2 - x1
        dy = y2 - y1
        
        # Vector from pos1 to obstacle
        fx = x1 - ox
        fy = y1 - oy
        
        a = dx*dx + dy*dy
        b = 2*(fx*dx + fy*dy)
        c = (fx*fx + fy*fy) - self.radius*self.radius
        
        if a == 0:
            return 0.0
        
        discriminant = b*b - 4*a*c
        
        if discriminant < 0:
            return 0.0  # No intersection
        
        # Check if intersection is on the line segment
        discriminant = math.sqrt(discriminant)
        t1 = (-b - discriminant) / (2*a)
        t2 = (-b + discriminant) / (2*a)
        
        if (0 <= t1 <= 1) or (0 <= t2 <= 1) or (t1 < 0 and t2 > 1):
            return self.attenuation
        
        return 0.0


class InterferenceSource:
    """Represents RF interference source."""
    
    def __init__(self, x: float, y: float, power_dbm: float = -40, range_m: float = 100):
        """
        Initialize interference source.
        
        Args:
            x, y: Position
            power_dbm: Interference signal power
            range_m: Effective range
        """
        self.position = (x, y)
        self.power = power_dbm
        self.range = range_m
    
    def calculate_interference(self, device_pos: Tuple[float, float]) -> float:
        """Calculate interference at device location."""
        distance = math.sqrt((device_pos[0] - self.position[0])**2 +
                           (device_pos[1] - self.position[1])**2)
        
        if distance > self.range:
            return 0.0
        
        # Interference decreases with distance
        interference = self.power * (1.0 - distance / self.range)
        return interference


class DynamicNetworkEnvironment:
    """
    Enhanced mesh network environment with dynamic features.
    Includes obstacles, interference, node failures, and congestion.
    """
    
    def __init__(self, task_difficulty: TaskDifficulty = TaskDifficulty.EASY,
                 features: Optional[List[EnvironmentFeature]] = None):
        """
        Initialize dynamic environment.
        
        Args:
            task_difficulty: Task difficulty level
            features: List of features to enable
        """
        self.task_difficulty = task_difficulty
        self.features = features or []
        
        # Environment elements
        self.obstacles: List[Obstacle] = []
        self.interference_sources: List[InterferenceSource] = []
        self.device_map: Dict[str, DeviceNode] = {}
        self.failed_devices: set = set()
        self.congestion_map: Dict[str, float] = {}  # Device congestion levels
        
        # Configuration
        self.rssi_reference_power = -50
        self.path_loss_exponent = 2.5
        self.base_battery_drain = 5.0
        
        # Statistics
        self.step_count = 0
        self.episode_reward = 0.0
        self.success = False
        self.done = False
    
    def _generate_obstacles(self):
        """Generate obstacles based on difficulty."""
        if EnvironmentFeature.DYNAMIC_OBSTACLES not in self.features:
            return
        
        if self.task_difficulty == TaskDifficulty.EASY:
            self.obstacles = [Obstacle(50, 50, 10, 5)]
        elif self.task_difficulty == TaskDifficulty.MEDIUM:
            self.obstacles = [
                Obstacle(40, 30, 15, 8),
                Obstacle(70, 70, 12, 6),
            ]
        else:  # HARD
            self.obstacles = [
                Obstacle(30, 20, 20, 10),
                Obstacle(80, 60, 18, 9),
                Obstacle(50, 40, 15, 7),
            ]
    
    def _generate_interference_sources(self):
        """Generate interference sources."""
        if EnvironmentFeature.RF_INTERFERENCE not in self.features:
            return
        
        if self.task_difficulty == TaskDifficulty.EASY:
            self.interference_sources = []
        elif self.task_difficulty == TaskDifficulty.MEDIUM:
            self.interference_sources = [InterferenceSource(100, 50, -60, 80)]
        else:  # HARD
            self.interference_sources = [
                InterferenceSource(80, 60, -55, 100),
                InterferenceSource(30, 20, -65, 70),
            ]
    
    def _calculate_enhanced_rssi(self, pos1: Tuple[float, float], 
                                 pos2: Tuple[float, float]) -> float:
        """Calculate RSSI with obstacles and interference."""
        # Base RSSI from distance
        distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        if distance < 1:
            distance = 1
        
        rssi = self.rssi_reference_power - 10 * self.path_loss_exponent * math.log10(distance)
        rssi += random.gauss(0, 2.0)
        
        # Apply obstacle attenuation
        for obstacle in self.obstacles:
            rssi -= obstacle.calculate_blockage(pos1, pos2)
        
        # Add interference
        for interference in self.interference_sources:
            interference_level = interference.calculate_interference(pos2)
            rssi += interference_level  # Interference degrades RSSI
        
        # Clamp to realistic bounds
        rssi = max(-100, min(-30, rssi))
        return rssi
    
    def _simulate_node_failure(self):
        """Simulate random node failures."""
        if EnvironmentFeature.NODE_FAILURES not in self.features:
            return
        
        failure_rate = {
            TaskDifficulty.EASY: 0.0,
            TaskDifficulty.MEDIUM: 0.05,
            TaskDifficulty.HARD: 0.1,
        }
        
        for device_id, device in self.device_map.items():
            if random.random() < failure_rate.get(self.task_difficulty, 0):
                if device_id not in self.failed_devices:
                    device.is_active = False
                    self.failed_devices.add(device_id)
    
    def _update_congestion(self):
        """Update network congestion levels."""
        if EnvironmentFeature.CONGESTION not in self.features:
            return
        
        # Increase congestion on heavily used devices
        for device_id in self.congestion_map:
            self.congestion_map[device_id] *= 0.9  # Decay
        
        # Add random congestion to devices
        if random.random() < 0.2:
            random_device = random.choice(list(self.device_map.keys()))
            self.congestion_map[random_device] = min(1.0, self.congestion_map.get(random_device, 0) + 0.3)
    
    def _adapt_topology(self):
        """Dynamically adapt network topology."""
        if EnvironmentFeature.ADAPTIVE_TOPOLOGY not in self.features:
            return
        
        # Randomly move devices slightly
        for device in self.device_map.values():
            if not device.is_gateway and random.random() < 0.1:
                move_x = random.uniform(-5, 5)
                move_y = random.uniform(-5, 5)
                device.position = (device.position[0] + move_x, device.position[1] + move_y)
    
    def reset(self, seed: Optional[int] = None) -> MeshObservation:
        """Reset environment with optional seed."""
        if seed is not None:
            random.seed(seed)
        
        # Generate obstacles and interference
        self._generate_obstacles()
        self._generate_interference_sources()
        
        # Initialize congestion
        self.congestion_map = {}
        self.failed_devices = set()
        self.step_count = 0
        self.episode_reward = 0.0
        self.success = False
        self.done = False
        
        # Create network (using simplified generation for now)
        self.device_map = self._generate_network()
        
        return self.state()
    
    def _generate_network(self) -> Dict[str, DeviceNode]:
        """Generate network topology."""
        devices = {}
        
        # Generate based on difficulty
        num_devices = {
            TaskDifficulty.EASY: 5,
            TaskDifficulty.MEDIUM: 8,
            TaskDifficulty.HARD: 12,
        }
        
        n = num_devices[self.task_difficulty]
        
        for i in range(n):
            x = random.uniform(0, 150) if self.task_difficulty == TaskDifficulty.HARD else (i * 30)
            y = random.uniform(0, 100) if self.task_difficulty == TaskDifficulty.HARD else random.uniform(-10, 10)
            
            devices[f"node_{i}"] = DeviceNode(
                device_id=f"node_{i}",
                position=(x, y),
                battery_level=random.uniform(60, 100) if self.task_difficulty != TaskDifficulty.EASY else 100,
                rssi=-50,
                is_gateway=False,
                is_active=True,
                hop_count=0,
            )
        
        # Add gateway
        gateway_pos = {
            TaskDifficulty.EASY: (150, 0),
            TaskDifficulty.MEDIUM: (120, 80),
            TaskDifficulty.HARD: (150 + random.uniform(0, 50), random.uniform(50, 150)),
        }
        
        devices["gateway_0"] = DeviceNode(
            device_id="gateway_0",
            position=gateway_pos[self.task_difficulty],
            battery_level=100.0,
            rssi=-30,
            is_gateway=True,
            is_active=True,
            hop_count=0,
        )
        
        return devices
    
    def state(self) -> MeshObservation:
        """Get current observation."""
        current_device = self.device_map["node_0"]
        neighbors = self._get_neighbors("node_0")
        gateway = self.device_map["gateway_0"]
        
        gateway_distance = math.sqrt(
            (current_device.position[0] - gateway.position[0])**2 +
            (current_device.position[1] - gateway.position[1])**2
        )
        
        return MeshObservation(
            current_device_id="node_0",
            current_rssi=current_device.rssi,
            current_battery=current_device.battery_level,
            neighboring_devices=neighbors,
            gateway_distance=gateway_distance,
            hops_taken=self.step_count,
            time_step=self.step_count,
            task_difficulty=self.task_difficulty,
            alert_payload={"features": [f.value for f in self.features]},
        )
    
    def _get_neighbors(self, device_id: str) -> List[DeviceNode]:
        """Get active neighbors within range."""
        device = self.device_map[device_id]
        neighbors = []
        
        for other_id, other_device in self.device_map.items():
            if other_id == device_id or not other_device.is_active:
                continue
            
            rssi = self._calculate_enhanced_rssi(device.position, other_device.position)
            
            if rssi > -90:  # In-range threshold
                neighbors.append(other_device)
        
        return neighbors
    
    def step(self, action: MeshAction) -> Tuple[MeshObservation, float, bool, Dict]:
        """Execute step with dynamic features."""
        self.step_count += 1
        
        # Apply dynamic features
        self._simulate_node_failure()
        self._update_congestion()
        self._adapt_topology()
        
        # Simplified step logic (full implementation would match base environment)
        reward = -0.05  # Base hop penalty
        self.episode_reward += reward
        
        if self.step_count > 20:
            self.done = True
        
        return self.state(), reward, self.done, {"features_active": self.features}


if __name__ == "__main__":
    print("Testing Enhanced Dynamic Environment...")
    
    # Test with all features enabled
    features = [
        EnvironmentFeature.DYNAMIC_OBSTACLES,
        EnvironmentFeature.RF_INTERFERENCE,
        EnvironmentFeature.NODE_FAILURES,
        EnvironmentFeature.ADAPTIVE_TOPOLOGY,
    ]
    
    env = DynamicNetworkEnvironment(TaskDifficulty.HARD, features=features)
    obs = env.reset(seed=42)
    
    print("[OK] Created dynamic environment with {} features".format(len(features)))
    print("     Obstacles: {}".format(len(env.obstacles)))
    print("     Interference sources: {}".format(len(env.interference_sources)))
    print("     Devices: {}".format(len(env.device_map)))
    print("     Neighbors visible: {}".format(len(obs.neighboring_devices)))
