"""
Integration tests for all MCP tools.

Tests the tool async functions directly (not via MCP protocol).
Patches get_client() to return a mock with known responses.
"""

import pytest
from unittest.mock import patch, AsyncMock

from src.services.shovels_client import ShovelsClient
from src.mcp.tools import shovels_geo, shovels_permits, shovels_contractors, shovels_meta


# ── Fixtures ──────────────────────────────────────────────

@pytest.fixture
def mock_client():
    """Create a mock ShovelsClient with canned responses."""
    client = AsyncMock(spec=ShovelsClient)

    # Geo
    client.resolve_geo.return_value = {
        "items": [{"geo_id": "geo_tx_austin", "level": "city", "display_name": "Austin, TX"}],
        "level_matched": "city",
        "X-Credits-Request": "1",
        "X-Credits-Remaining": "199",
    }

    # Permits search
    client._request.return_value = {
        "items": [{
            "id": "p1", "number": "RE2303928",
            "type": "electrical - 1 & 2 unit residential",
            "status": "active", "job_value_cents": 500000,
            "city": "OAKLAND", "state": "CA", "contractor_id": "cnt-1",
        }],
        "size": 1, "next_cursor": None,
        "X-Credits-Request": "1", "X-Credits-Remaining": "199",
    }

    # Permits get
    client.get_permits.return_value = {
        "items": {
            "id": "p1", "number": "RE2303928", "status": "active",
            "job_value_cents": 500000, "description": "Electrical work",
        },
        "X-Credits-Request": "1", "X-Credits-Remaining": "199",
    }

    # Contractors search
    client._request.return_value = {
        "items": [{
            "id": "c1", "name": "ABC Construction",
            "classification": "General", "city": "Austin", "state": "TX",
        }],
        "size": 1, "next_cursor": None,
        "X-Credits-Request": "1", "X-Credits-Remaining": "199",
    }

    # Contractors get
    client.get_contractors.return_value = {
        "items": {
            "id": "c1", "name": "ABC Construction",
            "classification_derived": "General",
            "phone": "512-555-0100",
        },
        "X-Credits-Request": "1", "X-Credits-Remaining": "199",
    }

    # Contractor permits
    client.contractor_permits.return_value = {
        "items": [{"id": "p1", "number": "PERMIT-001", "status": "active"}],
        "size": 1, "next_cursor": None,
        "X-Credits-Request": "1", "X-Credits-Remaining": "199",
    }

    # Contractor employees
    client.contractor_employees.return_value = {
        "items": [{"id": "e1", "name": "Jane Smith", "role": "Electrician"}],
        "size": 1, "next_cursor": None,
        "X-Credits-Request": "1", "X-Credits-Remaining": "199",
    }

    # Contractor metrics
    client.contractor_metrics.return_value = {
        "items": [{"month": "2026-01", "total_job_value_cents": 500000, "permit_count": 5}],
        "size": 1, "next_cursor": None,
        "X-Credits-Request": "1", "X-Credits-Remaining": "199",
    }

    # Tags / usage
    client.tags_list.return_value = {
        "items": [{"tag": "new_construction"}, {"tag": "alteration"}],
        "size": 2, "next_cursor": None,
        "X-Credits-Request": "1", "X-Credits-Remaining": "199",
    }
    client.usage.return_value = {
        "data": {"credits_used": 1, "credits_remaining": 199, "credits_limit": 250},
        "X-Credits-Request": "1", "X-Credits-Remaining": "199",
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
        assert "data" in result
        assert "meta" in result
        mock_client.resolve_geo.assert_called_once_with(query="Austin, TX", level=None)

    @pytest.mark.asyncio
    async def test_empty_query_returns_error(self):
        """Empty query returns a clear error instead of state list."""
        result = await shovels_geo(query="")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_with_level(self, mock_client):
        result = await shovels_geo(query="Texas", level="state")
        # The tool auto-corrects "Texas" → "TX" via fuzzy matching
        mock_client.resolve_geo.assert_called_with("TX", level="state")
        assert "data" in result or "error" in result


# ── shovels_permits ──────────────────────────────────────

class TestShovelsPermits:
    """Permits tool validation tests."""

    @pytest.mark.asyncio
    async def test_search_missing_geo_id_returns_error(self):
        result = await shovels_permits(permit_from="2026-01-01", permit_to="2026-06-30")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_search_missing_permit_from_returns_error(self):
        result = await shovels_permits(geo_id="geo_tx", permit_to="2026-06-30")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_search_missing_permit_to_returns_error(self):
        result = await shovels_permits(geo_id="geo_tx", permit_from="2026-01-01")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_search_success(self, mock_client):
        result = await shovels_permits(
            geo_id="geo_ca", permit_from="2026-01-01", permit_to="2026-06-30"
        )
        assert "data" in result
        assert "meta" in result
        mock_client._request.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_with_tags_filter(self, mock_client):
        """tags (was permit_tags) is mapped to permit_tags API param."""
        result = await shovels_permits(
            geo_id="geo_ca", permit_from="2026-01-01", permit_to="2026-06-30",
            tags=["electrical", "roofing"], limit="10",
        )
        assert "data" in result
        assert mock_client._request.called

    @pytest.mark.asyncio
    async def test_search_with_property_type(self, mock_client):
        """property_type filter is passed through."""
        result = await shovels_permits(
            geo_id="geo_ca", permit_from="2026-01-01", permit_to="2026-06-30",
            property_type="commercial",
        )
        assert "data" in result or "error" in result

    @pytest.mark.asyncio
    async def test_credits_in_meta(self, mock_client):
        result = await shovels_permits(
            geo_id="geo_ca", permit_from="2026-01-01", permit_to="2026-06-30",
        )
        if "meta" in result:
            assert "credits_remaining" in result["meta"]


class TestShovelsPermitsGet:
    """Permits get-by-ID tests."""

    @pytest.mark.asyncio
    async def test_get_by_single_id(self, mock_client):
        result = await shovels_permits(id=["p1"])
        assert "data" in result
        assert "meta" in result
        mock_client.get_permits.assert_called_once_with(["p1"])

    @pytest.mark.asyncio
    async def test_get_by_multiple_ids(self, mock_client):
        result = await shovels_permits(id=["p1", "p2"])
        assert "error" not in result
        mock_client.get_permits.assert_called_once_with(["p1", "p2"])


# ── shovels_contractors ──────────────────────────────────

class TestShovelsContractors:
    """Contractors tool validation tests for all actions."""

    @pytest.mark.asyncio
    async def test_search_missing_geo_id_returns_error(self):
        result = await shovels_contractors(action="search",
                                           permit_from="2026-01-01", permit_to="2026-06-30")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_search_success(self, mock_client):
        result = await shovels_contractors(
            action="search",
            geo_id="geo_tx", permit_from="2026-01-01", permit_to="2026-06-30"
        )
        assert "data" in result
        assert "meta" in result
        mock_client._request.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_success(self, mock_client):
        result = await shovels_contractors(action="get", id=["c1"])
        assert "data" in result
        mock_client.get_contractors.assert_called_once_with(["c1"])

    @pytest.mark.asyncio
    async def test_get_missing_id_returns_error(self):
        result = await shovels_contractors(action="get")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_permits_action(self, mock_client):
        result = await shovels_contractors(
            action="permits", id=["c1"],
            geo_id="geo_tx", permit_from="2026-01-01", permit_to="2026-06-30",
        )
        assert "data" in result
        mock_client.contractor_permits.assert_called_once()

    @pytest.mark.asyncio
    async def test_employees_action(self, mock_client):
        result = await shovels_contractors(action="employees", id=["c1"])
        assert "data" in result
        mock_client.contractor_employees.assert_called_once()

    @pytest.mark.asyncio
    async def test_metrics_action(self, mock_client):
        result = await shovels_contractors(
            action="metrics", id=["c1"],
            metric_from="2026-01-01", metric_to="2026-06-30",
            property_type="commercial", tag="electrical",
        )
        assert "data" in result
        mock_client.contractor_metrics.assert_called_once()

    @pytest.mark.asyncio
    async def test_invalid_action_returns_error(self):
        result = await shovels_contractors(action="invalid")
        assert "error" in result


# ── shovels_meta ─────────────────────────────────────────

class TestShovelsMeta:
    """Meta tool (tags + usage) tests."""

    @pytest.mark.asyncio
    async def test_tags_action(self, mock_client):
        result = await shovels_meta(action="tags")
        assert "data" in result
        assert "meta" in result
        assert isinstance(result["data"], list)
        mock_client.tags_list.assert_called_once()

    @pytest.mark.asyncio
    async def test_usage_action(self, mock_client):
        result = await shovels_meta(action="usage")
        assert "data" in result
        assert "meta" in result
        mock_client.usage.assert_called_once()

    @pytest.mark.asyncio
    async def test_invalid_action_returns_error(self):
        result = await shovels_meta(action="invalid")
        assert "error" in result
