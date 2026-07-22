"""
Health check endpoint for the Shovels MCP Server.
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Response from /health endpoint."""

    status: str = Field(..., description="Overall health: 'healthy' or 'degraded'")
    version: str = Field(..., description="API version")
    shovels_api: str = Field(default="unknown", description="Shovels API reachability")


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Basic health check. Verifies the Shovels API is reachable.
    """
    shovels_status = "unknown"

    try:
        from src.services.shovels_client import get_client

        client = get_client()
        # Lightweight ping via a geo search with a dummy query
        # (this will fail gracefully if the API key is wrong)
        result = await client.resolve_geo("US", level="state")
        items = result.get("items", [])
        if items:
            shovels_status = "reachable"
        else:
            shovels_status = "responded"
    except Exception as e:
        shovels_status = f"unreachable: {str(e)[:100]}"

    overall = "healthy" if shovels_status in ("reachable", "responded") else "degraded"

    return HealthResponse(
        status=overall,
        version="2.0.0",
        shovels_api=shovels_status,
    )
