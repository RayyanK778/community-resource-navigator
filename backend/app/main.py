"""
FastAPI app entrypoint.

Milestone 2: /resources read endpoints (list/search/filter, get by id) wired
in via the resources router. Create/update/admin endpoints come in a later
milestone (see docs/PRD.md Section 4a).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models import Base
from .routers import resources

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Community Resource Navigator API")

# Permissive for local dev only. Tighten before any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resources.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
