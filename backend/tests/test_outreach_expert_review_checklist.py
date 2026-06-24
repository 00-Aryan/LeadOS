"""File-based tests for the outreach expert review checklist."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLIST_DOC = REPO_ROOT / "docs" / "OUTREACH_EXPERT_REVIEW_CHECKLIST.md"
CONTEXT_INDEX = REPO_ROOT / "docs" / "CONTEXT_INDEX.md"


def test_outreach_expert_review_checklist_exists() -> None:
    assert CHECKLIST_DOC.exists()


def test_checklist_contains_decisions_channels_and_thresholds() -> None:
    document = CHECKLIST_DOC.read_text(encoding="utf-8").lower()

    for decision in ("approve", "revise", "reject"):
        assert decision in document

    for channel in ("short_email", "whatsapp_message"):
        assert channel in document

    assert "45 out of 60" in document
    assert "truthfulness score is at least **8 out of 10**" in document
    assert "cta quality score is at least **7 out of 10**" in document


def test_checklist_contains_required_review_controls() -> None:
    document = CHECKLIST_DOC.read_text(encoding="utf-8").lower()

    required_controls = (
        "evidence verification",
        "unsupported claims",
        "fake familiarity",
        "manipulative pressure",
        "manual review",
        "re-evaluation after revision",
        "no automatic sending",
    )

    for control in required_controls:
        assert control in document


def test_checklist_references_required_evaluator_output() -> None:
    document = CHECKLIST_DOC.read_text(encoding="utf-8").lower()

    evaluator_fields = (
        "score breakdown",
        "total score",
        "risk rating",
        "failure reasons",
        "bad lines",
        "suggested revision",
    )

    for field in evaluator_fields:
        assert field in document


def test_context_index_references_checklist_and_test() -> None:
    document = CONTEXT_INDEX.read_text(encoding="utf-8")

    assert "docs/OUTREACH_EXPERT_REVIEW_CHECKLIST.md" in document
    assert "backend/tests/test_outreach_expert_review_checklist.py" in document
