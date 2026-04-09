"""
FastAPI server - Emergency Mesh-Network Router
PHASE 1: Minimal implementation for OpenEnv validation
Zero external dependencies - guaranteed to start
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

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
    return {
        "service": "Emergency Mesh-Network Router",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/tasks")
async def list_tasks():
    return {
        "tasks": [
            {"difficulty": "easy", "description": "1 hop scenario", "max_hops": 5},
            {"difficulty": "medium", "description": "3 hop scenario", "max_hops": 10},
            {"difficulty": "hard", "description": "5+ hop scenario", "max_hops": 15}
        ]
    }

@app.post("/reset")
async def reset_default():
    """
    PHASE 1 CRITICAL: POST /reset endpoint
    Must respond immediately with valid JSON
    """
    return JSONResponse(
        content={
            "detail": "Environment reset successfully",
            "status": "ok",
            "difficulty": "easy"
        },
        status_code=200
    )

@app.get("/docs")
async def get_docs():
    return {
        "endpoints": [
            {"method": "GET", "path": "/", "description": "Root"},
            {"method": "GET", "path": "/health", "description": "Health check"},
            {"method": "GET", "path": "/tasks", "description": "List tasks"},
            {"method": "POST", "path": "/reset", "description": "Reset environment"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
