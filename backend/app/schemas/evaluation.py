"""Structured schemas for deterministic outreach evaluation."""

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.outreach import OutreachDraftResult

RiskRating = Literal["low", "medium", "high"]
PassOrReview = Literal["pass", "review"]


class OutreachEvaluationInput(BaseModel):
    """Draft and verified facts supplied to the evaluator."""

    draft: OutreachDraftResult
    supported_facts: list[str] = Field(default_factory=list)


class EvaluationScoreBreakdown(BaseModel):
    """Deterministic outreach quality scores."""

    relevance: int = Field(ge=0, le=10)
    personalization: int = Field(ge=0, le=10)
    clarity: int = Field(ge=0, le=10)
    tone: int = Field(ge=0, le=10)
    truthfulness: int = Field(ge=0, le=10)
    cta_quality: int = Field(ge=0, le=10)


class OutreachEvaluationResult(BaseModel):
    """Structured evaluation result before human use."""

    score_breakdown: EvaluationScoreBreakdown
    total_score: int = Field(ge=0, le=60)
    risk_rating: RiskRating
    pass_or_review: PassOrReview
    failure_reasons: list[str] = Field(default_factory=list)
    bad_lines: list[str] = Field(default_factory=list)
    suggested_revision: str | None = None
