"""
Integration tests for MCP Resource handlers.

Tests the resource functions directly (not via MCP protocol).
Patches get_client() to return a mock with known responses.
"""

import pytest
from unittest.mock import patch, AsyncMock

from src.services.shovels_client import ShovelsClient
from src.utils.errors import ShovelsClientError
from src.mcp.tools import (
    get_permit_resource,
    get_contractor_resource,
)


# ── Fixtures ──────────────────────────────────────────────

@pytest.fixture
def mock_client():
    """Create a mock ShovelsClient with canned responses."""
    client = AsyncMock(spec=ShovelsClient)

    # Permits get
    client.get_permits.return_value = {
        "items": {
            "id": "p1",
            "number": "RE2303928",
            "type": "electrical",
            "status": "active",
            "job_value_cents": 500000,
            "description": "New electrical panel and sub-panel wiring",
            "fees_cents": 15000,
            "property_assess_market_value_cents": 450000,
            "property_year_built": 2010,
            "property_square_footage": 2000,
            "contractor_id": "cnt-1",
            "contractor_name": "ABC Electric",
            "city": "Austin",
            "state": "TX",
        },
        "X-Credits-Request": "1",
        "X-Credits-Remaining": "199",
    }

    # Contractors get
    client.get_contractors.return_value = {
        "items": {
            "id": "c1",
            "name": "ABC Construction",
            "classification_derived": "General",
            "license_number": "LIC-12345",
            "phone": "512-555-0100",
            "email": "contact@abcconstruction.com",
            "city": "Austin",
            "state": "TX",
            "total_job_value_cents": 5000000,
            "active_permits_count": 12,
        },
        "X-Credits-Request": "1",
        "X-Credits-Remaining": "199",
    }

    return client


@pytest.fixture(autouse=True)
def patch_get_client(mock_client):
    """Replace get_client() with a function returning mock_client."""
    with patch("src.mcp.tools.get_client", return_value=mock_client):
        yield


# ── shovels://permits/{permit_id} ─────────────────────────

class TestPermitResource:
    """Permit resource handler tests."""

    @pytest.mark.asyncio
    async def test_read_by_id_returns_full_record(self, mock_client):
        """Reading a permit resource returns full data (not compact)."""
        result = await get_permit_resource(permit_id="p1")
        assert "data" in result
        assert "meta" in result
        # Full record fields that would not be in compact search result
        assert result["data"]["description"] == "New electrical panel and sub-panel wiring"
        assert result["data"]["fees_cents"] == 15000
        assert result["data"]["property_year_built"] == 2010
        mock_client.get_permits.assert_called_once_with(["p1"])

    @pytest.mark.asyncio
    async def test_meta_contains_credits(self, mock_client):
        """Credits are propagated to the meta envelope."""
        result = await get_permit_resource(permit_id="p1")
        assert result["meta"]["credits_used"] == 1
        assert result["meta"]["credits_remaining"] == 199

    @pytest.mark.asyncio
    async def test_client_error_returns_structured_error(self, mock_client):
        """API errors are wrapped in the structured error envelope."""
        mock_client.get_permits.side_effect = ShovelsClientError("Not found")
        result = await get_permit_resource(permit_id="nonexistent")
        assert "error" in result
        assert "error_type" in result

    @pytest.mark.asyncio
    async def test_rate_limit_is_caught(self, mock_client):
        """Rate limit errors (subclass of ShovelsClientError) are caught."""
        mock_client.get_permits.side_effect = ShovelsClientError("Rate limited")
        result = await get_permit_resource(permit_id="p1")
        assert "error" in result


# ── shovels://contractors/{contractor_id} ─────────────────

class TestContractorResource:
    """Contractor resource handler tests."""

    @pytest.mark.asyncio
    async def test_read_by_id_returns_full_record(self, mock_client):
        """Reading a contractor resource returns full data (not compact)."""
        result = await get_contractor_resource(contractor_id="c1")
        assert "data" in result
        assert "meta" in result
        # Full record fields
        assert result["data"]["phone"] == "512-555-0100"
        assert result["data"]["email"] == "contact@abcconstruction.com"
        assert result["data"]["total_job_value_cents"] == 5000000
        assert result["data"]["active_permits_count"] == 12
        mock_client.get_contractors.assert_called_once_with(["c1"])

    @pytest.mark.asyncio
    async def test_meta_contains_credits(self, mock_client):
        """Credits are propagated to the meta envelope."""
        result = await get_contractor_resource(contractor_id="c1")
        assert result["meta"]["credits_used"] == 1
        assert result["meta"]["credits_remaining"] == 199

    @pytest.mark.asyncio
    async def test_client_error_returns_structured_error(self, mock_client):
        """API errors are wrapped in the structured error envelope."""
        mock_client.get_contractors.side_effect = ShovelsClientError("API error")
        result = await get_contractor_resource(contractor_id="bad")
        assert "error" in result
        assert "error_type" in result
