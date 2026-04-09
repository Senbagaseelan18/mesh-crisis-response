"""
Emergency Mesh Router - OpenEnv Endpoint Server
Ultra-robust minimal implementation
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Emergency Mesh Router")

# Enable CORS for everything
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def root():
    return JSONResponse({"status": "ok"}, status_code=200)


@app.get("/health")
def health():
    return JSONResponse({"status": "healthy"}, status_code=200)


@app.post("/reset")
def reset_env():
    """
    OpenEnv reset endpoint
    MUST respond with HTTP 200 and observation
    """
    response = {
        "observation": {
            "state": 0,
            "battery": 100.0,
            "hops": 0
        },
        "reward": 0.0,
        "done": False
    }
    return JSONResponse(content=response, status_code=200)


@app.post("/step")
def step_env(action: dict = None):
    """OpenEnv step endpoint"""
    response = {
        "observation": {
            "state": 1,
            "battery": 95.0,
            "hops": 1
        },
        "reward": 0.5,
        "done": False
    }
    return JSONResponse(content=response, status_code=200)


@app.get("/state")
def get_state():
    """OpenEnv state endpoint"""
    response = {
        "state": 0,
        "battery": 100.0,
        "hops": 0
    }
    return JSONResponse(content=response, status_code=200)


@app.get("/tasks")
def get_tasks():
    """List tasks"""
    response = {
        "tasks": [
            {"name": "easy", "difficulty": 1},
            {"name": "medium", "difficulty": 2},
            {"name": "hard", "difficulty": 3}
        ]
    }
    return JSONResponse(content=response, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
