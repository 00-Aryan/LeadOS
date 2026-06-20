"""BI export service tests."""

import builtins

from sqlalchemy import func, select

from app.models import Lead, LeadAudit, LeadImportError, LeadImportRun, LeadScore
from app.repositories import AuditRepository, LeadRepository, ScoreRepository
from app.services import BIExportService


def test_dataset_contains_all_expected_report_tables(db_session) -> None:
    dataset = BIExportService().build_reporting_dataset(db_session)

    assert dataset.name == "leados_reporting_dataset"
    assert dataset.table_count == 7
    assert [table.name for table in dataset.tables] == [
        "leads_by_city_category",
        "missing_website_leads",
        "high_review_weak_presence_leads",
        "manual_review_leads",
        "score_distribution_by_category",
        "import_quality_summary",
        "missing_data_report",
    ]


def test_table_columns_are_explicit_and_stable(db_session) -> None:
    dataset = BIExportService().build_reporting_dataset(db_session)
    tables = {table.name: table for table in dataset.tables}

    assert [column.name for column in tables["leads_by_city_category"].columns] == [
        "city",
        "category",
        "lead_count",
    ]
    assert [column.name for column in tables["manual_review_leads"].columns] == [
        "lead_id",
        "business_name",
        "city",
        "category",
        "total_score",
        "priority_label",
        "confidence_level",
        "missing_data",
        "risk_flags",
    ]


def test_empty_database_produces_valid_empty_tables_with_headers(db_session) -> None:
    service = BIExportService()
    dataset = service.build_reporting_dataset(db_session)
    missing_website_table = next(
        table for table in dataset.tables if table.name == "missing_website_leads"
    )

    assert all(table.row_count == 0 for table in dataset.tables)
    assert service.to_csv(missing_website_table) == (
        "lead_id,business_name,city,category,website\n"
    )


def test_csv_output_includes_headers_and_sql_backed_rows(db_session) -> None:
    lead_repository = LeadRepository()
    _create_lead(
        lead_repository,
        db_session,
        business_name="Dashboard Clinic",
        category="Clinic",
        normalized_category="clinic",
        city="Jamshedpur",
        normalized_city="jamshedpur",
    )
    db_session.commit()
    service = BIExportService()
    dataset = service.build_reporting_dataset(db_session)
    table = next(table for table in dataset.tables if table.name == "leads_by_city_category")

    assert table.rows == [{"city": "Jamshedpur", "category": "Clinic", "lead_count": 1}]
    assert service.to_csv(table) == "city,category,lead_count\nJamshedpur,Clinic,1\n"


def test_csv_output_handles_none_values() -> None:
    service = BIExportService()
    table = service.build_table_from_rows(
        "custom_table",
        "custom_report",
        [{"name": None, "score": 5}],
    )

    assert service.to_csv(table) == "name,score\n,5\n"


def test_csv_output_serializes_list_and_dict_values_deterministically() -> None:
    service = BIExportService()
    table = service.build_table_from_rows(
        "custom_table",
        "custom_report",
        [{"payload": {"b": 2, "a": 1}, "items": ["z", "a"]}],
    )

    assert table.rows == [{"payload": "{\"a\":1,\"b\":2}", "items": "[\"z\",\"a\"]"}]
    assert service.to_csv(table) == (
        "payload,items\n"
        "\"{\"\"a\"\":1,\"\"b\"\":2}\",\"[\"\"z\"\",\"\"a\"\"]\"\n"
    )


def test_csv_bundle_returns_one_csv_string_per_table(db_session) -> None:
    service = BIExportService()
    dataset = service.build_reporting_dataset(db_session)

    bundle = service.to_csv_bundle(dataset)

    assert set(bundle) == {table.name for table in dataset.tables}
    assert bundle["score_distribution_by_category"].startswith(
        "category,priority_label,lead_count,average_score\n"
    )


def test_service_builds_from_sql_backed_report_repository_outputs(db_session) -> None:
    lead_repository = LeadRepository()
    score_repository = ScoreRepository()
    lead = _create_lead(
        lead_repository,
        db_session,
        business_name="Manual Review Clinic",
        normalized_business_name="manual review clinic",
    )
    score_repository.add_score_result(
        db_session,
        lead_id=lead.id,
        **_score_payload(priority_label="review_needed", confidence_level="medium"),
    )
    db_session.commit()

    dataset = BIExportService().build_reporting_dataset(db_session)
    table = next(table for table in dataset.tables if table.name == "manual_review_leads")

    assert table.row_count == 1
    assert table.rows[0]["business_name"] == "Manual Review Clinic"
    assert table.rows[0]["priority_label"] == "review_needed"


def test_service_does_not_write_files_or_mutate_database_state(db_session, monkeypatch) -> None:
    lead_repository = LeadRepository()
    lead = _create_lead(lead_repository, db_session, business_name="Read Only BI Clinic")
    lead_repository.create_import_run(
        db_session,
        source_name="sample.csv",
        total_records=1,
        valid_records=1,
        invalid_records=0,
        duplicate_records=0,
    )
    ScoreRepository().add_score_result(db_session, lead_id=lead.id, **_score_payload())
    AuditRepository().add_audit_result(
        db_session,
        lead_id=lead.id,
        requested_url="https://example.com",
        fetch_status="success",
        result_json={
            "website_url": "https://example.com",
            "fetch_status": None,
            "checks": [{"key": "title", "status": "false"}],
        },
    )
    db_session.commit()
    before_counts = _table_counts(db_session)

    def fail_open(*args, **kwargs):
        raise AssertionError("BI export service must not write files")

    monkeypatch.setattr(builtins, "open", fail_open)
    service = BIExportService()
    dataset = service.build_reporting_dataset(db_session)
    service.to_csv_bundle(dataset)

    assert _table_counts(db_session) == before_counts
    assert not db_session.new
    assert not db_session.dirty
    assert not db_session.deleted


def _create_lead(
    repository: LeadRepository,
    db_session,
    *,
    business_name: str,
    normalized_business_name: str | None = None,
    category: str = "Dentist",
    normalized_category: str = "dentist",
    city: str = "Ranchi",
    normalized_city: str = "ranchi",
    website: str | None = "https://example.com",
):
    return repository.add_lead(
        db_session,
        business_name=business_name,
        normalized_business_name=normalized_business_name or business_name.lower(),
        category=category,
        normalized_category=normalized_category,
        city=city,
        normalized_city=normalized_city,
        state="Jharkhand",
        phone="+91-9876543210",
        website=website,
        rating=4.6,
        review_count=150,
        address="Main Road",
    )


def _score_payload(
    *,
    total_score: float = 50,
    priority_label: str = "medium",
    confidence_level: str = "medium",
) -> dict:
    return {
        "scoring_version": "v1",
        "total_score": total_score,
        "category_scores": {
            "business_strength": 15,
            "digital_gap": 20,
            "contactability": 8,
            "commercial_fit": 10,
            "outreach_priority": 5,
        },
        "priority_label": priority_label,
        "confidence_level": confidence_level,
        "reason_summary": "Persisted test score.",
        "positive_signals": ["Strong reviews"],
        "risk_flags": [],
        "missing_data": [],
    }


def _table_counts(db_session) -> dict[str, int]:
    models = [Lead, LeadAudit, LeadImportError, LeadImportRun, LeadScore]
    return {
        model.__tablename__: db_session.execute(select(func.count(model.id))).scalar_one()
        for model in models
    }
