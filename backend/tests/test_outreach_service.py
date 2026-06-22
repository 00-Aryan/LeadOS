"""Tests for deterministic outreach draft generation."""

import pytest
from pydantic import ValidationError

from app.schemas.outreach import OutreachDraftInput, OutreachDraftResult
from app.services.outreach_service import create_outreach_draft


def test_short_email_uses_known_facts_and_requires_review() -> None:
    request = _draft_input(channel="short_email")

    result = create_outreach_draft(request)

    assert result.channel == "short_email"
    assert result.subject_line == "Quick website visibility idea for Healthy Smile Clinic"
    assert "Healthy Smile Clinic" in result.message_body
    assert "Dentist" in result.message_body
    assert "Ranchi" in result.message_body
    assert "missing meta description" in result.message_body
    assert "WhatsApp link not visible" in result.message_body
    assert "Lead scored 82" not in result.message_body
    assert any("Lead scored 82" in note for note in result.personalization_notes)
    assert result.review_required is True


def test_whatsapp_message_has_no_subject_and_stays_concise() -> None:
    result = create_outreach_draft(_draft_input(channel="whatsapp_message"))

    assert result.channel == "whatsapp_message"
    assert result.subject_line is None
    assert len(result.message_body) <= 500
    assert result.message_body.startswith("Hi Healthy Smile Clinic team")
    assert result.review_required is True


def test_missing_audit_findings_are_explicit_assumptions() -> None:
    request = _draft_input(channel="short_email")
    request.audit_findings.clear()

    result = create_outreach_draft(request)

    assert "I do not have a verified public website finding" in result.message_body
    assert any("No specific audit findings" in item for item in result.assumptions_used)
    assert result.review_required is True


def test_outreach_draft_result_serializes_with_review_required() -> None:
    result = create_outreach_draft(_draft_input(channel="short_email"))

    dumped = result.model_dump(mode="json")

    assert dumped["channel"] == "short_email"
    assert dumped["review_required"] is True
    assert isinstance(dumped["personalization_notes"], list)
    assert OutreachDraftResult(**dumped).review_required is True


def test_unknown_channel_is_rejected_by_schema() -> None:
    with pytest.raises(ValidationError):
        OutreachDraftInput(
            business_name="Healthy Smile Clinic",
            category="Dentist",
            location="Ranchi",
            audit_findings=[],
            score_reason=None,
            offer_angle="improving visible website trust signals",
            channel="sms",
        )


def _draft_input(channel: str) -> OutreachDraftInput:
    return OutreachDraftInput(
        business_name="Healthy Smile Clinic",
        category="Dentist",
        location="Ranchi",
        audit_findings=[
            "missing meta description",
            "WhatsApp link not visible",
            "booking link not visible",
        ],
        score_reason="Lead scored 82 because it has strong reviews and visible web gaps.",
        offer_angle="improving visible website trust signals",
        channel=channel,
    )
