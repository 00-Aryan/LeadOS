"""Audit repository tests."""

from app.repositories import AuditRepository, LeadRepository
from app.services.audit_service import audit_website_presence


def test_repository_stores_audit_linked_to_valid_lead(db_session) -> None:
    lead_repository = LeadRepository()
    audit_repository = AuditRepository()
    lead = _create_lead(
        lead_repository,
        db_session,
        business_name="Healthy Smile Clinic",
        normalized_business_name="healthy smile clinic",
        city="Ranchi",
        normalized_city="ranchi",
    )
    audit_result = audit_website_presence(
        "https://example.com",
        """
        <html>
          <head>
            <title>Healthy Smile Clinic</title>
            <meta name="description" content="Family dental care">
          </head>
          <body><a href="tel:5551234567">Call</a></body>
        </html>
        """,
    )

    created = audit_repository.add_audit_result(
        db_session,
        lead_id=lead.id,
        requested_url="https://example.com",
        fetch_status="success",
        result_json=audit_result.model_dump(mode="json"),
    )
    db_session.commit()

    assert created.id is not None
    assert created.lead_id == lead.id
    assert created.requested_url == "https://example.com"
    assert created.fetch_status == "success"
    assert created.result_json["website_url"] == "https://example.com"
    assert created.result_json["fetch_status"] is None
    assert created.result_json["checks"][0]["key"] == "https"
    assert created.result_json["checks"][0]["status"] == "true"


def test_repository_lists_only_audits_for_requested_lead(db_session) -> None:
    lead_repository = LeadRepository()
    audit_repository = AuditRepository()
    first_lead = _create_lead(
        lead_repository,
        db_session,
        business_name="Healthy Smile Clinic",
        normalized_business_name="healthy smile clinic",
        city="Ranchi",
        normalized_city="ranchi",
    )
    second_lead = _create_lead(
        lead_repository,
        db_session,
        business_name="Care Clinic",
        normalized_business_name="care clinic",
        city="Patna",
        normalized_city="patna",
    )
    first_result = audit_website_presence(
        "https://first.example",
        "<html><head><title>First</title></head><body></body></html>",
    ).model_dump(mode="json")
    second_result = audit_website_presence(
        "https://second.example",
        "<html><head><title>Second</title></head><body></body></html>",
    ).model_dump(mode="json")

    first_audit = audit_repository.add_audit_result(
        db_session,
        lead_id=first_lead.id,
        requested_url="https://first.example",
        fetch_status="success",
        result_json=first_result,
    )
    audit_repository.add_audit_result(
        db_session,
        lead_id=second_lead.id,
        requested_url="https://second.example",
        fetch_status="success",
        result_json=second_result,
    )
    db_session.commit()

    audits = audit_repository.list_by_lead_id(db_session, first_lead.id)

    assert [audit.id for audit in audits] == [first_audit.id]
    assert audits[0].requested_url == "https://first.example"


def test_repository_returns_latest_audit_for_lead(db_session) -> None:
    lead_repository = LeadRepository()
    audit_repository = AuditRepository()
    lead = _create_lead(
        lead_repository,
        db_session,
        business_name="Healthy Smile Clinic",
        normalized_business_name="healthy smile clinic",
        city="Ranchi",
        normalized_city="ranchi",
    )

    older = audit_repository.add_audit_result(
        db_session,
        lead_id=lead.id,
        requested_url="http://example.com",
        fetch_status="success",
        result_json=audit_website_presence(
            "http://example.com",
            "<html><head><title>Old</title></head><body></body></html>",
        ).model_dump(mode="json"),
    )
    newer = audit_repository.add_audit_result(
        db_session,
        lead_id=lead.id,
        requested_url="https://example.com",
        fetch_status="failed",
        result_json=audit_website_presence(
            "https://example.com",
            None,
            fetch_status="failed",
        ).model_dump(mode="json"),
    )
    db_session.commit()

    audits = audit_repository.list_by_lead_id(db_session, lead.id)
    latest = audit_repository.get_latest_by_lead_id(db_session, lead.id)

    assert [audit.id for audit in audits] == [older.id, newer.id]
    assert latest is not None
    assert latest.id == newer.id
    assert latest.fetch_status == "failed"
    assert latest.result_json["checks"][1]["status"] == "unknown"


def test_repository_returns_none_when_lead_has_no_audits(db_session) -> None:
    audit_repository = AuditRepository()

    assert audit_repository.list_by_lead_id(db_session, 999) == []
    assert audit_repository.get_latest_by_lead_id(db_session, 999) is None


def _create_lead(
    repository: LeadRepository,
    db_session,
    *,
    business_name: str,
    normalized_business_name: str,
    city: str,
    normalized_city: str,
):
    return repository.add_lead(
        db_session,
        business_name=business_name,
        normalized_business_name=normalized_business_name,
        category="Dentist",
        normalized_category="dentist",
        city=city,
        normalized_city=normalized_city,
        website="https://example.com",
    )
