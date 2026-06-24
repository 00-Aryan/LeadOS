"""Report repository tests."""

from sqlalchemy import func, select

from app.models import Lead, LeadAudit, LeadImportError, LeadImportRun, LeadScore
from app.repositories import AuditRepository, LeadRepository, ReportRepository, ScoreRepository


def test_reports_leads_grouped_by_city_and_category(db_session) -> None:
    repository = ReportRepository()
    lead_repository = LeadRepository()
    _create_lead(lead_repository, db_session, business_name="A Clinic", city="Ranchi")
    _create_lead(lead_repository, db_session, business_name="B Clinic", city="Ranchi")
    _create_lead(
        lead_repository,
        db_session,
        business_name="C Salon",
        category="Salon",
        normalized_category="salon",
        city="Patna",
        normalized_city="patna",
    )
    db_session.commit()

    rows = repository.leads_by_city_and_category(db_session)

    assert [(row.city, row.category, row.lead_count) for row in rows] == [
        ("Patna", "Salon", 1),
        ("Ranchi", "Dentist", 2),
    ]


def test_reports_missing_website_leads(db_session) -> None:
    repository = ReportRepository()
    lead_repository = LeadRepository()
    missing = _create_lead(
        lead_repository,
        db_session,
        business_name="No Site Clinic",
        website=None,
    )
    blank = _create_lead(
        lead_repository,
        db_session,
        business_name="Blank Site Clinic",
        normalized_business_name="blank site clinic",
        website="  ",
    )
    _create_lead(
        lead_repository,
        db_session,
        business_name="Site Clinic",
        normalized_business_name="site clinic",
        website="https://example.com",
    )
    db_session.commit()

    rows = repository.leads_missing_website(db_session)

    assert [row.lead_id for row in rows] == [blank.id, missing.id]
    assert {row.business_name for row in rows} == {"Blank Site Clinic", "No Site Clinic"}


def test_reports_high_review_weak_presence_from_persisted_audit_and_score(db_session) -> None:
    repository = ReportRepository()
    lead_repository = LeadRepository()
    audit_repository = AuditRepository()
    score_repository = ScoreRepository()
    weak = _create_lead(
        lead_repository,
        db_session,
        business_name="Busy Weak Clinic",
        review_count=210,
    )
    strong = _create_lead(
        lead_repository,
        db_session,
        business_name="Busy Strong Clinic",
        normalized_business_name="busy strong clinic",
        review_count=220,
    )
    low_review = _create_lead(
        lead_repository,
        db_session,
        business_name="Quiet Weak Clinic",
        normalized_business_name="quiet weak clinic",
        review_count=40,
    )
    audit_repository.add_audit_result(
        db_session,
        lead_id=weak.id,
        requested_url="https://weak.example",
        fetch_status="success",
        result_json=_audit_result(("title", "false"), ("phone_link", "false")),
    )
    score_repository.add_score_result(
        db_session,
        lead_id=weak.id,
        **_score_payload(
            total_score=82,
            priority_label="high",
            risk_flags=["Weak digital presence"],
            missing_data=["phone link missing"],
        ),
    )
    audit_repository.add_audit_result(
        db_session,
        lead_id=strong.id,
        requested_url="https://strong.example",
        fetch_status="success",
        result_json=_audit_result(("title", "true"), ("phone_link", "true")),
    )
    audit_repository.add_audit_result(
        db_session,
        lead_id=low_review.id,
        requested_url="https://quiet.example",
        fetch_status="success",
        result_json=_audit_result(("title", "false")),
    )
    db_session.commit()

    rows = repository.high_review_weak_presence_leads(db_session, min_review_count=100)

    assert [row.lead_id for row in rows] == [weak.id]
    assert rows[0].review_count == 210
    assert "audit title is false" in rows[0].weak_signals
    assert "Weak digital presence" in rows[0].weak_signals


def test_reports_manual_review_leads_from_persisted_scores(db_session) -> None:
    repository = ReportRepository()
    lead_repository = LeadRepository()
    score_repository = ScoreRepository()
    review_needed = _create_lead(
        lead_repository,
        db_session,
        business_name="Review Needed Clinic",
    )
    low_confidence = _create_lead(
        lead_repository,
        db_session,
        business_name="Low Confidence Clinic",
        normalized_business_name="low confidence clinic",
    )
    healthy = _create_lead(
        lead_repository,
        db_session,
        business_name="Healthy Clinic",
        normalized_business_name="healthy clinic",
    )
    score_repository.add_score_result(
        db_session,
        lead_id=review_needed.id,
        **_score_payload(priority_label="review_needed", confidence_level="medium"),
    )
    score_repository.add_score_result(
        db_session,
        lead_id=low_confidence.id,
        **_score_payload(priority_label="medium", confidence_level="low"),
    )
    score_repository.add_score_result(
        db_session,
        lead_id=healthy.id,
        **_score_payload(priority_label="medium", confidence_level="medium"),
    )
    db_session.commit()

    rows = repository.manual_review_leads(db_session)

    assert [row.lead_id for row in rows] == [low_confidence.id, review_needed.id]
    assert {row.priority_label for row in rows} == {"medium", "review_needed"}
    assert rows[0].confidence_level == "low"


def test_reports_score_distribution_by_category(db_session) -> None:
    repository = ReportRepository()
    lead_repository = LeadRepository()
    score_repository = ScoreRepository()
    dentist = _create_lead(lead_repository, db_session, business_name="Dentist One")
    another_dentist = _create_lead(
        lead_repository,
        db_session,
        business_name="Dentist Two",
        normalized_business_name="dentist two",
    )
    salon = _create_lead(
        lead_repository,
        db_session,
        business_name="Salon One",
        normalized_business_name="salon one",
        category="Salon",
        normalized_category="salon",
    )
    score_repository.add_score_result(
        db_session,
        lead_id=dentist.id,
        **_score_payload(total_score=80, priority_label="high"),
    )
    score_repository.add_score_result(
        db_session,
        lead_id=another_dentist.id,
        **_score_payload(total_score=60, priority_label="high"),
    )
    score_repository.add_score_result(
        db_session,
        lead_id=salon.id,
        **_score_payload(total_score=35, priority_label="low"),
    )
    db_session.commit()

    rows = repository.score_distribution_by_category(db_session)

    assert [(row.category, row.priority_label, row.lead_count) for row in rows] == [
        ("Dentist", "high", 2),
        ("Salon", "low", 1),
    ]
    assert rows[0].average_score == 70.0


def test_reports_import_quality_summary(db_session) -> None:
    repository = ReportRepository()
    lead_repository = LeadRepository()
    import_run = lead_repository.create_import_run(
        db_session,
        source_name="sample.csv",
        total_records=5,
        valid_records=3,
        invalid_records=1,
        duplicate_records=1,
    )
    lead_repository.add_import_error(
        db_session,
        import_run_id=import_run.id,
        row_number=4,
        reasons=["missing business_name"],
        raw_row={"business_name": ""},
    )
    db_session.commit()

    rows = repository.import_quality_summary(db_session)

    assert len(rows) == 1
    assert rows[0].import_run_id == import_run.id
    assert rows[0].source_name == "sample.csv"
    assert rows[0].total_records == 5
    assert rows[0].valid_records == 3
    assert rows[0].invalid_records == 1
    assert rows[0].duplicate_records == 1
    assert rows[0].error_count == 1


def test_reports_missing_data_from_leads_and_persisted_scores(db_session) -> None:
    repository = ReportRepository()
    lead_repository = LeadRepository()
    score_repository = ScoreRepository()
    lead = _create_lead(
        lead_repository,
        db_session,
        business_name="Sparse Clinic",
        website=None,
        phone=None,
        rating=None,
        review_count=None,
        address=None,
    )
    complete = _create_lead(
        lead_repository,
        db_session,
        business_name="Complete Clinic",
        normalized_business_name="complete clinic",
    )
    score_repository.add_score_result(
        db_session,
        lead_id=lead.id,
        **_score_payload(missing_data=["website missing", "phone missing"]),
    )
    score_repository.add_score_result(
        db_session,
        lead_id=complete.id,
        **_score_payload(missing_data=[]),
    )
    db_session.commit()

    rows = repository.missing_data_report(db_session)

    assert [row.lead_id for row in rows] == [lead.id]
    assert rows[0].missing_fields == ["phone", "website", "rating", "review_count", "address"]
    assert rows[0].score_missing_data == ["website missing", "phone missing"]


def test_report_methods_are_read_only_in_behavior(db_session) -> None:
    repository = ReportRepository()
    lead_repository = LeadRepository()
    lead = _create_lead(lead_repository, db_session, business_name="Read Only Clinic")
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
        result_json=_audit_result(("title", "false")),
    )
    db_session.commit()
    before_counts = _table_counts(db_session)

    repository.leads_by_city_and_category(db_session)
    repository.leads_missing_website(db_session)
    repository.high_review_weak_presence_leads(db_session)
    repository.manual_review_leads(db_session)
    repository.score_distribution_by_category(db_session)
    repository.import_quality_summary(db_session)
    repository.missing_data_report(db_session)

    assert _table_counts(db_session) == before_counts
    assert not db_session.new
    assert not db_session.dirty
    assert not db_session.deleted


def test_empty_database_returns_empty_report_lists(db_session) -> None:
    repository = ReportRepository()

    assert repository.leads_by_city_and_category(db_session) == []
    assert repository.leads_missing_website(db_session) == []
    assert repository.high_review_weak_presence_leads(db_session) == []
    assert repository.manual_review_leads(db_session) == []
    assert repository.score_distribution_by_category(db_session) == []
    assert repository.import_quality_summary(db_session) == []
    assert repository.missing_data_report(db_session) == []


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
    phone: str | None = "+91-9876543210",
    rating: float | None = 4.6,
    review_count: int | None = 150,
    address: str | None = "Main Road",
):
    normalized_name = normalized_business_name or business_name.lower()
    return repository.add_lead(
        db_session,
        business_name=business_name,
        normalized_business_name=normalized_name,
        category=category,
        normalized_category=normalized_category,
        city=city,
        normalized_city=normalized_city,
        state="Jharkhand",
        phone=phone,
        website=website,
        rating=rating,
        review_count=review_count,
        address=address,
    )


def _audit_result(*checks: tuple[str, str]) -> dict:
    return {
        "website_url": "https://example.com",
        "fetch_status": None,
        "checks": [
            {
                "key": key,
                "status": status,
                "label": key.replace("_", " ").title(),
                "evidence": None,
            }
            for key, status in checks
        ],
    }


def _score_payload(
    *,
    total_score: float = 50,
    priority_label: str = "medium",
    confidence_level: str = "medium",
    risk_flags: list[str] | None = None,
    missing_data: list[str] | None = None,
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
        "risk_flags": risk_flags or [],
        "missing_data": missing_data or [],
    }


def _table_counts(db_session) -> dict[str, int]:
    models = [Lead, LeadAudit, LeadImportError, LeadImportRun, LeadScore]
    return {
        model.__tablename__: db_session.execute(select(func.count(model.id))).scalar_one()
        for model in models
    }
