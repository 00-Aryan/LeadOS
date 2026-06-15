"""Repository for lead and import persistence."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Lead, LeadImportError, LeadImportRun


class LeadRepository:
    """Data access methods for leads and import runs."""

    def find_duplicate(self, db: Session, normalized_business_name: str, normalized_city: str) -> Lead | None:
        """Return an existing lead with the same normalized name and city."""
        stmt = select(Lead).where(
            Lead.normalized_business_name == normalized_business_name,
            Lead.normalized_city == normalized_city,
        )
        return db.execute(stmt).scalar_one_or_none()

    def add_lead(self, db: Session, **lead_data) -> Lead:
        """Add a lead to the current transaction and flush for ID assignment."""
        lead = Lead(**lead_data)
        db.add(lead)
        db.flush()
        return lead

    def list_leads(self, db: Session, limit: int = 100, offset: int = 0) -> list[Lead]:
        """Return paginated leads."""
        stmt = select(Lead).order_by(Lead.id).offset(offset).limit(limit)
        return list(db.execute(stmt).scalars())

    def create_import_run(
        self,
        db: Session,
        *,
        source_name: str | None,
        total_records: int,
        valid_records: int,
        invalid_records: int,
        duplicate_records: int,
    ) -> LeadImportRun:
        """Persist an import run summary."""
        run = LeadImportRun(
            source_name=source_name,
            total_records=total_records,
            valid_records=valid_records,
            invalid_records=invalid_records,
            duplicate_records=duplicate_records,
        )
        db.add(run)
        db.flush()
        return run

    def add_import_error(
        self,
        db: Session,
        *,
        import_run_id: int,
        row_number: int,
        reasons: list[str],
        raw_row: dict,
    ) -> LeadImportError:
        """Persist a rejected row for auditability."""
        error = LeadImportError(
            import_run_id=import_run_id,
            row_number=row_number,
            reasons=reasons,
            raw_row=raw_row,
        )
        db.add(error)
        db.flush()
        return error
