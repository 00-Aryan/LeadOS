"""Tests for lead API routes."""

from fastapi.testclient import TestClient

from app.main import app


def test_lead_import_route_returns_summary() -> None:
    client = TestClient(app)
    csv_content = (
        "business_name,category,city,state,phone,website,rating,review_count,address,source_url\n"
        "Ranchi Dental Care,Dentist,Ranchi,Jharkhand,+91-9876543210,https://example.com,4.5,128,Main Road,https://maps.example/1\n"
    )

    response = client.post("/leads/import", json={"csv_content": csv_content})

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_rows"] == 1
    assert payload["valid_rows"] == 1
    assert payload["invalid_rows"] == 0
    assert payload["accepted"][0]["business_name"] == "Ranchi Dental Care"
