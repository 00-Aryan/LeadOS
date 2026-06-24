"""LeadOS FastAPI application entrypoint."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_all_tables
from app.routers.leads import router as leads_router
from app.routers.scoring import router as scoring_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize local database tables for MVP development."""
    create_all_tables()
    yield


app = FastAPI(
    title="LeadOS API",
    description=(
        "Standalone lead intelligence API for import, audit, scoring, outreach, and evaluation."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(leads_router)
app.include_router(scoring_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return API health status."""
    return {"status": "ok", "service": "leados-api"}
