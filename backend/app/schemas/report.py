"""Pydantic schemas for read-only SQL reports."""

from datetime import datetime

from pydantic import BaseModel, Field


class LeadsByCityCategoryRow(BaseModel):
    """Lead count grouped by city and category."""

    city: str
    category: str
    lead_count: int = Field(ge=0)


class MissingWebsiteLeadRow(BaseModel):
    """Lead missing a usable website value."""

    lead_id: int
    business_name: str
    city: str
    category: str
    website: str | None = None


class HighReviewWeakPresenceLeadRow(BaseModel):
    """High-review lead with persisted evidence of weak digital presence."""

    lead_id: int
    business_name: str
    city: str
    category: str
    review_count: int
    priority_label: str | None = None
    confidence_level: str | None = None
    weak_signals: list[str] = Field(default_factory=list)


class ManualReviewLeadRow(BaseModel):
    """Lead whose persisted score requires manual review."""

    lead_id: int
    business_name: str
    city: str
    category: str
    total_score: float
    priority_label: str
    confidence_level: str
    missing_data: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)


class ScoreDistributionByCategoryRow(BaseModel):
    """Persisted score distribution by lead category and priority label."""

    category: str
    priority_label: str
    lead_count: int = Field(ge=0)
    average_score: float


class ImportQualitySummaryRow(BaseModel):
    """Persisted import run quality summary."""

    import_run_id: int
    source_name: str | None = None
    total_records: int = Field(ge=0)
    valid_records: int = Field(ge=0)
    invalid_records: int = Field(ge=0)
    duplicate_records: int = Field(ge=0)
    error_count: int = Field(ge=0)
    created_at: datetime


class MissingDataReportRow(BaseModel):
    """Lead-level and score-level missing data signals."""

    lead_id: int
    business_name: str
    city: str
    category: str
    missing_fields: list[str] = Field(default_factory=list)
    score_missing_data: list[str] = Field(default_factory=list)
