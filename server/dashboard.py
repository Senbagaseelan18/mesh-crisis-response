"""
Enhanced dashboard endpoints for visualization.
Serves interactive web interface and provides real-time metrics.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import json
import os

def add_dashboard_routes(app: FastAPI):
    """Add dashboard routes to FastAPI app."""
    
    @app.get("/dashboard", response_class=HTMLResponse)
    async def dashboard():
        """Serve interactive dashboard."""
        return DASHBOARD_HTML
    
    @app.get("/api/network-topology/{difficulty}")
    async def get_network_topology(difficulty: str):
        """Get network topology for visualization."""
        from server.environment import MeshNetworkEnvironment
        from models import TaskDifficulty
        
        try:
            env = MeshNetworkEnvironment(TaskDifficulty[difficulty.upper()])
            env.reset()
            
            # Build topology data
            nodes = []
            edges = []
            
            for device in env.devices.values():
                nodes.append({
                    "id": device.id,
                    "x": device.position[0],
                    "y": device.position[1],
                    "battery": device.battery,
                    "active": device.is_active,
                    "role": "gateway" if device.id == env.gateway_id else "router"
                })
            
            # Add edges between neighbors
            for device_id, device in env.devices.items():
                for neighbor in env._get_neighboring_devices(device_id):
                    edges.append({
                        "source": device_id,
                        "target": neighbor.id,
                        "rssi": neighbor.signal_strength
                    })
            
            return {
                "nodes": nodes,
                "edges": edges,
                "difficulty": difficulty,
                "max_hops": env.max_hops
            }
        except Exception as e:
            return {"error": str(e), "nodes": [], "edges": []}
    
    @app.post("/api/run-episode/{difficulty}/{agent}")
    async def run_episode(difficulty: str, agent: str, n_steps: int = 20):
        """Run a single episode and return step-by-step data."""
        try:
            from server.environment import MeshNetworkEnvironment
            from models import TaskDifficulty
            from agents.agents import (
                RandomAgent, GreedyAgent, IntelligentAgent, 
                ConservativeAgent, ExplorativeAgent
            )
            from agents.advanced_agents import DQNAgent, PPOAgent, AdaptiveAgent
            
            agent_map = {
                "random": RandomAgent(),
                "greedy": GreedyAgent(),
                "intelligent": IntelligentAgent(),
                "conservative": ConservativeAgent(),
                "explorative": ExplorativeAgent(),
                "dqn": DQNAgent(),
                "ppo": PPOAgent(),
                "adaptive": AdaptiveAgent(),
            }
            
            if agent not in agent_map:
                return {"error": f"Unknown agent: {agent}"}
            
            env = MeshNetworkEnvironment(TaskDifficulty[difficulty.upper()])
            selected_agent = agent_map[agent]
            
            obs = env.reset()
            steps_data = []
            total_reward = 0.0
            done = False
            
            for step in range(n_steps):
                action = selected_agent.act(obs)
                obs, reward, done = env.step(action)
                total_reward += reward
                
                steps_data.append({
                    "step": step + 1,
                    "action": action,
                    "reward": reward,
                    "total_reward": total_reward,
                    "current_device": obs.current_device_id,
                    "battery": obs.current_battery,
                    "rssi": obs.current_rssi,
                    "distance": obs.gateway_distance,
                    "hops": obs.hops_taken,
                    "done": done
                })
                
                if done:
                    break
            
            return {
                "agent": agent,
                "difficulty": difficulty,
                "success": done,
                "steps": steps_data,
                "total_reward": total_reward,
                "total_steps": len(steps_data)
            }
        except Exception as e:
            return {"error": str(e)}


DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emergency Mesh Network Router - Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 14px;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 30px;
        }
        
        .card {
            background: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
        }
        
        .card h2 {
            font-size: 18px;
            margin-bottom: 15px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .topology-canvas {
            width: 100%;
            height: 300px;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        .controls {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }
        
        select, button {
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            background: white;
            transition: all 0.3s;
        }
        
        select {
            flex: 1;
            min-width: 120px;
        }
        
        button {
            background: #667eea;
            color: white;
            border: none;
            font-weight: 600;
        }
        
        button:hover {
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        
        .metric {
            background: white;
            padding: 12px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }
        
        .metric-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        
        .steps-log {
            background: white;
            border: 1px solid #ddd;
            border-radius: 6px;
            max-height: 300px;
            overflow-y: auto;
            font-size: 12px;
        }
        
        .step-item {
            padding: 10px;
            border-bottom: 1px solid #f0f0f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .step-item:hover {
            background: #f8f9fa;
        }
        
        .step-num {
            font-weight: bold;
            color: #667eea;
            min-width: 30px;
        }
        
        .step-action {
            flex: 1;
            margin: 0 10px;
            color: #666;
        }
        
        .step-reward {
            color: #27ae60;
            font-weight: bold;
        }
        
        .chart-container {
            position: relative;
            height: 250px;
            margin-bottom: 20px;
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        
        .loading.active {
            display: block;
        }
        
        @media (max-width: 1024px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            margin-top: 5px;
        }
        
        .status-success {
            background: #d4edda;
            color: #155724;
        }
        
        .status-failure {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 Emergency Mesh Network Router</h1>
            <p>Real-time RL Environment Dashboard for Autonomous Alert Routing</p>
        </div>
        
        <div class="main-grid">
            <!-- Network Topology -->
            <div class="card">
                <h2>Network Topology</h2>
                <div class="controls">
                    <select id="difficultySelect">
                        <option value="easy">Easy</option>
                        <option value="medium" selected>Medium</option>
                        <option value="hard">Hard</option>
                    </select>
                    <button onclick="loadTopology()">Load Network</button>
                </div>
                <canvas id="topologyCanvas" class="topology-canvas"></canvas>
            </div>
            
            <!-- Live Metrics -->
            <div class="card">
                <h2>Live Episode Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-label">Total Reward</div>
                        <div class="metric-value" id="totalReward">0.00</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Hops Taken</div>
                        <div class="metric-value" id="hopsTaken">0</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Battery Level</div>
                        <div class="metric-value" id="batteryLevel">100%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Current RSSI</div>
                        <div class="metric-value" id="rssiValue">-50 dBm</div>
                    </div>
                </div>
            </div>
            
            <!-- Agent Tester -->
            <div class="card">
                <h2>Agent Tester</h2>
                <div class="controls">
                    <select id="agentSelect">
                        <optgroup label="Baseline Agents">
                            <option value="random">Random Agent</option>
                            <option value="greedy" selected>Greedy Agent</option>
                            <option value="intelligent">Intelligent Agent</option>
                            <option value="conservative">Conservative Agent</option>
                            <option value="explorative">Explorative Agent</option>
                        </optgroup>
                        <optgroup label="Advanced Agents">
                            <option value="dqn">DQN Agent</option>
                            <option value="ppo">PPO Agent</option>
                            <option value="adaptive">Adaptive Agent</option>
                        </optgroup>
                    </select>
                    <button id="runBtn" onclick="runEpisode()">Run Episode</button>
                </div>
                <div class="loading" id="loading">
                    <p>⏳ Running episode...</p>
                </div>
                <div id="episodeResult"></div>
            </div>
            
            <!-- Steps Log -->
            <div class="card">
                <h2>Episode Steps Log</h2>
                <div class="steps-log" id="stepsLog">
                    <div style="padding: 20px; text-align: center; color: #999;">
                        Run an episode to see steps here
                    </div>
                </div>
            </div>
            
            <!-- Reward Chart -->
            <div class="card full-width">
                <h2>Reward Progression</h2>
                <div class="chart-container">
                    <canvas id="rewardChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        let topologyCtx = null;
        let rewardCtx = null;
        let rewardChart = null;
        let currentEpisodeData = null;

        async function loadTopology() {
            const difficulty = document.getElementById('difficultySelect').value;
            try {
                const response = await fetch(`/api/network-topology/${difficulty}`);
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || `Server error: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.error) {
                    console.error('Topology error:', data.error);
                    alert('Error loading topology: ' + data.error);
                } else {
                    drawTopology(data);
                }
            } catch (error) {
                console.error('Error loading topology:', error);
                alert('Failed to load network topology: ' + error.message);
            }
        }

        function drawTopology(data) {
            const canvas = document.getElementById('topologyCanvas');
            
            if (!canvas || !data || !data.nodes || data.nodes.length === 0) {
                console.warn('Invalid topology data');
                return;
            }
            
            const ctx = canvas.getContext('2d');
            const width = canvas.width;
            const height = canvas.height;

            ctx.clearRect(0, 0, width, height);

            // Draw grid background
            ctx.fillStyle = '#f9f9f9';
            ctx.fillRect(0, 0, width, height);
            ctx.strokeStyle = '#e0e0e0';
            ctx.lineWidth = 0.5;
            for (let i = 0; i < width; i += 50) {
                ctx.beginPath();
                ctx.moveTo(i, 0);
                ctx.lineTo(i, height);
                ctx.stroke();
            }
            for (let i = 0; i < height; i += 50) {
                ctx.beginPath();
                ctx.moveTo(0, i);
                ctx.lineTo(width, i);
                ctx.stroke();
            }
            
            // Draw edges first
            ctx.strokeStyle = '#ddd';
            ctx.lineWidth = 1;
            if (data.edges && data.edges.length > 0) {
                data.edges.forEach(edge => {
                    const source = data.nodes.find(n => n.id === edge.source);
                    const target = data.nodes.find(n => n.id === edge.target);
                    if (source && target) {
                        ctx.beginPath();
                        ctx.moveTo(source.x, source.y);
                        ctx.lineTo(target.x, target.y);
                        ctx.stroke();
                    }
                });
            }

            // Draw nodes
            data.nodes.forEach(node => {
                if (!node.x || !node.y) return;
                
                ctx.fillStyle = node.role === 'gateway' ? '#ff6b6b' : '#667eea';
                if (!node.active) {
                    ctx.fillStyle = '#ccc';
                }
                
                ctx.beginPath();
                ctx.arc(node.x, node.y, 12, 0, 2 * Math.PI);
                ctx.fill();
                
                // Draw border
                ctx.strokeStyle = node.role === 'gateway' ? '#c92a2a' : '#5568d3';
                ctx.lineWidth = 2;
                ctx.stroke();
                
                // Draw label
                ctx.fillStyle = 'white';
                ctx.font = 'bold 10px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                const label = node.id.replace('node_', '');
                ctx.fillText(label, node.x, node.y);
            });

            // Draw legend
            ctx.font = '12px Arial';
            ctx.fillStyle = '#333';
            ctx.textAlign = 'left';
            ctx.fillText('● Gateway (Red)', 10, height - 30);
            ctx.fillText('● Router (Blue)', 10, height - 10);
        }

        async function runEpisode() {
            const difficulty = document.getElementById('difficultySelect').value;
            const agent = document.getElementById('agentSelect').value;
            const runBtn = document.getElementById('runBtn');
            const loading = document.getElementById('loading');

            runBtn.disabled = true;
            loading.classList.add('active');

            try {
                const response = await fetch(`/api/run-episode/${difficulty}/${agent}?n_steps=30`);
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || `Server error: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.error) {
                    alert('Error: ' + data.error);
                } else if (data.steps && data.steps.length > 0) {
                    currentEpisodeData = data;
                    displayEpisodeResult(data);
                    updateMetrics(data);
                    drawRewardChart(data);
                } else {
                    alert('No steps were recorded in the episode');
                }
            } catch (error) {
                console.error('Error running episode:', error);
                alert('Failed to run episode: ' + error.message);
            } finally {
                runBtn.disabled = false;
                loading.classList.remove('active');
            }
        }

        function displayEpisodeResult(data) {
            const result = document.getElementById('episodeResult');
            
            if (!data || !data.steps || data.steps.length === 0) {
                result.innerHTML = '<p style="color: #e74c3c;">No episode data available</p>';
                return;
            }
            
            const statusClass = data.success ? 'status-success' : 'status-failure';
            const statusText = data.success ? 'SUCCESS ✓' : 'INCOMPLETE';
            const totalReward = parseFloat(data.total_reward) || 0;
            
            result.innerHTML = `
                <div style="margin-top: 10px;">
                    <p><strong>Agent:</strong> ${data.agent}</p>
                    <p><strong>Difficulty:</strong> ${data.difficulty}</p>
                    <p><strong>Total Reward:</strong> ${totalReward.toFixed(2)}</p>
                    <p><strong>Total Steps:</strong> ${data.total_steps}</p>
                    <p><span class="status-badge ${statusClass}">${statusText}</span></p>
                </div>
            `;

            // Display steps log
            const stepsLog = document.getElementById('stepsLog');
            if (data.steps && data.steps.length > 0) {
                stepsLog.innerHTML = data.steps.map((step, idx) => {
                    const reward = parseFloat(step.reward) || 0;
                    return `
                        <div class="step-item">
                            <span class="step-num">#${step.step}</span>
                            <span class="step-action">${step.action}</span>
                            <span class="step-reward">+${reward.toFixed(3)}</span>
                        </div>
                    `;
                }).join('');
            }
        }

        function updateMetrics(data) {
            if (data.steps && data.steps.length > 0) {
                const lastStep = data.steps[data.steps.length - 1];
                document.getElementById('totalReward').textContent = parseFloat(data.total_reward || 0).toFixed(2);
                document.getElementById('hopsTaken').textContent = lastStep.hops || 0;
                document.getElementById('batteryLevel').textContent = parseFloat(lastStep.battery || 100).toFixed(0) + '%';
                document.getElementById('rssiValue').textContent = parseFloat(lastStep.rssi || -50).toFixed(1) + ' dBm';
            }
        }

        function drawRewardChart(data) {
            const canvas = document.getElementById('rewardChart');
            
            if (!data || !data.steps || data.steps.length === 0) {
                console.warn('No data available for chart');
                return;
            }
            
            if (rewardChart) {
                rewardChart.destroy();
            }

            const stepNumbers = data.steps.map(s => s.step);
            const rewards = data.steps.map(s => parseFloat(s.reward) || 0);
            const cumulativeRewards = [];
            let total = 0;
            data.steps.forEach(s => {
                total += parseFloat(s.reward) || 0;
                cumulativeRewards.push(total);
            });

            rewardChart = new Chart(canvas, {
                type: 'line',
                data: {
                    labels: stepNumbers,
                    datasets: [
                        {
                            label: 'Cumulative Reward',
                            data: cumulativeRewards,
                            borderColor: '#667eea',
                            backgroundColor: 'rgba(102, 126, 234, 0.1)',
                            borderWidth: 2,
                            tension: 0.4,
                            fill: true,
                            pointRadius: 3,
                            pointHoverRadius: 5
                        },
                        {
                            label: 'Step Reward',
                            data: rewards,
                            borderColor: '#764ba2',
                            backgroundColor: 'rgba(118, 75, 162, 0.1)',
                            borderWidth: 2,
                            tension: 0.4,
                            fill: true,
                            pointRadius: 3,
                            pointHoverRadius: 5
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        // Load initial topology on page load
        window.addEventListener('load', () => {
            loadTopology();
        });
    </script>
</body>
</html>
"""
