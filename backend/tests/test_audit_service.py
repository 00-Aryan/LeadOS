"""Tests for deterministic website audit service."""

import httpx

from app.services.audit_service import audit_website, fetch_website


def test_fetch_blocks_non_http_urls() -> None:
    result = fetch_website("file:///etc/passwd")

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
            text=(
                "<html><head><title>Clinic</title></head>"
                "<body>Contact us</body></html>"
            ),
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
