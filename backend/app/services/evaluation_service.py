"""Deterministic outreach quality and risk evaluation service.

This service evaluates draft content only. It does not rewrite, persist,
send, or route outreach messages.
"""

from app.schemas.evaluation import (
    EvaluationScoreBreakdown,
    OutreachEvaluationInput,
    OutreachEvaluationResult,
)

HIGH_RISK_PHRASES = (
    "guaranteed results",
    "guarantee results",
    "guaranteed revenue",
    "guaranteed growth",
    "you are losing customers",
    "you are losing business",
    "we audited your private data",
    "we accessed your private data",
)

MANIPULATIVE_PHRASES = (
    "act now",
    "last chance",
    "before it is too late",
    "urgent action required",
    "do not miss out",
)

FAKE_FAMILIARITY_PHRASES = (
    "as we discussed",
    "as you already know",
    "i know you personally",
    "following our previous conversation",
)

CTA_PHRASES = (
    "would you",
    "are you open",
    "would you like",
    "can i send",
    "may i send",
    "open to seeing",
)

EMAIL_WORD_LIMIT = 150
WHATSAPP_WORD_LIMIT = 80


def describe_service() -> str:
    """Return the service responsibility."""
    return "Evaluates outreach drafts for quality, truthfulness, and risk."


def evaluate_outreach_draft(
    request: OutreachEvaluationInput,
) -> OutreachEvaluationResult:
    """Evaluate one outreach draft using deterministic rules."""
    message = request.draft.message_body.strip()
    normalized_message = _normalize(message)
    supported_facts = [_normalize(fact) for fact in request.supported_facts if _normalize(fact)]

    high_risk_matches = _matching_phrases(
        normalized_message,
        HIGH_RISK_PHRASES,
    )
    manipulative_matches = _matching_phrases(
        normalized_message,
        MANIPULATIVE_PHRASES,
    )
    familiarity_matches = _matching_phrases(
        normalized_message,
        FAKE_FAMILIARITY_PHRASES,
    )

    word_limit = EMAIL_WORD_LIMIT if request.draft.channel == "short_email" else WHATSAPP_WORD_LIMIT
    too_long = len(message.split()) > word_limit

    score_breakdown = EvaluationScoreBreakdown(
        relevance=_score_relevance(normalized_message, supported_facts),
        personalization=_score_personalization(
            normalized_message,
            supported_facts,
        ),
        clarity=_score_clarity(message, too_long),
        tone=_score_tone(
            manipulative_matches,
            familiarity_matches,
        ),
        truthfulness=_score_truthfulness(high_risk_matches),
        cta_quality=_score_cta(normalized_message),
    )

    total_score = sum(score_breakdown.model_dump().values())

    bad_lines = _bad_lines(
        message,
        (
            *high_risk_matches,
            *manipulative_matches,
            *familiarity_matches,
        ),
    )

    failure_reasons = _failure_reasons(
        score_breakdown=score_breakdown,
        supported_facts=supported_facts,
        high_risk_matches=high_risk_matches,
        manipulative_matches=manipulative_matches,
        familiarity_matches=familiarity_matches,
        too_long=too_long,
    )

    risk_rating = _risk_rating(
        high_risk_matches=high_risk_matches,
        manipulative_matches=manipulative_matches,
        familiarity_matches=familiarity_matches,
        too_long=too_long,
        truthfulness=score_breakdown.truthfulness,
    )

    passes = (
        total_score >= 45
        and risk_rating in {"low", "medium"}
        and score_breakdown.truthfulness >= 8
        and score_breakdown.cta_quality >= 7
        and not too_long
        and not high_risk_matches
        and not manipulative_matches
        and not familiarity_matches
    )

    return OutreachEvaluationResult(
        score_breakdown=score_breakdown,
        total_score=total_score,
        risk_rating=risk_rating,
        pass_or_review="pass" if passes else "review",
        failure_reasons=failure_reasons,
        bad_lines=bad_lines,
        suggested_revision=_suggested_revision(failure_reasons),
    )


def _score_relevance(
    message: str,
    supported_facts: list[str],
) -> int:
    if not supported_facts:
        return 2

    matched = sum(fact in message for fact in supported_facts)

    if matched >= 4:
        return 10
    if matched >= 2:
        return 8
    if matched == 1:
        return 5
    return 2


def _score_personalization(
    message: str,
    supported_facts: list[str],
) -> int:
    if not supported_facts:
        return 2

    matched = sum(fact in message for fact in supported_facts)

    if matched >= 3:
        return 10
    if matched == 2:
        return 8
    if matched == 1:
        return 5
    return 2


def _score_clarity(message: str, too_long: bool) -> int:
    score = 10

    if too_long:
        score -= 4

    if len(message.splitlines()) == 1 and len(message.split()) > 60:
        score -= 2

    if len(message.strip()) < 40:
        score -= 3

    return max(score, 0)


def _score_tone(
    manipulative_matches: list[str],
    familiarity_matches: list[str],
) -> int:
    score = 10
    score -= 4 * len(manipulative_matches)
    score -= 3 * len(familiarity_matches)
    return max(score, 0)


def _score_truthfulness(high_risk_matches: list[str]) -> int:
    if not high_risk_matches:
        return 10

    return max(10 - (4 * len(high_risk_matches)), 0)


def _score_cta(message: str) -> int:
    has_question = "?" in message
    has_clear_cta = any(phrase in message for phrase in CTA_PHRASES)

    if has_question and has_clear_cta:
        return 10
    if has_clear_cta:
        return 7
    if has_question:
        return 6
    return 3


def _failure_reasons(
    score_breakdown: EvaluationScoreBreakdown,
    supported_facts: list[str],
    high_risk_matches: list[str],
    manipulative_matches: list[str],
    familiarity_matches: list[str],
    too_long: bool,
) -> list[str]:
    reasons: list[str] = []

    if not supported_facts:
        reasons.append("No supported facts were supplied for evidence review.")

    if high_risk_matches:
        reasons.append("Draft contains unsupported or overpromising claims.")

    if manipulative_matches:
        reasons.append("Draft uses manipulative pressure or artificial urgency.")

    if familiarity_matches:
        reasons.append("Draft uses unverified familiarity.")

    if too_long:
        reasons.append("Draft is too long for the selected channel.")

    if score_breakdown.relevance < 7:
        reasons.append("Draft has weak relevance to the supplied facts.")

    if score_breakdown.personalization < 7:
        reasons.append("Draft has insufficient evidence-based personalization.")

    if score_breakdown.clarity < 7:
        reasons.append("Draft requires clearer or shorter wording.")

    if score_breakdown.tone < 8:
        reasons.append("Draft tone requires human revision.")

    if score_breakdown.truthfulness < 8:
        reasons.append("Draft truthfulness score is below the required threshold.")

    if score_breakdown.cta_quality < 7:
        reasons.append("Draft does not contain a sufficiently clear next step.")

    return list(dict.fromkeys(reasons))


def _risk_rating(
    high_risk_matches: list[str],
    manipulative_matches: list[str],
    familiarity_matches: list[str],
    too_long: bool,
    truthfulness: int,
) -> str:
    if high_risk_matches or truthfulness < 6:
        return "high"

    if manipulative_matches or familiarity_matches or too_long:
        return "medium"

    return "low"


def _matching_phrases(
    message: str,
    phrases: tuple[str, ...],
) -> list[str]:
    return [phrase for phrase in phrases if phrase in message]


def _bad_lines(
    message: str,
    matched_phrases: tuple[str, ...],
) -> list[str]:
    if not matched_phrases:
        return []

    bad_lines: list[str] = []

    for line in message.splitlines():
        normalized_line = _normalize(line)
        if any(phrase in normalized_line for phrase in matched_phrases):
            cleaned = line.strip()
            if cleaned:
                bad_lines.append(cleaned)

    return list(dict.fromkeys(bad_lines))


def _suggested_revision(
    failure_reasons: list[str],
) -> str | None:
    if not failure_reasons:
        return None

    return (
        "Revise the draft using only verified facts, remove pressure or "
        "unsupported outcome claims, keep the channel length appropriate, "
        "and end with one clear low-pressure question."
    )


def _normalize(value: str) -> str:
    return " ".join(value.lower().strip().split())
