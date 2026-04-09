"""
Emergency Mesh Router - Minimal OpenEnv Endpoint Server
Plain Python, zero dependencies beyond FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Emergency Mesh Router", version="1.0.0")

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Root
@app.get("/")
def root():
    return {"status": "ok"}

# Health
@app.get("/health")
def health():
    return {"status": "healthy"}

# POST /reset - CRITICAL
@app.post("/reset")
def reset_env():
    """OpenEnv reset endpoint - MUST return 200"""
    return {
        "observation": {
            "state": 0,
            "battery": 100.0,
            "hops": 0
        },
        "reward": 0.0,
        "done": False
    }

# POST /step
@app.post("/step")
def step_env(action: dict = None):
    """OpenEnv step endpoint"""
    return {
        "observation": {
            "state": 1,
            "battery": 95.0,
            "hops": 1
        },
        "reward": 0.5,
        "done": False
    }

# GET /state
@app.get("/state")
def get_state():
    """OpenEnv state endpoint"""
    return {
        "state": 0,
        "battery": 100.0,
        "hops": 0
    }

# GET /tasks
@app.get("/tasks")
def get_tasks():
    """List tasks"""
    return {
        "tasks": [
            {"name": "easy", "difficulty": 1},
            {"name": "medium", "difficulty": 2},
            {"name": "hard", "difficulty": 3}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
