"""ORM model for a business lead."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Lead(Base):
    """Persisted local business lead."""

    __tablename__ = "leads"
    __table_args__ = (
        UniqueConstraint(
            "normalized_business_name",
            "normalized_city",
            name="uq_lead_name_city",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    business_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    normalized_business_name: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    normalized_category: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    normalized_city: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )
    state: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    review_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    audits = relationship("LeadAudit", back_populates="lead", cascade="all, delete-orphan")
    scores = relationship("LeadScore", back_populates="lead", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Lead id={self.id} business_name={self.business_name!r}>"
