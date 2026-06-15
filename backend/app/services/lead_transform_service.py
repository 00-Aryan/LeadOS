"""Lead cleaning and transformation helpers.

This module is intentionally deterministic. It turns noisy CSV strings into
normalized values and explicit validation errors before any row is persisted.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class TransformResult:
    """Normalized row plus validation reasons."""

    data: dict[str, object | None]
    reasons: list[str]


def normalize_text(value: str | None) -> str | None:
    """Trim repeated whitespace and return None for blank values."""
    if value is None:
        return None
    cleaned = re.sub(r"\s+", " ", str(value).strip())
    return cleaned or None


def normalize_key(value: str | None) -> str | None:
    """Normalize text for dedupe/search keys."""
    cleaned = normalize_text(value)
    if cleaned is None:
        return None
    return cleaned.casefold()


def normalize_phone(value: str | None) -> str | None:
    """Normalize a phone number conservatively without assuming locale."""
    cleaned = normalize_text(value)
    if cleaned is None:
        return None
    if cleaned.startswith("+"):
        prefix = "+"
        digits = re.sub(r"\D", "", cleaned[1:])
    else:
        prefix = ""
        digits = re.sub(r"\D", "", cleaned)
    return f"{prefix}{digits}" if digits else None


def parse_rating(value: str | None) -> tuple[float | None, str | None]:
    """Parse rating and return explicit validation error when invalid."""
    cleaned = normalize_text(value)
    if cleaned is None:
        return None, None
    try:
        rating = float(cleaned)
    except ValueError:
        return None, "rating must be numeric"
    if rating < 0 or rating > 5:
        return None, "rating must be between 0 and 5"
    return rating, None


def parse_review_count(value: str | None) -> tuple[int | None, str | None]:
    """Parse review count and return explicit validation error when invalid."""
    cleaned = normalize_text(value)
    if cleaned is None:
        return None, None
    try:
        count = int(cleaned)
    except ValueError:
        return None, "review_count must be an integer"
    if count < 0:
        return None, "review_count cannot be negative"
    return count, None


def transform_lead_row(row: dict[str, str | None]) -> TransformResult:
    """Validate and normalize one raw CSV row."""
    reasons: list[str] = []

    business_name = normalize_text(row.get("business_name"))
    category = normalize_text(row.get("category"))
    city = normalize_text(row.get("city"))

    if business_name is None:
        reasons.append("business_name is required")
    if category is None:
        reasons.append("category is required")
    if city is None:
        reasons.append("city is required")

    rating, rating_error = parse_rating(row.get("rating"))
    if rating_error:
        reasons.append(rating_error)

    review_count, review_error = parse_review_count(row.get("review_count"))
    if review_error:
        reasons.append(review_error)

    website = normalize_text(row.get("website"))
    if website and not website.startswith(("http://", "https://")):
        reasons.append("website must start with http:// or https://")

    data = {
        "business_name": business_name,
        "normalized_business_name": normalize_key(business_name),
        "category": category,
        "normalized_category": normalize_key(category),
        "city": city,
        "normalized_city": normalize_key(city),
        "state": normalize_text(row.get("state")),
        "phone": normalize_phone(row.get("phone")),
        "website": website,
        "rating": rating,
        "review_count": review_count,
        "address": normalize_text(row.get("address")),
        "source_url": normalize_text(row.get("source_url")),
    }
    return TransformResult(data=data, reasons=reasons)
