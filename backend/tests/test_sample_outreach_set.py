"""Deterministic tests for the fictional sample outreach set."""

import json
from collections import Counter
from pathlib import Path

from app.schemas.evaluation import OutreachEvaluationInput
from app.schemas.outreach import OutreachDraftInput, OutreachDraftResult
from app.services.evaluation_service import evaluate_outreach_draft
from app.services.outreach_service import create_outreach_draft

REPO_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_JSON = REPO_ROOT / "data" / "outreach_samples" / "sample_outreach_cases.json"
SAMPLE_DOC = REPO_ROOT / "docs" / "SAMPLE_OUTREACH_SET.md"
CONTEXT_INDEX = REPO_ROOT / "docs" / "CONTEXT_INDEX.md"

REQUIRED_CASE_FIELDS = {
    "case_id",
    "scenario",
    "fictional_business",
    "input",
    "draft",
    "supported_facts",
    "evaluation",
    "expert_review",
}

FICTIONAL_BUSINESS_FIELDS = {
    "business_name",
    "category",
    "location",
    "fictional",
}

INPUT_FIELDS = {
    "business_name",
    "category",
    "location",
    "audit_findings",
    "score_reason",
    "offer_angle",
    "channel",
}

DRAFT_FIELDS = {
    "channel",
    "subject_line",
    "message_body",
    "personalization_notes",
    "assumptions_used",
    "review_required",
}

EVALUATION_FIELDS = {
    "score_breakdown",
    "total_score",
    "risk_rating",
    "pass_or_review",
    "failure_reasons",
    "bad_lines",
    "suggested_revision",
}

EXPERT_REVIEW_FIELDS = {
    "decision",
    "evidence_verified",
    "unresolved_concerns",
    "required_revisions",
    "re_evaluation_required",
    "automatic_sending_permitted",
    "review_notes",
}

REQUIRED_SCENARIOS = {
    "well-supported personalization",
    "missing supported facts",
    "unclear cta",
    "excessive channel length",
    "manipulative urgency",
    "fake familiarity",
    "guaranteed results",
    "unsupported customer-loss",
    "unsupported revenue claim",
}


def test_sample_outreach_json_exists_and_contains_six_cases() -> None:
    assert SAMPLE_JSON.exists()
    assert SAMPLE_DOC.exists()

    cases = _load_cases()

    assert len(cases) == 6
    assert all(case.keys() >= REQUIRED_CASE_FIELDS for case in cases)
    assert all(case["fictional_business"]["fictional"] is True for case in cases)

    for case in cases:
        fictional_business = case["fictional_business"]
        outreach_input = case["input"]

        assert fictional_business.keys() == FICTIONAL_BUSINESS_FIELDS
        assert outreach_input.keys() == INPUT_FIELDS
        assert case["draft"].keys() == DRAFT_FIELDS
        assert case["evaluation"].keys() == EVALUATION_FIELDS
        assert case["expert_review"].keys() == EXPERT_REVIEW_FIELDS
        assert fictional_business["business_name"] == outreach_input["business_name"]
        assert fictional_business["category"] == outreach_input["category"]
        assert fictional_business["location"] == outreach_input["location"]


def test_sample_set_has_required_channel_and_decision_distribution() -> None:
    cases = _load_cases()
    channels = Counter(case["input"]["channel"] for case in cases)
    decisions = Counter(case["expert_review"]["decision"] for case in cases)

    assert channels == {"short_email": 3, "whatsapp_message": 3}
    assert decisions == {"approve": 2, "revise": 2, "reject": 2}


def test_expert_review_records_follow_decision_rules() -> None:
    for case in _load_cases():
        evaluation = case["evaluation"]
        review = case["expert_review"]

        assert review["automatic_sending_permitted"] is False

        if review["decision"] == "approve":
            assert evaluation["pass_or_review"] == "pass"
            assert evaluation["risk_rating"] in {"low", "medium"}
            assert review["evidence_verified"] is True
            assert review["unresolved_concerns"] == []
            assert review["re_evaluation_required"] is False

        if review["decision"] == "revise":
            assert evaluation["pass_or_review"] == "review"
            assert review["required_revisions"]
            assert review["re_evaluation_required"] is True

        if review["decision"] == "reject":
            assert evaluation["pass_or_review"] == "review"
            evidence_failure = review["evidence_verified"] is False
            assert evaluation["risk_rating"] == "high" or evidence_failure


def test_current_services_reproduce_committed_drafts_and_evaluations() -> None:
    for case in _load_cases():
        draft = create_outreach_draft(OutreachDraftInput(**case["input"]))
        reproduced_draft = _apply_mutation(draft, case.get("draft_mutation"))

        assert reproduced_draft.model_dump(mode="json") == case["draft"]

        evaluation = evaluate_outreach_draft(
            OutreachEvaluationInput(
                draft=reproduced_draft,
                supported_facts=case["supported_facts"],
            ),
        )

        assert evaluation.model_dump(mode="json") == case["evaluation"]


def test_sample_set_documents_required_scenarios() -> None:
    cases = _load_cases()
    documented_text = json.dumps(cases).lower()

    for scenario in REQUIRED_SCENARIOS:
        assert scenario in documented_text


def test_context_index_references_sample_fixture_doc_and_test() -> None:
    document = CONTEXT_INDEX.read_text(encoding="utf-8")

    assert "data/outreach_samples/sample_outreach_cases.json" in document
    assert "docs/SAMPLE_OUTREACH_SET.md" in document
    assert "backend/tests/test_sample_outreach_set.py" in document


def _load_cases() -> list[dict]:
    return json.loads(SAMPLE_JSON.read_text(encoding="utf-8"))


def _apply_mutation(
    draft: OutreachDraftResult,
    mutation: dict | None,
) -> OutreachDraftResult:
    if mutation is None:
        return draft

    draft_data = draft.model_dump(mode="json")
    message_body = draft_data["message_body"]

    for operation in mutation["operations"]:
        if operation["operation"] == "replace_text":
            assert operation["old"] in message_body
            message_body = message_body.replace(
                operation["old"],
                operation["new"],
                1,
            )
        elif operation["operation"] == "append_text":
            message_body += operation["text"]
        elif operation["operation"] == "append_repeated_text":
            message_body += operation["text"] * operation["count"]
        else:
            raise AssertionError(f"Unsupported fixture mutation: {operation}")

    draft_data["message_body"] = message_body
    return OutreachDraftResult(**draft_data)
