---
title: Emergency Mesh-Network Router
emoji: 🚨
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Emergency Mesh-Network Router

An RL-based solution for emergency alert routing through mesh networks using reinforcement learning agents.

## Features

- **Multiple Agents**: Baseline agents (Random, Greedy, Intelligent, Conservative, Explorative) and advanced ML agents (DQN, PPO, Adaptive)
- **Interactive Dashboard**: Real-time visualization of mesh network topology and agent performance
- **Task Difficulties**: Easy, Medium, and Hard difficulty levels
- **API Endpoints**: RESTful API for environment interaction

## Getting Started

The application runs a FastAPI server on port 8000 with:
- `/dashboard` - Interactive web interface
- `/api/reset` - Reset environment
- `/api/run-episode/{difficulty}/{agent}` - Run episodes
- `/health` - Health check

See https://huggingface.co/docs/hub/spaces-config-reference for configuration reference.

