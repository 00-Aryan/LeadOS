"""Structured schemas for deterministic outreach drafts."""

from typing import Literal

from pydantic import BaseModel, Field

OutreachChannel = Literal["short_email", "whatsapp_message"]


class OutreachDraftInput(BaseModel):
    """Known facts available to build one outreach draft."""

    business_name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    location: str = Field(min_length=1)
    audit_findings: list[str] = Field(default_factory=list)
    score_reason: str | None = None
    offer_angle: str = Field(min_length=1)
    channel: OutreachChannel


class OutreachDraftResult(BaseModel):
    """Draft output that always requires human review before use."""

    channel: OutreachChannel
    subject_line: str | None = None
    message_body: str = Field(min_length=1)
    personalization_notes: list[str] = Field(default_factory=list)
    assumptions_used: list[str] = Field(default_factory=list)
    review_required: Literal[True] = True
