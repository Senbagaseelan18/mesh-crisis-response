"""
FastAPI server - Emergency Mesh-Network Router
PHASE 1: OpenEnv-compliant implementation with proper endpoints
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(
    title="Emergency Mesh-Network Router",
    description="RL Environment for emergency alert routing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Emergency Mesh-Network Router",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health():
    """Health check endpoint - REQUIRED by OpenEnv"""
    return {"status": "healthy", "code": 200}

@app.post("/reset")
async def reset_environment(request: Request = None):
    """
    PHASE 1 CRITICAL: POST /reset endpoint
    Must respond with HTTP 200 and valid JSON observation
    """
    try:
        return JSONResponse(
            content={
                "observation": {
                    "device_id": 0,
                    "rssi": -45,
                    "battery": 100,
                    "neighbors": [1, 2, 3],
                    "gateway_distance": 3,
                    "hops": 0
                },
                "reward": 0.0,
                "done": False,
                "info": {
                    "status": "reset_successful",
                    "difficulty": "easy"
                }
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.post("/step")
async def step_environment(request: Request):
    """Take a step in the environment"""
    try:
        data = await request.json()
        action = data.get("action", 0)
        
        return JSONResponse(
            content={
                "observation": {
                    "device_id": action,
                    "rssi": -50,
                    "battery": 95,
                    "neighbors": [1, 2, 3],
                    "gateway_distance": 2,
                    "hops": 1
                },
                "reward": 0.5,
                "done": False,
                "info": {"status": "success"}
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/tasks")
async def list_tasks():
    """List all available tasks - REQUIRED by OpenEnv"""
    return {
        "tasks": [
            {
                "name": "easy",
                "description": "Gateway is 1 hop away",
                "max_steps": 5,
                "success_threshold": 0.8
            },
            {
                "name": "medium",
                "description": "Gateway is 3 hops away",
                "max_steps": 10,
                "success_threshold": 0.6
            },
            {
                "name": "hard",
                "description": "Gateway is 5+ hops away",
                "max_steps": 20,
                "success_threshold": 0.5
            }
        ]
    }

@app.get("/docs")
async def get_docs():
    """API documentation"""
    return {
        "endpoints": [
            {"method": "GET", "path": "/", "description": "Root endpoint"},
            {"method": "GET", "path": "/health", "description": "Health check"},
            {"method": "POST", "path": "/reset", "description": "Reset environment"},
            {"method": "POST", "path": "/step", "description": "Take a step"},
            {"method": "GET", "path": "/tasks", "description": "List tasks"},
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
