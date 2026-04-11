---
title: Emergency Mesh-Network Router
emoji: 🚨
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: true
---

<div align="center">

# 🚨 **EMERGENCY MESH-NETWORK ROUTER** 🚨

## *Your AI's Mission: Save Lives Through Intelligent Routing* 💪

<br>

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-2E86AB?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?logo=fastapi&logoColor=white&style=for-the-badge)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/LLM-Integrated-412991?logo=openai&logoColor=white&style=for-the-badge)](https://openai.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white&style=for-the-badge)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![HF Spaces](https://img.shields.io/badge/🤗_HuggingFace-Live_Demo-orange?style=for-the-badge)](https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router)

### 🎯 *Advanced RL Environment with LLM Integration*

✨ **Train intelligent AI agents to route emergency alerts through mesh networks**  
🌍 *Real-world inspired crisis communication*  
⚡ *Production-ready with full API support*

</div>

<br>

---

## 🚀 **Quick Navigation**

<div align="center">

| 📖 | 💻 | 🎮 | 🌐 |
|:--:|:--:|:--:|:--:|
| [**About**](#-about) | [**Install**](#-setup) | [**Tasks**](#-challenge-levels) | [**API**](#-api-reference) |

</div>

---

## 📋 **About This Project**

<div align="left">

> ### 💡 **The Challenge**
> 
> In disaster scenarios, **communication networks collapse**. Emergency services must get their message through. 
> But routing through failed nodes while managing **battery, bandwidth, and latency** is a **complex optimization problem**.
>
> **Your job?** Train RL agents using specialized graders to find the best routes. 🎯

### 🌟 Why This Matters

- 🚨 **Real-World Impact**: Crisis communication is critical for disaster response
- 🤖 **Advanced AI**: Multi-phase training with 5 specialized evaluation systems  
- 🌐 **Complex Environment**: Dynamic networks, cascading failures, resource constraints
- 📈 **Scalable Learning**: Progressive difficulty from novice to expert challenge
- 🧠 **LLM Ready**: Integrates with OpenAI for intelligent routing decisions

</div>

---

## ⚡ **Key Features**

<table align="center">
<tr>
<td align="center" width="33%">

### 🤖 5 Task Levels
Easy → Expert → Extreme  
Progressive complexity

</td>
<td align="center" width="33%">

### 🧠 5 Specialized Graders
Comprehensive evaluation  
Reward-based learning

</td>
<td align="center" width="33%">

### 📊 Live Dashboard
Real-time metrics  
Beautiful UI

</td>
</tr>
<tr>
<td align="center" width="33%">

### 🔌 Full APIs
Phase 2+ compliant  
Complete endpoints

</td>
<td align="center" width="33%">

### 🐳 Docker Ready
One-click deploy  
Production quality

</td>
<td align="center" width="33%">

### ⚙️ Configurable
YAML-based settings  
Easy customization

</td>
</tr>
</table>

---

## 💻 **Setup**

### 📦 Installation (2 Minutes)

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Senbagaseelan18/mesh-crisis-response.git
cd mesh-crisis-response

# 2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt
```

### ▶️ Run Locally

```bash
# Start the FastAPI server
python -m server.app

# 🌐 Open in your browser
# http://localhost:7860

# 📊 View dashboard
# http://localhost:7860/dashboard
```

### 🐳 Docker Deployment

```bash
# Build image
docker build -t mesh-router .

# Run container
docker run -p 7860:7860 mesh-router

# 🌐 Access
# http://localhost:7860
```

### 🌍 Live Demo

**[🚀 Try the Live Demo](https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router)**

---

## 🎮 **Challenge Levels**

### 🟢 **EASY: Basic Routing**
```
📍 Scenario: Small 5-node network
🔋 Reliability: 80% connectivity
📏 Max Steps: 15
🎯 Objective: Route 3 alerts successfully
✅ Success: Score ≥ 0.6
```

### 🟡 **MEDIUM: Multi-Network**
```
📍 Scenario: 8 nodes with 2 subnets
🔋 Reliability: 70% connectivity
📏 Max Steps: 20
🎯 Objective: Handle congestion
✅ Success: Score ≥ 0.7
```

### 🔴 **HARD: Crisis Mode**
```
📍 Scenario: 12 nodes with cascading failures
🔋 Reliability: 60% connectivity
📏 Max Steps: 30
🎯 Objective: Dynamic priority routing
✅ Success: Score ≥ 0.8
```

### 🟣 **EXPERT: Advanced Tactics**
```
📍 Scenario: 15 nodes, complex topology
🔋 Reliability: 50% connectivity
📏 Max Steps: 40
🎯 Objective: Battery & bandwidth optimization
✅ Success: Score ≥ 0.85
```

### ⚫ **EXTREME: Master Challenge**
```
📍 Scenario: 20 nodes, full chaos
🔋 Reliability: 40% connectivity
📏 Max Steps: 50
🎯 Objective: Balanced metrics excellence
✅ Success: Score ≥ 0.9
```

---

## 🔌 **API Reference**

### 📡 **Core Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Server status |
| `GET` | `/health` | Health check |
| `POST` | `/reset` | Initialize environment |
| `POST` | `/step` | Execute action |
| `GET` | `/state` | Get current state |
| `GET` | `/tasks` | List available tasks |
| `GET` | `/graders` | List grading systems |
| `GET` | `/validate-tasks` | Validate configuration |

### 💬 **Usage Examples**

```bash
# Reset environment for easy task
curl -X POST http://localhost:7860/reset?difficulty=easy

# Take an action  
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "target_device_id": "node_3",
    "priority": 1
  }'

# Get current state
curl -X GET http://localhost:7860/state

# List all tasks
curl -X GET http://localhost:7860/tasks

# View grading systems
curl -X GET http://localhost:7860/graders

# Validate tasks configuration
curl -X GET http://localhost:7860/validate-tasks
```

---

## 📊 **Reward System**

```
Total Reward = (Successful Alerts × Alert_Weight)
             - (Failed Alerts × Failure_Penalty)
             - (Network_Congestion × Congestion_Cost)
             - (Steps_Taken × Step_Penalty)
```

**Partial rewards encourage efficient routing!** ✨

---

## 🧠 **Grading Systems**

| Grader | Focus | Best For |
|--------|-------|----------|
| 🏆 **RewardThreshold** | Total reward | Balanced learning |
| ⚡ **Efficient** | Hop optimization | Quick routing |
| 💪 **Robustness** | Failure handling | Reliability |
| 🔋 **BatteryEfficient** | Energy management | Long-term ops |
| ⚖️ **BalancedMetrics** | Multi-objective | Expert challenge |

---

## 📁 **Project Structure**

```
📦 mesh-crisis-response/
│
├── 🤖 agents/                    # AI Routing Agents
│   ├── agents.py                 # Baseline agents
│   └── advanced_agents.py        # Advanced ML agents
│
├── 🧠 ml/                        # Machine Learning
│   ├── benchmarks.py             # Performance metrics
│   ├── training_framework.py     # Training pipeline
│   ├── enhanced_environment.py   # Features & obstacles
│   └── metrics_dashboard.py      # Visualization
│
├── 🔌 server/                    # FastAPI Server
│   ├── app.py                    # Main server
│   ├── environment.py            # Environment class
│   ├── dashboard.py              # Web interface
│   └── conftest.py               # Testing config
│
├── 📋 Configuration
│   ├── openenv.yaml              # Environment config
│   ├── pyproject.toml            # Project settings
│   └── requirements.txt          # Dependencies
│
├── 🎯 Core Logic
│   ├── graders.py                # 5 grading systems
│   ├── tasks.py                  # 5 task definitions
│   ├── models.py                 # Data models
│   └── inference.py              # LLM inference
│
└── 📚 Documentation
    └── README.md                 # This file
```

---

## 🚀 **Deployment**

### HuggingFace Spaces

```yaml
# .hf-config.yml
title: Emergency Mesh-Network Router
sdk: docker
sdk_version: latest
app_file: server/app.py
models:
  - gpt-3.5-turbo
  - gpt-4
```

### Docker Hub

```bash
docker build -t username/mesh-router:latest .
docker push username/mesh-router:latest
```

### Local Docker Compose

```yaml
version: '3.8'
services:
  mesh-router:
    build: .
    ports:
      - "7860:7860"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

---

## 📈 **Performance Metrics**

Track your agent's performance:

- 📊 **Success Rate**: Percentage of alerts delivered
- ⏱️ **Hop Count**: Average hops per alert
- 🔋 **Battery Usage**: Energy efficiency
- 🚀 **Latency**: Time to delivery
- 💰 **Cost Efficiency**: Resource optimization

---

## 🔒 **License**

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 📞 **Support**

- 🐛 **Issues**: [GitHub Issues](https://github.com/Senbagaseelan18/mesh-crisis-response/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Senbagaseelan18/mesh-crisis-response/discussions)
- 📧 **Email**: See repository contact info

---

## 🎉 **Get Involved**

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

<div align="center">

### 🌟 **Made with ❤️ for Emergency Response** 🌟

**[⭐ Star Us on GitHub](https://github.com/Senbagaseelan18/mesh-crisis-response)** | **[🚀 Try Live Demo](https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router)** | **[📖 Read Docs](docs/README.md)**

</div>

---

**Last Updated:** April 2026 | **Version:** 1.0.0 | **Status:** ✅ Production Ready
