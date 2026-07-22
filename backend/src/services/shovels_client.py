"""
HTTP client for the Shovels REST API (api.shovels.ai/v2).

Provides methods for searching and fetching permits, contractors,
and geo-resolution — all wrapped with retry logic, credit header
extraction, and auto-pagination.
"""

import asyncio
import random
from typing import Optional, Any
from urllib.parse import urlencode

import httpx

from src.config.settings import settings
from src.utils.errors import ShovelsClientError, ShovelsClientRateLimited
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ShovelsClient:
    """Lightweight async HTTP client for api.shovels.ai/v2."""

    def __init__(self, api_key: str, base_url: str = "https://api.shovels.ai/v2"):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")

    # ── Internal request helpers ──────────────────────────────

    def _headers(self) -> dict:
        return {"X-API-Key": self._api_key}

    def _extract_credits(self, response: httpx.Response) -> dict:
        """Pull X-Credits-* headers from the response."""
        credits = {}
        for header in ("X-Credits-Request", "X-Credits-Limit", "X-Credits-Remaining"):
            value = response.headers.get(header)
            if value is not None:
                credits[header] = value
        return credits

    def _build_response(self, data: Any, response: httpx.Response) -> dict:
        """Normalise a Shovels API response into our standard shape."""
        credits = self._extract_credits(response)

        if isinstance(data, list):
            return {"items": data, "size": len(data), "next_cursor": None, **credits}

        if isinstance(data, dict):
            result = dict(data)
            result.update(credits)
            return result

        return {"items": [], "size": 0, "next_cursor": None, **credits}

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        no_retry: bool = False,
    ) -> dict:
        """
        Make an HTTP request to the Shovels API with retry on transient
        errors and (optionally) on rate limits.

        Retries on network errors (ConnectError, TimeoutException) with
        exponential backoff.  When *no_retry* is ``False`` (the default),
        also retries on HTTP 429 with jitter and Retry-After support.

        API-level errors (4xx, 5xx) that are not 429 or survive retry
        propagate as ``ShovelsClientError`` or ``ShovelsClientRateLimited``.
        """
        url = self._build_url(path, params)

        max_rate_retries = 1 if no_retry else settings.RATE_LIMIT_RETRY_MAX
        rate_attempts = 0
        network_attempts = 0

        while True:
            try:
                return await self._do_request(method, url)
            except ShovelsClientRateLimited as e:
                rate_attempts += 1
                credits_str = str(e) if hasattr(e, "args") and e.args else "?"
                if rate_attempts >= max_rate_retries:
                    raise

                # Calculate delay with jitter; prefer Retry-After header
                if e.retry_after is not None:
                    delay = e.retry_after + random.uniform(-0.5, 0.5)
                else:
                    delay = min(
                        settings.RATE_LIMIT_INITIAL_BACKOFF * (2.0 ** (rate_attempts - 1)),
                        settings.RATE_LIMIT_MAX_BACKOFF,
                    )
                    jitter = random.uniform(-delay * 0.25, delay * 0.25)
                    delay = max(0.1, delay + jitter)

                logger.warning(
                    "Rate limited, retrying",
                    extra={"attempt": rate_attempts, "delay": round(delay, 2)},
                )
                await asyncio.sleep(delay)

            except (httpx.ConnectError, httpx.TimeoutException, httpx.RemoteProtocolError) as e:
                network_attempts += 1
                if network_attempts >= settings.MAX_RETRIES:
                    raise ShovelsClientError(
                        f"Shovels API unreachable after {settings.MAX_RETRIES} attempts: {e}"
                    ) from e

                delay = 2.0 ** network_attempts
                logger.warning(
                    "Shovels API network error, retrying",
                    extra={"attempt": network_attempts, "delay": delay, "error": str(e)},
                )
                await asyncio.sleep(delay)

    async def _do_request(self, method: str, url: str, no_retry: bool = False) -> dict:
        """Single HTTP request to Shovels API — no retry logic, but handles
        429 via the typed error so the caller can decide whether to retry."""
        logger.debug("Shovels API request", extra={"method": method, "url": url})

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(method, url, headers=self._headers())
            credits = self._extract_credits(response)

            if response.status_code == 429:
                retry_after_str = response.headers.get("Retry-After")
                retry_after = float(retry_after_str) if retry_after_str else None
                remaining = credits.get("X-Credits-Remaining", "?")
                logger.warning(
                    "Shovels API rate limited",
                    extra={"credits_remaining": remaining, "retry_after": retry_after},
                )
                raise ShovelsClientRateLimited(
                    f"Rate limited (429) — {remaining} credits remaining",
                    retry_after=retry_after,
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

    def _build_url(self, path: str, params: Optional[dict] = None) -> str:
        """Build the full URL with query parameters, filtering out None values."""
        url = f"{self._base_url}/{path.lstrip('/')}"
        if params:
            clean = {k: v for k, v in params.items() if v is not None}
            if clean:
                url = f"{url}?{urlencode(clean, doseq=True)}"
        return url

    # ── Auto-pagination ───────────────────────────────────────

    async def _auto_paginate(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        limit: str = "50",
        max_records: int = 10000,
        no_retry: bool = False,
    ) -> dict:
        """
        Execute a search with ``limit``/``max_records`` semantics.

        When the effective target > 100, multiple pages are fetched
        automatically by following the cursor.  Each internal page is
        logged at DEBUG level.
        """
        # Parse limit
        target: int
        if limit == "all":
            target = max_records
        else:
            try:
                target = min(int(limit), max_records)
            except (ValueError, TypeError):
                target = settings.DEFAULT_LIMIT

        if target <= 100:
            params = dict(params or {})
            params["size"] = target
            return await self._request(method, path, params, no_retry=no_retry)

        # Accumulate pages
        all_items: list[dict] = []
        cursor: Optional[str] = None
        while len(all_items) < target:
            page_size = min(100, target - len(all_items))
            page_params = dict(params or {})
            page_params["size"] = page_size
            if cursor:
                page_params["cursor"] = cursor

            logger.debug(
                "Auto-paginate fetching page",
                extra={"path": path, "offset": len(all_items), "page_size": page_size},
            )
            result = await self._request(method, path, page_params, no_retry=no_retry)
            items = result.get("items", [])
            all_items.extend(items)
            cursor = result.get("next_cursor")
            if not cursor or not items:
                break

        return {"items": all_items, "size": len(all_items), "next_cursor": cursor}

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
        property_type: Optional[str] = None,
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
        if property_type:
            params["property_type"] = property_type
        if cursor:
            params["cursor"] = cursor

        return await self._request("GET", "permits/search", params)

    async def get_permits(self, ids: list[str]) -> dict:
        """Fetch full permit records by ID(s)."""
        if len(ids) == 1:
            return await self._request("GET", f"permits/{ids[0]}")

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

    async def contractor_permits(
        self,
        contractor_id: str,
        geo_id: str,
        permit_from: str,
        permit_to: str,
        limit: str = "50",
        max_records: int = 10000,
        no_retry: bool = False,
    ) -> dict:
        """List permits filed by a contractor."""
        params = {
            "geo_id": geo_id,
            "permit_from": permit_from,
            "permit_to": permit_to,
        }
        return await self._auto_paginate(
            "GET",
            f"contractors/{contractor_id}/permits",
            params,
            limit=limit,
            max_records=max_records,
            no_retry=no_retry,
        )

    async def contractor_employees(
        self,
        contractor_id: str,
        limit: str = "50",
        no_retry: bool = False,
    ) -> dict:
        """List employees of a contractor."""
        try:
            size = int(limit)
        except (ValueError, TypeError):
            size = settings.DEFAULT_LIMIT
        return await self._request(
            "GET",
            f"contractors/{contractor_id}/employees",
            {"size": size},
            no_retry=no_retry,
        )

    async def contractor_metrics(
        self,
        contractor_id: str,
        metric_from: str,
        metric_to: str,
        property_type: str,
        tag: str,
        no_retry: bool = False,
    ) -> dict:
        """Monthly performance metrics for a contractor."""
        params = {
            "metric_from": metric_from,
            "metric_to": metric_to,
            "property_type": property_type,
            "tag": tag,
        }
        return await self._request(
            "GET",
            f"contractors/{contractor_id}/metrics",
            params,
            no_retry=no_retry,
        )

    # ── Tags / usage (meta) ──────────────────────────────────

    async def tags_list(self, limit: int = 50, no_retry: bool = False) -> dict:
        """List valid permit tag values."""
        return await self._request("GET", "tags", {"size": limit}, no_retry=no_retry)

    async def usage(self, no_retry: bool = False) -> dict:
        """Show current API credit usage."""
        return await self._request("GET", "usage", no_retry=no_retry)

    # ── Geo resolution ────────────────────────────────────────

    async def resolve_geo(self, query: str, level: Optional[str] = None) -> dict:
        """Resolve a free-text query to geo_id(s)."""
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
    """Get the ShovelsClient singleton."""
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
