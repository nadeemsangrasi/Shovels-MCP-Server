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
            "X-Credits-Request": "1",
        }
    if "contractors/search" in path:
        return {
            "items": [{"id": "c1", "name": "ABC Construction", "classification": "General"}],
            "size": 1, "next_cursor": None,
            "X-Credits-Request": "1", "X-Credits-Remaining": "198",
        }
    if "permits/" in path and "/search" not in path and "/metrics" not in path and "/employees" not in path:
        return {"id": "p1", "status": "active", "job_value_cents": 500000,
                "X-Credits-Request": "1", "X-Credits-Remaining": "198"}
    if "contractors/" in path and "/search" not in path and "/permits" not in path and "/employees" not in path and "/metrics" not in path:
        return {"id": "c1", "name": "ABC Construction", "classification_derived": "General",
                "X-Credits-Request": "1", "X-Credits-Remaining": "198"}
    if "tags" in path:
        return {
            "items": [{"tag": "new_construction", "description": "New building construction"},
                      {"tag": "alteration", "description": "Building alteration"}],
            "size": 2, "next_cursor": None,
            "X-Credits-Request": "1", "X-Credits-Remaining": "198",
        }
    if "usage" in path:
        return {"data": {"credits_used": 1, "credits_remaining": 198, "credits_limit": 250},
                "X-Credits-Request": "1", "X-Credits-Remaining": "198"}
    if "contractors/" in path and "/permits" in path:
        return {
            "items": [{"id": "p1", "number": "PERMIT-001", "type": "electrical", "status": "active"}],
            "size": 1, "next_cursor": None,
            "X-Credits-Request": "1", "X-Credits-Remaining": "198",
        }
    if "contractors/" in path and "/employees" in path:
        return {
            "items": [{"id": "e1", "name": "Jane Smith", "role": "Electrician"}],
            "size": 1, "next_cursor": None,
            "X-Credits-Request": "1", "X-Credits-Remaining": "198",
        }
    if "contractors/" in path and "/metrics" in path:
        return {
            "items": [{"month": "2026-01", "total_job_value_cents": 500000, "permit_count": 5}],
            "size": 1, "next_cursor": None,
            "X-Credits-Request": "1", "X-Credits-Remaining": "198",
        }
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
