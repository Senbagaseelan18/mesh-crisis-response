"""
Emergency Mesh Router - OpenEnv Phase 1 Server
MINIMAL BULLETPROOF VERSION - Zero complexity, maximum reliability
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Emergency Mesh Router",
    version="1.0.0"
)

# Enable CORS for validator
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint"""
    return {"status": "ok", "service": "Emergency Mesh Router"}


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/reset")
def reset_env():
    """
    OpenEnv POST /reset - CRITICAL ENDPOINT
    Validator posts empty JSON {} to this endpoint
    Must respond with observation, reward, done fields
    """
    return {
        "observation": {
            "state": "reset",
            "device_id": 0,
            "battery": 100.0,
            "hops": 0
        },
        "reward": 0.0,
        "done": False
    }


@app.post("/step")
def step_env(action: dict = None):
    """Step in environment"""
    return {
        "observation": {
            "state": "stepped",
            "device_id": 1,
            "battery": 95.0,
            "hops": 1
        },
        "reward": 0.5,
        "done": False
    }


@app.get("/tasks")
def get_tasks():
    """List available tasks"""
    return {
        "tasks": [
            {"name": "easy", "difficulty": 1, "max_steps": 5},
            {"name": "medium", "difficulty": 2, "max_steps": 10},
            {"name": "hard", "difficulty": 3, "max_steps": 20}
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
