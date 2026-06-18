"""Deterministic website audit service."""

from __future__ import annotations

import ipaddress
import re
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlparse

import httpx

from app.schemas.audit import (
    AuditCheck,
    WebsiteAuditResult,
    WebsiteFetchResult,
    WebsitePresenceAuditCheck,
    WebsitePresenceAuditResult,
)

DEFAULT_TIMEOUT_SECONDS = 5.0
MAX_HTML_CHARS = 200_000
MAX_EVIDENCE_CHARS = 120
HTML_DEPENDENT_CHECKS = (
    ("title", "Title"),
    ("meta_description", "Meta description"),
    ("phone_link", "Phone link"),
    ("whatsapp_link", "WhatsApp link"),
    ("booking_signal", "Booking signal"),
    ("contact_signal", "Contact signal"),
    ("social_link", "Social link"),
    ("schema_markup", "Schema markup"),
)
BOOKING_SIGNALS = (
    "book",
    "booking",
    "appointment",
    "reserve",
    "reservation",
    "schedule",
    "calendly",
)
CONTACT_SIGNALS = (
    "mailto:",
    "contact us",
    "contact",
    "email",
    "address",
)
SOCIAL_DOMAINS = (
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "x.com",
    "twitter.com",
    "youtube.com",
)
WHATSAPP_SIGNALS = (
    "wa.me",
    "whatsapp.com",
    "api.whatsapp.com",
)


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


def audit_website_presence(
    website_url: str | None,
    html: str | None,
    *,
    fetch_status: str | None = None,
) -> WebsitePresenceAuditResult:
    """Audit already available website HTML without fetching or persisting anything."""
    checks = [_https_presence_check(website_url)]
    if fetch_status not in {None, "success"} or html is None or not html.strip():
        checks.extend(
            WebsitePresenceAuditCheck(
                key=key,
                status="unknown",
                label=label,
                evidence=_unknown_evidence(fetch_status),
            )
            for key, label in HTML_DEPENDENT_CHECKS
        )
        return WebsitePresenceAuditResult(
            website_url=website_url,
            fetch_status=fetch_status,
            checks=checks,
        )

    parsed_html = _ParsedHTML.from_html(html)
    checks.extend(
        [
            _title_check(parsed_html),
            _meta_description_check(parsed_html),
            _phone_link_check(parsed_html),
            _whatsapp_link_check(parsed_html),
            _booking_signal_check(parsed_html),
            _contact_signal_check(parsed_html),
            _social_link_check(parsed_html),
            _schema_markup_check(parsed_html),
        ]
    )
    return WebsitePresenceAuditResult(
        website_url=website_url,
        fetch_status=fetch_status,
        checks=checks,
    )


def build_audit_checks(fetch: WebsiteFetchResult) -> list[AuditCheck]:
    """Build deterministic checks from fetched HTML."""
    if fetch.status != "success" or not fetch.html:
        return [
            AuditCheck(
                name="website_loads",
                status="false",
                evidence=fetch.error_type,
            ),
            AuditCheck(
                name="https_enabled",
                status=_https_status(fetch.requested_url),
            ),
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
        AuditCheck(
            name="website_loads",
            status="true",
            evidence=str(fetch.status_code),
        ),
        AuditCheck(
            name="https_enabled",
            status=_https_status(fetch.final_url or fetch.requested_url),
        ),
        _regex_check("title_exists", html, r"<title[^>]*>\s*[^<]+\s*</title>"),
        _regex_check(
            "meta_description_exists",
            html,
            r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"'][^\"']+[\"']",
        ),
        _regex_check("phone_detected", html, r"tel:\+?[0-9][0-9\-\s()]{6,}"),
        _contains_check(
            "whatsapp_detected",
            lower_html,
            "whatsapp",
            "WhatsApp signal found",
        ),
        _contains_any_check(
            "booking_link_detected",
            lower_html,
            ("book appointment", "booking", "calendly", "appoint"),
        ),
        _contains_any_check(
            "contact_signal_detected",
            lower_html,
            ("contact", "enquiry", "inquiry"),
        ),
        _contains_any_check(
            "social_link_detected",
            lower_html,
            ("facebook.com", "instagram.com", "linkedin.com", "youtube.com"),
        ),
        _contains_check(
            "schema_markup_detected",
            lower_html,
            "schema.org",
            "schema.org found",
        ),
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
        return (
            "Direct requests to private, local, link-local, multicast, or reserved IPs are blocked."
        )
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


def _contains_check(
    name: str,
    lower_html: str,
    needle: str,
    evidence: str,
) -> AuditCheck:
    if needle in lower_html:
        return AuditCheck(name=name, status="true", evidence=evidence)
    return AuditCheck(name=name, status="false")


def _contains_any_check(
    name: str,
    lower_html: str,
    needles: tuple[str, ...],
) -> AuditCheck:
    for needle in needles:
        if needle in lower_html:
            return AuditCheck(name=name, status="true", evidence=needle)
    return AuditCheck(name=name, status="false")


class _PresenceHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.in_script = False
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.hrefs: list[str] = []
        self.meta_description: str | None = None
        self.schema_signals: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): value or "" for name, value in attrs}
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "script":
            self.in_script = True
            if attr_map.get("type", "").lower() == "application/ld+json":
                self.schema_signals.append("application/ld+json")
        if tag.lower() == "meta" and attr_map.get("name", "").lower() == "description":
            content = _collapse_whitespace(attr_map.get("content", ""))
            if content:
                self.meta_description = content
        if tag.lower() == "a" and attr_map.get("href"):
            self.hrefs.append(attr_map["href"])
        if "itemscope" in attr_map:
            self.schema_signals.append("itemscope")
        for value in attr_map.values():
            if "schema.org" in value.lower():
                self.schema_signals.append("schema.org")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False
        if tag.lower() == "script":
            self.in_script = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
            return
        if self.in_script:
            if "schema.org" in data.lower():
                self.schema_signals.append("schema.org")
            return
        text = _collapse_whitespace(data)
        if text:
            self.text_parts.append(text)


class _ParsedHTML:
    def __init__(self, parser: _PresenceHTMLParser) -> None:
        self.title = _collapse_whitespace(" ".join(parser.title_parts))
        self.meta_description = parser.meta_description
        self.hrefs = [_collapse_whitespace(href) for href in parser.hrefs if href.strip()]
        self.text = _collapse_whitespace(" ".join(parser.text_parts))
        self.search_text = _collapse_whitespace(f"{self.text} {' '.join(self.hrefs)}").lower()
        self.schema_signals = parser.schema_signals

    @classmethod
    def from_html(cls, html: str) -> _ParsedHTML:
        parser = _PresenceHTMLParser()
        parser.feed(html)
        parser.close()
        return cls(parser)


def _https_presence_check(website_url: str | None) -> WebsitePresenceAuditCheck:
    if website_url is None or not website_url.strip():
        return WebsitePresenceAuditCheck(
            key="https",
            status="unknown",
            label="HTTPS",
            evidence="website URL unavailable",
        )
    normalized_url = website_url.strip()
    if normalized_url.lower().startswith("https://"):
        return WebsitePresenceAuditCheck(
            key="https",
            status="true",
            label="HTTPS",
            evidence=_safe_evidence(normalized_url),
        )
    if normalized_url.lower().startswith("http://"):
        return WebsitePresenceAuditCheck(
            key="https",
            status="false",
            label="HTTPS",
            evidence=_safe_evidence(normalized_url),
        )
    return WebsitePresenceAuditCheck(
        key="https",
        status="unknown",
        label="HTTPS",
        evidence="Malformed or unsupported website URL",
    )


def _title_check(parsed_html: _ParsedHTML) -> WebsitePresenceAuditCheck:
    if parsed_html.title:
        return _true_check("title", "Title", parsed_html.title)
    return _false_check("title", "Title", "No title tag found")


def _meta_description_check(parsed_html: _ParsedHTML) -> WebsitePresenceAuditCheck:
    if parsed_html.meta_description:
        return _true_check(
            "meta_description",
            "Meta description",
            parsed_html.meta_description,
        )
    return _false_check(
        "meta_description",
        "Meta description",
        "No meta description found",
    )


def _phone_link_check(parsed_html: _ParsedHTML) -> WebsitePresenceAuditCheck:
    href = _first_href_with_prefix(parsed_html.hrefs, "tel:")
    if href:
        return _true_check("phone_link", "Phone link", href)
    return _false_check("phone_link", "Phone link", "No tel: link found")


def _whatsapp_link_check(parsed_html: _ParsedHTML) -> WebsitePresenceAuditCheck:
    evidence = _first_href_for_domain(parsed_html.hrefs, WHATSAPP_SIGNALS)
    if evidence is None:
        evidence = _first_signal_excerpt(parsed_html.search_text, WHATSAPP_SIGNALS)
    if evidence:
        return _true_check("whatsapp_link", "WhatsApp link", evidence)
    return _false_check("whatsapp_link", "WhatsApp link", "No WhatsApp link found")


def _booking_signal_check(parsed_html: _ParsedHTML) -> WebsitePresenceAuditCheck:
    evidence = _first_word_signal(parsed_html.search_text, BOOKING_SIGNALS)
    if evidence:
        return _true_check("booking_signal", "Booking signal", evidence)
    return _false_check("booking_signal", "Booking signal", "No booking signal found")


def _contact_signal_check(parsed_html: _ParsedHTML) -> WebsitePresenceAuditCheck:
    evidence = _first_word_signal(parsed_html.search_text, CONTACT_SIGNALS)
    if evidence:
        return _true_check("contact_signal", "Contact signal", evidence)
    return _false_check("contact_signal", "Contact signal", "No contact signal found")


def _social_link_check(parsed_html: _ParsedHTML) -> WebsitePresenceAuditCheck:
    evidence = _first_href_for_domain(parsed_html.hrefs, SOCIAL_DOMAINS)
    if evidence:
        return _true_check("social_link", "Social link", evidence)
    return _false_check("social_link", "Social link", "No social link found")


def _schema_markup_check(parsed_html: _ParsedHTML) -> WebsitePresenceAuditCheck:
    if parsed_html.schema_signals:
        return _true_check("schema_markup", "Schema markup", parsed_html.schema_signals[0])
    return _false_check("schema_markup", "Schema markup", "No schema markup found")


def _true_check(key: str, label: str, evidence: str) -> WebsitePresenceAuditCheck:
    return WebsitePresenceAuditCheck(
        key=key,
        status="true",
        label=label,
        evidence=_safe_evidence(evidence),
    )


def _false_check(key: str, label: str, evidence: str) -> WebsitePresenceAuditCheck:
    return WebsitePresenceAuditCheck(
        key=key,
        status="false",
        label=label,
        evidence=_safe_evidence(evidence),
    )


def _first_href_with_prefix(hrefs: list[str], prefix: str) -> str | None:
    for href in hrefs:
        if href.lower().startswith(prefix):
            return href
    return None


def _first_href_for_domain(hrefs: list[str], domains: tuple[str, ...]) -> str | None:
    for href in hrefs:
        hostname = urlparse(href).hostname or ""
        normalized_hostname = hostname.removeprefix("www.").lower()
        for domain in domains:
            if normalized_hostname == domain or normalized_hostname.endswith(f".{domain}"):
                return href
    return None


def _first_signal_excerpt(text: str, signals: tuple[str, ...]) -> str | None:
    for signal in signals:
        index = text.find(signal)
        if index == -1:
            continue
        start = max(0, index - 40)
        end = min(len(text), index + len(signal) + 40)
        return text[start:end]
    return None


def _first_word_signal(text: str, signals: tuple[str, ...]) -> str | None:
    for signal in signals:
        if not signal[-1].isalnum() and signal in text:
            return signal
        if re.search(rf"(?<![a-z0-9]){re.escape(signal)}(?![a-z0-9])", text):
            return signal
    return None


def _unknown_evidence(fetch_status: str | None) -> str:
    if fetch_status not in {None, "success"}:
        return f"html unavailable: {fetch_status}"
    return "html unavailable"


def _safe_evidence(value: str) -> str:
    return _collapse_whitespace(value)[:MAX_EVIDENCE_CHARS]


def _collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(value)).strip()
