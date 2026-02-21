"""
Job Match Platform - FastAPI Backend
No user data is persisted after the session ends.
All processing is ephemeral and in-memory.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from routes.profile import router as profile_router
from routes.jobs import router as jobs_router
from routes.apply import router as apply_router

app = FastAPI(
    title="AI Job Match Platform",
    description=(
        "AI-powered job matching for candidates. "
        "No data is stored after the session completes."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router, prefix="/api/profile", tags=["Profile"])
app.include_router(jobs_router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(apply_router, prefix="/api/apply", tags=["Apply"])


@app.get("/api/health")
async def health():
    return {"status": "ok", "data_persistence": False}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
