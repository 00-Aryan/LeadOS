"""Application configuration settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="LEADOS_", extra="ignore")

    app_name: str = "LeadOS"
    environment: str = "development"
    database_url: str = "sqlite:///./data/leados.db"


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
