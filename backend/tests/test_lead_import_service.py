"""Tests for CSV lead import validation."""

from app.services.lead_import_service import import_leads_from_csv


def test_import_accepts_valid_rows() -> None:
    csv_content = (
        "business_name,category,city,state,phone,website,rating,review_count,address,source_url\n"
        "Ranchi Dental Care,Dentist,Ranchi,Jharkhand,+91-9876543210,https://example.com,4.5,128,Main Road,https://maps.example/1\n"
    )

    summary = import_leads_from_csv(csv_content)

    assert summary.total_rows == 1
    assert summary.valid_rows == 1
    assert summary.invalid_rows == 0
    assert summary.accepted[0].business_name == "Ranchi Dental Care"
    assert summary.accepted[0].rating == 4.5
    assert summary.accepted[0].review_count == 128


def test_import_rejects_missing_required_fields() -> None:
    csv_content = (
        "business_name,category,city,state,phone,website,rating,review_count,address,source_url\n"
        ",Dentist,,Jharkhand,+91-9876543210,https://example.com,4.5,128,Main Road,https://maps.example/1\n"
    )

    summary = import_leads_from_csv(csv_content)

    assert summary.total_rows == 1
    assert summary.valid_rows == 0
    assert summary.invalid_rows == 1
    assert "business_name is required." in summary.rejected[0].reasons
    assert "city is required." in summary.rejected[0].reasons


def test_import_rejects_invalid_numeric_and_website_fields() -> None:
    csv_content = (
        "business_name,category,city,state,phone,website,rating,review_count,address,source_url\n"
        "Bad Lead,Dentist,Ranchi,Jharkhand,+91-9876543210,www.example.com,six,-1,Main Road,https://maps.example/1\n"
    )

    summary = import_leads_from_csv(csv_content)

    assert summary.invalid_rows == 1
    reasons = summary.rejected[0].reasons
    assert "rating must be numeric." in reasons
    assert "review_count cannot be negative." in reasons
    assert "website must start with http:// or https://." in reasons


def test_import_supports_partial_success() -> None:
    csv_content = (
        "business_name,category,city,state,phone,website,rating,review_count,address,source_url\n"
        "Good Clinic,Clinic,Ranchi,Jharkhand,+91-1111111111,https://good.example,4.2,80,Hinoo,https://maps.example/1\n"
        ",Clinic,Ranchi,Jharkhand,+91-2222222222,https://bad.example,4.1,40,Lalpur,https://maps.example/2\n"
    )

    summary = import_leads_from_csv(csv_content)

    assert summary.total_rows == 2
    assert summary.valid_rows == 1
    assert summary.invalid_rows == 1
    assert summary.accepted[0].business_name == "Good Clinic"
