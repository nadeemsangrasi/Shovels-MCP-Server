"""
HTTP client for the Shovels REST API (api.shovels.ai/v2).

Provides methods for searching and fetching permits, contractors,
decisions, and geo-resolution — all wrapped with retry logic,
credit header extraction, and cursor management.
"""

import httpx
from typing import Optional, Any
from urllib.parse import urlencode

from src.config.settings import settings
from src.utils.logger import get_logger
logger = get_logger(__name__)


class ShovelsClientError(Exception):
    """Raised on Shovels API errors."""


class ShovelsClient:
    """Lightweight async HTTP client for api.shovels.ai/v2."""

    def __init__(self, api_key: str, base_url: str = "https://api.shovels.ai/v2"):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")

    # ── Internal request helpers ──────────────────────────────

    def _headers(self) -> dict:
        return {"X-API-Key": self._api_key}

    def _extract_credits(self, response: httpx.Response) -> dict:
        """
        Pull X-Credits-* headers from the response.
        Returns a dict with raw header values (strings).
        """
        credits = {}
        for header in ("X-Credits-Request", "X-Credits-Limit", "X-Credits-Remaining"):
            value = response.headers.get(header)
            if value is not None:
                credits[header] = value
        return credits

    def _build_response(self, data: Any, response: httpx.Response, items_key: str = "items") -> dict:
        """
        Normalise a Shovels API response into our standard shape.

        Handles:
        - Search responses: {"items": [...], "size": N, "next_cursor": "..."}
        - Single-item responses: a dict (for fetch-by-id)
        """
        credits = self._extract_credits(response)

        if isinstance(data, list):
            # Direct array response — unlikely for v2 but handle gracefully
            return {
                "items": data,
                "size": len(data),
                "next_cursor": None,
                **credits,
            }

        if isinstance(data, dict):
            # Pass through the Shovels shape, merge credits
            result = dict(data)
            result.update(credits)
            return result

        return {"items": [], "size": 0, "next_cursor": None, **credits}

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
    ) -> dict:
        """
        Make an HTTP request to the Shovels API with retry on transient errors.

        Retries on network errors (ConnectionError, TimeoutError) with
        exponential backoff. API-level errors (4xx, 5xx, 429) propagate
        immediately as ShovelsClientError.
        """
        url = f"{self._base_url}/{path.lstrip('/')}"
        if params:
            # Filter out None values
            clean_params = {k: v for k, v in params.items() if v is not None}
            if clean_params:
                url = f"{url}?{urlencode(clean_params, doseq=True)}"

        last_error: Optional[Exception] = None
        for attempt in range(1, settings.MAX_RETRIES + 1):
            try:
                return await self._do_request(method, url)
            except (httpx.ConnectError, httpx.TimeoutException, httpx.RemoteProtocolError) as e:
                last_error = e
                if attempt < settings.MAX_RETRIES:
                    import asyncio
                    delay = 2.0 ** attempt  # exponential: 2, 4, 8...
                    logger.warning(
                        "Shovels API network error, retrying",
                        extra={"attempt": attempt, "delay": delay, "error": str(e)},
                    )
                    await asyncio.sleep(delay)
                continue

        # All retries exhausted — re-raise last network error
        if last_error:
            raise ShovelsClientError(
                f"Shovels API unreachable after {settings.MAX_RETRIES} attempts: {last_error}"
            ) from last_error

        # Should not reach here
        raise ShovelsClientError("Unexpected error in _request")

    async def _do_request(self, method: str, url: str) -> dict:
        """Single HTTP request to Shovels API — no retry logic."""
        logger.debug(
            "Shovels API request",
            extra={"method": method, "url": url},
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(method, url, headers=self._headers())

            # Extract credits even on error for visibility
            credits = self._extract_credits(response)

            if response.status_code == 429:
                logger.warning(
                    "Shovels API rate limited",
                    extra={"credits_remaining": credits.get("X-Credits-Remaining", "unknown")},
                )
                raise ShovelsClientError(
                    f"Rate limited (429) — {credits.get('X-Credits-Remaining', '?')} credits remaining"
                )

            if response.status_code >= 500:
                logger.error(
                    "Shovels API server error",
                    extra={"status": response.status_code, "body": response.text[:500]},
                )
                raise ShovelsClientError(
                    f"Shovels API error: HTTP {response.status_code}"
                )

            if response.status_code >= 400:
                detail = response.text[:500]
                logger.error(
                    "Shovels API client error",
                    extra={"status": response.status_code, "detail": detail},
                )
                raise ShovelsClientError(
                    f"Shovels API error {response.status_code}: {detail}"
                )

            data = response.json()
            return self._build_response(data, response)

    # ── Permits ───────────────────────────────────────────────

    async def search_permits(
        self,
        geo_id: str,
        permit_from: str,
        permit_to: str,
        permit_tags: Optional[list[str]] = None,
        permit_status: Optional[list[str]] = None,
        permit_min_job_value: Optional[int] = None,
        contractor_classification_derived: Optional[list[str]] = None,
        cursor: Optional[str] = None,
        size: int = 20,
    ) -> dict:
        """Search permits by geo and date range."""
        params = {
            "geo_id": geo_id,
            "permit_from": permit_from,
            "permit_to": permit_to,
            "size": size,
        }
        if permit_tags:
            params["permit_tags"] = permit_tags
        if permit_status:
            params["permit_status"] = permit_status
        if permit_min_job_value is not None:
            params["permit_min_job_value"] = permit_min_job_value
        if contractor_classification_derived:
            params["contractor_classification_derived"] = contractor_classification_derived
        if cursor:
            params["cursor"] = cursor

        return await self._request("GET", "permits/search", params)

    async def get_permits(self, ids: list[str]) -> dict:
        """Fetch full permit records by ID(s)."""
        # The spec shows GET /permits/{id} — for multiple IDs we fetch one by one
        # and return as items. For a single ID, return the single record.
        if len(ids) == 1:
            return await self._request("GET", f"permits/{ids[0]}")

        # Multiple IDs — parallel fetch
        import asyncio

        results = await asyncio.gather(
            *(self._request("GET", f"permits/{pid}") for pid in ids),
            return_exceptions=True,
        )
        items = []
        for pid, result in zip(ids, results):
            if isinstance(result, Exception):
                logger.error("Failed to fetch permit", extra={"id": pid, "error": str(result)})
                continue
            items.append(result)

        return {"items": items, "size": len(items), "next_cursor": None}

    # ── Contractors ───────────────────────────────────────────

    async def search_contractors(
        self,
        geo_id: str,
        permit_from: str,
        permit_to: str,
        contractor_classification_derived: Optional[list[str]] = None,
        contractor_name: Optional[str] = None,
        contractor_min_total_job_value: Optional[int] = None,
        cursor: Optional[str] = None,
        size: int = 20,
    ) -> dict:
        """Search contractors by geo and date range."""
        params = {
            "geo_id": geo_id,
            "permit_from": permit_from,
            "permit_to": permit_to,
            "size": size,
        }
        if contractor_classification_derived:
            params["contractor_classification_derived"] = contractor_classification_derived
        if contractor_name:
            params["contractor_name"] = contractor_name
        if contractor_min_total_job_value is not None:
            params["contractor_min_total_job_value"] = contractor_min_total_job_value
        if cursor:
            params["cursor"] = cursor

        return await self._request("GET", "contractors/search", params)

    async def get_contractors(self, ids: list[str]) -> dict:
        """Fetch full contractor records by ID(s)."""
        if len(ids) == 1:
            return await self._request("GET", f"contractors/{ids[0]}")

        import asyncio

        results = await asyncio.gather(
            *(self._request("GET", f"contractors/{cid}") for cid in ids),
            return_exceptions=True,
        )
        items = []
        for cid, result in zip(ids, results):
            if isinstance(result, Exception):
                logger.error("Failed to fetch contractor", extra={"id": cid, "error": str(result)})
                continue
            items.append(result)

        return {"items": items, "size": len(items), "next_cursor": None}

    # ── Decisions ─────────────────────────────────────────────

    async def search_decisions(
        self,
        geo_id: str,
        decision_from: str,
        decision_to: str,
        category: Optional[list[str]] = None,
        decision_q: Optional[str] = None,
        cursor: Optional[str] = None,
        size: int = 20,
    ) -> dict:
        """Search decisions by geo and date range."""
        params = {
            "geo_id": geo_id,
            "decision_from": decision_from,
            "decision_to": decision_to,
            "size": size,
        }
        if category:
            params["category"] = category
        if decision_q:
            params["decision_q"] = decision_q
        if cursor:
            params["cursor"] = cursor

        return await self._request("GET", "decisions/search", params)

    async def get_decisions(self, ids: list[str]) -> dict:
        """Fetch full decision records by ID(s)."""
        if len(ids) == 1:
            return await self._request("GET", f"decisions/{ids[0]}")

        import asyncio

        results = await asyncio.gather(
            *(self._request("GET", f"decisions/{did}") for did in ids),
            return_exceptions=True,
        )
        items = []
        for did, result in zip(ids, results):
            if isinstance(result, Exception):
                logger.error("Failed to fetch decision", extra={"id": did, "error": str(result)})
                continue
            items.append(result)

        return {"items": items, "size": len(items), "next_cursor": None}

    # ── Geo resolution ────────────────────────────────────────

    async def resolve_geo(self, query: str, level: Optional[str] = None) -> dict:
        """
        Resolve a free-text query to geo_id(s).

        When level is provided, hits the specific endpoint.
        When omitted, tries address first (most specific), then falls
        back through city → county → jurisdiction → state.
        """
        levels = (
            [level]
            if level
            else ["address", "city", "county", "jurisdiction", "state"]
        )

        for lvl in levels:
            try:
                result = await self._request(
                    "GET",
                    f"{lvl}s/search" if lvl != "address" else "addresses/search",
                    {"q": query, "size": 5},
                )
                items = result.get("items", result if isinstance(result, list) else [])
                if items:
                    return {"items": items, "level_matched": lvl, **self._extract_credits_from_result(result)}
            except ShovelsClientError as e:
                logger.debug(
                    "Geo level returned no results, trying next",
                    extra={"level": lvl, "error": str(e)},
                )
                continue

        return {"items": [], "next_cursor": None}

    def _extract_credits_from_result(self, result: dict) -> dict:
        """Pull credit keys from a response dict."""
        return {
            k: result.get(k)
            for k in ("X-Credits-Request", "X-Credits-Limit", "X-Credits-Remaining")
            if k in result
        }


# Singleton — lazily created on first use
_client: Optional[ShovelsClient] = None


def get_client() -> ShovelsClient:
    """
    Get the ShovelsClient singleton.

    The client is lazily initialised with credentials from settings.
    """
    global _client
    if _client is None:
        logger.info("Initialising ShovelsClient")
        _client = ShovelsClient(
            api_key=settings.SHOVELS_API_KEY,
            base_url=settings.SHOVELS_API_BASE,
        )
    return _client


def reset_client():
    """Force re-initialisation on next get_client() call (useful in tests)."""
    global _client
    _client = None
