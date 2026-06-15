"""CSV lead import service with validation, transformation and persistence."""

import csv
from io import StringIO

from sqlalchemy.orm import Session

from app.repositories import LeadRepository
from app.schemas.lead import LeadImportErrorItem, LeadImportSummary
from app.services.lead_transform_service import transform_lead_row


class LeadImportService:
    """Import CSV lead data into SQL with deterministic validation."""

    def __init__(self, repository: LeadRepository | None = None) -> None:
        self.repository = repository or LeadRepository()

    def import_csv_text(
        self,
        db: Session,
        csv_content: str,
        *,
        source_name: str | None = None,
    ) -> LeadImportSummary:
        """Import CSV content and commit once at the end.

        The service avoids per-row commits to reduce partial-write risk. Invalid
        rows and duplicates are reported explicitly.
        """
        reader = csv.DictReader(StringIO(csv_content))
        if reader.fieldnames is None:
            return LeadImportSummary(
                total_records=0,
                valid_records=0,
                invalid_records=1,
                duplicate_records=0,
                imported_ids=[],
                errors=[
                    LeadImportErrorItem(
                        row_number=0,
                        reasons=["CSV header is missing"],
                        raw_row={},
                    )
                ],
            )

        total = 0
        valid = 0
        invalid = 0
        duplicates = 0
        imported_ids: list[int] = []
        errors: list[LeadImportErrorItem] = []

        try:
            for row_number, row in enumerate(reader, start=2):
                total += 1
                transformed = transform_lead_row(row)
                if transformed.reasons:
                    invalid += 1
                    errors.append(
                        LeadImportErrorItem(
                            row_number=row_number,
                            reasons=transformed.reasons,
                            raw_row=dict(row),
                        )
                    )
                    continue

                normalized_name = str(transformed.data["normalized_business_name"])
                normalized_city = str(transformed.data["normalized_city"])
                if self.repository.find_duplicate(db, normalized_name, normalized_city):
                    duplicates += 1
                    continue

                lead = self.repository.add_lead(db, **transformed.data)
                imported_ids.append(lead.id)
                valid += 1

            import_run = self.repository.create_import_run(
                db,
                source_name=source_name,
                total_records=total,
                valid_records=valid,
                invalid_records=invalid,
                duplicate_records=duplicates,
            )
            for error in errors:
                self.repository.add_import_error(
                    db,
                    import_run_id=import_run.id,
                    row_number=error.row_number,
                    reasons=error.reasons,
                    raw_row=error.raw_row,
                )
            db.commit()

            return LeadImportSummary(
                import_run_id=import_run.id,
                total_records=total,
                valid_records=valid,
                invalid_records=invalid,
                duplicate_records=duplicates,
                imported_ids=imported_ids,
                errors=errors,
            )
        except Exception:
            db.rollback()
            raise
