"""Database boundary for LeadOS.

Phase 0 intentionally avoids choosing the final persistence implementation.
The first real build should define SQLAlchemy or SQLModel models after the
schema is reviewed.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseStatus:
    """Simple database status value object."""

    configured: bool
    detail: str


def get_database_status() -> DatabaseStatus:
    """Return current database configuration status."""
    return DatabaseStatus(
        configured=False,
        detail="Persistence is not configured in Phase 0.",
    )
