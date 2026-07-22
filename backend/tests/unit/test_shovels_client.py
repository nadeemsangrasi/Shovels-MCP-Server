"""
Unit tests for the Shovels API HTTP client.

Tests all public methods — search, fetch, geo resolution — with
mocked HTTP responses. Covers URL building, param passing, credit
header extraction, error handling, and the singleton pattern.
"""

import pytest
from unittest.mock import patch, AsyncMock
from httpx import Request, Response

from src.services.shovels_client import (
    ShovelsClient,
    ShovelsClientError,
    get_client,
    reset_client,
)


# ── Fixtures ──────────────────────────────────────────────

@pytest.fixture
def client():
    """Fresh ShovelsClient with a dummy API key for each test."""
    return ShovelsClient(api_key="test-key")


def _assert_url_contains(mock_request, substring: str):
    """Assert that the URL passed to httpx.AsyncClient.request contains text."""
    # The URL is the second positional argument (index 1)
    call_url = mock_request.call_args[0][1]
    assert substring in call_url, f"Expected '{substring}' in URL '{call_url}'"


def _mock_success(body: dict, status: int = 200, **extra_headers):
    """Create an AsyncMock that returns a successful response."""
    headers = {
        "X-Credits-Request": "1",
        "X-Credits-Limit": "250",
        "X-Credits-Remaining": "199",
        **extra_headers,
    }
    mock = AsyncMock()
    mock.return_value = Response(status_code=status, json=body, headers=headers)
    return mock


# ── _build_response ──────────────────────────────────────

class TestBuildResponse:
    """_build_response internal helper tests."""

    def test_dict_input_merges_credits(self, client):
        response = Response(200, json={"items": [{"id": "1"}]}, headers={
            "X-Credits-Remaining": "100",
        })
        result = client._build_response({"items": [{"id": "1"}]}, response)
        assert result["items"] == [{"id": "1"}]
        assert "X-Credits-Remaining" in result

    def test_list_input_wraps_in_items(self, client):
        response = Response(200, json=[{"id": "1"}], headers={
            "X-Credits-Remaining": "100",
        })
        result = client._build_response([{"id": "1"}], response)
        assert result["items"] == [{"id": "1"}]
        assert result["size"] == 1

    def test_credit_headers_mapped(self, client):
        """Verify all three credit headers appear in the response."""
        response = Response(200, json={"items": []}, headers={
            "X-Credits-Request": "1",
            "X-Credits-Limit": "250",
            "X-Credits-Remaining": "200",
        })
        result = client._build_response({"items": []}, response)
        assert result["X-Credits-Request"] == "1"
        assert result["X-Credits-Limit"] == "250"
        assert result["X-Credits-Remaining"] == "200"


# ── _extract_credits ─────────────────────────────────────

class TestExtractCredits:
    """Credit header extraction tests."""

    def test_extracts_all_headers(self, client):
        response = Response(200, json={}, headers={
            "X-Credits-Request": "1",
            "X-Credits-Limit": "250",
            "X-Credits-Remaining": "199",
        })
        credits = client._extract_credits(response)
        assert credits["X-Credits-Request"] == "1"
        assert credits["X-Credits-Limit"] == "250"
        assert credits["X-Credits-Remaining"] == "199"

    def test_missing_headers_omitted(self, client):
        response = Response(200, json={}, headers={})
        credits = client._extract_credits(response)
        assert credits == {}


# ── search_permits ───────────────────────────────────────

class TestSearchPermits:
    """Permits search method tests."""

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_required_params(self, mock_request, client):
        """Required params — geo_id, permit_from, permit_to — are passed in URL."""
        mock_request.return_value = Response(
            200,
            json={"items": [{"id": "p1"}], "size": 1},
            headers={"X-Credits-Remaining": "199"},
        )
        result = await client.search_permits(
            geo_id="geo_tx",
            permit_from="2026-01-01",
            permit_to="2026-06-30",
        )
        assert result["size"] == 1
        _assert_url_contains(mock_request, "geo_id=geo_tx")
        _assert_url_contains(mock_request, "permit_from=2026-01-01")
        _assert_url_contains(mock_request, "permit_to=2026-06-30")
        _assert_url_contains(mock_request, "permits/search")

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_optional_params(self, mock_request, client):
        """Optional filters are included when provided."""
        mock_request.return_value = Response(
            200,
            json={"items": [], "size": 0},
            headers={"X-Credits-Remaining": "199"},
        )
        await client.search_permits(
            geo_id="geo_tx",
            permit_from="2026-01-01",
            permit_to="2026-06-30",
            permit_tags=["roofing", "-electrical"],
            permit_status=["active"],
            permit_min_job_value=100000,
            contractor_classification_derived=["general"],
            cursor="next_page",
            size=5,
        )
        _assert_url_contains(mock_request, "permit_tags=roofing")
        _assert_url_contains(mock_request, "permit_status=active")
        _assert_url_contains(mock_request, "permit_min_job_value=100000")
        _assert_url_contains(mock_request, "cursor=next_page")
        _assert_url_contains(mock_request, "size=5")

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_credit_headers_in_response(self, mock_request, client):
        """Credit remaining info is surfaced in the response."""
        mock_request.return_value = Response(
            200,
            json={"items": [{"id": "p1"}], "size": 1},
            headers={
                "X-Credits-Request": "1",
                "X-Credits-Limit": "250",
                "X-Credits-Remaining": "199",
            },
        )
        result = await client.search_permits("geo_tx", "2026-01-01", "2026-06-30")
        assert result["X-Credits-Remaining"] == "199"
        assert result["X-Credits-Limit"] == "250"
        assert result["X-Credits-Request"] == "1"

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_method_is_get(self, mock_request, client):
        mock_request.return_value = Response(200, json={"items": [], "size": 0}, headers={})
        await client.search_permits("geo_tx", "2026-01-01", "2026-06-30")
        # First positional arg is the HTTP method
        assert mock_request.call_args[0][0] == "GET"

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_api_key_header_sent(self, mock_request, client):
        mock_request.return_value = Response(200, json={"items": [], "size": 0}, headers={})
        await client.search_permits("geo_tx", "2026-01-01", "2026-06-30")
        headers = mock_request.call_args[1].get("headers", {})
        assert headers.get("X-API-Key") == "test-key"


# ── get_permits ──────────────────────────────────────────

class TestGetPermits:
    """Permits fetch-by-ID tests."""

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_single_id(self, mock_request, client):
        """Single ID fetches /permits/{id} directly."""
        mock_request.return_value = Response(
            200,
            json={"id": "p1", "type": "electrical", "status": "active"},
            headers={"X-Credits-Remaining": "199"},
        )
        result = await client.get_permits(["p1"])
        assert result["id"] == "p1"
        _assert_url_contains(mock_request, "permits/p1")

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_multiple_ids(self, mock_request, client):
        """Multiple IDs — parallel fetches aggregated into items."""
        mock_request.side_effect = [
            Response(200, json={"id": "p1", "status": "active"}, headers={"X-Credits-Remaining": "199"}),
            Response(200, json={"id": "p2", "status": "final"}, headers={"X-Credits-Remaining": "198"}),
        ]
        result = await client.get_permits(["p1", "p2"])
        assert len(result["items"]) == 2
        assert result["items"][0]["id"] == "p1"
        assert result["items"][1]["id"] == "p2"

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_partial_failure_returns_valid_results(self, mock_request, client):
        """One ID fails — returns the successful ones."""
        mock_request.side_effect = [
            Response(200, json={"id": "p1", "status": "active"}, headers={}),
            ShovelsClientError("Not found"),
        ]
        result = await client.get_permits(["p1", "p2"])
        assert len(result["items"]) == 1
        assert result["items"][0]["id"] == "p1"


# ── search_contractors ───────────────────────────────────

class TestSearchContractors:
    """Contractors search tests (same pattern as permits)."""

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_required_params(self, mock_request, client):
        mock_request.return_value = Response(
            200,
            json={"items": [{"id": "c1"}], "size": 1},
            headers={"X-Credits-Remaining": "199"},
        )
        result = await client.search_contractors("geo_tx", "2026-01-01", "2026-06-30")
        assert result["size"] == 1
        _assert_url_contains(mock_request, "contractors/search")
        _assert_url_contains(mock_request, "geo_id=geo_tx")

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_optional_params(self, mock_request, client):
        mock_request.return_value = Response(200, json={"items": [], "size": 0}, headers={})
        await client.search_contractors(
            "geo_tx", "2026-01-01", "2026-06-30",
            contractor_classification_derived=["electrical"],
            contractor_name="ABC",
            contractor_min_total_job_value=500000,
            size=10,
        )
        _assert_url_contains(mock_request, "contractor_name=ABC")
        _assert_url_contains(mock_request, "contractor_min_total_job_value=500000")


# ── get_contractors ──────────────────────────────────────

class TestGetContractors:
    """Contractors fetch-by-ID tests."""

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_single_id(self, mock_request, client):
        mock_request.return_value = Response(200, json={"id": "c1"}, headers={})
        result = await client.get_contractors(["c1"])
        assert result["id"] == "c1"
        _assert_url_contains(mock_request, "contractors/c1")

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_multiple_ids(self, mock_request, client):
        mock_request.side_effect = [
            Response(200, json={"id": "c1"}, headers={}),
            Response(200, json={"id": "c2"}, headers={}),
        ]
        result = await client.get_contractors(["c1", "c2"])
        assert len(result["items"]) == 2


# ── search_decisions ─────────────────────────────────────

class TestSearchDecisions:
    """Decisions search tests."""

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_required_params(self, mock_request, client):
        mock_request.return_value = Response(200, json={"items": [], "size": 0}, headers={})
        await client.search_decisions("geo_ca", "2026-01-01", "2026-06-30")
        _assert_url_contains(mock_request, "decisions/search")
        _assert_url_contains(mock_request, "decision_from=2026-01-01")

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_decision_q_passed(self, mock_request, client):
        mock_request.return_value = Response(200, json={"items": [], "size": 0}, headers={})
        await client.search_decisions("geo_ca", "2026-01-01", "2026-06-30", decision_q="variance side yard")
        _assert_url_contains(mock_request, "decision_q=variance+side+yard")

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_category_filter(self, mock_request, client):
        mock_request.return_value = Response(200, json={"items": [], "size": 0}, headers={})
        await client.search_decisions("geo_ca", "2026-01-01", "2026-06-30", category=["Rezoning", "Variance"])
        _assert_url_contains(mock_request, "category=Rezoning")
        _assert_url_contains(mock_request, "category=Variance")


# ── get_decisions ────────────────────────────────────────

class TestGetDecisions:
    """Decisions fetch-by-ID tests."""

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_single_id(self, mock_request, client):
        mock_request.return_value = Response(200, json={"id": "d1"}, headers={})
        result = await client.get_decisions(["d1"])
        assert result["id"] == "d1"

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_multiple_ids(self, mock_request, client):
        mock_request.side_effect = [
            Response(200, json={"id": "d1"}, headers={}),
            Response(200, json={"id": "d2"}, headers={}),
        ]
        result = await client.get_decisions(["d1", "d2"])
        assert len(result["items"]) == 2


# ── resolve_geo ──────────────────────────────────────────

class TestResolveGeo:
    """Geo resolution tests — level targeting and fallback chain."""

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_with_level_state(self, mock_request, client):
        """When level is specified, only that endpoint is called."""
        mock_request.return_value = Response(200, json={
            "items": [{"geo_id": "geo_tx", "name": "Texas"}],
            "size": 1,
        }, headers={})
        result = await client.resolve_geo("Texas", level="state")
        assert result["level_matched"] == "state"
        _assert_url_contains(mock_request, "states/search")

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_with_level_address(self, mock_request, client):
        """Address level targets addresses/search."""
        mock_request.return_value = Response(200, json={
            "items": [{"geo_id": "a1"}], "size": 1,
        }, headers={})
        result = await client.resolve_geo("123 Main St", level="address")
        assert result["level_matched"] == "address"
        _assert_url_contains(mock_request, "addresses/search")

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_fallback_chain(self, mock_request, client):
        """No level — tries address first, falls through to state."""
        mock_request.side_effect = [
            ShovelsClientError("no results"),
            ShovelsClientError("no results"),
            ShovelsClientError("no results"),
            ShovelsClientError("no results"),
            Response(200, json={
                "items": [{"geo_id": "geo_tx", "name": "Texas"}],
                "size": 1,
            }, headers={}),
        ]
        result = await client.resolve_geo("Texas")
        assert result["level_matched"] == "state"
        assert mock_request.call_count == 5

    @patch("httpx.AsyncClient.request", new_callable=AsyncMock)
    async def test_address_match_stops_chain(self, mock_request, client):
        """Address match returns immediately, no further calls."""
        mock_request.return_value = Response(200, json={
            "items": [{"geo_id": "geo_addr_123", "name": "123 Main St"}],
            "size": 1,
        }, headers={})
        result = await client.resolve_geo("123 Main St, Austin TX")
        assert result["level_matched"] == "address"
        assert mock_request.call_count == 1


# ── Error handling ───────────────────────────────────────

class TestErrorHandling:
    """Error responses raise ShovelsClientError after retry exhaustion."""

    @pytest.mark.asyncio
    async def test_401_unauthorized(self, client):
        """401 is a ShovelsClientError."""
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = Response(
                401, json={"detail": "Missing API Key"}, headers={"X-Credits-Remaining": "249"},
            )
            with pytest.raises(ShovelsClientError, match="401"):
                await client.search_permits("geo_tx", "2026-01-01", "2026-06-30")

    @pytest.mark.asyncio
    async def test_429_rate_limit(self, client):
        """429 raises rate limit error."""
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = Response(
                429, json={"detail": "Too Many Requests"}, headers={"X-Credits-Remaining": "0"},
            )
            with pytest.raises(ShovelsClientError, match="Rate limited"):
                await client.search_permits("geo_tx", "2026-01-01", "2026-06-30")

    @pytest.mark.asyncio
    async def test_500_server_error(self, client):
        """5xx raises server error."""
        with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = Response(
                500, json={"detail": "Internal Server Error"}, headers={},
            )
            with pytest.raises(ShovelsClientError, match="500"):
                await client.search_permits("geo_tx", "2026-01-01", "2026-06-30")


# ── Singleton pattern ────────────────────────────────────

class TestSingleton:
    """get_client() / reset_client() tests."""

    def test_get_client_returns_same_instance(self):
        reset_client()
        c1 = get_client()
        c2 = get_client()
        assert c1 is c2

    def test_reset_client_forces_new_instance(self):
        reset_client()
        c1 = get_client()
        reset_client()
        c2 = get_client()
        assert c1 is not c2
