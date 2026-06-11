"""Lead import API routes."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.schemas.lead import LeadImportSummary
from app.services.lead_import_service import import_leads_from_csv

router = APIRouter(prefix="/leads", tags=["leads"])


class LeadImportRequest(BaseModel):
    """Request body for CSV import."""

    csv_content: str


@router.post("/import", response_model=LeadImportSummary)
def import_leads(request: LeadImportRequest) -> LeadImportSummary:
    """Validate CSV lead data and return an import summary."""
    return import_leads_from_csv(request.csv_content)
