"""
Test suite for Emergency Mesh-Network Router environment.
Demonstrates environment usage and grading system.
"""

import pytest
from models import TaskDifficulty, MeshAction
from server.environment import MeshNetworkEnvironment, TaskGrader


class TestMeshNetworkEnvironment:
    """Tests for the basic environment functionality."""
    
    def test_easy_environment_reset(self):
        """Test resetting easy environment."""
        env = MeshNetworkEnvironment(TaskDifficulty.EASY)
        obs = env.reset()
        
        assert obs is not None
        assert obs.current_device_id == "node_0"
        assert obs.task_difficulty == TaskDifficulty.EASY
        assert env.max_hops == 5
        assert env.current_hop == 0
    
    def test_medium_environment_reset(self):
        """Test resetting medium environment."""
        env = MeshNetworkEnvironment(TaskDifficulty.MEDIUM)
        obs = env.reset()
        
        assert obs.task_difficulty == TaskDifficulty.MEDIUM
        assert env.max_hops == 10
    
    def test_hard_environment_reset(self):
        """Test resetting hard environment."""
        env = MeshNetworkEnvironment(TaskDifficulty.HARD)
        obs = env.reset()
        
        assert obs.task_difficulty == TaskDifficulty.HARD
        assert env.max_hops == 15
    
    def test_get_neighbors(self):
        """Test neighbor detection based on RSSI."""
        env = MeshNetworkEnvironment(TaskDifficulty.EASY)
        env.reset(seed=42)
        
        neighbors = env._get_neighboring_devices("node_0")
        assert len(neighbors) > 0
        assert all(n.is_active for n in neighbors)
    
    def test_step_valid_action(self):
        """Test taking a valid step."""
        env = MeshNetworkEnvironment(TaskDifficulty.EASY)
        obs = env.reset(seed=42)
        
        if obs.neighboring_devices:
            target = obs.neighboring_devices[0]
            action = MeshAction(target_device_id=target.device_id)
            
            obs, reward, done, info = env.step(action)
            
            assert env.current_hop == 1
            assert obs.hops_taken == 1
    
    def test_battery_drain(self):
        """Test battery drain on device."""
        env = MeshNetworkEnvironment(TaskDifficulty.EASY)
        env.reset(seed=42)
        
        initial_battery = env.device_map["node_0"].battery_level
        
        # Get neighbor and send alert
        neighbors = env._get_neighboring_devices("node_0")
        if neighbors:
            action = MeshAction(target_device_id=neighbors[0].device_id)
            env.step(action)
            
            # Battery should have decreased
            current_battery = env.device_map["node_0"].battery_level
            assert current_battery < initial_battery
    
    def test_successful_delivery(self):
        """Test successful delivery to gateway."""
        env = MeshNetworkEnvironment(TaskDifficulty.EASY)
        obs = env.reset(seed=42)
        
        # In easy mode, gateway should be reachable within a few hops
        for _ in range(env.max_hops):
            if env.done or env.success:
                break
            
            neighbors = obs.neighboring_devices
            if neighbors:
                # Try to find gateway or a device closer to it
                target = min(neighbors, key=lambda d: 
                           ((d.position[0] - env.device_map[env.gateway_location].position[0])**2 +
                            (d.position[1] - env.device_map[env.gateway_location].position[1])**2)**0.5)
                
                action = MeshAction(target_device_id=target.device_id)
                obs, reward, done, info = env.step(action)
                
                if env.success:
                    break
    
    def test_max_hops_exceeded(self):
        """Test termination when max hops exceeded."""
        env = MeshNetworkEnvironment(TaskDifficulty.EASY)
        obs = env.reset(seed=42)
        
        # Take steps until max hops or success
        for i in range(env.max_hops + 1):
            if env.done:
                break
            
            neighbors = obs.neighboring_devices
            if neighbors:
                action = MeshAction(target_device_id=neighbors[0].device_id)
                obs, reward, done, info = env.step(action)
        
        # Should be done (either success or max hops exceeded)
        assert env.done or env.current_hop >= env.max_hops
    
    def test_render(self):
        """Test environment rendering."""
        env = MeshNetworkEnvironment(TaskDifficulty.EASY)
        env.reset()
        rendered = env.render()
        
        assert isinstance(rendered, str)
        assert "Mesh Network State" in rendered
        assert "Hops Taken" in rendered
    
    def test_episode_stats(self):
        """Test episode statistics."""
        env = MeshNetworkEnvironment(TaskDifficulty.EASY)
        env.reset()
        
        stats = env.get_episode_stats()
        
        assert "success" in stats
        assert "hops" in stats
        assert "reward" in stats
        assert "difficulty" in stats


class TestTaskGrader:
    """Tests for the task grading system."""
    
    def test_grader_initialization(self):
        """Test grader initialization."""
        grader = TaskGrader(n_episodes=5)
        assert grader.n_episodes == 5
    
    def test_grade_easy_task(self):
        """Test grading on easy task."""
        grader = TaskGrader(n_episodes=3)
        
        def dummy_agent(obs):
            """Simple agent that chooses first neighbor."""
            if obs.neighboring_devices:
                return MeshAction(target_device_id=obs.neighboring_devices[0].device_id)
            else:
                return MeshAction(target_device_id=obs.current_device_id)
        
        result = grader.grade_task(dummy_agent, TaskDifficulty.EASY)
        
        assert result.difficulty == TaskDifficulty.EASY
        assert 0.0 <= result.score <= 1.0
        assert 0.0 <= result.success_rate <= 1.0
        assert result.average_hops >= 0
    
    def test_grade_medium_task(self):
        """Test grading on medium task."""
        grader = TaskGrader(n_episodes=2)
        
        def smart_agent(obs):
            """Agent that moves toward gateway."""
            gateway_dist = obs.gateway_distance
            best_neighbor = None
            best_distance = gateway_dist
            
            for neighbor in obs.neighboring_devices:
                if neighbor.is_active and neighbor.battery_level > 10:
                    # Approximation: prefer neighbors that haven't been used much
                    if neighbor.hop_count < (best_neighbor.hop_count if best_neighbor else float('inf')):
                        best_neighbor = neighbor
                        best_distance = obs.gateway_distance - 1  # Approximate
            
            if best_neighbor:
                return MeshAction(target_device_id=best_neighbor.device_id)
            elif obs.neighboring_devices:
                return MeshAction(target_device_id=obs.neighboring_devices[0].device_id)
            else:
                return MeshAction(target_device_id=obs.current_device_id)
        
        result = grader.grade_task(smart_agent, TaskDifficulty.MEDIUM)
        
        assert result.difficulty == TaskDifficulty.MEDIUM
        assert 0.0 <= result.score <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
