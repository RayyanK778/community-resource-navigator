"""
Pydantic schemas — the shapes of data going in/out of the API.

Kept separate from models.py (the DB layer) on purpose: it's a small amount
of extra boilerplate, but it means the API contract can stay stable even if
the DB table changes shape later, and it's the standard FastAPI pattern so
it won't look unfamiliar to another engineer picking this up.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from .constants import CATEGORIES


class ResourceBase(BaseModel):
    name: str
    category: str
    description: str
    eligibility_notes: Optional[str] = None
    service_area: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    hours: Optional[str] = None
    application_process: Optional[str] = None
    active: bool = True
    last_verified: date

    @field_validator("category")
    @classmethod
    def category_must_be_known(cls, v: str) -> str:
        if v not in CATEGORIES:
            raise ValueError(f"category must be one of {CATEGORIES}, got '{v}'")
        return v


class ResourceCreate(ResourceBase):
    """Fields required to create a resource."""

    pass


class ResourceUpdate(BaseModel):
    """All fields optional — used for partial updates (e.g. toggling active)."""

    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    eligibility_notes: Optional[str] = None
    service_area: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    hours: Optional[str] = None
    application_process: Optional[str] = None
    active: Optional[bool] = None
    last_verified: Optional[date] = None

    @field_validator("category")
    @classmethod
    def category_must_be_known(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in CATEGORIES:
            raise ValueError(f"category must be one of {CATEGORIES}, got '{v}'")
        return v


class ResourceOut(ResourceBase):
    """What the API returns for a resource, including DB-generated fields."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
