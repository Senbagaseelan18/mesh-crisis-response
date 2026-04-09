"""
Real-time visualization and metrics dashboard for the mesh network environment.
Provides comprehensive analytics, performance metrics, and visualization.
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json
import math
import random

from models import MeshObservation, TaskDifficulty, MeshAction


@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics."""
    episode: int
    timestamp: str
    task_difficulty: str
    success: bool
    total_hops: int
    max_hops: int
    total_reward: float
    episode_length: int
    battery_efficiency: float  # Reward per battery used
    path_efficiency: float  # Hops vs optimal
    average_rssi: float
    final_battery: float
    convergence_time: int


class MetricsCollector:
    """Collects and analyzes metrics from environment episodes."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.episodes = []
        self.current_episode = None
        self.episode_counter = 0
    
    def start_episode(self, difficulty: TaskDifficulty):
        """Start collecting metrics for new episode."""
        self.episode_counter += 1
        self.current_episode = {
            "episode": self.episode_counter,
            "difficulty": difficulty.value,
            "start_time": datetime.now(),
            "steps": [],
            "total_reward": 0.0,
            "hops": 0,
            "success": False,
            "rssi_values": [],
            "battery_values": [],
        }
    
    def record_step(self, observation: MeshObservation, reward: float, action: str):
        """Record a single step in episode."""
        if self.current_episode is None:
            return
        
        self.current_episode["steps"].append({
            "timestep": observation.time_step,
            "current_device": observation.current_device_id,
            "reward": reward,
            "action": action,
            "battery": observation.current_battery,
            "rssi": observation.current_rssi,
            "distance_to_gateway": observation.gateway_distance,
        })
        
        self.current_episode["total_reward"] += reward
        self.current_episode["hops"] = observation.hops_taken
        self.current_episode["rssi_values"].append(observation.current_rssi)
        self.current_episode["battery_values"].append(observation.current_battery)
    
    def end_episode(self, success: bool, max_hops: int, final_battery: float):
        """Finish collecting metrics for episode."""
        if self.current_episode is None:
            return
        
        end_time = datetime.now()
        duration = (end_time - self.current_episode["start_time"]).total_seconds()
        
        # Calculate efficiency metrics
        battery_used = 100.0 - final_battery
        battery_efficiency = self.current_episode["total_reward"] / (battery_used + 0.1)
        path_efficiency = (self.current_episode["hops"] / max_hops) if max_hops > 0 else 1.0
        avg_rssi = sum(self.current_episode["rssi_values"]) / len(self.current_episode["rssi_values"]) if self.current_episode["rssi_values"] else 0.0
        
        # Create metrics object
        metrics = PerformanceMetrics(
            episode=self.current_episode["episode"],
            timestamp=end_time.isoformat(),
            task_difficulty=self.current_episode["difficulty"],
            success=success,
            total_hops=self.current_episode["hops"],
            max_hops=max_hops,
            total_reward=self.current_episode["total_reward"],
            episode_length=len(self.current_episode["steps"]),
            battery_efficiency=battery_efficiency,
            path_efficiency=path_efficiency,
            average_rssi=avg_rssi,
            final_battery=final_battery,
            convergence_time=int(duration * 1000),  # milliseconds
        )
        
        self.episodes.append(metrics)
        self.current_episode = None
        
        return metrics
    
    def get_summary(self) -> Dict:
        """Get summary statistics across all episodes."""
        if not self.episodes:
            return {}
        
        difficulty_groups = {}
        for metrics in self.episodes:
            diff = metrics.task_difficulty
            if diff not in difficulty_groups:
                difficulty_groups[diff] = []
            difficulty_groups[diff].append(metrics)
        
        summary = {}
        for difficulty, episodes in difficulty_groups.items():
            successes = sum(1 for e in episodes if e.success)
            total_reward = sum(e.total_reward for e in episodes)
            avg_hops = sum(e.total_hops for e in episodes) / len(episodes)
            avg_efficiency = sum(e.path_efficiency for e in episodes) / len(episodes)
            
            summary[difficulty] = {
                "episodes_run": len(episodes),
                "success_rate": successes / len(episodes),
                "average_reward": total_reward / len(episodes),
                "average_hops": avg_hops,
                "path_efficiency": avg_efficiency,
                "best_reward": max(e.total_reward for e in episodes),
                "worst_reward": min(e.total_reward for e in episodes),
            }
        
        return summary
    
    def get_episodes_json(self) -> str:
        """Export episodes as JSON."""
        episodes_data = [asdict(e) for e in self.episodes]
        return json.dumps(episodes_data, indent=2)
    
    def get_csv_report(self) -> str:
        """Export metrics as CSV."""
        if not self.episodes:
            return ""
        
        # CSV header
        header = ",".join([
            "Episode", "Difficulty", "Success", "Total_Hops", "Max_Hops",
            "Total_Reward", "Episode_Length", "Battery_Efficiency", "Path_Efficiency",
            "Average_RSSI", "Final_Battery", "Convergence_Time_ms", "Timestamp"
        ])
        
        # CSV rows
        rows = [header]
        for metrics in self.episodes:
            row = ",".join([
                str(metrics.episode),
                metrics.task_difficulty,
                str(metrics.success),
                str(metrics.total_hops),
                str(metrics.max_hops),
                f"{metrics.total_reward:.4f}",
                str(metrics.episode_length),
                f"{metrics.battery_efficiency:.4f}",
                f"{metrics.path_efficiency:.4f}",
                f"{metrics.average_rssi:.2f}",
                f"{metrics.final_battery:.2f}",
                str(metrics.convergence_time),
                metrics.timestamp,
            ])
            rows.append(row)
        
        return "\n".join(rows)


class VisualizationGenerator:
    """Generates visualization and rendering of mesh network."""
    
    @staticmethod
    def generate_ascii_topology(observation: MeshObservation, current_device_id: str) -> str:
        """Generate ASCII representation of network topology."""
        if not observation.neighboring_devices:
            return f"Current: [{current_device_id}] - No neighbors visible"
        
        output = f"\n{'═' * 60}\n"
        output += f"MESH NETWORK TOPOLOGY - {observation.task_difficulty.value.upper()}\n"
        output += f"{'═' * 60}\n\n"
        
        output += f"📍 Current Device: {current_device_id}\n"
        output += f"🔋 Battery: {observation.current_battery:.1f}%\n"
        output += f"📡 RSSI: {observation.current_rssi:.1f} dBm\n"
        output += f"🎯 Gateway Distance: {observation.gateway_distance:.1f}m\n"
        output += f"📊 Hops: {observation.hops_taken}\n"
        output += f"⏱️  Timestep: {observation.time_step}\n"
        output += f"\n{'─' * 60}\n"
        
        output += f"📡 NEIGHBORING DEVICES ({len(observation.neighboring_devices)}):\n"
        output += f"{'─' * 60}\n"
        
        for i, neighbor in enumerate(observation.neighboring_devices, 1):
            status = "🟢" if neighbor.is_active else "🔴"
            gateway_marker = "🏛️ " if neighbor.is_gateway else ""
            
            output += f"{i}. {status} {neighbor.device_id:15} {gateway_marker}\n"
            output += f"   Position: ({neighbor.position[0]:.1f}, {neighbor.position[1]:.1f})\n"
            output += f"   Battery:  {neighbor.battery_level:6.1f}%\n"
            output += f"   RSSI:     {neighbor.rssi:6.1f} dBm\n"
            output += f"   Hops:     {neighbor.hop_count}\n"
        
        output += f"\n{'═' * 60}\n"
        
        return output
    
    @staticmethod
    def generate_metrics_report(metrics: PerformanceMetrics) -> str:
        """Generate detailed metrics report."""
        output = f"\n{'═' * 60}\n"
        output += f"EPISODE METRICS REPORT\n"
        output += f"{'═' * 60}\n\n"
        
        output += f"Episode Information:\n"
        output += f"  Episode #:        {metrics.episode}\n"
        output += f"  Difficulty:       {metrics.task_difficulty.upper()}\n"
        output += f"  Status:           {'✅ SUCCESS' if metrics.success else '❌ FAILED'}\n"
        output += f"  Timestamp:        {metrics.timestamp}\n\n"
        
        output += f"Routing Statistics:\n"
        output += f"  Hops Used:        {metrics.total_hops} / {metrics.max_hops}\n"
        output += f"  Path Efficiency:  {metrics.path_efficiency * 100:.1f}%\n"
        output += f"  Episode Length:   {metrics.episode_length} steps\n"
        output += f"  Convergence Time: {metrics.convergence_time}ms\n\n"
        
        output += f"Reward Analysis:\n"
        output += f"  Total Reward:     {metrics.total_reward:.4f}\n"
        output += f"  Avg Reward/Step:  {metrics.total_reward / max(1, metrics.episode_length):.4f}\n"
        output += f"  Battery Efficiency: {metrics.battery_efficiency:.4f}\n\n"
        
        output += f"Network Health:\n"
        output += f"  Average RSSI:     {metrics.average_rssi:.1f} dBm\n"
        output += f"  Final Battery:    {metrics.final_battery:.1f}%\n"
        output += f"  Battery Used:     {100 - metrics.final_battery:.1f}%\n\n"
        
        output += f"{'═' * 60}\n"
        
        return output
    
    @staticmethod
    def generate_comparison_report(metrics_list: List[PerformanceMetrics]) -> str:
        """Generate comparison report across multiple episodes."""
        if not metrics_list:
            return "No metrics to compare"
        
        output = f"\n{'═' * 60}\n"
        output += f"EPISODE COMPARISON REPORT ({len(metrics_list)} episodes)\n"
        output += f"{'═' * 60}\n\n"
        
        # Group by difficulty
        difficulties = {}
        for m in metrics_list:
            if m.task_difficulty not in difficulties:
                difficulties[m.task_difficulty] = []
            difficulties[m.task_difficulty].append(m)
        
        for difficulty, metrics in sorted(difficulties.items()):
            successes = sum(1 for m in metrics if m.success)
            avg_reward = sum(m.total_reward for m in metrics) / len(metrics)
            avg_hops = sum(m.total_hops for m in metrics) / len(metrics)
            avg_battery_eff = sum(m.battery_efficiency for m in metrics) / len(metrics)
            
            output += f"\n{difficulty.upper()}:\n"
            output += f"  Episodes:      {len(metrics)}\n"
            output += f"  Success Rate:  {successes}/{len(metrics)} ({successes*100/len(metrics):.1f}%)\n"
            output += f"  Avg Reward:    {avg_reward:.4f}\n"
            output += f"  Avg Hops:      {avg_hops:.1f}\n"
            output += f"  Battery Eff:   {avg_battery_eff:.4f}\n"
        
        output += f"\n{'═' * 60}\n"
        
        return output


class DashboardServer:
    """Simple dashboard server for real-time metrics visualization."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        """Initialize dashboard."""
        self.metrics = metrics_collector
    
    def get_dashboard_html(self) -> str:
        """Generate HTML dashboard."""
        summary = self.metrics.get_summary()
        
        html = """
        <html>
        <head>
            <title>Emergency Mesh-Network Router Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                h1 { color: #333; }
                .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
                .metric-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .metric-card h3 { margin: 0 0 10px 0; color: #666; }
                .metric-value { font-size: 24px; font-weight: bold; color: #2196F3; }
                .chart-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 20px 0; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #2196F3; color: white; }
                tr:hover { background: #f5f5f5; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎯 Emergency Mesh-Network Router Dashboard</h1>
                <div class="metrics-grid">
        """
        
        for difficulty, stats in summary.items():
            html += f"""
                    <div class="metric-card">
                        <h3>{difficulty.upper()}</h3>
                        <p><strong>Success Rate:</strong> <span class="metric-value">{stats['success_rate']*100:.1f}%</span></p>
                        <p><strong>Avg Reward:</strong> {stats['average_reward']:.2f}</p>
                        <p><strong>Avg Hops:</strong> {stats['average_hops']:.1f}</p>
                        <p><strong>Episodes:</strong> {stats['episodes_run']}</p>
                    </div>
            """
        
        html += """
                </div>
                <div class="chart-container">
                    <h2>Success Rate by Difficulty</h2>
                    <canvas id="successChart" style="max-height: 300px;"></canvas>
                </div>
            </div>
            <script>
                const ctx = document.getElementById('successChart').getContext('2d');
                const labels = Object.keys(""" + json.dumps({k: v['success_rate']*100 for k,v in summary.items()}) + """);
                const data = Object.values(""" + json.dumps({k: v['success_rate']*100 for k,v in summary.items()}) + """);
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Success Rate (%)',
                            data: data,
                            backgroundColor: '#2196F3',
                        }]
                    }
                });
            </script>
        </body>
        </html>
        """
        
        return html


if __name__ == "__main__":
    import random
    from server.environment import MeshNetworkEnvironment
    from models import MeshAction
    
    print("Testing Metrics Collection and Visualization...")
    
    collector = MetricsCollector()
    env = MeshNetworkEnvironment(TaskDifficulty.EASY)
    
    # Run a few episodes
    for i in range(3):
        collector.start_episode(env.task_difficulty)
        obs = env.reset(seed=i)
        done = False
        
        while not done:
            action = random.choice(obs.neighboring_devices).device_id if obs.neighboring_devices else obs.current_device_id
            obs, reward, done, info = env.step(MeshAction(target_device_id=action))
            collector.record_step(obs, reward, action)
        
        metrics = collector.end_episode(env.success, env.max_hops, env.device_map[env.alert_location].battery_level)
        print(VisualizationGenerator.generate_metrics_report(metrics))
    
    print(VisualizationGenerator.generate_comparison_report(collector.episodes))
    print("\nSummary:")
    print(json.dumps(collector.get_summary(), indent=2))
