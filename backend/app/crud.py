"""
Query layer: all direct database access for resources lives here, not in the
route handlers. Kept separate so the same queries can be reused later by the
AI triage endpoint (Day 4-6), which needs the same "active resources, optionally
filtered" query the search endpoint uses.
"""

from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import Resource


def get_resource(db: Session, resource_id: int) -> Optional[Resource]:
    return db.query(Resource).filter(Resource.id == resource_id).first()


def list_resources(
    db: Session,
    category: Optional[str] = None,
    q: Optional[str] = None,
    active_only: bool = True,
) -> list[Resource]:
    """
    List resources, optionally filtered by category and/or a keyword search.

    Keyword search matches against name, description, eligibility_notes, and
    service_area (case-insensitive substring match) — a caseworker searching
    "eviction" should find resources that mention it in any of those fields,
    not just the name.
    """
    query = db.query(Resource)

    if active_only:
        query = query.filter(Resource.active == True)  # noqa: E712

    if category:
        query = query.filter(Resource.category == category)

    if q:
        like_pattern = f"%{q}%"
        query = query.filter(
            or_(
                Resource.name.ilike(like_pattern),
                Resource.description.ilike(like_pattern),
                Resource.eligibility_notes.ilike(like_pattern),
                Resource.service_area.ilike(like_pattern),
            )
        )

    return query.order_by(Resource.name).all()
