"""Tests for deterministic website audit service."""

import httpx

from app.services.audit_service import audit_website, audit_website_presence, fetch_website


def test_fetch_blocks_non_http_urls() -> None:
    result = fetch_website("ftp://example.com/resource")

    assert result.status == "blocked"
    assert result.error_type == "invalid_url"


def test_fetch_blocks_direct_private_ip() -> None:
    result = fetch_website("http://127.0.0.1:8000")

    assert result.status == "blocked"
    assert result.error_type == "invalid_url"


def test_fetch_returns_structured_success_with_mock_transport() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"content-type": "text/html"},
            text=("<html><head><title>Clinic</title></head><body>Contact us</body></html>"),
            request=request,
        )

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport, follow_redirects=False) as client:
        result = fetch_website("https://example.com", client=client)

    assert result.status == "success"
    assert result.status_code == 200
    assert result.final_url == "https://example.com"
    assert result.html is not None


def test_fetch_returns_structured_request_error_with_mock_transport() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection failed", request=request)

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport, follow_redirects=False) as client:
        result = fetch_website("https://example.com", client=client)

    assert result.status == "failed"
    assert result.error_type == "request_error"


def test_audit_detects_basic_digital_signals() -> None:
    html = """
    <html>
      <head>
        <title>Healthy Smile Clinic</title>
        <meta name="description" content="Dental clinic in Ranchi">
        <script type="application/ld+json">{"@context":"https://schema.org"}</script>
      </head>
      <body>
        <a href="tel:+919876543210">Call</a>
        <a href="https://wa.me/919876543210">WhatsApp</a>
        <a href="/contact">Contact</a>
        <a href="/book-appointment">Book appointment</a>
        <a href="https://instagram.com/example">Instagram</a>
      </body>
    </html>
    """

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"content-type": "text/html"},
            text=html,
            request=request,
        )

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport, follow_redirects=False) as client:
        result = audit_website("https://example.com", client=client)

    checks = {check.name: check.status for check in result.checks}
    assert checks["website_loads"] == "true"
    assert checks["https_enabled"] == "true"
    assert checks["title_exists"] == "true"
    assert checks["meta_description_exists"] == "true"
    assert checks["phone_detected"] == "true"
    assert checks["whatsapp_detected"] == "true"
    assert checks["booking_link_detected"] == "true"
    assert checks["contact_signal_detected"] == "true"
    assert checks["social_link_detected"] == "true"
    assert checks["schema_markup_detected"] == "true"


def test_audit_returns_unknown_checks_when_fetch_blocked() -> None:
    result = audit_website("http://127.0.0.1")

    checks = {check.name: check.status for check in result.checks}
    assert result.fetch.status == "blocked"
    assert checks["website_loads"] == "false"
    assert checks["title_exists"] == "unknown"
    assert checks["meta_description_exists"] == "unknown"


def test_presence_audit_detects_all_expected_signals_from_static_html() -> None:
    html = """
    <html itemscope itemtype="https://schema.org/Dentist">
      <head>
        <title>Healthy Smile Clinic</title>
        <META NAME="description" CONTENT="Family dental care in Ranchi">
        <script type="application/ld+json">{"@context":"https://schema.org"}</script>
      </head>
      <body>
        <a href="tel:+919876543210">Call us</a>
        <a href="https://wa.me/919876543210">WhatsApp</a>
        <a href="/book-appointment">Book appointment</a>
        <a href="/contact">Contact us</a>
        <a href="https://facebook.com/healthy-smile">Facebook</a>
        <p>Email care@example.com or visit our address on Main Road.</p>
      </body>
    </html>
    """

    result = audit_website_presence("https://example.com", html)

    checks = {check.key: check for check in result.checks}
    assert set(checks) == {
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
    assert all(check.label for check in checks.values())
    assert checks["https"].status == "true"
    assert checks["title"].status == "true"
    assert checks["title"].evidence == "Healthy Smile Clinic"
    assert checks["meta_description"].status == "true"
    assert checks["phone_link"].status == "true"
    assert checks["whatsapp_link"].status == "true"
    assert checks["booking_signal"].status == "true"
    assert checks["contact_signal"].status == "true"
    assert checks["social_link"].status == "true"
    assert checks["schema_markup"].status == "true"


def test_presence_audit_marks_absent_html_signals_false() -> None:
    html = "<html><head></head><body><p>Welcome to our clinic.</p></body></html>"

    result = audit_website_presence("http://example.com", html)

    checks = {check.key: check for check in result.checks}
    assert checks["https"].status == "false"
    assert checks["title"].status == "false"
    assert checks["title"].evidence == "No title tag found"
    assert checks["meta_description"].status == "false"
    assert checks["phone_link"].status == "false"
    assert checks["whatsapp_link"].status == "false"
    assert checks["booking_signal"].status == "false"
    assert checks["contact_signal"].status == "false"
    assert checks["social_link"].status == "false"
    assert checks["schema_markup"].status == "false"


def test_presence_audit_uses_unknown_for_unavailable_html() -> None:
    result = audit_website_presence("https://example.com", None, fetch_status="failed")

    checks = {check.key: check for check in result.checks}
    assert checks["https"].status == "true"
    for key in (
        "title",
        "meta_description",
        "phone_link",
        "whatsapp_link",
        "booking_signal",
        "contact_signal",
        "social_link",
        "schema_markup",
    ):
        assert checks[key].status == "unknown"
        assert checks[key].evidence == "html unavailable: failed"


def test_presence_audit_uses_unknown_for_blank_html_and_missing_url() -> None:
    result = audit_website_presence(None, "   ")

    checks = {check.key: check.status for check in result.checks}
    assert checks["https"] == "unknown"
    assert checks["title"] == "unknown"
    assert checks["meta_description"] == "unknown"


def test_presence_audit_uses_unknown_for_malformed_url() -> None:
    result = audit_website_presence("example.com", "<html><title>Clinic</title></html>")

    checks = {check.key: check for check in result.checks}
    assert checks["https"].status == "unknown"
    assert checks["https"].evidence == "Malformed or unsupported website URL"


def test_presence_audit_detects_individual_signals() -> None:
    html = """
    <html>
      <head>
        <title>Care Clinic</title>
        <meta name="DESCRIPTION" content="Appointments and contact details">
      </head>
      <body>
        <a href="tel:5551234567">Phone</a>
        <a href="https://api.whatsapp.com/send?phone=5551234567">Chat</a>
        <a href="https://calendly.com/care-clinic">Schedule a visit</a>
        <a href="mailto:care@example.com">Email us</a>
        <a href="https://x.com/careclinic">X</a>
        <div itemscope>Local clinic</div>
      </body>
    </html>
    """

    result = audit_website_presence("https://example.com", html)

    checks = {check.key: check for check in result.checks}
    assert checks["meta_description"].evidence == "Appointments and contact details"
    assert checks["phone_link"].evidence == "tel:5551234567"
    assert checks["whatsapp_link"].evidence == "https://api.whatsapp.com/send?phone=5551234567"
    assert checks["booking_signal"].evidence == "schedule"
    assert checks["contact_signal"].evidence == "mailto:"
    assert checks["social_link"].evidence == "https://x.com/careclinic"
    assert checks["schema_markup"].evidence == "itemscope"


def test_presence_audit_evidence_is_concise() -> None:
    long_title = "Healthy Smile Clinic " * 20
    html = f"<html><head><title>{long_title}</title></head><body></body></html>"

    result = audit_website_presence("https://example.com", html)

    checks = {check.key: check for check in result.checks}
    assert checks["title"].status == "true"
    assert checks["title"].evidence is not None
    assert len(checks["title"].evidence) <= 120
    assert "<html>" not in checks["title"].evidence
