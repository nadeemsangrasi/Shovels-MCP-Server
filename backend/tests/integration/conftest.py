"""
Integration test fixtures.

Provides a session-scoped FastAPI TestClient (for health endpoint tests)
and a mock for the ShovelsClient used by MCP tool tests.
"""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from src.services.shovels_client import ShovelsClient


async def _mock_request(self, method: str, path: str, params: dict = None) -> dict:
    """Mock _request returns appropriate canned data based on the path."""
    if "addresses/search" in path or "states/search" in path:
        return {
            "items": [{"geo_id": "geo_tx_austin", "level": "city", "display_name": "Austin, TX"}],
            "level_matched": "city",
        }
    if "permits/search" in path:
        return {
            "items": [{"id": "p1", "number": "RE2303928", "type": "electrical", "status": "active"}],
            "size": 1, "next_cursor": None, "X-Credits-Remaining": "199",
        }
    if "contractors/search" in path:
        return {
            "items": [{"id": "c1", "name": "ABC Construction", "classification": "General"}],
            "size": 1, "next_cursor": None,
        }
    if "decisions/search" in path:
        return {
            "items": [{"id": "d1", "category": "Rezoning", "status": "approved"}],
            "size": 1, "next_cursor": None,
        }
    if "permits/" in path and "/search" not in path:
        return {"id": "p1", "status": "active", "job_value_cents": 500000}
    if "contractors/" in path and "/search" not in path:
        return {"id": "c1", "name": "ABC Construction", "classification_derived": "General"}
    if "decisions/" in path and "/search" not in path:
        return {"id": "d1", "category": "Rezoning", "status": "approved"}
    return {"items": [], "size": 0, "next_cursor": None}


@pytest.fixture(scope="session")
def app():
    """
    FastAPI TestClient — session-scoped so FastMCP's session manager
    runs exactly once across all integration tests.
    """
    from main import app as fastapi_app

    with TestClient(fastapi_app) as client:
        yield client


@pytest.fixture(autouse=True)
def mock_shovels_api(app):
    """
    Patch ShovelsClient._request to return canned data.
    Auto-used for all integration tests so they never hit the real API.
    """
    from src.services.shovels_client import reset_client

    reset_client()

    patcher = patch.object(ShovelsClient, "_request", _mock_request)
    with patcher:
        yield
