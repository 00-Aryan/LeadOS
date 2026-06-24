"""Deterministic outreach draft service.

This service prepares draft copy only. It does not send messages, persist
drafts, call an evaluator, or use external/LLM services.
"""

from app.schemas.outreach import OutreachDraftInput, OutreachDraftResult


def describe_service() -> str:
    """Return the service responsibility."""
    return "Prepares outreach drafts from known lead facts and audit findings."


def create_outreach_draft(request: OutreachDraftInput) -> OutreachDraftResult:
    """Create one deterministic outreach draft from supplied facts only."""
    if request.channel == "short_email":
        return _build_short_email(request)
    return _build_whatsapp_message(request)


def _build_short_email(request: OutreachDraftInput) -> OutreachDraftResult:
    audit_sentence = _audit_sentence(request.audit_findings)
    message_body = "\n\n".join(
        [
            f"Hi {request.business_name} team,",
            (
                f"Your listing shows {request.business_name} as a "
                f"{request.category} business in {request.location}. "
                f"{audit_sentence}"
            ),
            (
                "I can prepare a short, human-reviewed website improvement "
                f"note focused on {request.offer_angle}. Would you be open "
                "to seeing the 2-3 highest-priority fixes?"
            ),
            "Regards,",
        ],
    )

    return OutreachDraftResult(
        channel=request.channel,
        subject_line=f"Quick website visibility idea for {request.business_name}",
        message_body=message_body,
        personalization_notes=_personalization_notes(request),
        assumptions_used=_assumptions_used(request),
    )


def _build_whatsapp_message(request: OutreachDraftInput) -> OutreachDraftResult:
    audit_sentence = _audit_sentence(request.audit_findings)
    message_body = (
        f"Hi {request.business_name} team, your listing shows a "
        f"{request.category} business in {request.location}. {audit_sentence} "
        "I can prepare a short, human-reviewed improvement note focused on "
        f"{request.offer_angle}. Would you like the top 2-3 fixes?"
    )

    return OutreachDraftResult(
        channel=request.channel,
        subject_line=None,
        message_body=message_body,
        personalization_notes=_personalization_notes(request),
        assumptions_used=_assumptions_used(request),
    )


def _audit_sentence(audit_findings: list[str]) -> str:
    findings = [_clean_text(finding) for finding in audit_findings if _clean_text(finding)]
    if not findings:
        return "I do not have a verified public website finding to mention yet."

    if len(findings) == 1:
        return f"A public website audit note says: {findings[0]}."

    return f"Public website audit notes include: {findings[0]} and {findings[1]}."


def _personalization_notes(request: OutreachDraftInput) -> list[str]:
    notes = [
        (
            f"Business fact: {request.business_name} is a {request.category} "
            f"business in {request.location}."
        ),
        f"Offer angle: {_clean_text(request.offer_angle)}.",
    ]

    for finding in request.audit_findings[:3]:
        cleaned = _clean_text(finding)
        if cleaned:
            notes.append(f"Audit fact for reviewer: {cleaned}.")

    if request.score_reason:
        notes.append(f"Scoring context for reviewer only: {_clean_text(request.score_reason)}.")

    return notes


def _assumptions_used(request: OutreachDraftInput) -> list[str]:
    assumptions = [
        f"The recipient is the correct contact for {request.business_name}.",
        "Public audit facts will be manually verified before use.",
        "No revenue, ranking, or conversion impact is assumed.",
    ]

    if not request.audit_findings:
        assumptions.append(
            "No specific audit findings were supplied, so the draft avoids naming a gap.",
        )

    return assumptions


def _clean_text(value: str) -> str:
    return " ".join(value.strip().rstrip(".").split())
