"""Lead import service tests."""

from app.models import LeadImportError, LeadImportRun
from app.services.lead_import_service import LeadImportService


def test_import_csv_persists_valid_rows_and_run_summary(db_session) -> None:
    csv_content = (
        "business_name,category,city,state,phone,website,rating,review_count,address,source_url\n"
        "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91 98765 43210,https://example.com,4.6,150,Main Road,source\n"
    )

    summary = LeadImportService().import_csv_text(db_session, csv_content, source_name="test.csv")

    assert summary.total_records == 1
    assert summary.valid_records == 1
    assert summary.invalid_records == 0
    assert summary.duplicate_records == 0
    assert len(summary.imported_ids) == 1
    assert summary.import_run_id is not None
    run = db_session.get(LeadImportRun, summary.import_run_id)
    assert run is not None
    assert run.source_name == "test.csv"


def test_import_csv_rejects_invalid_rows_and_persists_errors(db_session) -> None:
    csv_content = (
        "business_name,category,city,state,phone,website,rating,review_count,address,source_url\n"
        ",Dentist,Ranchi,Jharkhand,+91,example.com,bad,-1,Main Road,source\n"
    )

    summary = LeadImportService().import_csv_text(db_session, csv_content)

    assert summary.valid_records == 0
    assert summary.invalid_records == 1
    assert summary.errors[0].row_number == 2
    assert "business_name is required" in summary.errors[0].reasons
    assert db_session.query(LeadImportError).count() == 1


def test_import_csv_detects_duplicates_with_normalized_keys(db_session) -> None:
    csv_content = (
        "business_name,category,city,state,phone,website,rating,review_count,address,source_url\n"
        "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91,https://example.com,4.6,150,Main Road,source\n"
        " healthy  smile clinic ,Dentist,RANCHI,Jharkhand,+91,https://example.com,4.6,150,Main Road,source\n"
    )

    summary = LeadImportService().import_csv_text(db_session, csv_content)

    assert summary.valid_records == 1
    assert summary.duplicate_records == 1
