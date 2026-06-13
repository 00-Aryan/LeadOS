"""Deterministic website audit service."""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse

import httpx

from app.schemas.audit import AuditCheck, WebsiteAuditResult, WebsiteFetchResult

DEFAULT_TIMEOUT_SECONDS = 5.0
MAX_HTML_CHARS = 200_000


def describe_service() -> str:
    """Return the service responsibility."""
    return "Runs deterministic digital-presence checks with evidence."


def fetch_website(url: str, client: httpx.Client | None = None) -> WebsiteFetchResult:
    """Fetch one explicitly provided website URL safely.

    This is not a crawler. Redirects are disabled to reduce SSRF bypass risk.
    """
    validation_error = _validate_fetch_url(url)
    if validation_error is not None:
        return WebsiteFetchResult(
            status="blocked",
            requested_url=url,
            error_type="invalid_url",
            error_message=validation_error,
        )

    owns_client = client is None
    active_client = client or httpx.Client(
        timeout=DEFAULT_TIMEOUT_SECONDS,
        follow_redirects=False,
        headers={"User-Agent": "LeadOSAuditBot/0.1"},
    )

    try:
        response = active_client.get(url)
        content_type = response.headers.get("content-type")
        html = response.text[:MAX_HTML_CHARS] if _looks_like_html(content_type) else None
        return WebsiteFetchResult(
            status="success",
            requested_url=url,
            final_url=str(response.url),
            status_code=response.status_code,
            content_type=content_type,
            html=html,
        )
    except httpx.TimeoutException as exc:
        return WebsiteFetchResult(
            status="failed",
            requested_url=url,
            error_type="timeout",
            error_message=str(exc) or "Website fetch timed out.",
        )
    except httpx.RequestError as exc:
        return WebsiteFetchResult(
            status="failed",
            requested_url=url,
            error_type="request_error",
            error_message=str(exc) or "Website fetch failed.",
        )
    finally:
        if owns_client:
            active_client.close()


def audit_website(url: str, client: httpx.Client | None = None) -> WebsiteAuditResult:
    """Fetch and audit one provided website URL."""
    fetch = fetch_website(url, client=client)
    checks = build_audit_checks(fetch)
    return WebsiteAuditResult(requested_url=url, fetch=fetch, checks=checks)


def build_audit_checks(fetch: WebsiteFetchResult) -> list[AuditCheck]:
    """Build deterministic checks from fetched HTML."""
    if fetch.status != "success" or not fetch.html:
        return [
            AuditCheck(name="website_loads", status="false", evidence=fetch.error_type),
            AuditCheck(name="https_enabled", status=_https_status(fetch.requested_url)),
            AuditCheck(name="title_exists", status="unknown"),
            AuditCheck(name="meta_description_exists", status="unknown"),
            AuditCheck(name="phone_detected", status="unknown"),
            AuditCheck(name="whatsapp_detected", status="unknown"),
            AuditCheck(name="booking_link_detected", status="unknown"),
            AuditCheck(name="contact_signal_detected", status="unknown"),
            AuditCheck(name="social_link_detected", status="unknown"),
            AuditCheck(name="schema_markup_detected", status="unknown"),
        ]

    html = fetch.html
    lower_html = html.lower()
    return [
        AuditCheck(name="website_loads", status="true", evidence=str(fetch.status_code)),
        AuditCheck(name="https_enabled", status=_https_status(fetch.final_url or fetch.requested_url)),
        _regex_check("title_exists", html, r"<title[^>]*>\s*[^<]+\s*</title>"),
        _regex_check(
            "meta_description_exists",
            html,
            r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"'][^\"']+[\"']",
        ),
        _regex_check("phone_detected", html, r"tel:\+?[0-9][0-9\-\s()]{6,}"),
        _contains_check("whatsapp_detected", lower_html, "whatsapp", "WhatsApp signal found"),
        _contains_any_check(
            "booking_link_detected",
            lower_html,
            ("book appointment", "booking", "calendly", "appoint"),
        ),
        _contains_any_check("contact_signal_detected", lower_html, ("contact", "enquiry", "inquiry")),
        _contains_any_check(
            "social_link_detected",
            lower_html,
            ("facebook.com", "instagram.com", "linkedin.com", "youtube.com"),
        ),
        _contains_check("schema_markup_detected", lower_html, "schema.org", "schema.org found"),
    ]


def _validate_fetch_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return "Only http and https URLs are allowed."
    if not parsed.hostname:
        return "URL must include a hostname."

    try:
        ip = ipaddress.ip_address(parsed.hostname)
    except ValueError:
        return None

    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
        return "Direct requests to private, local, link-local, multicast, or reserved IPs are blocked."
    return None


def _looks_like_html(content_type: str | None) -> bool:
    if content_type is None:
        return True
    return "html" in content_type.lower() or "text/plain" in content_type.lower()


def _https_status(url: str) -> str:
    return "true" if urlparse(url).scheme == "https" else "false"


def _regex_check(name: str, html: str, pattern: str) -> AuditCheck:
    match = re.search(pattern, html, flags=re.IGNORECASE)
    if match:
        return AuditCheck(name=name, status="true", evidence=match.group(0)[:120])
    return AuditCheck(name=name, status="false")


def _contains_check(name: str, lower_html: str, needle: str, evidence: str) -> AuditCheck:
    if needle in lower_html:
        return AuditCheck(name=name, status="true", evidence=evidence)
    return AuditCheck(name=name, status="false")


def _contains_any_check(name: str, lower_html: str, needles: tuple[str, ...]) -> AuditCheck:
    for needle in needles:
        if needle in lower_html:
            return AuditCheck(name=name, status="true", evidence=needle)
    return AuditCheck(name=name, status="false")
