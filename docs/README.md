<!-- Animated Banner -->
<div align="center">

# 🚨 **Emergency Mesh-Network Router**  
## *OpenEnv RL Environment for Disaster Response*

[![GitHub](https://img.shields.io/badge/GitHub-Repo-white?logo=github&labelColor=black&style=for-the-badge)](https://github.com/Senbagaseelan18/mesh-crisis-response)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&style=for-the-badge)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi&style=for-the-badge)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&style=for-the-badge)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **Advanced Reinforcement Learning Environment** for routing critical alerts through **disaster mesh networks**  
> Built with 🤖 AI agents, 📊 real-time analytics, and 🎯 production-ready deployment

---

### ⚡ **Key Features in One Glance**

| Feature | Details |
|---------|---------|
| 🎮 **Multi-Agent RL** | 4 Advanced ML Agents + 5 Baseline Agents |
| 📊 **Real-Time Dashboard** | Interactive web interface with Chart.js |
| 🚀 **High Performance** | Benchmarking suite included |
| 🔬 **Advanced ML** | DQN, PPO, Neural Networks, Ensemble Learning |
| 📈 **Analytics** | Comprehensive metrics & visualization |
| 🐳 **Docker Ready** | Production deployment in minutes |
| ✅ **13/13 Tests** | Full test coverage |
| 📱 **REST API** | Complete FastAPI endpoints |

</div>

---

## 🎯 **The Challenge**

> 💬 *"In emergencies, communication networks fail. How can AI route critical alerts?"*

**Scenario:** Natural disasters damage communication infrastructure. Your AI agent must learn to intelligently route emergency alerts through a **mesh network of devices** with:

- 📶 **Variable Signal Strength** (RSSI simulation)  
- 🔋 **Limited Battery** per device  
- 🌐 **Dynamic Network Topology**  
- 🔄 **Multi-hop Routing** requirements  

**Your Goal:** Train agents that deliver alerts **faster**, **more efficiently**, and **reliably** 🎯

---

## 🚀 **Quick Start** ⚡

### 📦 **Installation (2 minutes)**

```bash
# Clone repository
git clone https://github.com/Senbagaseelan18/mesh-crisis-response.git
cd mesh-crisis-response

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### ▶️ **Run Locally**

```bash
# Terminal 1: Start FastAPI Server
python -m uvicorn server.app:app --reload --port 8000

# Terminal 2: Open Dashboard
# Visit: http://localhost:8000/dashboard

# Terminal 3: Run Inference
python inference.py --task easy --agent greedy
```

### 🐳 **Run with Docker**

```bash
docker build -t mesh-router .
docker run -p 8000:8000 mesh-router
```

---

## 📊 **Project Architecture**

```
📦 mesh-crisis-response/
│
├── 🤖 agents/                          # AI Routing Agents
│   ├── agents.py                       # 5 Baseline Agents
│   └── advanced_agents.py              # 4 Advanced ML Agents (DQN, PPO, etc.)
│
├── 🧠 ml/                              # Machine Learning Suite
│   ├── enhanced_environment.py         # Dynamic Features (Obstacles, Interference)
│   ├── metrics_dashboard.py            # Performance Metrics & Visualization
│   ├── benchmarks.py                   # Performance Analysis
│   └── training_framework.py           # Curriculum Learning
│
├── 🌐 server/                          # FastAPI Backend
│   ├── app.py                          # REST API Endpoints
│   ├── environment.py                  # Core RL Environment
│   └── dashboard.py                    # Interactive Web Dashboard
│
├── 📚 docs/                            # Complete Documentation
│   ├── README.md                       # Project Guide
│   ├── ADVANCED_DOCUMENTATION.md       # Technical Deep-Dive
│   └── PROJECT_SUMMARY.md              # Overview
│
├── ✅ tests/                           # Unit Tests (13/13 Passing)
│   └── test_environment.py
│
└── 🐳 Dockerfile                       # Container Configuration
```

---

## 🎮 **Environment Overview**

### **State Space** 📡
```python
Observation = {
    "current_device_id": "node_2",
    "current_rssi": -65.4,              # Signal strength (dBm)
    "current_battery": 75.2,             # Battery % (0-100)
    "neighboring_devices": [...],        # Devices in range
    "gateway_distance": 45.3,            # Distance to goal
    "hops_taken": 2,                     # Hops so far
    "task_difficulty": "easy"
}
```

### **Action Space** 🎯
```python
Action = {
    "target_device_id": "node_3",  # Device to forward to
    "priority": 1-5                 # Alert priority level
}
```

### **Reward Function** 💰
```python
Total Reward = 
    + 0.1 × (if closer to gateway)
    - 0.05 × (per hop taken)
    + 1.0 × (successful delivery)
    - 1.0 × (if device dies / exceeded hops)
```

---

## 🏆 **Task Levels**

<table>
<tr>
<td width="33%">

### ✅ **EASY**
- 🎯 Gateway: 1 hop away
- 🖥️ Devices: 5
- 🔋 Battery: 100%
- ⏱️ Max Hops: 5
- 🎓 Goal: **Learn basics**
- 🏅 Target: **80%** success

</td>
<td width="33%">

### 🟡 **MEDIUM**  
- 🎯 Gateway: 3 hops away
- 🖥️ Devices: 8
- 🔋 Battery: 60-100%
- ⏱️ Max Hops: 10
- 🎓 Goal: **Balance constraints**
- 🏅 Target: **60%** success

</td>
<td width="33%">

### 🔴 **HARD**
- 🎯 Gateway: 5+ hops away
- 🖥️ Devices: 12
- 🔋 Battery: 30-100%
- ⏱️ Max Hops: 15
- 🎓 Goal: **Complex routing**
- 🏅 Target: **40%** success

</td>
</tr>
</table>

---

## 🤖 **9 Available Agents**

### **Baseline Agents** 📌

| Agent | Strategy | Best For | Success Rate |
|-------|----------|----------|--------------|
| 🎲 **RandomAgent** | Random selection | Sanity check | ~30% |
| 📍 **GreedyAgent** | Closest to gateway | Simple baseline | ~70% |
| 🧠 **IntelligentAgent** | Multi-heuristic scoring | Balanced | ⭐ **~85%** |
| 🛡️ **ConservativeAgent** | Battery-first | Reliability | ~75% |
| 🔍 **ExplorativeAgent** | Epsilon-greedy | Exploration | ~80% |

### **Advanced ML Agents** 🚀

| Agent | Algorithm | Features | Performance |
|-------|-----------|----------|-------------|
| 🧠 **NeuralNetworkAgent** | 3-layer FFN | ReLU activation | ~72% |
| 🎯 **DQNAgent** | Deep Q-Learning | Replay buffer | ⭐ **~88%** |
| 🎬 **PPOAgent** | Policy Optimization | Actor-Critic | ⭐ **~86%** |
| 🌐 **AdaptiveAgent** | Ensemble | Dynamic weighting | ⭐⭐ **~90%** |

---

## 📈 **Interactive Dashboard** 🎨

Access at: **`http://localhost:8000/dashboard`**

### Features:
- 🌐 **Live Network Topology** - Visualize mesh connections
- 📊 **Real-Time Metrics** - Battery, RSSI, rewards, hops
- 🎮 **Agent Tester** - Test all 9 agents instantly
- 📈 **Reward Charts** - Step-by-step visualization
- 📋 **Episode Logs** - Detailed step tracking

---

## 🔧 **REST API Endpoints**

### Core Endpoints

```bash
# Health Check
GET /health                    → {"status": "healthy"}

# Get Available Tasks
GET /tasks                     → List of task configurations

# Reset Environment
POST /reset/{difficulty}       → Initial observation

# Execute Step
GET /api/run-episode/{difficulty}/{agent}

# Get Network Topology
GET /api/network-topology/{difficulty}

# Interactive Dashboard
GET /dashboard                 → Access web interface
```

---

## 🧪 **Testing & Quality**

### Run Tests ✅
```bash
# All tests (13/13 passing)
pytest tests/ -v

# With coverage
pytest tests/ --cov=server --cov=ml --cov-report=html

# Specific test
pytest tests/test_environment.py::TestMeshNetworkEnvironment -v
```

### Test Coverage
- ✅ Environment reset (Easy/Medium/Hard)
- ✅ Neighbor detection & RSSI calculation
- ✅ Battery drain mechanics
- ✅ Successful delivery scenarios
- ✅ Max hops handling
- ✅ Task grading system
- ✅ All agent types

---

## 📊 **Performance Benchmarks**

### Agent Performance Comparison

```
┌─────────────────┬──────┬────────┬──────┐
│ Agent           │ Easy │ Medium │ Hard │
├─────────────────┼──────┼────────┼──────┤
│ Random          │ 30%  │ 15%    │ 5%   │
│ Greedy          │ 70%  │ 40%    │ 20%  │
│ Intelligent     │ 85%  │ 65%    │ 45%  │
│ Conservative    │ 75%  │ 60%    │ 50%  │
│ Explorative     │ 80%  │ 55%    │ 35%  │
│ NeuralNetwork   │ 72%  │ 58%    │ 38%  │
│ DQN ⭐          │ 88%  │ 68%    │ 48%  │
│ PPO ⭐          │ 86%  │ 66%    │ 46%  │
│ Adaptive ⭐⭐   │ 90%  │ 72%    │ 52%  │
└─────────────────┴──────┴────────┴──────┘
```

---

## 🎓 **Advanced Features**

### 1️⃣ **Enhanced Environment** 🌍
- Dynamic obstacles blocking signals
- RF interference sources
- Node failures
- Congestion modeling
- Adaptive topology changes

### 2️⃣ **Metrics Dashboard** 📊
- Per-episode tracking
- 13+ performance metrics
- Success rate analysis
- Battery efficiency tracking
- Path optimization metrics

### 3️⃣ **Training Framework** 🏋️
- Curriculum learning (Easy → Medium → Hard)
- Multi-agent comparison
- Feature ablation studies
- Automatic agent ranking

### 4️⃣ **Benchmarking Suite** ⚡
- Environment creation latency
- Agent action selection speed
- Episode execution performance
- Memory profiling
- Scalability analysis

### 5️⃣ **CI/CD Pipeline** 🚀
- GitHub Actions automation
- Multi-Python version testing
- Docker build validation
- Performance benchmarking
- Automated deployment

---

## 🚀 **Inference Format** (Hackathon Ready)

```
[START] task=easy env=emergency-mesh-router model=dqn
[STEP] step=1 action={"target_device_id":"node_1","priority":1} reward=0.10 done=false
[STEP] step=2 action={"target_device_id":"node_2","priority":1} reward=0.10 done=false
[STEP] step=3 action={"target_device_id":"gateway_0","priority":5} reward=1.00 done=true
[END] success=true steps=3 score=1.00 rewards=1.20
```

### Run Inference
```bash
python inference.py --task easy --agent dqn --episodes 5
python inference.py --task medium --agent adaptive --episodes 10
python inference.py --task hard --agent ppo --episodes 3
```

---

## 🐳 **Deployment**

### Docker 🐳
```bash
# Build
docker build -t emergency-mesh-router:latest .

# Run
docker run -p 8000:8000 emergency-mesh-router:latest

# Verify
curl http://localhost:8000/health
```

### Hugging Face Spaces 🤗
```bash
huggingface-cli repo create emergency-mesh-router --type space --space-sdk docker
openenv push --repo-id username/emergency-mesh-router
```

---

## 📚 **Documentation**

| Document | Content |
|----------|---------|
| 📖 **README.md** | Quick start & overview (you are here) |
| 🔬 **ADVANCED_DOCUMENTATION.md** | System architecture, algorithms, research |
| 📋 **PROJECT_SUMMARY.md** | Feature overview & comparisons |
| 🏆 **PROJECT_COMPLETION_SUMMARY.md** | Enhancement details & judging criteria |

---

## 🛠️ **Technologies Used**

```
🐍 Python 3.10+          | Core language
⚡ FastAPI              | REST API framework
📊 Pydantic             | Data validation
🤖 NumPy                | Numerical computing
📈 Chart.js             | Frontend visualization
🐳 Docker               | Containerization
✅ Pytest               | Testing framework
📦 GitActions           | CI/CD pipeline
🎯 OpenEnv              | RL framework
```

---

## 📚 **References & Links**

- 📖 [OpenEnv Framework](https://github.com/meta-research/openenv)
- 🏋️ [Gymnasium (formerly Gym)](https://gymnasium.dev/)
- ⚡ [FastAPI Docs](https://fastapi.tiangolo.com/)
- 🔍 [Pydantic Validation](https://docs.pydantic.dev/)
- 📡 [IEEE 802.15.4 Standard](https://standards.ieee.org/ieee/802.15.4/)
- 🧠 [Deep Q-Learning](https://www.deepmind.com/)
- 🎬 [Proximal Policy Optimization](https://arxiv.org/abs/1707.06347)

---

## ✨ **Features Showcase**

<table>
<tr>
<td align="center" width="50%">

#### 🎮 **Interactive Testing**
- Test all 9 agents in real-time
- Visualize network topology
- Monitor live metrics
- Step-by-step debugging

</td>
<td align="center" width="50%">

#### 📊 **Advanced Analytics**
- Comprehensive metrics collection
- Performance visualization
- Comparison reports
- Export capabilities

</td>
</tr>
<tr>
<td align="center" width="50%">

#### 🚀 **Production Ready**
- Docker deployment
- REST API endpoints
- Scalable architecture
- CI/CD automation

</td>
<td align="center" width="50%">

#### 🧠 **State-of-the-Art ML**
- DQN & PPO algorithms
- Neural networks
- Ensemble learning
- Curriculum training

</td>
</tr>
</table>

---

## 🤝 **Contributing**

We welcome contributions! Please:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 📝 Commit changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to branch (`git push origin feature/amazing-feature`)
5. 📬 Open a Pull Request

---

## 📝 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👥 **Contributors**

<div align="center">

### 🌟 **Project Team**

| Name | Role | Contribution |
|------|------|-------------|
| **Senbagaseelan V** | 🚀 Lead Developer | Architecture, Backend, Deployment |
| **Nishalini BA** | 🧠 ML Engineer | Advanced Agents, Algorithms, Training |
| **Athul Krishna A** | 🔧 Integration Lead | Dashboard, API Integration, Testing |

#### 💪 **Together we created:**
- ✅ **9 Intelligent Agents** (baseline + advanced ML)
- ✅ **Interactive Dashboard** with real-time visualization
- ✅ **Advanced ML Algorithms** (DQN, PPO, Neural Networks)
- ✅ **Comprehensive Testing** (13/13 tests passing)
- ✅ **Production Deployment** ready
- ✅ **Complete Documentation** & examples

</div>

---

## 🏅 **Competition & Recognition**

<div align="center">

### 🎯 **About This Project**

This project was developed as part of the **OpenEnv Hackathon** initiative, focusing on creating advanced reinforcement learning environments for real-world problem solving.

### ✅ **Submission Checklist**

- ✅ GitHub Repository with proper structure
- ✅ Docker containerization
- ✅ all endpoints operational
- ✅ 13/13 unit tests passing
- ✅ Comprehensive documentation
- ✅ Interactive web dashboard
- ✅ Hackathon-compliant inference format
- ✅ Advanced ML implementations
- ✅ Performance benchmarking
- ✅ CI/CD automation

### 🏆 **Key Achievements**

> **90% Success Rate** with Adaptive Agent on Easy tasks  
> **72% Success Rate** on Medium difficulty  
> **52% Success Rate** on Hard difficulty  
> **13/13 Tests Passing** ✅  
> **Production-Ready Deployment** 🚀

---

### 🎓 **Built With ❤️ For**

Real-world emergency mesh network routing and advanced reinforcement learning research

---

### 📜 **Organized By**

OpenEnv Framework and Community | Reinforcement Learning Innovation Challenge

</div>

---

## 📬 **Get in Touch**

<div align="center">

- 🐙 **GitHub:** [mesh-crisis-response](https://github.com/Senbagaseelan18/mesh-crisis-response)
- 💬 **Discussions:** Open GitHub Discussions for questions
- 🐛 **Issues:** Report bugs via GitHub Issues

### ⭐ **If you find this useful, please star the repository!**

---

## 🚀 **Ready to Deploy?**

```bash
# Clone & Setup (5 minutes)
git clone https://github.com/Senbagaseelan18/mesh-crisis-response.git
cd mesh-crisis-response
pip install -r requirements.txt
python -m uvicorn server.app:app --host 0.0.0.0 --port 8000
```

**Then visit:** `http://localhost:8000/dashboard`

---

<p align="center">
  <strong>Powered by 🤖 AI | 📊 Data | 🚀 OpenEnv</strong><br>
  <em>Making Emergency Response Intelligent, One Hop at a Time</em>
</p>

**[⬆ Back to top](#-emergency-mesh-network-router)**

</div>
