"""Website audit schemas."""

from typing import Literal

from pydantic import BaseModel, Field

FetchStatus = Literal["success", "failed", "blocked"]
CheckStatus = Literal["true", "false", "unknown"]


class WebsiteFetchResult(BaseModel):
    """Structured result from fetching one provided website URL."""

    status: FetchStatus
    requested_url: str
    final_url: str | None = None
    status_code: int | None = None
    content_type: str | None = None
    html: str | None = None
    error_type: str | None = None
    error_message: str | None = None


class AuditCheck(BaseModel):
    """One deterministic audit check result."""

    name: str
    status: CheckStatus
    evidence: str | None = None


class WebsiteAuditResult(BaseModel):
    """Website audit output for one lead website."""

    requested_url: str
    fetch: WebsiteFetchResult
    checks: list[AuditCheck] = Field(default_factory=list)


class WebsitePresenceAuditCheck(BaseModel):
    """One deterministic website presence check from provided HTML."""

    key: str
    status: CheckStatus
    label: str
    evidence: str | None = None


class WebsitePresenceAuditResult(BaseModel):
    """Deterministic website audit output from already available HTML."""

    website_url: str | None = None
    fetch_status: str | None = None
    checks: list[WebsitePresenceAuditCheck] = Field(default_factory=list)
