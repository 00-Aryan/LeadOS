"""Tests for deterministic lead scoring."""

from app.schemas.audit import AuditCheck, WebsiteAuditResult, WebsiteFetchResult
from app.schemas.lead import LeadInput
from app.services.audit_service import audit_website_presence
from app.services.scoring_service import score_lead


def test_strong_business_with_weak_digital_presence_scores_high() -> None:
    result = score_lead(_strong_clinic_lead(), _legacy_audit_with_gaps())

    assert result.total_score >= 75
    assert result.priority_label == "high"
    assert result.confidence_level == "high"
    assert result.category_scores.business_strength == 25
    assert result.category_scores.digital_gap >= 20
    assert "clear digital improvement gap" in result.positive_signals
    _assert_total_matches_category_sum(result)
    _assert_category_ranges(result)


def test_strong_business_with_strong_digital_presence_has_lower_digital_gap() -> None:
    weak_site_result = score_lead(_strong_clinic_lead(), _legacy_audit_with_gaps())
    strong_site_result = score_lead(_strong_clinic_lead(), _legacy_audit_with_strong_site())

    assert strong_site_result.category_scores.digital_gap < 10
    assert (
        strong_site_result.category_scores.digital_gap
        < weak_site_result.category_scores.digital_gap
    )
    assert strong_site_result.total_score < weak_site_result.total_score
    assert strong_site_result.priority_label == "medium"
    _assert_total_matches_category_sum(strong_site_result)
    _assert_category_ranges(strong_site_result)


def test_presence_audit_keys_score_like_legacy_audit_names() -> None:
    presence_audit = audit_website_presence(
        "https://example.com",
        """
        <html>
          <head><title>Healthy Smile Clinic</title></head>
          <body>No contact links or social proof here.</body>
        </html>
        """,
    )

    result = score_lead(_strong_clinic_lead(), presence_audit)

    assert result.category_scores.digital_gap >= 15
    assert result.priority_label == "high"
    assert "clear digital improvement gap" in result.positive_signals


def test_missing_audit_reduces_confidence_and_adds_context() -> None:
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
    assert result.confidence_level == "low"
    assert result.priority_label == "review_needed"


def test_blocked_fetch_produces_bounded_low_digital_gap_with_risk_flag() -> None:
    result = score_lead(_strong_clinic_lead(), _legacy_audit_with_fetch_status("blocked"))

    assert result.category_scores.digital_gap == 5
    assert "website fetch blocked" in result.risk_flags
    assert result.confidence_level == "medium"
    _assert_category_ranges(result)


def test_failed_fetch_produces_bounded_digital_gap_with_risk_flag() -> None:
    result = score_lead(_strong_clinic_lead(), _legacy_audit_with_fetch_status("failed"))

    assert result.category_scores.digital_gap == 10
    assert "website fetch failed" in result.risk_flags
    assert result.confidence_level == "medium"
    _assert_category_ranges(result)


def test_low_rating_and_no_reviews_is_not_high_priority() -> None:
    lead = LeadInput(
        business_name="Unknown Shop",
        category="Miscellaneous",
        city="Ranchi",
        rating=2.8,
        review_count=0,
    )

    result = score_lead(lead, audit=None)

    assert result.priority_label == "review_needed"
    assert "low rating" in result.risk_flags
    assert "no review volume" in result.risk_flags
    assert "category commercial value unverified" in result.risk_flags


def test_missing_phone_website_and_address_reduce_contactability_and_confidence() -> None:
    lead = LeadInput(
        business_name="Healthy Smile Clinic",
        category="Dentist",
        city="Ranchi",
        rating=4.6,
        review_count=150,
    )

    result = score_lead(lead, _legacy_audit_with_strong_site())

    assert result.category_scores.contactability < 8
    assert {"phone", "website", "address"}.issubset(set(result.missing_data))
    assert result.confidence_level == "medium"
    assert result.priority_label == "low"


def test_commercial_category_fit_is_deterministic() -> None:
    dentist_result = score_lead(_strong_clinic_lead(category="Dentist"), _legacy_audit_with_gaps())
    clinic_result = score_lead(_strong_clinic_lead(category="Clinic"), _legacy_audit_with_gaps())

    assert dentist_result.category_scores.commercial_fit == 15
    assert clinic_result.category_scores.commercial_fit == 15
    assert "commercially relevant category" in dentist_result.positive_signals
    assert "commercially relevant category" in clinic_result.positive_signals


def test_non_commercial_unverified_category_adds_risk_flag() -> None:
    result = score_lead(
        _strong_clinic_lead(category="Miscellaneous"),
        _legacy_audit_with_gaps(),
    )

    assert result.category_scores.commercial_fit == 8
    assert "category commercial value unverified" in result.risk_flags
    assert result.confidence_level == "medium"


def test_total_score_equals_sum_of_category_scores() -> None:
    result = score_lead(_strong_clinic_lead(), _legacy_audit_with_gaps())

    _assert_total_matches_category_sum(result)


def test_category_score_ranges_never_exceed_rubric_caps() -> None:
    scenarios = [
        score_lead(_strong_clinic_lead(), _legacy_audit_with_gaps()),
        score_lead(_strong_clinic_lead(), _legacy_audit_with_strong_site()),
        score_lead(_strong_clinic_lead(), _legacy_audit_with_fetch_status("failed")),
        score_lead(
            LeadInput(business_name="Unknown Shop", category="Miscellaneous", city="Ranchi"),
            audit=None,
        ),
    ]

    for result in scenarios:
        _assert_category_ranges(result)
        assert 0 <= result.total_score <= 100


def test_priority_label_transitions_are_deterministic() -> None:
    high = score_lead(_strong_clinic_lead(), _legacy_audit_with_gaps())
    medium = score_lead(_strong_clinic_lead(), _legacy_audit_with_strong_site())
    review_needed = score_lead(
        LeadInput(business_name="Unknown Shop", category="Miscellaneous", city="Ranchi"),
        audit=None,
    )

    assert high.priority_label == "high"
    assert medium.priority_label == "medium"
    assert review_needed.priority_label == "review_needed"


def test_reason_summary_contains_score_and_priority_label() -> None:
    result = score_lead(_strong_clinic_lead(), _legacy_audit_with_gaps())

    assert str(result.total_score) in result.reason_summary
    assert result.priority_label in result.reason_summary


def test_scoring_output_remains_serializable_through_model_dump() -> None:
    result = score_lead(_strong_clinic_lead(), _legacy_audit_with_gaps())

    dumped = result.model_dump(mode="json")

    assert dumped["total_score"] == result.total_score
    assert dumped["category_scores"]["digital_gap"] == result.category_scores.digital_gap
    assert dumped["priority_label"] == result.priority_label
    assert isinstance(dumped["positive_signals"], list)
    assert isinstance(dumped["risk_flags"], list)
    assert isinstance(dumped["missing_data"], list)


def _strong_clinic_lead(category: str = "Dentist") -> LeadInput:
    return LeadInput(
        business_name="Healthy Smile Clinic",
        category=category,
        city="Ranchi",
        state="Jharkhand",
        phone="+91-9876543210",
        website="https://example.com",
        rating=4.6,
        review_count=150,
        address="Main Road",
    )


def _legacy_audit_with_gaps() -> WebsiteAuditResult:
    return _legacy_audit(
        fetch_status="success",
        checks=[
            AuditCheck(name="website_loads", status="true"),
            AuditCheck(name="https_enabled", status="true"),
            AuditCheck(name="title_exists", status="true"),
            AuditCheck(name="meta_description_exists", status="false"),
            AuditCheck(name="phone_detected", status="false"),
            AuditCheck(name="whatsapp_detected", status="false"),
            AuditCheck(name="booking_link_detected", status="false"),
            AuditCheck(name="contact_signal_detected", status="false"),
            AuditCheck(name="social_link_detected", status="false"),
            AuditCheck(name="schema_markup_detected", status="false"),
        ],
    )


def _legacy_audit_with_strong_site() -> WebsiteAuditResult:
    return _legacy_audit(
        fetch_status="success",
        checks=[
            AuditCheck(name="website_loads", status="true"),
            AuditCheck(name="https_enabled", status="true"),
            AuditCheck(name="title_exists", status="true"),
            AuditCheck(name="meta_description_exists", status="true"),
            AuditCheck(name="phone_detected", status="true"),
            AuditCheck(name="whatsapp_detected", status="true"),
            AuditCheck(name="booking_link_detected", status="true"),
            AuditCheck(name="contact_signal_detected", status="true"),
            AuditCheck(name="social_link_detected", status="true"),
            AuditCheck(name="schema_markup_detected", status="true"),
        ],
    )


def _legacy_audit_with_fetch_status(fetch_status: str) -> WebsiteAuditResult:
    return _legacy_audit(fetch_status=fetch_status, checks=[])


def _legacy_audit(fetch_status: str, checks: list[AuditCheck]) -> WebsiteAuditResult:
    return WebsiteAuditResult(
        requested_url="https://example.com",
        fetch=WebsiteFetchResult(
            status=fetch_status,
            requested_url="https://example.com",
            final_url="https://example.com" if fetch_status == "success" else None,
            status_code=200 if fetch_status == "success" else None,
            content_type="text/html" if fetch_status == "success" else None,
            html="<html><title>Clinic</title></html>" if fetch_status == "success" else None,
            error_type="fetch_error" if fetch_status != "success" else None,
        ),
        checks=checks,
    )


def _assert_total_matches_category_sum(result) -> None:
    assert result.total_score == sum(result.category_scores.model_dump().values())


def _assert_category_ranges(result) -> None:
    assert 0 <= result.category_scores.business_strength <= 25
    assert 0 <= result.category_scores.digital_gap <= 30
    assert 0 <= result.category_scores.contactability <= 20
    assert 0 <= result.category_scores.commercial_fit <= 15
    assert 0 <= result.category_scores.outreach_priority <= 10
