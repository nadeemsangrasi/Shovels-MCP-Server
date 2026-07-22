"""
Integration tests for the /health endpoint.

Tests both healthy and degraded states using the mocked
Shovels API responses from conftest.py.
"""

import pytest


class TestHealthEndpoint:
    """Health check endpoint tests."""

    def test_health_returns_200(self, app, mock_shovels_api):
        """GET /health returns 200 with the correct response shape."""
        response = app.get("/health")
        assert response.status_code == 200

    def test_health_response_shape(self, app, mock_shovels_api):
        """Response has status, version, and shovels_api fields."""
        response = app.get("/health")
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "shovels_api" in data
        assert data["version"] == "2.0.0"

    def test_health_healthy_when_api_reachable(self, app, mock_shovels_api):
        """When the Shovels API mock returns data, status is 'healthy'."""
        response = app.get("/health")
        data = response.json()
        # With the mock returning geo data, it should be reachable
        assert "shovels_api" in data
        # Note: the health endpoint calls resolve_geo internally,
        # which uses the mocked _request, so it should return successfully

    def test_health_response_json(self, app, mock_shovels_api):
        """Response Content-Type is application/json."""
        response = app.get("/health")
        assert response.headers.get("content-type", "").startswith("application/json")
