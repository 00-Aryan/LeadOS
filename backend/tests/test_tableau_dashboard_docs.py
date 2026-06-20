"""Tableau dashboard documentation and fixture tests."""

import csv
from pathlib import Path

from app.services import BIExportService

REPO_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_DOC = REPO_ROOT / "docs" / "TABLEAU_DASHBOARD.md"
CONTEXT_INDEX = REPO_ROOT / "docs" / "CONTEXT_INDEX.md"
FIXTURE_DIR = REPO_ROOT / "data" / "bi_exports"

REQUIRED_DASHBOARDS = {
    "Executive Lead Overview",
    "Market/Category Opportunity",
    "Digital Gap Prioritization",
    "Outreach Queue",
    "Data Quality Monitor",
}

TABLEAU_WORKBOOK_PATTERNS = ("*.twb", "*.twbx", "*.hyper")


def test_tableau_dashboard_doc_exists_and_references_bi_export_tables(db_session) -> None:
    tables = _dataset_tables(db_session)

    assert DASHBOARD_DOC.exists()
    document = DASHBOARD_DOC.read_text(encoding="utf-8")

    for table_name in tables:
        assert f"`{table_name}`" in document


def test_tableau_dashboard_doc_references_required_dashboards() -> None:
    document = DASHBOARD_DOC.read_text(encoding="utf-8")

    for dashboard_name in REQUIRED_DASHBOARDS:
        assert dashboard_name in document


def test_csv_fixtures_exist_with_non_empty_headers() -> None:
    fixture_paths = sorted(FIXTURE_DIR.glob("*.csv"))

    assert fixture_paths

    for fixture_path in fixture_paths:
        assert _csv_header(fixture_path)


def test_no_tableau_workbook_files_exist_and_doc_defers_manual_creation() -> None:
    for pattern in TABLEAU_WORKBOOK_PATTERNS:
        assert list(REPO_ROOT.rglob(pattern)) == []

    document = DASHBOARD_DOC.read_text(encoding="utf-8").lower()

    assert ".twb" in document
    assert ".twbx" in document
    assert ".hyper" in document
    assert "manual" in document
    assert "deferred" in document


def test_context_index_references_tableau_doc_and_test() -> None:
    document = CONTEXT_INDEX.read_text(encoding="utf-8")

    assert "docs/TABLEAU_DASHBOARD.md" in document
    assert "backend/tests/test_tableau_dashboard_docs.py" in document


def _dataset_tables(db_session):
    dataset = BIExportService().build_reporting_dataset(db_session)
    return {table.name: table for table in dataset.tables}


def _csv_header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        return next(reader, [])
