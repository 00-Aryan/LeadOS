"""Application configuration for LeadOS."""

from pydantic import BaseModel


class Settings(BaseModel):
    """Runtime settings.

    Keep this minimal during Phase 0. Environment-backed settings can be added
    when persistence and external providers are introduced.
    """

    app_name: str = "LeadOS"
    environment: str = "development"
    enable_future_tenant_fields: bool = True


settings = Settings()
