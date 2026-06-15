"""Lead import service tests."""

from io import BytesIO

from app.models import LeadImportError, LeadImportRun
from app.services.lead_import_service import LeadImportService

CSV_HEADER = (
    "business_name,category,city,state,phone,website,rating,review_count,"
    "address,source_url\n"
)
VALID_ROW = (
    " Healthy  Smile Clinic , Dentist , Ranchi , Jharkhand , +91 98765 43210 ,"
    "https://Example.com,4.6,150, Main Road , source \n"
)


def test_import_csv_persists_valid_rows_and_run_summary(db_session) -> None:
    result = LeadImportService().import_csv_text(
        db_session,
        CSV_HEADER + VALID_ROW,
        source_name="test.csv",
    )

    assert result.summary.total_rows == 1
    assert result.summary.valid_rows == 1
    assert result.summary.invalid_rows == 0
    assert result.summary.duplicate_rows == 0
    assert len(result.imported_ids) == 1
    assert result.import_run_id is not None
    assert result.valid_rows[0].business_name == "Healthy Smile Clinic"
    assert result.valid_rows[0].category == "Dentist"
    assert result.valid_rows[0].city == "Ranchi"
    assert result.valid_rows[0].phone == "+919876543210"
    assert result.valid_rows[0].website == "https://Example.com"
    assert result.valid_rows[0].rating == 4.6
    assert result.valid_rows[0].review_count == 150

    run = db_session.get(LeadImportRun, result.import_run_id)
    assert run is not None
    assert run.source_name == "test.csv"


def test_import_csv_rejects_invalid_rows_and_persists_errors(db_session) -> None:
    csv_content = (
        CSV_HEADER
        + ",Dentist,Ranchi,Jharkhand,+91,example.com,bad,-1,Main Road,source\n"
    )

    result = LeadImportService().import_csv_text(db_session, csv_content)

    assert result.summary.valid_rows == 0
    assert result.summary.invalid_rows == 1
    assert result.invalid_rows[0].row_number == 2
    assert "business_name is required" in result.invalid_rows[0].reasons
    assert "website must start with http:// or https://" in result.invalid_rows[0].reasons
    assert "rating must be numeric" in result.invalid_rows[0].reasons
    assert "review_count cannot be negative" in result.invalid_rows[0].reasons
    assert db_session.query(LeadImportError).count() == 1


def test_import_csv_supports_partial_import(db_session) -> None:
    csv_content = (
        CSV_HEADER
        + "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91,https://example.com,"
        "4.6,150,Main Road,source\n"
        "Broken Clinic,Dentist,Ranchi,Jharkhand,+91,example.com,4.2,20,"
        "Main Road,source\n"
    )

    result = LeadImportService().import_csv_text(db_session, csv_content)

    assert result.summary.total_rows == 2
    assert result.summary.valid_rows == 1
    assert result.summary.invalid_rows == 1
    assert result.valid_rows[0].business_name == "Healthy Smile Clinic"
    assert result.invalid_rows[0].row_number == 3


def test_import_csv_rejects_missing_required_field_header(db_session) -> None:
    result = LeadImportService().import_csv_text(
        db_session,
        "business_name,category,rating\nHealthy Smile Clinic,Dentist,4.6\n",
    )

    assert result.summary.total_rows == 0
    assert result.summary.valid_rows == 0
    assert result.summary.invalid_rows == 1
    assert result.invalid_rows[0].row_number == 1
    assert result.invalid_rows[0].reasons == ["CSV header missing required field: city"]


def test_import_csv_rejects_blank_required_field(db_session) -> None:
    result = LeadImportService().import_csv_text(
        db_session,
        CSV_HEADER + "Healthy Smile Clinic,Dentist,  ,Jharkhand,+91,https://example.com,"
        "4.6,150,Main Road,source\n",
    )

    assert result.summary.invalid_rows == 1
    assert "city is required" in result.invalid_rows[0].reasons


def test_import_csv_rejects_invalid_url(db_session) -> None:
    result = LeadImportService().import_csv_text(
        db_session,
        CSV_HEADER + "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91,example.com,"
        "4.6,150,Main Road,source\n",
    )

    assert result.summary.invalid_rows == 1
    assert "website must start with http:// or https://" in result.invalid_rows[0].reasons


def test_import_csv_rejects_invalid_rating(db_session) -> None:
    result = LeadImportService().import_csv_text(
        db_session,
        CSV_HEADER + "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91,"
        "https://example.com,not-a-rating,150,Main Road,source\n",
    )

    assert result.summary.invalid_rows == 1
    assert "rating must be numeric" in result.invalid_rows[0].reasons


def test_import_csv_rejects_rating_outside_range(db_session) -> None:
    result = LeadImportService().import_csv_text(
        db_session,
        CSV_HEADER + "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91,"
        "https://example.com,5.5,150,Main Road,source\n",
    )

    assert result.summary.invalid_rows == 1
    assert "rating must be between 0 and 5" in result.invalid_rows[0].reasons


def test_import_csv_rejects_invalid_review_count(db_session) -> None:
    result = LeadImportService().import_csv_text(
        db_session,
        CSV_HEADER + "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91,"
        "https://example.com,4.6,many,Main Road,source\n",
    )

    assert result.summary.invalid_rows == 1
    assert "review_count must be an integer" in result.invalid_rows[0].reasons


def test_import_csv_rejects_negative_review_count(db_session) -> None:
    result = LeadImportService().import_csv_text(
        db_session,
        CSV_HEADER + "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91,"
        "https://example.com,4.6,-1,Main Road,source\n",
    )

    assert result.summary.invalid_rows == 1
    assert "review_count cannot be negative" in result.invalid_rows[0].reasons


def test_import_csv_handles_empty_csv_without_crash(db_session) -> None:
    result = LeadImportService().import_csv_text(db_session, "")

    assert result.summary.total_rows == 0
    assert result.summary.valid_rows == 0
    assert result.summary.invalid_rows == 0
    assert result.valid_rows == []
    assert result.invalid_rows == []


def test_import_csv_handles_header_only_csv_without_crash(db_session) -> None:
    result = LeadImportService().import_csv_text(db_session, CSV_HEADER)

    assert result.summary.total_rows == 0
    assert result.summary.valid_rows == 0
    assert result.summary.invalid_rows == 0
    assert result.valid_rows == []
    assert result.invalid_rows == []


def test_import_csv_detects_duplicates_with_normalized_keys(db_session) -> None:
    csv_content = (
        CSV_HEADER
        + "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91,https://example.com,"
        "4.6,150,Main Road,source\n"
        " healthy  smile clinic ,Dentist,RANCHI,Jharkhand,+91,"
        "https://example.com,4.6,150,Main Road,source\n"
    )

    result = LeadImportService().import_csv_text(db_session, csv_content)

    assert result.summary.valid_rows == 1
    assert result.summary.duplicate_rows == 1
    assert len(result.valid_rows) == 1


def test_import_csv_ignores_unknown_optional_fields(db_session) -> None:
    result = LeadImportService().import_csv_text(
        db_session,
        CSV_HEADER.removesuffix("\n") + ",unknown_field\n" + VALID_ROW.rstrip("\n") + ",ignored\n",
    )

    assert result.summary.valid_rows == 1
    assert result.summary.invalid_rows == 0


def test_import_csv_accepts_bytes_file_like_content(db_session) -> None:
    result = LeadImportService().import_csv_content(
        db_session,
        BytesIO((CSV_HEADER + VALID_ROW).encode()),
    )

    assert result.summary.valid_rows == 1
    assert result.valid_rows[0].business_name == "Healthy Smile Clinic"
