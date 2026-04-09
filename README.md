---
title: Emergency Mesh-Network Router
emoji: 🚨
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: true
---

<div align="center">

# 🚨 Emergency Mesh-Network Router

### An OpenEnv RL Environment for Emergency Alert Routing

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![HF Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router)
[![OpenEnv](https://img.shields.io/badge/openenv-core-green)](https://github.com/openenv-ai/openenv-core)

*A reinforcement learning challenge environment for training intelligent agents to optimize emergency alert routing through mesh networks during crisis scenarios.*

</div>

---

## 🎯 Overview

The **Emergency Mesh-Network Router** is a complete OpenEnv environment designed to train and evaluate RL agents in handling real-world emergency communications. Agents must route critical alerts through limited, unreliable mesh network nodes while managing bandwidth, latency, and node failures—a simulation of actual crisis response challenges.

### 🌟 Why This Matters
- **Real-world relevance**: Crisis communication routing is a critical problem in disaster management
- **Multi-agent learning**: Train agents to make optimal routing decisions under uncertainty
- **Scalable complexity**: Three difficulty levels from basic routing to complex multi-network scenarios

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multiple Agent Types** | Baseline (Random, Greedy, Intelligent, Conservative, Explorative) + Advanced ML (DQN, PPO, Adaptive) |
| 📊 **Interactive Dashboard** | Real-time visualization of mesh topology, agent performance, and network metrics |
| 🎚️ **Task Difficulties** | Easy → Medium → Hard with progressive complexity and reward shaping |
| 🔌 **RESTful API** | Full OpenEnv spec compliance with async/await support |
| 🐳 **Docker Ready** | One-command deployment to Hugging Face Spaces or local environments |
| 📈 **Performance Tracking** | Detailed metrics, reward graphs, and episode history |

---

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/Senbagaseelan18/mesh-crisis-response
cd mesh-crisis-response

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m server.app

# Open dashboard
# Visit: http://localhost:8000/dashboard
```

### Deployed Instance

👉 **Live Demo**: [Emergency Mesh-Network Router on HF Spaces](https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router)

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Environment health status |
| `/reset` | POST | Reset environment and return initial observation |
| `/step` | POST | Execute an action and return observation, reward, done, info |
| `/state` | GET | Get current environment state |
| `/dashboard` | GET | Interactive web interface |

### Example API Usage

```bash
# Reset environment
curl -X POST http://localhost:8000/reset

# Take a step
curl -X POST http://localhost:8000/step \
  -H "Content-Type: application/json" \
  -d '{"action": "route_alert_via_node_5"}'

# Get current state
curl -X GET http://localhost:8000/state
```

---

## 🎓 Tasks & Difficulty Levels

### Easy: Basic Routing Challenge
- **Scenario**: 5-node network, 80% reliability
- **Objective**: Route 3 alerts successfully
- **Max Steps**: 15
- **Success Threshold**: Score ≥ 0.7

### Medium: Multi-Network Routing  
- **Scenario**: 8-node network with 2 subnets, 70% reliability
- **Objective**: Route 5 alerts while managing congestion
- **Max Steps**: 25
- **Success Threshold**: Score ≥ 0.75

### Hard: Crisis Optimization
- **Scenario**: 12-node network, cascading failures, 60% reliability
- **Objective**: Route 10 alerts with dynamic priorities
- **Max Steps**: 40
- **Success Threshold**: Score ≥ 0.8

---

## 📊 Reward Function

```
Total Reward = (Successful Alerts × Alert_Weight)
             - (Failed Alerts × Failure_Penalty)  
             - (Network Congestion × Congestion_Penalty)
             - (Step_Penalty × Steps_Taken)
```

Rewards provide **partial progress signals** throughout episodes, encouraging agents to find optimal routing quickly without unnecessary steps.

---

## 🔧 Configuration

Environment behavior is controlled via `openenv.yaml`:

```yaml
Environment:
  name: "emergency-mesh-router"
  version: "1.0.0"
  description: "RL environment for emergency alert routing"
  
Tasks:
  - name: "easy"
    difficulty: 1
    max_steps: 15
  - name: "medium"  
    difficulty: 2
    max_steps: 25
  - name: "hard"
    difficulty: 3
    max_steps: 40
```

---

## 👥 Contributors

<div align="center">

### 🏆 Team Members

| Name | Role |
|------|------|
| **Senbagaseelan V** | Lead Developer, RL Implementation |
| **Nishalini BA** | Environment Design, Reward Shaping |
| **Athul Krishna A** | Dashboard Development, API Integration |

</div>

---

## 🙏 Acknowledgments

This project was developed for the **OpenEnv Hackathon 2026**, organized by the OpenEnv community. We're grateful to the organizing team for creating this platform to advance RL environment development and benchmarking.

**Hackathon Organizers**:
- OpenEnv Core Team
- Hugging Face Spaces Team
- OpenEnv Community Contributors

---

## 📋 Requirements

- **Python**: 3.10+
- **Docker**: For containerized deployment
- **System**: 2+ vCPU, 8GB+ RAM
- **Runtime**: Inference completes in <20 minutes

---

## 📦 Installation

### From Source

```bash
git clone https://github.com/Senbagaseelan18/mesh-crisis-response
cd mesh-crisis-response
pip install -r requirements.txt
```

### Docker

```bash
docker build -t emergency-mesh-router .
docker run -p 8000:8000 emergency-mesh-router
```

---

## 🧪 Testing

Run the validation suite:

```bash
# Validate OpenEnv spec compliance
openenv validate

# Run baseline inference
python inference.py

# Test endpoints locally
python test_endpoints_local.py http://localhost:8000
```

---

## 📚 Documentation

- 📖 [Full Documentation](./docs/)
- 🚀 [Deployment Guide](./DEPLOY_TO_HF_SPACES.md)
- 🐛 [Debugging Guide](./DEBUGGING_GUIDE.md)
- 📊 [Project Summary](./docs/PROJECT_SUMMARY.md)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for bugs and feature requests.

---

<div align="center">

### 🎉 Built with OpenEnv

**[View on GitHub](https://github.com/Senbagaseelan18/mesh-crisis-response)** | **[Try on HF Spaces](https://huggingface.co/spaces/SenbagaseelanV/emergency-mesh-router)**

Made with ❤️ for emergency response systems

</div>

