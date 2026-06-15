"""Lead scoring API routes."""

from pydantic import BaseModel
from fastapi import APIRouter

from app.schemas.audit import WebsiteAuditResult
from app.schemas.lead import LeadInput
from app.schemas.score import LeadScoreResult
from app.services.scoring_service import score_lead

router = APIRouter(prefix="/scoring", tags=["scoring"])


class ScorePreviewRequest(BaseModel):
    """Request body for stateless lead score preview."""

    lead: LeadInput
    audit: WebsiteAuditResult | None = None


@router.post("/preview", response_model=LeadScoreResult)
def preview_score(request: ScorePreviewRequest) -> LeadScoreResult:
    """Return a deterministic explainable score without saving data."""
    return score_lead(lead=request.lead, audit=request.audit)
