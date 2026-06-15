"""ORM model for lead scoring results."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LeadScore(Base):
    """Persisted lead score result."""

    __tablename__ = "lead_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), nullable=False, index=True)
    scoring_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1")
    total_score: Mapped[float] = mapped_column(Float, nullable=False)
    category_scores: Mapped[dict] = mapped_column(JSON, nullable=False)
    priority_label: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence_level: Mapped[str] = mapped_column(String(50), nullable=False)
    reason_summary: Mapped[str] = mapped_column(String(1000), nullable=False)
    positive_signals: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    risk_flags: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    missing_data: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    lead = relationship("Lead", back_populates="scores")
