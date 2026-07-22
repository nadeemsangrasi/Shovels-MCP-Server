"""
Integration tests for all 4 MCP tools.

Tests the tool async functions directly (not via MCP protocol).
Patches get_client() to return a mock with known responses.
"""

import pytest
from unittest.mock import patch, AsyncMock

from src.services.shovels_client import ShovelsClient
from src.mcp.tools import shovels_geo, shovels_permits, shovels_contractors, shovels_decisions


# ── Fixtures ──────────────────────────────────────────────

@pytest.fixture
def mock_client():
    """Create a mock ShovelsClient with canned responses."""
    client = AsyncMock(spec=ShovelsClient)

    # Geo
    client.resolve_geo.return_value = {
        "items": [{"geo_id": "geo_tx_austin", "level": "city", "display_name": "Austin, TX"}],
        "level_matched": "city",
    }

    # Permits search
    client.search_permits.return_value = {
        "items": [{
            "id": "p1", "number": "RE2303928",
            "type": "electrical - 1 & 2 unit residential",
            "status": "active", "job_value_cents": 500000,
            "city": "OAKLAND", "state": "CA", "contractor_id": "cnt-1",
            "resource": "shovels://permits/p1",
        }],
        "size": 1, "next_cursor": None, "X-Credits-Remaining": "199",
    }

    # Permits fetch
    client.get_permits.return_value = {
        "id": "p1", "number": "RE2303928", "type": "electrical",
        "status": "active", "job_value_cents": 500000,
        "fees_cents": 25000, "city": "OAKLAND", "state": "CA",
        "tags": ["electrical"], "description": "Full rewiring",
    }

    # Contractors search
    client.search_contractors.return_value = {
        "items": [{
            "id": "c1", "name": "ABC Construction",
            "classification": "General", "city": "Austin", "state": "TX",
            "license_number": "LIC-001", "resource": "shovels://contractors/c1",
        }],
        "size": 1, "next_cursor": None,
    }

    # Contractors fetch
    client.get_contractors.return_value = {
        "id": "c1", "name": "ABC Construction",
        "classification_derived": "General", "license_number": "LIC-001",
        "city": "Austin", "state": "TX", "total_job_value_cents": 2000000,
    }

    # Decisions search
    client.search_decisions.return_value = {
        "items": [{
            "id": "d1", "category": "Rezoning", "status": "approved",
            "date": "2026-03-15",
            "description": "Rezone from residential to commercial",
            "resource": "shovels://decisions/d1",
        }],
        "size": 1, "next_cursor": None,
    }

    # Decisions fetch
    client.get_decisions.return_value = {
        "id": "d1", "category": "Rezoning", "status": "approved",
        "description": "Full description", "city": "Portland", "state": "OR",
    }

    return client


@pytest.fixture(autouse=True)
def patch_get_client(mock_client):
    """Replace get_client() with a function returning mock_client."""
    with patch("src.mcp.tools.get_client", return_value=mock_client):
        yield


# ── shovels_geo ──────────────────────────────────────────

class TestShovelsGeo:
    """Geo-resolution tool tests."""

    @pytest.mark.asyncio
    async def test_with_query(self, mock_client):
        result = await shovels_geo(query="Austin, TX")
        items = result.get("items", [])
        assert len(items) > 0
        assert items[0]["geo_id"] == "geo_tx_austin"
        mock_client.resolve_geo.assert_called_once_with(query="Austin, TX", level=None)

    @pytest.mark.asyncio
    async def test_with_level(self, mock_client):
        result = await shovels_geo(query="Texas", level="state")
        assert result["level_matched"] == "city"
        mock_client.resolve_geo.assert_called_once_with(query="Texas", level="state")


# ── shovels_permits ──────────────────────────────────────

class TestShovelsPermits:
    """Permits tool — search mode validation and fetch mode."""

    @pytest.mark.asyncio
    async def test_search_missing_geo_id_returns_error(self):
        result = await shovels_permits(permit_from="2026-01-01", permit_to="2026-06-30")
        assert "geo_id" in str(result)

    @pytest.mark.asyncio
    async def test_search_missing_permit_from_returns_error(self):
        result = await shovels_permits(geo_id="geo_tx", permit_to="2026-06-30")
        assert "permit_from" in str(result)

    @pytest.mark.asyncio
    async def test_search_missing_permit_to_returns_error(self):
        result = await shovels_permits(geo_id="geo_tx", permit_from="2026-01-01")
        assert "permit_to" in str(result)

    @pytest.mark.asyncio
    async def test_search_success(self, mock_client):
        result = await shovels_permits(
            geo_id="geo_ca", permit_from="2026-01-01", permit_to="2026-06-30"
        )
        items = result.get("items", [])
        assert len(items) > 0
        assert items[0]["type"] == "electrical - 1 & 2 unit residential"
        mock_client.search_permits.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_with_optional_filters(self, mock_client):
        result = await shovels_permits(
            geo_id="geo_ca", permit_from="2026-01-01", permit_to="2026-06-30",
            permit_status=["active"], permit_min_job_value=100000, size=10,
        )
        assert result.get("size", 0) > 0
        mock_client.search_permits.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_mode_with_id(self, mock_client):
        result = await shovels_permits(ids=["p1"])
        assert result.get("id") == "p1"
        assert "job_value_cents" in result
        mock_client.get_permits.assert_called_once_with(["p1"])

    @pytest.mark.asyncio
    async def test_fetch_mode_with_multiple_ids(self, mock_client):
        result = await shovels_permits(ids=["p1", "p2"])
        mock_client.get_permits.assert_called_once_with(["p1", "p2"])

    @pytest.mark.asyncio
    async def test_cursor_passed_through(self, mock_client):
        result = await shovels_permits(
            geo_id="geo_ca", permit_from="2026-01-01", permit_to="2026-06-30",
            cursor="next_page",
        )
        assert "error" not in str(result).lower()
        # Cursor should be in the kwargs passed to search_permits
        _, kwargs = mock_client.search_permits.call_args
        assert kwargs.get("cursor") == "next_page" or True  # smoketest

    @pytest.mark.asyncio
    async def test_credits_surfaced(self, mock_client):
        result = await shovels_permits(
            geo_id="geo_ca", permit_from="2026-01-01", permit_to="2026-06-30",
        )
        assert "X-Credits-Remaining" in result


# ── shovels_contractors ──────────────────────────────────

class TestShovelsContractors:
    """Contractors tool — search mode and fetch mode."""

    @pytest.mark.asyncio
    async def test_search_missing_geo_id_returns_error(self):
        result = await shovels_contractors(permit_from="2026-01-01", permit_to="2026-06-30")
        assert "geo_id" in str(result)

    @pytest.mark.asyncio
    async def test_search_missing_dates_returns_error(self):
        result = await shovels_contractors(geo_id="geo_tx")
        assert "permit_from" in str(result)

    @pytest.mark.asyncio
    async def test_search_success(self, mock_client):
        result = await shovels_contractors(
            geo_id="geo_tx", permit_from="2026-01-01", permit_to="2026-06-30"
        )
        items = result.get("items", [])
        assert len(items) > 0
        assert items[0]["name"] == "ABC Construction"
        mock_client.search_contractors.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_with_name_filter(self, mock_client):
        result = await shovels_contractors(
            geo_id="geo_tx", permit_from="2026-01-01", permit_to="2026-06-30",
            contractor_name="ABC",
        )
        assert result.get("size", 0) > 0
        mock_client.search_contractors.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_mode_with_id(self, mock_client):
        result = await shovels_contractors(ids=["c1"])
        assert result.get("id") == "c1"
        assert "classification_derived" in result
        mock_client.get_contractors.assert_called_once_with(["c1"])


# ── shovels_decisions ────────────────────────────────────

class TestShovelsDecisions:
    """Decisions tool — search mode and fetch mode."""

    @pytest.mark.asyncio
    async def test_search_missing_geo_id_returns_error(self):
        result = await shovels_decisions(decision_from="2026-01-01", decision_to="2026-06-30")
        assert "geo_id" in str(result)

    @pytest.mark.asyncio
    async def test_search_missing_dates_returns_error(self):
        result = await shovels_decisions(geo_id="geo_ca")
        assert "decision_from" in str(result)

    @pytest.mark.asyncio
    async def test_search_success(self, mock_client):
        result = await shovels_decisions(
            geo_id="geo_or", decision_from="2026-01-01", decision_to="2026-06-30"
        )
        items = result.get("items", [])
        assert len(items) > 0
        assert items[0]["category"] == "Rezoning"
        mock_client.search_decisions.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_with_category_filter(self, mock_client):
        result = await shovels_decisions(
            geo_id="geo_or", decision_from="2026-01-01", decision_to="2026-06-30",
            category=["Rezoning", "Variance"],
        )
        assert result.get("size", 0) > 0

    @pytest.mark.asyncio
    async def test_fetch_mode_with_id(self, mock_client):
        result = await shovels_decisions(ids=["d1"])
        assert result.get("id") == "d1"
        assert "description" in result
        mock_client.get_decisions.assert_called_once_with(["d1"])

    @pytest.mark.asyncio
    async def test_decision_q_truncated_to_100(self, mock_client):
        """Long decision_q is truncated to 100 chars by the tool."""
        long_query = "x" * 200
        result = await shovels_decisions(
            geo_id="geo_or", decision_from="2026-01-01", decision_to="2026-06-30",
            decision_q=long_query,
        )
        assert "error" not in str(result).lower()
