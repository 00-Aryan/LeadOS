"""Lead import and listing API routes."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.repositories import LeadRepository
from app.schemas.lead import LeadImportSummary, LeadOutput
from app.services.lead_import_service import LeadImportService

router = APIRouter(prefix="/leads", tags=["leads"])


class LeadImportRequest(BaseModel):
    """Request body for importing CSV lead data."""

    csv_content: str = Field(min_length=1)
    source_name: str | None = None


@router.post("/import", response_model=LeadImportSummary)
def import_leads(
    request: LeadImportRequest,
    db: Session = Depends(get_db_session),
) -> LeadImportSummary:
    """Validate, transform and persist leads from CSV content."""
    service = LeadImportService()
    return service.import_csv_text(db, request.csv_content, source_name=request.source_name)


@router.get("", response_model=list[LeadOutput])
def list_leads(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db_session),
) -> list[LeadOutput]:
    """Return persisted leads."""
    repository = LeadRepository()
    return list(repository.list_leads(db, limit=limit, offset=offset))
