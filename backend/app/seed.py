"""
Seed the database with the fictional resource dataset (app/seed_data.py).

Idempotent by design: running this twice won't create duplicates. It matches
existing rows by `name` and updates them in place, and only inserts rows that
don't already exist. This matters because during development you'll run this
script repeatedly, and because "seed" scripts that duplicate data on rerun
are a classic source of confusing demo bugs.

Usage:
    python3 -m app.seed
"""

from .database import SessionLocal, engine
from .models import Base, Resource
from .seed_data import SEED_RESOURCES


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        created, updated = 0, 0
        for entry in SEED_RESOURCES:
            existing = db.query(Resource).filter(Resource.name == entry["name"]).first()
            if existing:
                for key, value in entry.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                db.add(Resource(**entry))
                created += 1
        db.commit()
        print(f"Seed complete: {created} created, {updated} updated, {len(SEED_RESOURCES)} total.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
