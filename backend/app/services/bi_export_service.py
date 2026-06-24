"""BI export dataset service."""

import csv
import io
import json
from datetime import UTC, date, datetime
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.repositories import ReportRepository
from app.schemas.bi_export import (
    BIExportCellValue,
    BIExportColumn,
    BIExportColumnType,
    BIExportDataset,
    BIExportTable,
)


class BIExportService:
    """Build dashboard-ready datasets from SQL-backed reports."""

    def __init__(self, report_repository: ReportRepository | None = None) -> None:
        self.report_repository = report_repository or ReportRepository()

    def build_reporting_dataset(self, db: Session) -> BIExportDataset:
        """Build the standard LeadOS reporting dataset."""
        generated_at = datetime.now(UTC)
        report_tables = [
            self.build_table_from_rows(
                "leads_by_city_category",
                "leads_by_city_and_category",
                self.report_repository.leads_by_city_and_category(db),
                generated_at=generated_at,
            ),
            self.build_table_from_rows(
                "missing_website_leads",
                "leads_missing_website",
                self.report_repository.leads_missing_website(db),
                generated_at=generated_at,
            ),
            self.build_table_from_rows(
                "high_review_weak_presence_leads",
                "high_review_weak_presence_leads",
                self.report_repository.high_review_weak_presence_leads(db),
                generated_at=generated_at,
            ),
            self.build_table_from_rows(
                "manual_review_leads",
                "manual_review_leads",
                self.report_repository.manual_review_leads(db),
                generated_at=generated_at,
            ),
            self.build_table_from_rows(
                "score_distribution_by_category",
                "score_distribution_by_category",
                self.report_repository.score_distribution_by_category(db),
                generated_at=generated_at,
            ),
            self.build_table_from_rows(
                "import_quality_summary",
                "import_quality_summary",
                self.report_repository.import_quality_summary(db),
                generated_at=generated_at,
            ),
            self.build_table_from_rows(
                "missing_data_report",
                "missing_data_report",
                self.report_repository.missing_data_report(db),
                generated_at=generated_at,
            ),
        ]
        return BIExportDataset(
            name="leados_reporting_dataset",
            tables=report_tables,
            table_count=len(report_tables),
            generated_at=generated_at,
        )

    def build_table_from_rows(
        self,
        name: str,
        source_report: str,
        rows: list[Any],
        generated_at: datetime | None = None,
    ) -> BIExportTable:
        """Build a flat BI export table from report rows or dictionaries."""
        columns = _columns_for(source_report, rows)
        column_names = [column.name for column in columns]
        flat_rows = [
            {
                column_name: _normalize_cell_value(_row_value(row, column_name))
                for column_name in column_names
            }
            for row in rows
        ]
        return BIExportTable(
            name=name,
            source_report=source_report,
            columns=columns,
            rows=flat_rows,
            row_count=len(flat_rows),
            generated_at=generated_at or datetime.now(UTC),
        )

    def to_csv(self, table: BIExportTable) -> str:
        """Return one BI export table as CSV content."""
        output = io.StringIO()
        fieldnames = [column.name for column in table.columns]
        writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in table.rows:
            writer.writerow({field: _csv_value(row.get(field)) for field in fieldnames})
        return output.getvalue()

    def to_csv_bundle(self, dataset: BIExportDataset) -> dict[str, str]:
        """Return one CSV string per table without writing files."""
        return {table.name: self.to_csv(table) for table in dataset.tables}


def _columns_for(source_report: str, rows: list[Any]) -> list[BIExportColumn]:
    definitions = _REPORT_COLUMNS.get(source_report)
    if definitions:
        return [
            BIExportColumn(name=column_name, data_type=data_type)
            for column_name, data_type in definitions
        ]
    if not rows:
        return []
    return [
        BIExportColumn(
            name=column_name,
            data_type=_infer_column_type(_row_value(rows[0], column_name)),
        )
        for column_name in _row_keys(rows[0])
    ]


def _row_keys(row: Any) -> list[str]:
    if isinstance(row, BaseModel):
        return list(row.__class__.model_fields.keys())
    if isinstance(row, dict):
        return list(row.keys())
    return list(vars(row).keys())


def _row_value(row: Any, column_name: str) -> Any:
    if isinstance(row, BaseModel):
        return row.model_dump(mode="python").get(column_name)
    if isinstance(row, dict):
        return row.get(column_name)
    return getattr(row, column_name, None)


def _normalize_cell_value(value: Any) -> BIExportCellValue:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, list | dict):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _csv_value(value: Any) -> str | int | float | bool:
    normalized = _normalize_cell_value(value)
    if normalized is None:
        return ""
    return normalized


def _infer_column_type(value: Any) -> BIExportColumnType:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, datetime | date):
        return "datetime"
    return "string"


_REPORT_COLUMNS: dict[str, tuple[tuple[str, BIExportColumnType], ...]] = {
    "leads_by_city_and_category": (
        ("city", "string"),
        ("category", "string"),
        ("lead_count", "integer"),
    ),
    "leads_missing_website": (
        ("lead_id", "integer"),
        ("business_name", "string"),
        ("city", "string"),
        ("category", "string"),
        ("website", "string"),
    ),
    "high_review_weak_presence_leads": (
        ("lead_id", "integer"),
        ("business_name", "string"),
        ("city", "string"),
        ("category", "string"),
        ("review_count", "integer"),
        ("priority_label", "string"),
        ("confidence_level", "string"),
        ("weak_signals", "string"),
    ),
    "manual_review_leads": (
        ("lead_id", "integer"),
        ("business_name", "string"),
        ("city", "string"),
        ("category", "string"),
        ("total_score", "number"),
        ("priority_label", "string"),
        ("confidence_level", "string"),
        ("missing_data", "string"),
        ("risk_flags", "string"),
    ),
    "score_distribution_by_category": (
        ("category", "string"),
        ("priority_label", "string"),
        ("lead_count", "integer"),
        ("average_score", "number"),
    ),
    "import_quality_summary": (
        ("import_run_id", "integer"),
        ("source_name", "string"),
        ("total_records", "integer"),
        ("valid_records", "integer"),
        ("invalid_records", "integer"),
        ("duplicate_records", "integer"),
        ("error_count", "integer"),
        ("created_at", "datetime"),
    ),
    "missing_data_report": (
        ("lead_id", "integer"),
        ("business_name", "string"),
        ("city", "string"),
        ("category", "string"),
        ("missing_fields", "string"),
        ("score_missing_data", "string"),
    ),
}
