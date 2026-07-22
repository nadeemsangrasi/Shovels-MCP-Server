"""
MCP tool definitions for the Shovels MCP Server.

Defines the four Shovels API tools that AI agents use to search
and retrieve permit, contractor, decision, and geo data.
"""

from typing import Optional

from src.mcp.server import mcp
from src.services.shovels_client import get_client, ShovelsClientError


def _safe_call(fn, *args, **kwargs) -> dict:
    """Call an async function and return a clean error dict on ShovelsClientError."""
    try:
        return fn(*args, **kwargs)
    except ShovelsClientError as e:
        return {"error": str(e), "hint": "Check your parameters and try again."}


@mcp.tool()
async def shovels_permits(
    geo_id: Optional[str] = None,
    permit_from: Optional[str] = None,
    permit_to: Optional[str] = None,
    ids: Optional[list[str]] = None,
    permit_tags: Optional[list[str]] = None,
    permit_status: Optional[list[str]] = None,
    permit_min_job_value: Optional[int] = None,
    contractor_classification_derived: Optional[list[str]] = None,
    cursor: Optional[str] = None,
    size: int = 20,
) -> dict:
    """
    Search U.S. building permits.

    **Search mode**: Requires geo_id + permit_from + permit_to.
    Pass `permits_status`, `permit_tags`, etc. to filter results.

    💰 All monetary values in **cents** (job_value, fees).

    Args:
        geo_id: **Required.** State code (e.g. "TX"), ZIP, or geo_id from shovels_geo.
        permit_from: **Required.** Start date (YYYY-MM-DD).
        permit_to: **Required.** End date (YYYY-MM-DD).
        ids: Permit IDs from a previous search — fetches full details.
        permit_tags: Filter by tags. Prefix with '-' to exclude (e.g. '-roofing').
        permit_status: Filter by status: final, in_review, inactive, active.
        permit_min_job_value: Minimum job value in cents.
        contractor_classification_derived: Filter by contractor classification.
        cursor: Pagination cursor from a previous response.
        size: Results per page (max 100).

    Returns:
        Search results with credits_remaining info.
    """
    client = get_client()

    # Fetch mode
    if ids and len(ids) > 0:
        try:
            return await client.get_permits(ids)
        except ShovelsClientError as e:
            return {"error": str(e), "note": "The Shovels API may not support direct ID lookup for all permit IDs. Try searching with geo_id + dates instead."}

    # Search mode — validate required params
    if not geo_id:
        return {"error": "geo_id is required. Use shovels_geo to resolve a location first."}
    if not permit_from:
        return {"error": "permit_from is required (YYYY-MM-DD)."}
    if not permit_to:
        return {"error": "permit_to is required (YYYY-MM-DD)."}

    try:
        return await client.search_permits(
            geo_id=geo_id,
            permit_from=permit_from,
            permit_to=permit_to,
            permit_tags=permit_tags,
            permit_status=permit_status,
            permit_min_job_value=permit_min_job_value,
            contractor_classification_derived=contractor_classification_derived,
            cursor=cursor,
            size=min(size, 100),
        )
    except ShovelsClientError as e:
        return {"error": str(e)}


@mcp.tool()
async def shovels_contractors(
    geo_id: Optional[str] = None,
    permit_from: Optional[str] = None,
    permit_to: Optional[str] = None,
    ids: Optional[list[str]] = None,
    contractor_classification_derived: Optional[list[str]] = None,
    contractor_name: Optional[str] = None,
    contractor_min_total_job_value: Optional[int] = None,
    cursor: Optional[str] = None,
    size: int = 20,
) -> dict:
    """
    Search contractors active in a geography.

    **Search mode**: Requires geo_id + permit_from + permit_to.
    Pass `contractor_name` (min 3 chars) to narrow results.

    💰 Job values in **cents**.

    Args:
        geo_id: **Required.** State code (e.g. "TX"), ZIP, or geo_id from shovels_geo.
        permit_from: **Required.** Start date (YYYY-MM-DD).
        permit_to: **Required.** End date (YYYY-MM-DD).
        ids: Contractor IDs from a previous search — fetches full details.
        contractor_classification_derived: Filter by trade classification.
        contractor_name: Name search (min 3 chars).
        contractor_min_total_job_value: Minimum total job value in cents.
        cursor: Pagination cursor from a previous response.
        size: Results per page (max 100).

    Returns:
        Search results with credits_remaining info.
    """
    client = get_client()

    # Fetch mode
    if ids and len(ids) > 0:
        try:
            return await client.get_contractors(ids)
        except ShovelsClientError as e:
            return {"error": str(e), "note": "The Shovels API may not support direct ID lookup for all contractor IDs. Try searching with geo_id + dates instead."}

    # Search mode — validate required params
    if not geo_id:
        return {"error": "geo_id is required. Use shovels_geo to resolve a location."}
    if not permit_from:
        return {"error": "permit_from is required (YYYY-MM-DD)."}
    if not permit_to:
        return {"error": "permit_to is required (YYYY-MM-DD)."}

    try:
        return await client.search_contractors(
            geo_id=geo_id,
            permit_from=permit_from,
            permit_to=permit_to,
            contractor_classification_derived=contractor_classification_derived,
            contractor_name=contractor_name,
            contractor_min_total_job_value=contractor_min_total_job_value,
            cursor=cursor,
            size=min(size, 100),
        )
    except ShovelsClientError as e:
        return {"error": str(e)}


@mcp.tool()
async def shovels_decisions(
    geo_id: Optional[str] = None,
    decision_from: Optional[str] = None,
    decision_to: Optional[str] = None,
    ids: Optional[list[str]] = None,
    category: Optional[list[str]] = None,
    decision_q: Optional[str] = None,
    cursor: Optional[str] = None,
    size: int = 20,
) -> dict:
    """
    Search local zoning/land-use decisions (rezonings, variances).

    **Search mode**: Requires geo_id + decision_from + decision_to.
    ZIP codes are NOT supported — use state or place geo_id only.

    ℹ️ `decision_q` is capped at 100 characters.

    Args:
        geo_id: **Required.** State or place geo_id only (ZIP not supported).
        decision_from: **Required.** Start date (YYYY-MM-DD).
        decision_to: **Required.** End date (YYYY-MM-DD).
        ids: Decision IDs from a previous search — fetches full details.
        category: Filter by category (e.g. Rezoning, Variance).
        decision_q: Text search (max 100 chars).
        cursor: Pagination cursor from a previous response.
        size: Results per page (max 100).

    Returns:
        Search results with credits_remaining info.
    """
    client = get_client()

    # Fetch mode
    if ids and len(ids) > 0:
        try:
            return await client.get_decisions(ids[:50])
        except ShovelsClientError as e:
            return {"error": str(e), "note": "The Shovels API may not support direct ID lookup for all decision IDs. Try searching with geo_id + dates instead."}

    # Search mode — validate required params
    if not geo_id:
        return {"error": "geo_id is required. Use shovels_geo to resolve a location."}
    if not decision_from:
        return {"error": "decision_from is required (YYYY-MM-DD)."}
    if not decision_to:
        return {"error": "decision_to is required (YYYY-MM-DD)."}

    try:
        return await client.search_decisions(
            geo_id=geo_id,
            decision_from=decision_from,
            decision_to=decision_to,
            category=category,
            decision_q=decision_q[:100] if decision_q else None,
            cursor=cursor,
            size=min(size, 100),
        )
    except ShovelsClientError as e:
        return {"error": str(e)}


@mcp.tool()
async def shovels_geo(
    query: str,
    level: Optional[str] = None,
) -> dict:
    """
    Resolve free-text place names to Shovels geo_ids.

    **Required first step** before permits/contractors/decisions search,
    since those endpoints reject free-text addresses.

    When `level` is omitted, tries address first (most specific),
    then falls back through city → county → jurisdiction → state.

    💡 For city/state queries, use 2-letter state codes (e.g. "TX" not "Texas").

    Args:
        query: Address, city, state code, county, or jurisdiction name.
        level: Pin to a resolver: address, city, county, jurisdiction, state.

    Returns:
        Geo results with geo_id — use as input to other tools.
    """
    client = get_client()
    try:
        return await client.resolve_geo(query=query, level=level)
    except ShovelsClientError as e:
        return {"error": str(e)}
