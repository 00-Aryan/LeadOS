"""CSV lead import validation service."""

from __future__ import annotations

import csv
from io import StringIO
from typing import Iterable

from app.schemas.lead import LeadImportError, LeadImportSummary, LeadInput

REQUIRED_COLUMNS = ("business_name", "category", "city")
EXPECTED_COLUMNS = (
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


def describe_service() -> str:
    """Return the service responsibility."""
    return "Validates and normalizes incoming lead rows."


def import_leads_from_csv(csv_content: str) -> LeadImportSummary:
    """Validate CSV text and return accepted/rejected rows.

    This function is intentionally deterministic and persistence-free. Storage
    will be added behind a repository boundary after the import contract is
    stable.
    """
    reader = csv.DictReader(StringIO(csv_content))
    accepted: list[LeadInput] = []
    rejected: list[LeadImportError] = []

    if reader.fieldnames is None:
        return LeadImportSummary(
            total_rows=0,
            valid_rows=0,
            invalid_rows=1,
            accepted=[],
            rejected=[
                LeadImportError(
                    row_number=0,
                    reasons=["CSV header is missing."],
                    raw_row={},
                )
            ],
        )

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
    if missing_columns:
        return LeadImportSummary(
            total_rows=0,
            valid_rows=0,
            invalid_rows=1,
            accepted=[],
            rejected=[
                LeadImportError(
                    row_number=0,
                    reasons=[f"Missing required column: {column}" for column in missing_columns],
                    raw_row={"header": ",".join(reader.fieldnames)},
                )
            ],
        )

    total_rows = 0
    for row_number, raw_row in enumerate(reader, start=2):
        total_rows += 1
        normalized_row = _normalize_row(raw_row)
        reasons = _validate_row(normalized_row)

        if reasons:
            rejected.append(
                LeadImportError(
                    row_number=row_number,
                    reasons=reasons,
                    raw_row=normalized_row,
                )
            )
            continue

        accepted.append(
            LeadInput(
                business_name=normalized_row["business_name"] or "",
                category=normalized_row["category"] or "",
                city=normalized_row["city"] or "",
                state=normalized_row.get("state"),
                phone=normalized_row.get("phone"),
                website=normalized_row.get("website"),
                rating=_parse_float(normalized_row.get("rating")),
                review_count=_parse_int(normalized_row.get("review_count")),
                address=normalized_row.get("address"),
                source_url=normalized_row.get("source_url"),
            )
        )

    return LeadImportSummary(
        total_rows=total_rows,
        valid_rows=len(accepted),
        invalid_rows=len(rejected),
        accepted=accepted,
        rejected=rejected,
    )


def _normalize_row(row: dict[str, str | None]) -> dict[str, str | None]:
    """Normalize known columns and ignore unexpected fields."""
    normalized: dict[str, str | None] = {}
    for column in EXPECTED_COLUMNS:
        value = row.get(column)
        normalized[column] = value.strip() if isinstance(value, str) and value.strip() else None
    return normalized


def _validate_row(row: dict[str, str | None]) -> list[str]:
    """Return validation errors for one normalized row."""
    reasons: list[str] = []

    for column in REQUIRED_COLUMNS:
        if not row.get(column):
            reasons.append(f"{column} is required.")

    rating = row.get("rating")
    if rating is not None:
        parsed_rating = _parse_float(rating)
        if parsed_rating is None:
            reasons.append("rating must be numeric.")
        elif parsed_rating < 0 or parsed_rating > 5:
            reasons.append("rating must be between 0 and 5.")

    review_count = row.get("review_count")
    if review_count is not None:
        parsed_review_count = _parse_int(review_count)
        if parsed_review_count is None:
            reasons.append("review_count must be an integer.")
        elif parsed_review_count < 0:
            reasons.append("review_count cannot be negative.")

    website = row.get("website")
    if website is not None and not website.startswith(("http://", "https://")):
        reasons.append("website must start with http:// or https://.")

    return reasons


def _parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None
