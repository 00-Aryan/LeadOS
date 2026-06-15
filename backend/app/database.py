"""Database setup and session utilities for LeadOS."""

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""


def _engine_kwargs(database_url: str) -> dict:
    if database_url.startswith("sqlite"):
        sqlite_path = database_url.removeprefix("sqlite:///")
        if sqlite_path and sqlite_path != ":memory:":
            Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
        return {"connect_args": {"check_same_thread": False}}
    return {}


DATABASE_URL = get_settings().database_url
engine = create_engine(DATABASE_URL, **_engine_kwargs(DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_all_tables() -> None:
    """Create tables for local development and tests.

    Production should use migrations, but this helper keeps the current MVP
    setup reproducible without adding Alembic before the schema stabilizes.
    """
    from app import models  # noqa: F401  Import registers models with metadata.

    Base.metadata.create_all(bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
