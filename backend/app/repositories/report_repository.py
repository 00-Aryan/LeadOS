"""Read-only SQL reporting repository."""

from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import Lead, LeadAudit, LeadImportError, LeadImportRun, LeadScore
from app.schemas.report import (
    HighReviewWeakPresenceLeadRow,
    ImportQualitySummaryRow,
    LeadsByCityCategoryRow,
    ManualReviewLeadRow,
    MissingDataReportRow,
    MissingWebsiteLeadRow,
    ScoreDistributionByCategoryRow,
)


class ReportRepository:
    """SQL-backed read-only report queries."""

    def leads_by_city_and_category(self, db: Session) -> list[LeadsByCityCategoryRow]:
        """Return lead counts grouped by city and category."""
        stmt = (
            select(Lead.city, Lead.category, func.count(Lead.id).label("lead_count"))
            .group_by(Lead.city, Lead.category)
            .order_by(Lead.city, Lead.category)
        )
        return [
            LeadsByCityCategoryRow(city=city, category=category, lead_count=lead_count)
            for city, category, lead_count in db.execute(stmt)
        ]

    def leads_missing_website(self, db: Session) -> list[MissingWebsiteLeadRow]:
        """Return leads where website is null or blank."""
        stmt = (
            select(Lead)
            .where(or_(Lead.website.is_(None), func.trim(Lead.website) == ""))
            .order_by(Lead.city, Lead.category, Lead.business_name, Lead.id)
        )
        return [
            MissingWebsiteLeadRow(
                lead_id=lead.id,
                business_name=lead.business_name,
                city=lead.city,
                category=lead.category,
                website=lead.website,
            )
            for lead in db.execute(stmt).scalars()
        ]

    def high_review_weak_presence_leads(
        self,
        db: Session,
        min_review_count: int = 100,
    ) -> list[HighReviewWeakPresenceLeadRow]:
        """Return high-review leads with persisted weak-presence signals."""
        latest_score_id = _latest_score_id_for_lead()
        latest_audit_id = _latest_audit_id_for_lead()
        stmt = (
            select(Lead, LeadScore, LeadAudit)
            .outerjoin(LeadScore, LeadScore.id == latest_score_id)
            .outerjoin(LeadAudit, LeadAudit.id == latest_audit_id)
            .where(Lead.review_count >= min_review_count)
            .order_by(Lead.city, Lead.category, Lead.business_name, Lead.id)
        )

        rows: list[HighReviewWeakPresenceLeadRow] = []
        for lead, score, audit in db.execute(stmt):
            weak_signals = _weak_presence_signals(lead, score, audit)
            if not weak_signals:
                continue
            rows.append(
                HighReviewWeakPresenceLeadRow(
                    lead_id=lead.id,
                    business_name=lead.business_name,
                    city=lead.city,
                    category=lead.category,
                    review_count=lead.review_count or 0,
                    priority_label=score.priority_label if score else None,
                    confidence_level=score.confidence_level if score else None,
                    weak_signals=weak_signals,
                )
            )
        return rows

    def manual_review_leads(self, db: Session) -> list[ManualReviewLeadRow]:
        """Return leads whose latest persisted score needs manual review."""
        latest_score_id = _latest_score_id_for_lead()
        stmt = (
            select(Lead, LeadScore)
            .join(LeadScore, LeadScore.id == latest_score_id)
            .where(
                or_(
                    LeadScore.priority_label == "review_needed",
                    LeadScore.confidence_level == "low",
                )
            )
            .order_by(Lead.city, Lead.category, Lead.business_name, Lead.id)
        )
        return [
            ManualReviewLeadRow(
                lead_id=lead.id,
                business_name=lead.business_name,
                city=lead.city,
                category=lead.category,
                total_score=score.total_score,
                priority_label=score.priority_label,
                confidence_level=score.confidence_level,
                missing_data=_list_value(score.missing_data),
                risk_flags=_list_value(score.risk_flags),
            )
            for lead, score in db.execute(stmt)
        ]

    def score_distribution_by_category(
        self,
        db: Session,
    ) -> list[ScoreDistributionByCategoryRow]:
        """Return latest persisted score counts by category and priority label."""
        latest_score_id = _latest_score_id_for_lead()
        stmt = (
            select(
                Lead.category,
                LeadScore.priority_label,
                func.count(LeadScore.id).label("lead_count"),
                func.avg(LeadScore.total_score).label("average_score"),
            )
            .join(LeadScore, LeadScore.id == latest_score_id)
            .group_by(Lead.category, LeadScore.priority_label)
            .order_by(Lead.category, LeadScore.priority_label)
        )
        return [
            ScoreDistributionByCategoryRow(
                category=category,
                priority_label=priority_label,
                lead_count=lead_count,
                average_score=float(average_score or 0),
            )
            for category, priority_label, lead_count, average_score in db.execute(stmt)
        ]

    def import_quality_summary(self, db: Session) -> list[ImportQualitySummaryRow]:
        """Return import run summaries with persisted rejected-row counts."""
        stmt = (
            select(
                LeadImportRun,
                func.count(LeadImportError.id).label("error_count"),
            )
            .outerjoin(LeadImportError, LeadImportError.import_run_id == LeadImportRun.id)
            .group_by(LeadImportRun.id)
            .order_by(LeadImportRun.created_at, LeadImportRun.id)
        )
        return [
            ImportQualitySummaryRow(
                import_run_id=run.id,
                source_name=run.source_name,
                total_records=run.total_records,
                valid_records=run.valid_records,
                invalid_records=run.invalid_records,
                duplicate_records=run.duplicate_records,
                error_count=error_count,
                created_at=run.created_at,
            )
            for run, error_count in db.execute(stmt)
        ]

    def missing_data_report(self, db: Session) -> list[MissingDataReportRow]:
        """Return leads with lead-level or score-level missing data."""
        latest_score_id = _latest_score_id_for_lead()
        stmt = (
            select(Lead, LeadScore)
            .outerjoin(LeadScore, LeadScore.id == latest_score_id)
            .order_by(Lead.city, Lead.category, Lead.business_name, Lead.id)
        )

        rows: list[MissingDataReportRow] = []
        for lead, score in db.execute(stmt):
            missing_fields = _lead_missing_fields(lead)
            score_missing_data = _list_value(score.missing_data) if score else []
            if not missing_fields and not score_missing_data:
                continue
            rows.append(
                MissingDataReportRow(
                    lead_id=lead.id,
                    business_name=lead.business_name,
                    city=lead.city,
                    category=lead.category,
                    missing_fields=missing_fields,
                    score_missing_data=score_missing_data,
                )
            )
        return rows


def _latest_score_id_for_lead():
    return (
        select(func.max(LeadScore.id))
        .where(LeadScore.lead_id == Lead.id)
        .correlate(Lead)
        .scalar_subquery()
    )


def _latest_audit_id_for_lead():
    return (
        select(func.max(LeadAudit.id))
        .where(LeadAudit.lead_id == Lead.id)
        .correlate(Lead)
        .scalar_subquery()
    )


def _weak_presence_signals(
    lead: Lead,
    score: LeadScore | None,
    audit: LeadAudit | None,
) -> list[str]:
    signals: list[str] = []
    if _is_blank(lead.website):
        signals.append("missing website")

    if audit:
        for check in audit.result_json.get("checks", []):
            key = str(check.get("key") or check.get("name") or "unknown")
            status = check.get("status")
            if status == "false" and key in _DIGITAL_PRESENCE_KEYS:
                signals.append(f"audit {key} is false")

    if score:
        category_scores = score.category_scores or {}
        digital_gap = category_scores.get("digital_gap")
        if isinstance(digital_gap, int | float) and digital_gap >= 20:
            signals.append("score digital_gap is high")

        for value in [*_list_value(score.risk_flags), *_list_value(score.missing_data)]:
            lowered = value.lower()
            if any(token in lowered for token in _WEAK_SIGNAL_TOKENS):
                signals.append(value)

    return _deduplicate(signals)


def _lead_missing_fields(lead: Lead) -> list[str]:
    missing_fields: list[str] = []
    for field_name in ("phone", "website", "rating", "review_count", "address"):
        if _is_blank(getattr(lead, field_name)):
            missing_fields.append(field_name)
    return missing_fields


def _is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    return False


def _list_value(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _deduplicate(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduplicated: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduplicated.append(value)
    return deduplicated


_DIGITAL_PRESENCE_KEYS = {
    "https",
    "title",
    "meta_description",
    "phone_link",
    "whatsapp_link",
    "booking_signal",
    "contact_signal",
    "social_link",
    "schema_markup",
}

_WEAK_SIGNAL_TOKENS = {
    "website",
    "digital",
    "presence",
    "contact",
    "phone",
    "whatsapp",
    "booking",
    "social",
}
