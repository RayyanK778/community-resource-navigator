"""
Resource endpoints: read-only for Milestone 2 (search/filter/detail).

Create/update/deactivate endpoints for the admin UI are deferred to a later
milestone per the PRD's tiering (Section 4a) — the caseworker-facing search
and detail views are Tier 1 and come first.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud
from ..constants import CATEGORIES, CATEGORY_LABELS
from ..database import get_db
from ..schemas import ResourceOut

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=list[ResourceOut])
def list_resources(
    category: Optional[str] = Query(
        default=None, description=f"Filter by category. One of: {CATEGORIES}"
    ),
    q: Optional[str] = Query(
        default=None, description="Keyword search across name, description, eligibility, and service area"
    ),
    include_inactive: bool = Query(
        default=False, description="Include deactivated resources (admin use)"
    ),
    db: Session = Depends(get_db),
):
    if category is not None and category not in CATEGORIES:
        raise HTTPException(
            status_code=422, detail=f"category must be one of {CATEGORIES}, got '{category}'"
        )

    return crud.list_resources(
        db, category=category, q=q, active_only=not include_inactive
    )


@router.get("/categories")
def get_categories():
    """Returns the fixed category list with display labels, for UI filter dropdowns."""
    return [{"value": c, "label": CATEGORY_LABELS[c]} for c in CATEGORIES]


@router.get("/{resource_id}", response_model=ResourceOut)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = crud.get_resource(db, resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail=f"Resource {resource_id} not found")
    return resource
