"""File-based tests for the Phase 0 completion report."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPLETION_REPORT = REPO_ROOT / "docs" / "PHASE_0_COMPLETION_REPORT.md"
CONTEXT_INDEX = REPO_ROOT / "docs" / "CONTEXT_INDEX.md"

REQUIRED_MVP_CRITERIA = (
    "CSV-based lead import",
    "Lead validation",
    "Basic persistence model",
    "Deterministic website audit checks",
    "Explainable lead scoring",
    "Outreach draft structure",
    "Outreach evaluation and risk guardrails",
    "Backend service boundaries",
    "Reviewed sample outreach workflow",
)

CORE_WORKFLOW_STAGES = (
    "CSV import",
    "validation",
    "persistence",
    "deterministic audit",
    "explainable score",
    "outreach draft",
    "deterministic evaluation",
    "expert review",
    "reviewed sample output",
)

DEFERRED_ITEMS = (
    "migrations",
    "authentication",
    "billing",
    "production deployment",
    "CRM integration",
    "scraping",
)


def test_phase_0_completion_report_exists_and_references_verified_baseline() -> None:
    assert COMPLETION_REPORT.exists()

    document = COMPLETION_REPORT.read_text(encoding="utf-8")

    assert "7012d052e37e12b458420e38e03f80e011faf1b2" in document
    assert "#108" in document


def test_report_contains_required_mvp_criteria_and_workflow_stages() -> None:
    document = COMPLETION_REPORT.read_text(encoding="utf-8").lower()

    for criterion in REQUIRED_MVP_CRITERIA:
        assert criterion.lower() in document

    for stage in CORE_WORKFLOW_STAGES:
        assert stage.lower() in document


def test_report_contains_statuses_and_merge_readiness_decision() -> None:
    document = COMPLETION_REPORT.read_text(encoding="utf-8")

    for status in ("Pass", "Partial", "Fail"):
        assert status in document

    assert "Merge-readiness decision" in document
    assert "ready for final human review" in document


def test_report_preserves_deferred_scope_and_manual_merge_review() -> None:
    document = COMPLETION_REPORT.read_text(encoding="utf-8").lower()

    assert "automatic outbound sending" in document
    assert "deferred" in document

    for item in DEFERRED_ITEMS:
        assert item.lower() in document

    assert "review the final pr diff" in document
    assert "merge manually only after final review" in document


def test_report_contains_final_sign_off_block() -> None:
    document = COMPLETION_REPORT.read_text(encoding="utf-8")

    sign_off_fields = (
        "Phase 0 status:",
        "Verified commit:",
        "Verified CI:",
        "Critical blockers:",
        "Deferred items acknowledged:",
        "Final human reviewer:",
        "Review date:",
        "Merge approved:",
    )

    for field in sign_off_fields:
        assert field in document


def test_context_index_references_completion_report_and_test() -> None:
    document = CONTEXT_INDEX.read_text(encoding="utf-8")

    assert "docs/PHASE_0_COMPLETION_REPORT.md" in document
    assert "backend/tests/test_phase_0_completion_docs.py" in document
