"""Lead transformation tests."""

from app.services.lead_transform_service import normalize_phone, transform_lead_row


def test_normalize_phone_removes_separators() -> None:
    assert normalize_phone("+91 98765-43210") == "+919876543210"


def test_transform_valid_row_normalizes_fields() -> None:
    result = transform_lead_row(
        {
            "business_name": "  Healthy   Smile Clinic ",
            "category": " Dentist ",
            "city": " Ranchi ",
            "phone": "+91 98765-43210",
            "website": "https://example.com",
            "rating": "4.5",
            "review_count": "120",
        }
    )
    assert result.reasons == []
    assert result.data["business_name"] == "Healthy Smile Clinic"
    assert result.data["normalized_business_name"] == "healthy smile clinic"
    assert result.data["phone"] == "+919876543210"
    assert result.data["rating"] == 4.5
    assert result.data["review_count"] == 120


def test_transform_rejects_invalid_rating_and_website() -> None:
    result = transform_lead_row(
        {
            "business_name": "Clinic",
            "category": "Dentist",
            "city": "Ranchi",
            "website": "example.com",
            "rating": "bad",
            "review_count": "-1",
        }
    )
    assert "rating must be numeric" in result.reasons
    assert "review_count cannot be negative" in result.reasons
    assert "website must start with http:// or https://" in result.reasons
