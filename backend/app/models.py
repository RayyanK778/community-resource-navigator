"""
SQLAlchemy models for Community Resource Navigator.

Schema matches PRD Section 8 (Functional Requirements, FR1):
id, name, category, description, eligibility notes, service area,
address/contact, hours, application process, active flag, last-verified date.
"""

from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Resource(Base):
    """A single community resource (program, service, or agency)."""

    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)

    # Core identity
    name = Column(String(200), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    # e.g. one of: housing, food, healthcare, legal, childcare,
    # employment, financial_assistance, other

    description = Column(Text, nullable=False)
    eligibility_notes = Column(Text, nullable=True)
    service_area = Column(String(200), nullable=True)

    # Contact / logistics
    address = Column(String(300), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(300), nullable=True)
    hours = Column(String(200), nullable=True)
    application_process = Column(Text, nullable=True)

    # Data quality / lifecycle
    active = Column(Boolean, nullable=False, default=True, index=True)
    last_verified = Column(Date, nullable=False, default=date.today)

    # Housekeeping
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
