"""Tests for deterministic outreach draft evaluation."""

from app.schemas.evaluation import OutreachEvaluationInput
from app.schemas.outreach import OutreachDraftInput, OutreachDraftResult
from app.services.evaluation_service import evaluate_outreach_draft
from app.services.outreach_service import create_outreach_draft


def test_supported_truthful_outreach_passes_with_low_risk() -> None:
    draft = create_outreach_draft(_outreach_input())

    result = evaluate_outreach_draft(
        OutreachEvaluationInput(
            draft=draft,
            supported_facts=_supported_facts(),
        ),
    )

    assert result.pass_or_review == "pass"
    assert result.risk_rating == "low"
    assert result.total_score >= 45
    assert result.score_breakdown.truthfulness >= 8
    assert result.score_breakdown.cta_quality >= 7
    assert result.failure_reasons == []
    assert result.bad_lines == []
    assert result.suggested_revision is None


def test_guaranteed_result_claim_is_high_risk_and_requires_review() -> None:
    draft = OutreachDraftResult(
        channel="short_email",
        subject_line="Guaranteed growth",
        message_body=(
            "Hi Healthy Smile Clinic team,\n\n"
            "We guarantee results and guaranteed revenue within one month.\n\n"
            "Would you like to proceed?"
        ),
        personalization_notes=[],
        assumptions_used=[],
    )

    result = evaluate_outreach_draft(
        OutreachEvaluationInput(
            draft=draft,
            supported_facts=_supported_facts(),
        ),
    )

    assert result.pass_or_review == "review"
    assert result.risk_rating == "high"
    assert result.score_breakdown.truthfulness < 8
    assert result.bad_lines
    assert any("unsupported" in reason.lower() for reason in result.failure_reasons)
    assert result.suggested_revision is not None


def test_manipulative_urgency_requires_review() -> None:
    draft = OutreachDraftResult(
        channel="whatsapp_message",
        subject_line=None,
        message_body=(
            "Hi Healthy Smile Clinic team. Act now before it is too late. "
            "Would you like the details?"
        ),
        personalization_notes=[],
        assumptions_used=[],
    )

    result = evaluate_outreach_draft(
        OutreachEvaluationInput(
            draft=draft,
            supported_facts=_supported_facts(),
        ),
    )

    assert result.pass_or_review == "review"
    assert result.risk_rating == "medium"
    assert result.score_breakdown.tone < 8
    assert result.bad_lines


def test_missing_supported_facts_reduces_relevance_and_requires_review() -> None:
    draft = create_outreach_draft(_outreach_input())

    result = evaluate_outreach_draft(
        OutreachEvaluationInput(
            draft=draft,
            supported_facts=[],
        ),
    )

    assert result.pass_or_review == "review"
    assert result.score_breakdown.relevance < 7
    assert result.score_breakdown.personalization < 7
    assert any("supported facts" in reason.lower() for reason in result.failure_reasons)


def test_overlong_whatsapp_message_requires_review() -> None:
    repeated_text = " ".join(["verified website observation"] * 90)
    draft = OutreachDraftResult(
        channel="whatsapp_message",
        subject_line=None,
        message_body=(
            f"Hi Healthy Smile Clinic team. {repeated_text} "
            "Would you be open to a brief conversation?"
        ),
        personalization_notes=[],
        assumptions_used=[],
    )

    result = evaluate_outreach_draft(
        OutreachEvaluationInput(
            draft=draft,
            supported_facts=_supported_facts(),
        ),
    )

    assert result.pass_or_review == "review"
    assert result.risk_rating == "medium"
    assert result.score_breakdown.clarity < 10
    assert any("too long" in reason.lower() for reason in result.failure_reasons)


def test_evaluation_result_is_json_serializable() -> None:
    draft = create_outreach_draft(_outreach_input())

    result = evaluate_outreach_draft(
        OutreachEvaluationInput(
            draft=draft,
            supported_facts=_supported_facts(),
        ),
    )
    dumped = result.model_dump(mode="json")

    assert dumped["total_score"] == result.total_score
    assert dumped["risk_rating"] == result.risk_rating
    assert dumped["pass_or_review"] == result.pass_or_review
    assert isinstance(dumped["score_breakdown"], dict)
    assert isinstance(dumped["failure_reasons"], list)
    assert isinstance(dumped["bad_lines"], list)


def _outreach_input() -> OutreachDraftInput:
    return OutreachDraftInput(
        business_name="Healthy Smile Clinic",
        category="Dentist",
        location="Ranchi",
        audit_findings=[
            "missing meta description",
            "WhatsApp link not visible",
        ],
        score_reason="Lead scored 82 because of strong reviews and visible web gaps.",
        offer_angle="improving visible website trust signals",
        channel="short_email",
    )


def _supported_facts() -> list[str]:
    return [
        "Healthy Smile Clinic",
        "Dentist",
        "Ranchi",
        "missing meta description",
        "WhatsApp link not visible",
        "improving visible website trust signals",
    ]
