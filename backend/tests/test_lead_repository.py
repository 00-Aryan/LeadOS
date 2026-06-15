"""Lead repository tests."""

from app.repositories import LeadRepository


def test_repository_adds_and_finds_duplicate(db_session) -> None:
    repository = LeadRepository()
    lead = repository.add_lead(
        db_session,
        business_name="Healthy Smile Clinic",
        normalized_business_name="healthy smile clinic",
        category="Dentist",
        normalized_category="dentist",
        city="Ranchi",
        normalized_city="ranchi",
    )
    db_session.commit()

    duplicate = repository.find_duplicate(db_session, "healthy smile clinic", "ranchi")

    assert lead.id is not None
    assert duplicate is not None
    assert duplicate.id == lead.id
