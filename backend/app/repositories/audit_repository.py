"""Repository for deterministic audit persistence."""

import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LeadAudit


class AuditRepository:
    """Data access methods for persisted website audits."""

    def add_audit_result(
        self,
        db: Session,
        *,
        lead_id: int,
        requested_url: str | None,
        fetch_status: str,
        result_json: dict[str, Any],
    ) -> LeadAudit:
        """Add an audit result to the current transaction and flush for ID assignment."""
        audit = LeadAudit(
            lead_id=lead_id,
            requested_url=requested_url,
            fetch_status=fetch_status,
            result_json=_json_serializable_copy(result_json),
        )
        db.add(audit)
        db.flush()
        return audit

    def list_by_lead_id(self, db: Session, lead_id: int) -> list[LeadAudit]:
        """Return audits for one lead in stable creation order."""
        stmt = (
            select(LeadAudit)
            .where(LeadAudit.lead_id == lead_id)
            .order_by(LeadAudit.created_at, LeadAudit.id)
        )
        return list(db.execute(stmt).scalars())

    def get_latest_by_lead_id(self, db: Session, lead_id: int) -> LeadAudit | None:
        """Return the newest audit for one lead, if any."""
        stmt = (
            select(LeadAudit)
            .where(LeadAudit.lead_id == lead_id)
            .order_by(LeadAudit.created_at.desc(), LeadAudit.id.desc())
            .limit(1)
        )
        return db.execute(stmt).scalar_one_or_none()


def _json_serializable_copy(result_json: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(result_json))
