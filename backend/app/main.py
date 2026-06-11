"""LeadOS FastAPI application entrypoint."""

from fastapi import FastAPI

app = FastAPI(
    title="LeadOS API",
    description="Standalone lead intelligence API for import, audit, scoring, outreach, and evaluation.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return API health status."""
    return {"status": "ok", "service": "leados-api"}
