"""Pydantic schemas for lead import and lead output."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LeadInput(BaseModel):
    """Incoming lead row after validation."""

    business_name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    city: str = Field(min_length=1)
    state: str | None = None
    phone: str | None = None
    website: str | None = None
    rating: float | None = Field(default=None, ge=0, le=5)
    review_count: int | None = Field(default=None, ge=0)
    address: str | None = None
    source_url: str | None = None


class LeadOutput(LeadInput):
    """Lead API response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class LeadImportValidRow(LeadInput):
    """Validated and normalized CSV lead row returned in import results."""


class LeadImportInvalidRow(BaseModel):
    """Rejected CSV row information."""

    row_number: int
    reasons: list[str]
    raw_row: dict[str, str | None]


class LeadImportSummary(BaseModel):
    """CSV import result summary."""

    total_rows: int
    valid_rows: int
    invalid_rows: int
    duplicate_rows: int = 0


class LeadImportResult(BaseModel):
    """Structured CSV import result."""

    summary: LeadImportSummary
    valid_rows: list[LeadImportValidRow]
    invalid_rows: list[LeadImportInvalidRow]
    import_run_id: int | None = None
    imported_ids: list[int]
