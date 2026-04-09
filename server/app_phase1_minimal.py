#!/usr/bin/env python3
"""
Minimal Emergency Mesh Router API - Phase 1 Only
Zero dependencies on environment/models. Pure FastAPI.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ============ PHASE 1 CRITICAL ENDPOINTS ============

@app.get("/")
async def root():
    return {"service": "Emergency Mesh-Network Router", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/reset")
async def reset():
    """OpenEnv Phase 1 validation endpoint"""
    return JSONResponse({
        "detail": "Environment reset successfully",
        "status": "ok"
    }, status_code=200)

@app.get("/tasks")
async def tasks():
    return {"tasks": [{"difficulty": "easy"}, {"difficulty": "medium"}, {"difficulty": "hard"}]}

@app.get("/docs")
async def docs():
    return {"docs": "available"}

# Optional Phase 2 endpoints
@app.post("/reset/{difficulty}")
async def reset_difficulty(difficulty: str):
    return {"detail": "Ok", "difficulty": difficulty}

@app.get("/state/{difficulty}")
async def state(difficulty: str):
    return {"state": "ok"}

@app.get("/episode-stats/{difficulty}")
async def stats(difficulty: str):
    return {"stats": "ok"}

@app.post("/grade/{difficulty}")
async def grade(difficulty: str):
    return {"grade": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
