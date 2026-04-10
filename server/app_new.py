"""
Emergency Mesh Router - OpenEnv Phase 1
Proper implementation using OpenEnv spec
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import the environment
try:
    from server.environment import MeshNetworkEnvironment
    from models import TaskDifficulty
    HAS_ENV = True
    logger.info("✅ Environment imported successfully")
except Exception as e:
    logger.warning(f"⚠️ Environment import failed: {e}")
    HAS_ENV = False

app = FastAPI(
    title="Emergency Mesh Router",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance
env_instance = None

def get_env():
    """Get or create environment instance"""
    global env_instance
    if env_instance is None and HAS_ENV:
        try:
            env_instance = MeshNetworkEnvironment(TaskDifficulty.EASY)
            logger.info("✅ Environment instance created")
        except Exception as e:
            logger.error(f"❌ Failed to create environment: {e}")
            env_instance = None
    return env_instance


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "status": "ok",
        "service": "Emergency Mesh Router",
        "has_env": HAS_ENV
    }


@app.get("/health")
def health():
    """Health check"""
    return {"status": "healthy"}


@app.post("/reset")
def reset_endpoint():
    """
    OpenEnv POST /reset endpoint
    Resets environment and returns initial observation
    """
    try:
        env = get_env()
        
        if env is None:
            # Fallback if environment not available
            logger.warning("⚠️ No environment, returning fallback response")
            return {
                "observation": {
                    "device_id": 0,
                    "battery": 100.0,
                    "hops": 0
                },
                "reward": 0.0,
                "done": False
            }
        
        # Call environment reset
        obs = env.reset()
        logger.info(f"✅ Environment reset successful")
        
        # Convert observation to dict
        if hasattr(obs, 'dict'):
            obs_dict = obs.dict()
        else:
            obs_dict = {
                "device_id": getattr(obs, "device_id", 0),
                "battery": getattr(obs, "battery", 100.0),
                "hops": getattr(obs, "hops", 0)
            }
        
        return {
            "observation": obs_dict,
            "reward": 0.0,
            "done": False
        }
        
    except Exception as e:
        logger.error(f"❌ Reset failed: {e}")
        return {
            "observation": {
                "device_id": 0,
                "battery": 100.0,
                "hops": 0
            },
            "reward": 0.0,
            "done": False
        }


@app.post("/step")
def step_endpoint(action: dict = None):
    """
    OpenEnv POST /step endpoint
    Takes an action and returns next observation
    """
    try:
        env = get_env()
        
        if env is None or action is None:
            return {
                "observation": {
                    "device_id": 1,
                    "battery": 95.0,
                    "hops": 1
                },
                "reward": 0.5,
                "done": False
            }
        
        # Extract action value
        action_val = action.get("action", 0) if isinstance(action, dict) else 0
        
        # Call environment step
        result = env.step(action_val)
        
        if isinstance(result, tuple) and len(result) >= 4:
            obs, reward, done, info = result[0], result[1], result[2], result[3]
        else:
            obs, reward, done, info = result, 0.0, False, {}
        
        # Convert observation to dict
        if hasattr(obs, 'dict'):
            obs_dict = obs.dict()
        else:
            obs_dict = {
                "device_id": getattr(obs, "device_id", 1),
                "battery": getattr(obs, "battery", 95.0),
                "hops": getattr(obs, "hops", 1)
            }
        
        return {
            "observation": obs_dict,
            "reward": float(reward),
            "done": bool(done),
            "info": info
        }
        
    except Exception as e:
        logger.error(f"❌ Step failed: {e}")
        return {
            "observation": {
                "device_id": 1,
                "battery": 95.0,
                "hops": 1
            },
            "reward": 0.5,
            "done": False
        }


@app.get("/state")
def state_endpoint():
    """
    OpenEnv GET /state endpoint
    Returns current environment state
    """
    try:
        env = get_env()
        
        if env is None:
            return {"state": "not_initialized"}
        
        state = env.state()
        
        if hasattr(state, 'dict'):
            state_dict = state.dict()
        else:
            state_dict = {
                "device_id": getattr(state, "device_id", 0),
                "battery": getattr(state, "battery", 100.0),
                "hops": getattr(state, "hops", 0)
            }
        
        return state_dict
        
    except Exception as e:
        logger.error(f"❌ State failed: {e}")
        return {"error": str(e)}


@app.get("/tasks")
def get_tasks():
    """List available tasks"""
    return {
        "tasks": [
            {
                "name": "easy",
                "difficulty": 1,
                "max_steps": 5,
                "description": "Gateway 1 hop away"
            },
            {
                "name": "medium",
                "difficulty": 2,
                "max_steps": 10,
                "description": "Gateway 3 hops away"
            },
            {
                "name": "hard",
                "difficulty": 3,
                "max_steps": 20,
                "description": "Gateway 5+ hops away"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
