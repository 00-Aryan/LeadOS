"""CSV lead import service with validation, transformation and persistence."""

import csv
from io import StringIO
from typing import BinaryIO, TextIO

from sqlalchemy.orm import Session

from app.repositories import LeadRepository
from app.schemas.lead import (
    LeadImportInvalidRow,
    LeadImportResult,
    LeadImportSummary,
    LeadImportValidRow,
)
from app.services.lead_transform_service import transform_lead_row

REQUIRED_COLUMNS = {"business_name", "category", "city"}
PUBLIC_LEAD_FIELDS = (
    "business_name",
    "category",
    "city",
    "state",
    "phone",
    "website",
    "rating",
    "review_count",
    "address",
    "source_url",
)


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
    ) -> LeadImportResult:
        """Import CSV content and commit once at the end.

        The service avoids per-row commits to reduce partial-write risk. Invalid
        rows and duplicates are reported explicitly.
        """
        csv_content = csv_content.lstrip("\ufeff")
        if not csv_content.strip():
            return self._persist_result(
                db,
                source_name=source_name,
                total_records=0,
                valid_rows=[],
                invalid_rows=[],
                duplicate_records=0,
                imported_ids=[],
            )

        reader = csv.DictReader(StringIO(csv_content))
        if reader.fieldnames is None:
            return self._persist_result(
                db,
                source_name=source_name,
                total_records=0,
                valid_rows=[],
                invalid_rows=[],
                duplicate_records=0,
                imported_ids=[],
            )

        missing_columns = sorted(REQUIRED_COLUMNS.difference(reader.fieldnames))
        if missing_columns:
            return self._persist_result(
                db,
                source_name=source_name,
                total_records=0,
                valid_rows=[],
                invalid_rows=[
                    LeadImportInvalidRow(
                        row_number=1,
                        reasons=[
                            f"CSV header missing required field: {field}"
                            for field in missing_columns
                        ],
                        raw_row={},
                    )
                ],
                duplicate_records=0,
                imported_ids=[],
            )

        total = 0
        duplicates = 0
        imported_ids: list[int] = []
        valid_rows: list[LeadImportValidRow] = []
        invalid_rows: list[LeadImportInvalidRow] = []

        try:
            for row_number, row in enumerate(reader, start=2):
                total += 1
                transformed = transform_lead_row(row)
                if transformed.reasons:
                    invalid_rows.append(
                        LeadImportInvalidRow(
                            row_number=row_number,
                            reasons=transformed.reasons,
                            raw_row=_clean_raw_row(row),
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
                valid_rows.append(_build_valid_row(transformed.data))

            return self._persist_result(
                db,
                source_name=source_name,
                total_records=total,
                valid_rows=valid_rows,
                invalid_rows=invalid_rows,
                duplicate_records=duplicates,
                imported_ids=imported_ids,
            )
        except Exception:
            db.rollback()
            raise

    def import_csv_content(
        self,
        db: Session,
        csv_content: str | bytes | TextIO | BinaryIO,
        *,
        source_name: str | None = None,
    ) -> LeadImportResult:
        """Import CSV content from text, bytes, or a file-like object."""
        return self.import_csv_text(
            db,
            _coerce_csv_text(csv_content),
            source_name=source_name,
        )

    def _persist_result(
        self,
        db: Session,
        *,
        source_name: str | None,
        total_records: int,
        valid_rows: list[LeadImportValidRow],
        invalid_rows: list[LeadImportInvalidRow],
        duplicate_records: int,
        imported_ids: list[int],
    ) -> LeadImportResult:
        import_run = self.repository.create_import_run(
            db,
            source_name=source_name,
            total_records=total_records,
            valid_records=len(valid_rows),
            invalid_records=len(invalid_rows),
            duplicate_records=duplicate_records,
        )
        for row in invalid_rows:
            self.repository.add_import_error(
                db,
                import_run_id=import_run.id,
                row_number=row.row_number,
                reasons=row.reasons,
                raw_row=row.raw_row,
            )
        db.commit()

        return LeadImportResult(
            summary=LeadImportSummary(
                total_rows=total_records,
                valid_rows=len(valid_rows),
                invalid_rows=len(invalid_rows),
                duplicate_rows=duplicate_records,
            ),
            valid_rows=valid_rows,
            invalid_rows=invalid_rows,
            import_run_id=import_run.id,
            imported_ids=imported_ids,
        )


def _coerce_csv_text(csv_content: str | bytes | TextIO | BinaryIO) -> str:
    if isinstance(csv_content, str):
        return csv_content
    if isinstance(csv_content, bytes):
        return csv_content.decode("utf-8-sig")

    content = csv_content.read()
    if isinstance(content, bytes):
        return content.decode("utf-8-sig")
    return content


def _build_valid_row(data: dict[str, object | None]) -> LeadImportValidRow:
    return LeadImportValidRow(**{field: data[field] for field in PUBLIC_LEAD_FIELDS})


def _clean_raw_row(row: dict[str | None, object]) -> dict[str, str | None]:
    cleaned: dict[str, str | None] = {}
    for key, value in row.items():
        cleaned_key = key if key is not None else "_extra"
        if isinstance(value, list):
            cleaned[cleaned_key] = ",".join(str(item) for item in value)
        elif value is None or isinstance(value, str):
            cleaned[cleaned_key] = value
        else:
            cleaned[cleaned_key] = str(value)
    return cleaned
