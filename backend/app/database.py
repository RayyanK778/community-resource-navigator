"""
Database engine and session setup.

SQLite, single file. See PRD Section 11: chosen deliberately over
Postgres/Mongo/a vector DB because the actual data scale (tens to low
hundreds of rows, single-writer admin usage) doesn't warrant anything heavier.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "resource_navigator.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# check_same_thread=False is safe here: FastAPI's default sync request
# handling means each request gets its own session (see get_db below),
# and SQLite serializes writes internally.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency: yields a DB session, closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
