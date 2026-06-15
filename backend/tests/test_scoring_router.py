"""Tests for scoring API routes."""

from fastapi.testclient import TestClient

from app.main import app


def test_scoring_preview_route_returns_explainable_score() -> None:
    client = TestClient(app)
    payload = {
        "lead": {
            "business_name": "Healthy Smile Clinic",
            "category": "Dentist",
            "city": "Ranchi",
            "state": "Jharkhand",
            "phone": "+91-9876543210",
            "website": "https://example.com",
            "rating": 4.6,
            "review_count": 150,
            "address": "Main Road",
        },
        "audit": {
            "requested_url": "https://example.com",
            "fetch": {
                "status": "success",
                "requested_url": "https://example.com",
                "final_url": "https://example.com",
                "status_code": 200,
                "content_type": "text/html",
                "html": "<html><title>Clinic</title></html>",
            },
            "checks": [
                {"name": "website_loads", "status": "true"},
                {"name": "https_enabled", "status": "true"},
                {"name": "meta_description_exists", "status": "false"},
                {"name": "phone_detected", "status": "false"},
                {"name": "whatsapp_detected", "status": "false"},
                {"name": "booking_link_detected", "status": "false"},
                {"name": "contact_signal_detected", "status": "false"},
                {"name": "social_link_detected", "status": "false"},
                {"name": "schema_markup_detected", "status": "false"},
            ],
        },
    }

    response = client.post("/scoring/preview", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["total_score"] >= 75
    assert body["priority_label"] == "high"
    assert "category_scores" in body
    assert "reason_summary" in body
    assert "positive_signals" in body
    assert "risk_flags" in body
    assert "missing_data" in body


def test_scoring_preview_route_rejects_invalid_lead_payload() -> None:
    client = TestClient(app)

    response = client.post(
        "/scoring/preview",
        json={"lead": {"business_name": ""}},
    )

    assert response.status_code == 422
