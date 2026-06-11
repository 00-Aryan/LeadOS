"""Lead import schemas."""

from pydantic import BaseModel, Field


class LeadInput(BaseModel):
    """Normalized valid lead row."""

    business_name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    city: str = Field(min_length=1)
    state: str | None = None
    phone: str | None = None
    website: str | None = None
    rating: float | None = None
    review_count: int | None = None
    address: str | None = None
    source_url: str | None = None


class LeadImportError(BaseModel):
    """Validation error for one CSV row."""

    row_number: int
    reasons: list[str]
    raw_row: dict[str, str | None]


class LeadImportSummary(BaseModel):
    """Summary of a lead import run."""

    total_rows: int
    valid_rows: int
    invalid_rows: int
    accepted: list[LeadInput]
    rejected: list[LeadImportError]
