"""Lead scoring schemas."""

from typing import Literal

from pydantic import BaseModel, Field

PriorityLabel = Literal["high", "medium", "low", "review_needed"]
ConfidenceLevel = Literal["high", "medium", "low"]


class ScoreBreakdown(BaseModel):
    """Category-level scoring output."""

    business_strength: int = Field(ge=0, le=25)
    digital_gap: int = Field(ge=0, le=30)
    contactability: int = Field(ge=0, le=20)
    commercial_fit: int = Field(ge=0, le=15)
    outreach_priority: int = Field(ge=0, le=10)


class LeadScoreResult(BaseModel):
    """Explainable score for one lead."""

    total_score: int = Field(ge=0, le=100)
    category_scores: ScoreBreakdown
    priority_label: PriorityLabel
    confidence_level: ConfidenceLevel
    reason_summary: str
    positive_signals: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)
