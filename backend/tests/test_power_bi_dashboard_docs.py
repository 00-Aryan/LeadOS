"""Power BI dashboard documentation and fixture tests."""

import csv
from pathlib import Path

from app.services import BIExportService

REPO_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_DOC = REPO_ROOT / "docs" / "POWER_BI_DASHBOARD.md"
FIXTURE_DIR = REPO_ROOT / "data" / "bi_exports"


def test_dashboard_doc_exists_and_references_bi_export_tables(db_session) -> None:
    tables = _dataset_tables(db_session)

    assert DASHBOARD_DOC.exists()
    document = DASHBOARD_DOC.read_text(encoding="utf-8")

    for table_name in tables:
        assert f"`{table_name}`" in document


def test_csv_fixtures_match_bi_export_table_names_and_headers(db_session) -> None:
    tables = _dataset_tables(db_session)
    fixture_paths = sorted(FIXTURE_DIR.glob("*.csv"))

    assert {path.stem for path in fixture_paths} == set(tables)

    for fixture_path in fixture_paths:
        header = _csv_header(fixture_path)

        assert header
        assert header == [column.name for column in tables[fixture_path.stem].columns]


def test_no_power_bi_binary_exists_and_doc_defers_pbix_creation() -> None:
    assert list(REPO_ROOT.rglob("*.pbix")) == []

    document = DASHBOARD_DOC.read_text(encoding="utf-8").lower()

    assert ".pbix" in document
    assert "manual" in document
    assert "deferred" in document


def _dataset_tables(db_session):
    dataset = BIExportService().build_reporting_dataset(db_session)
    return {table.name: table for table in dataset.tables}


def _csv_header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        return next(reader, [])
