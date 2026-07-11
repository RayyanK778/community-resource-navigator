"""
FastAPI app entrypoint.

Day 1 scope: boot the app, create tables, expose a health check.
Day 2 adds the actual /resources CRUD endpoints (see PRD milestones).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Community Resource Navigator API")

# Permissive for local dev only. Tighten before any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
