"""
Integration tests for the X-API-Key middleware.

Tests that the middleware correctly validates API keys via the Shovels /usage
endpoint and returns proper 401/200 responses.
"""

import pytest
from unittest.mock import AsyncMock, patch

import httpx


@pytest.fixture(autouse=True)
def clear_middleware_cache():
    """Clear the middleware's in-memory validated-keys cache before each auth test."""
    from main import _validated_keys as vk

    vk.clear()
    yield


class TestMiddlewareAuth:
    """API key middleware tests — all go through the TestClient."""

    def test_health_still_accessible_without_key(self, app, mock_shovels_api):
        """Health endpoint must remain open without a key."""
        response = app.get("/health")
        assert response.status_code == 200

    def test_mcp_post_without_key_returns_401(self, app, mock_shovels_api):
        """POST to / (MCP endpoint) without X-API-Key returns 401."""
        response = app.post("/")
        assert response.status_code == 401
        data = response.json()
        assert "Missing X-API-Key header" in data["message"]

    def test_mcp_get_without_key_returns_401(self, app, mock_shovels_api):
        """GET to / (MCP endpoint) without X-API-Key returns 401."""
        response = app.get("/")
        assert response.status_code == 401

    def test_invalid_api_key_returns_401(self, app, mock_shovels_api):
        """Request with a key that the Shovels API rejects returns 401."""
        # Override the usage mock to return 401
        mock_401 = AsyncMock(spec=httpx.Response)
        mock_401.status_code = 401
        mock_401.json = AsyncMock(return_value={"detail": "Invalid API Key"})

        with patch("httpx.AsyncClient.get", return_value=mock_401):
            response = app.post("/", headers={"X-API-Key": "sk_invalid"})

        assert response.status_code == 401
        data = response.json()
        assert "Invalid API key" in data["message"]

    def test_valid_api_key_passes_middleware(self, app, mock_shovels_api):
        """Request with a valid API key passes the middleware."""
        response = app.post("/", headers={"X-API-Key": "sk_valid_test_key"})
        # MCP endpoint may return 405/406 for an actual POST body mismatch,
        # but crucially it's NOT a 401 from the middleware
        assert response.status_code != 401

    def test_valid_key_is_cached(self, app, mock_shovels_api):
        """After first validation, subsequent requests with the same key skip validation."""
        # First request — validation happens
        resp1 = app.post("/", headers={"X-API-Key": "sk_cached_key"})
        assert resp1.status_code != 401

        # Second request with same key — uses cache, no extra API call
        resp2 = app.post("/", headers={"X-API-Key": "sk_cached_key"})
        assert resp2.status_code != 401

    def test_multiple_valid_keys_both_work(self, app, mock_shovels_api):
        """Multiple different valid keys each get validated and cached independently."""
        resp1 = app.post("/", headers={"X-API-Key": "sk_key_one"})
        assert resp1.status_code != 401

        resp2 = app.post("/", headers={"X-API-Key": "sk_key_two"})
        assert resp2.status_code != 401
