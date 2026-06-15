"""Deterministic, explainable lead scoring service."""

from app.schemas.audit import WebsiteAuditResult
from app.schemas.lead import LeadInput
from app.schemas.score import LeadScoreResult, ScoreBreakdown

HIGH_VALUE_CATEGORIES = {
    "dentist",
    "clinic",
    "doctor",
    "dermatologist",
    "physiotherapist",
    "gym",
    "coaching",
    "salon",
    "real estate",
    "interior designer",
}


def describe_service() -> str:
    """Return the service responsibility."""
    return "Converts lead and audit data into an explainable opportunity score."


def score_lead(lead: LeadInput, audit: WebsiteAuditResult | None = None) -> LeadScoreResult:
    """Score one lead using deterministic rules.

    The score is an opportunity score, not a promise of conversion. Missing data
    reduces confidence and may trigger review.
    """
    positive_signals: list[str] = []
    risk_flags: list[str] = []
    missing_data: list[str] = []

    business_strength = _score_business_strength(
        lead,
        positive_signals,
        risk_flags,
        missing_data,
    )
    digital_gap = _score_digital_gap(audit, positive_signals, risk_flags, missing_data)
    contactability = _score_contactability(lead, audit, positive_signals, missing_data)
    commercial_fit = _score_commercial_fit(lead, positive_signals, risk_flags)
    outreach_priority = _score_outreach_priority(
        business_strength=business_strength,
        digital_gap=digital_gap,
        contactability=contactability,
        positive_signals=positive_signals,
        risk_flags=risk_flags,
    )

    category_scores = ScoreBreakdown(
        business_strength=business_strength,
        digital_gap=digital_gap,
        contactability=contactability,
        commercial_fit=commercial_fit,
        outreach_priority=outreach_priority,
    )
    total_score = sum(category_scores.model_dump().values())
    confidence_level = _confidence_level(
        missing_data=missing_data,
        risk_flags=risk_flags,
    )
    priority_label = _priority_label(
        total_score=total_score,
        confidence_level=confidence_level,
    )

    return LeadScoreResult(
        total_score=total_score,
        category_scores=category_scores,
        priority_label=priority_label,
        confidence_level=confidence_level,
        reason_summary=_build_reason_summary(
            total_score,
            priority_label,
            positive_signals,
            risk_flags,
        ),
        positive_signals=positive_signals,
        risk_flags=risk_flags,
        missing_data=missing_data,
    )


def _score_business_strength(
    lead: LeadInput,
    positive_signals: list[str],
    risk_flags: list[str],
    missing_data: list[str],
) -> int:
    score = 0

    if lead.rating is None:
        missing_data.append("rating")
    elif lead.rating >= 4.3:
        score += 10
        positive_signals.append("strong rating")
    elif lead.rating >= 3.8:
        score += 6
        positive_signals.append("acceptable rating")
    else:
        score += 2
        risk_flags.append("low rating")

    if lead.review_count is None:
        missing_data.append("review_count")
    elif lead.review_count >= 100:
        score += 10
        positive_signals.append("strong review volume")
    elif lead.review_count >= 30:
        score += 6
        positive_signals.append("moderate review volume")
    elif lead.review_count > 0:
        score += 3
    else:
        risk_flags.append("no review volume")

    if lead.business_name and lead.category and lead.city:
        score += 5
        positive_signals.append("complete core lead identity")

    return min(score, 25)


def _score_digital_gap(
    audit: WebsiteAuditResult | None,
    positive_signals: list[str],
    risk_flags: list[str],
    missing_data: list[str],
) -> int:
    if audit is None:
        missing_data.append("audit")
        risk_flags.append("audit missing")
        return 8

    checks = {check.name: check.status for check in audit.checks}
    score = 0

    if audit.fetch.status == "blocked":
        risk_flags.append("website fetch blocked")
        return 5
    if audit.fetch.status == "failed":
        risk_flags.append("website fetch failed")
        return 10

    if checks.get("website_loads") == "true":
        positive_signals.append("website loads")
    else:
        score += 10
        positive_signals.append("website unavailable creates digital gap")

    missing_or_weak_checks = [
        "meta_description_exists",
        "phone_detected",
        "whatsapp_detected",
        "booking_link_detected",
        "contact_signal_detected",
        "social_link_detected",
        "schema_markup_detected",
    ]
    for check_name in missing_or_weak_checks:
        if checks.get(check_name) == "false":
            score += 3

    if checks.get("https_enabled") == "false":
        score += 4
        risk_flags.append("website lacks https")

    if score >= 15:
        positive_signals.append("clear digital improvement gap")

    return min(score, 30)


def _score_contactability(
    lead: LeadInput,
    audit: WebsiteAuditResult | None,
    positive_signals: list[str],
    missing_data: list[str],
) -> int:
    score = 0

    if lead.phone:
        score += 8
        positive_signals.append("phone available")
    else:
        missing_data.append("phone")

    if lead.website:
        score += 4
        positive_signals.append("website available")
    else:
        missing_data.append("website")

    if lead.address:
        score += 3
        positive_signals.append("address available")
    else:
        missing_data.append("address")

    if audit is not None:
        checks = {check.name: check.status for check in audit.checks}
        if checks.get("contact_signal_detected") == "true":
            score += 3
        if checks.get("whatsapp_detected") == "true" or checks.get("phone_detected") == "true":
            score += 2

    return min(score, 20)


def _score_commercial_fit(
    lead: LeadInput,
    positive_signals: list[str],
    risk_flags: list[str],
) -> int:
    category = lead.category.lower().strip()

    if any(value in category for value in HIGH_VALUE_CATEGORIES):
        positive_signals.append("commercially relevant category")
        return 15

    risk_flags.append("category commercial value unverified")
    return 8


def _score_outreach_priority(
    business_strength: int,
    digital_gap: int,
    contactability: int,
    positive_signals: list[str],
    risk_flags: list[str],
) -> int:
    if business_strength >= 18 and digital_gap >= 15 and contactability >= 12:
        positive_signals.append("strong outreach priority pattern")
        return 10
    if business_strength >= 12 and digital_gap >= 10 and contactability >= 8:
        return 7
    if contactability < 6:
        risk_flags.append("low contactability")
        return 2
    return 4


def _confidence_level(missing_data: list[str], risk_flags: list[str]) -> str:
    if len(missing_data) >= 4 or len(risk_flags) >= 3:
        return "low"
    if len(missing_data) >= 2 or risk_flags:
        return "medium"
    return "high"


def _priority_label(total_score: int, confidence_level: str) -> str:
    if confidence_level == "low":
        return "review_needed"
    if total_score >= 75:
        return "high"
    if total_score >= 50:
        return "medium"
    return "low"


def _build_reason_summary(
    total_score: int,
    priority_label: str,
    positive_signals: list[str],
    risk_flags: list[str],
) -> str:
    signal_summary = ", ".join(positive_signals[:4]) or "limited positive signals"
    risk_summary = ", ".join(risk_flags[:3]) or "no major risk flags"
    return (
        f"Lead scored {total_score} with priority '{priority_label}' because of "
        f"{signal_summary}. Risk context: {risk_summary}."
    )
