"""Repository for deterministic lead score persistence."""

import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LeadScore


class ScoreRepository:
    """Data access methods for persisted lead scores."""

    def add_score_result(
        self,
        db: Session,
        *,
        lead_id: int,
        scoring_version: str,
        total_score: float,
        category_scores: dict[str, Any],
        priority_label: str,
        confidence_level: str,
        reason_summary: str,
        positive_signals: list[str],
        risk_flags: list[str],
        missing_data: list[str],
    ) -> LeadScore:
        """Add a score result to the current transaction and flush for ID assignment."""
        score = LeadScore(
            lead_id=lead_id,
            scoring_version=scoring_version,
            total_score=total_score,
            category_scores=_json_serializable_copy(category_scores),
            priority_label=priority_label,
            confidence_level=confidence_level,
            reason_summary=reason_summary,
            positive_signals=_json_serializable_copy(positive_signals),
            risk_flags=_json_serializable_copy(risk_flags),
            missing_data=_json_serializable_copy(missing_data),
        )
        db.add(score)
        db.flush()
        return score

    def list_by_lead_id(self, db: Session, lead_id: int) -> list[LeadScore]:
        """Return scores for one lead in stable creation order."""
        stmt = (
            select(LeadScore)
            .where(LeadScore.lead_id == lead_id)
            .order_by(LeadScore.created_at, LeadScore.id)
        )
        return list(db.execute(stmt).scalars())

    def get_latest_by_lead_id(self, db: Session, lead_id: int) -> LeadScore | None:
        """Return the newest score for one lead, if any."""
        stmt = (
            select(LeadScore)
            .where(LeadScore.lead_id == lead_id)
            .order_by(LeadScore.created_at.desc(), LeadScore.id.desc())
            .limit(1)
        )
        return db.execute(stmt).scalar_one_or_none()


def _json_serializable_copy(value: Any) -> Any:
    return json.loads(json.dumps(value))
