"""Tests for deterministic lead scoring."""

from app.schemas.audit import AuditCheck, WebsiteAuditResult, WebsiteFetchResult
from app.schemas.lead import LeadInput
from app.services.scoring_service import score_lead


def _audit_with_gaps() -> WebsiteAuditResult:
    return WebsiteAuditResult(
        requested_url="https://example.com",
        fetch=WebsiteFetchResult(
            status="success",
            requested_url="https://example.com",
            final_url="https://example.com",
            status_code=200,
            content_type="text/html",
            html="<html><title>Clinic</title></html>",
        ),
        checks=[
            AuditCheck(name="website_loads", status="true"),
            AuditCheck(name="https_enabled", status="true"),
            AuditCheck(name="meta_description_exists", status="false"),
            AuditCheck(name="phone_detected", status="false"),
            AuditCheck(name="whatsapp_detected", status="false"),
            AuditCheck(name="booking_link_detected", status="false"),
            AuditCheck(name="contact_signal_detected", status="false"),
            AuditCheck(name="social_link_detected", status="false"),
            AuditCheck(name="schema_markup_detected", status="false"),
        ],
    )


def _audit_with_strong_site() -> WebsiteAuditResult:
    return WebsiteAuditResult(
        requested_url="https://example.com",
        fetch=WebsiteFetchResult(
            status="success",
            requested_url="https://example.com",
            final_url="https://example.com",
            status_code=200,
            content_type="text/html",
            html="<html><title>Clinic</title></html>",
        ),
        checks=[
            AuditCheck(name="website_loads", status="true"),
            AuditCheck(name="https_enabled", status="true"),
            AuditCheck(name="meta_description_exists", status="true"),
            AuditCheck(name="phone_detected", status="true"),
            AuditCheck(name="whatsapp_detected", status="true"),
            AuditCheck(name="booking_link_detected", status="true"),
            AuditCheck(name="contact_signal_detected", status="true"),
            AuditCheck(name="social_link_detected", status="true"),
            AuditCheck(name="schema_markup_detected", status="true"),
        ],
    )


def test_strong_business_with_digital_gaps_scores_high() -> None:
    lead = LeadInput(
        business_name="Healthy Smile Clinic",
        category="Dentist",
        city="Ranchi",
        state="Jharkhand",
        phone="+91-9876543210",
        website="https://example.com",
        rating=4.6,
        review_count=150,
        address="Main Road",
    )

    result = score_lead(lead, _audit_with_gaps())

    assert result.total_score >= 75
    assert result.priority_label == "high"
    assert result.confidence_level == "high"
    assert "clear digital improvement gap" in result.positive_signals


def test_strong_business_with_strong_site_has_lower_gap_score() -> None:
    lead = LeadInput(
        business_name="Healthy Smile Clinic",
        category="Dentist",
        city="Ranchi",
        phone="+91-9876543210",
        website="https://example.com",
        rating=4.6,
        review_count=150,
        address="Main Road",
    )

    result = score_lead(lead, _audit_with_strong_site())

    assert result.category_scores.digital_gap < 10
    assert result.total_score < 75


def test_missing_audit_triggers_review_context() -> None:
    lead = LeadInput(
        business_name="Care Clinic",
        category="Clinic",
        city="Ranchi",
        rating=4.1,
        review_count=50,
    )

    result = score_lead(lead, audit=None)

    assert "audit" in result.missing_data
    assert "audit missing" in result.risk_flags
    assert result.confidence_level in {"medium", "low"}


def test_low_quality_lead_is_not_high_priority() -> None:
    lead = LeadInput(
        business_name="Unknown Shop",
        category="Miscellaneous",
        city="Ranchi",
        rating=2.8,
        review_count=0,
    )

    result = score_lead(lead, audit=None)

    assert result.priority_label in {"low", "review_needed"}
    assert "low rating" in result.risk_flags
    assert "no review volume" in result.risk_flags


def test_blocked_fetch_reduces_digital_gap_confidence() -> None:
    lead = LeadInput(
        business_name="Blocked Clinic",
        category="Clinic",
        city="Ranchi",
        phone="+91-9876543210",
        website="http://127.0.0.1",
        rating=4.5,
        review_count=120,
        address="Main Road",
    )
    audit = WebsiteAuditResult(
        requested_url="http://127.0.0.1",
        fetch=WebsiteFetchResult(
            status="blocked",
            requested_url="http://127.0.0.1",
            error_type="invalid_url",
        ),
        checks=[],
    )

    result = score_lead(lead, audit)

    assert "website fetch blocked" in result.risk_flags
    assert result.category_scores.digital_gap == 5
