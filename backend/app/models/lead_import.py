"""ORM models for import run tracking and rejected rows."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LeadImportRun(Base):
    """One CSV import execution summary."""

    __tablename__ = "lead_import_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    total_records: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    valid_records: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    invalid_records: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    duplicate_records: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )

    errors = relationship(
        "LeadImportError",
        back_populates="import_run",
        cascade="all, delete-orphan",
    )


class LeadImportError(Base):
    """Rejected CSV row with structured validation reasons."""

    __tablename__ = "lead_import_errors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    import_run_id: Mapped[int] = mapped_column(
        ForeignKey("lead_import_runs.id"), nullable=False, index=True
    )
    row_number: Mapped[int] = mapped_column(Integer, nullable=False)
    reasons: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    raw_row: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )

    import_run = relationship("LeadImportRun", back_populates="errors")
