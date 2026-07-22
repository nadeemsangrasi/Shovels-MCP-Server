"""
Configuration settings for the Shovels MCP Server.

Loads environment variables via Pydantic Settings.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Required: Shovels API
    SHOVELS_API_KEY: Optional[str] = None
    SHOVELS_API_BASE: str = "https://api.shovels.ai/v2"

    # Retry / back-off
    MAX_RETRIES: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
