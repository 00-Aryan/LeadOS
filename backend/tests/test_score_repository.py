"""Score repository tests."""

from app.repositories import LeadRepository, ScoreRepository
from app.schemas.lead import LeadInput
from app.services.audit_service import audit_website_presence
from app.services.scoring_service import score_lead


def test_repository_stores_score_linked_to_valid_lead(db_session) -> None:
    lead_repository = LeadRepository()
    score_repository = ScoreRepository()
    lead = _create_lead(
        lead_repository,
        db_session,
        business_name="Healthy Smile Clinic",
        normalized_business_name="healthy smile clinic",
        city="Ranchi",
        normalized_city="ranchi",
    )
    score_result = score_lead(_lead_input(), _presence_audit())
    score_payload = score_result.model_dump(mode="json")

    created = score_repository.add_score_result(
        db_session,
        lead_id=lead.id,
        scoring_version="v1",
        **score_payload,
    )
    db_session.commit()

    assert created.id is not None
    assert created.lead_id == lead.id
    assert created.scoring_version == "v1"
    assert created.total_score == score_payload["total_score"]
    assert created.category_scores == score_payload["category_scores"]
    assert created.priority_label == score_payload["priority_label"]
    assert created.confidence_level == score_payload["confidence_level"]
    assert created.reason_summary == score_payload["reason_summary"]
    assert created.positive_signals == score_payload["positive_signals"]
    assert created.risk_flags == score_payload["risk_flags"]
    assert created.missing_data == score_payload["missing_data"]


def test_repository_lists_only_scores_for_requested_lead(db_session) -> None:
    lead_repository = LeadRepository()
    score_repository = ScoreRepository()
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

    first_score = score_repository.add_score_result(
        db_session,
        lead_id=first_lead.id,
        scoring_version="v1",
        **score_lead(_lead_input(), _presence_audit()).model_dump(mode="json"),
    )
    score_repository.add_score_result(
        db_session,
        lead_id=second_lead.id,
        scoring_version="v1",
        **score_lead(_lead_input(business_name="Care Clinic", city="Patna"), None).model_dump(
            mode="json"
        ),
    )
    db_session.commit()

    scores = score_repository.list_by_lead_id(db_session, first_lead.id)

    assert [score.id for score in scores] == [first_score.id]
    assert scores[0].lead_id == first_lead.id


def test_repository_returns_latest_score_for_lead(db_session) -> None:
    lead_repository = LeadRepository()
    score_repository = ScoreRepository()
    lead = _create_lead(
        lead_repository,
        db_session,
        business_name="Healthy Smile Clinic",
        normalized_business_name="healthy smile clinic",
        city="Ranchi",
        normalized_city="ranchi",
    )

    older = score_repository.add_score_result(
        db_session,
        lead_id=lead.id,
        scoring_version="v1",
        **score_lead(_lead_input(), None).model_dump(mode="json"),
    )
    newer = score_repository.add_score_result(
        db_session,
        lead_id=lead.id,
        scoring_version="v2",
        **score_lead(_lead_input(), _presence_audit()).model_dump(mode="json"),
    )
    db_session.commit()

    scores = score_repository.list_by_lead_id(db_session, lead.id)
    latest = score_repository.get_latest_by_lead_id(db_session, lead.id)

    assert [score.id for score in scores] == [older.id, newer.id]
    assert latest is not None
    assert latest.id == newer.id
    assert latest.scoring_version == "v2"


def test_repository_returns_empty_results_when_lead_has_no_scores(db_session) -> None:
    score_repository = ScoreRepository()

    assert score_repository.list_by_lead_id(db_session, 999) == []
    assert score_repository.get_latest_by_lead_id(db_session, 999) is None


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
        state="Jharkhand",
        phone="+91-9876543210",
        website="https://example.com",
        rating=4.6,
        review_count=150,
        address="Main Road",
    )


def _lead_input(business_name: str = "Healthy Smile Clinic", city: str = "Ranchi") -> LeadInput:
    return LeadInput(
        business_name=business_name,
        category="Dentist",
        city=city,
        state="Jharkhand",
        phone="+91-9876543210",
        website="https://example.com",
        rating=4.6,
        review_count=150,
        address="Main Road",
    )


def _presence_audit():
    return audit_website_presence(
        "https://example.com",
        """
        <html>
          <head><title>Healthy Smile Clinic</title></head>
          <body>No contact links or social proof here.</body>
        </html>
        """,
    )
