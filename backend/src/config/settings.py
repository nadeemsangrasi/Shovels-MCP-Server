"""
Configuration settings for the Shovels MCP Server.

Loads environment variables via Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Required: Shovels API
    SHOVELS_API_KEY: Optional[str] = None
    SHOVELS_API_BASE: str = "https://api.shovels.ai/v2"

    # Retry / back-off
    MAX_RETRIES: int = 3

    # Rate-limit (429) retry settings
    RATE_LIMIT_RETRY_MAX: int = 5
    RATE_LIMIT_INITIAL_BACKOFF: float = 1.0
    RATE_LIMIT_MAX_BACKOFF: float = 60.0

    # Pagination defaults
    DEFAULT_LIMIT: int = 50
    MAX_RECORDS: int = 10000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=True)


# Global settings instance
settings = Settings()
