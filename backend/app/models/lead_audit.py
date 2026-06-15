"""ORM model for website audit results."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LeadAudit(Base):
    """Persisted deterministic website audit result."""

    __tablename__ = "lead_audits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"), nullable=False, index=True)
    requested_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    fetch_status: Mapped[str] = mapped_column(String(50), nullable=False)
    result_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )

    lead = relationship("Lead", back_populates="audits")
