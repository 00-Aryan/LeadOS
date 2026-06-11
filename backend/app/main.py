"""LeadOS FastAPI application entrypoint."""

from fastapi import FastAPI

from app.routers.leads import router as leads_router

app = FastAPI(
    title="LeadOS API",
    description="Standalone lead intelligence API for import, audit, scoring, outreach, and evaluation.",
    version="0.1.0",
)

app.include_router(leads_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return API health status."""
    return {"status": "ok", "service": "leados-api"}
