"""
MCP tool definitions for the Shovels MCP Server.

Defines the four Shovels API tools that AI agents use to search
and retrieve permit, contractor, decision, and geo data.
"""

from src.mcp.server import mcp
from src.services.shovels_client import get_client


@mcp.tool()
async def shovels_permits(
    geo_id: str = None,
    permit_from: str = None,
    permit_to: str = None,
    ids: list[str] = None,
    permit_tags: list[str] = None,
    permit_status: list[str] = None,
    permit_min_job_value: int = None,
    contractor_classification_derived: list[str] = None,
    cursor: str = None,
    size: int = 20,
) -> dict:
    """
    Search U.S. building permits or fetch full permit records.

    **Search mode** (when `ids` is omitted — requires geo_id, permit_from, permit_to):
    Returns compact rows (id, number, type, status, job_value_cents, city, state, contractor_id, resource URI).
    Each result includes a `resource` URI — pass the `id` back to this tool to get the full record.

    **Fetch mode** (when `ids` is supplied):
    Returns the full permit record including all property_*, timing, fee, and tag fields.

    💰 All values in **cents** (job_value, fees, property_assess_market_value).

    Args:
        geo_id: **Required for search.** State code, ZIP, or geo_id from shovels_geo.
        permit_from: **Required for search.** Start date (YYYY-MM-DD).
        permit_to: **Required for search.** End date (YYYY-MM-DD).
        ids: One or more permit IDs — switches to fetch mode for full records.
        permit_tags: Filter by tags. Prefix with '-' to exclude (e.g. '-roofing').
        permit_status: Filter by status: final, in_review, inactive, active.
        permit_min_job_value: Minimum job value in **cents**.
        contractor_classification_derived: Filter by contractor classification.
        cursor: Pagination cursor from a previous response.
        size: Results per page (max 100).

    Returns:
        Search results or full record(s) with credits_remaining info.
    """
    client = get_client()

    # Fetch mode
    if ids and len(ids) > 0:
        return await client.get_permits(ids)

    # Search mode — validate required params
    if not geo_id:
        return {"error": "geo_id is required for search mode. Use shovels_geo to resolve a location first."}
    if not permit_from:
        return {"error": "permit_from is required for search mode (YYYY-MM-DD)."}
    if not permit_to:
        return {"error": "permit_to is required for search mode (YYYY-MM-DD)."}

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


@mcp.tool()
async def shovels_contractors(
    geo_id: str = None,
    permit_from: str = None,
    permit_to: str = None,
    ids: list[str] = None,
    contractor_classification_derived: list[str] = None,
    contractor_name: str = None,
    contractor_min_total_job_value: int = None,
    cursor: str = None,
    size: int = 20,
) -> dict:
    """
    Search contractors or fetch full contractor profiles.

    **Search mode** (when `ids` is omitted — requires geo_id, permit_from, permit_to):
    Returns compact rows (id, name, classification, city, state, license_number, resource URI).

    **Fetch mode** (when `ids` is supplied):
    Returns the full contractor profile including address, license info, total job value.

    💰 Job values in **cents**.
    ℹ️ `contractor_name` requires **3+ characters** (trigram index minimum).

    Args:
        geo_id: **Required for search.** State code, ZIP, or geo_id from shovels_geo.
        permit_from: **Required for search.** Start date (YYYY-MM-DD).
        permit_to: **Required for search.** End date (YYYY-MM-DD).
        ids: One or more contractor IDs — switches to fetch mode.
        contractor_classification_derived: Filter by trade classification.
        contractor_name: Name search (min 3 chars required by Shovels API).
        contractor_min_total_job_value: Minimum total job value in cents.
        cursor: Pagination cursor from a previous response.
        size: Results per page (max 100).

    Returns:
        Search results or full record(s) with credits_remaining info.
    """
    client = get_client()

    # Fetch mode
    if ids and len(ids) > 0:
        return await client.get_contractors(ids)

    # Search mode — validate required params
    if not geo_id:
        return {"error": "geo_id is required for search mode. Use shovels_geo to resolve a location."}
    if not permit_from:
        return {"error": "permit_from is required for search mode (YYYY-MM-DD)."}
    if not permit_to:
        return {"error": "permit_to is required for search mode (YYYY-MM-DD)."}

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


@mcp.tool()
async def shovels_decisions(
    geo_id: str = None,
    decision_from: str = None,
    decision_to: str = None,
    ids: list[str] = None,
    category: list[str] = None,
    decision_q: str = None,
    cursor: str = None,
    size: int = 20,
) -> dict:
    """
    Search local zoning/land-use decisions or fetch full decision records.

    **Search mode** (when `ids` is omitted — requires geo_id, decision_from, decision_to):
    Returns compact rows (id, category, status, date, description, resource URI).

    **Fetch mode** (when `ids` is supplied, max 50):
    Returns the full decision record including address, geo_id, and description.

    ⚠️ **ZIP codes are NOT supported** for decisions — use state or place geo_id only.
    ℹ️ `decision_q` is capped at **100 characters**.

    Args:
        geo_id: **Required for search.** State or place geo_id only (ZIP not supported).
        decision_from: **Required for search.** Start date (YYYY-MM-DD).
        decision_to: **Required for search.** End date (YYYY-MM-DD).
        ids: Decision IDs (max 50) — switches to fetch mode.
        category: Filter by category (e.g. Rezoning, Variance).
        decision_q: Text search query (max 100 chars).
        cursor: Pagination cursor from a previous response.
        size: Results per page (max 100).

    Returns:
        Search results or full record(s) with credits_remaining info.
    """
    client = get_client()

    # Fetch mode
    if ids and len(ids) > 0:
        return await client.get_decisions(ids[:50])

    # Search mode — validate required params
    if not geo_id:
        return {"error": "geo_id is required for search mode. Use shovels_geo to resolve a location."}
    if not decision_from:
        return {"error": "decision_from is required for search mode (YYYY-MM-DD)."}
    if not decision_to:
        return {"error": "decision_to is required for search mode (YYYY-MM-DD)."}

    return await client.search_decisions(
        geo_id=geo_id,
        decision_from=decision_from,
        decision_to=decision_to,
        category=category,
        decision_q=decision_q[:100] if decision_q else None,
        cursor=cursor,
        size=min(size, 100),
    )


@mcp.tool()
async def shovels_geo(
    query: str,
    level: str = None,
) -> dict:
    """
    Resolve free-text place names to Shovels geo_ids.

    **Required first step** before any permits/contractors/decisions search,
    since those endpoints reject free-text addresses.

    When no `level` is specified, the tool tries address first (most specific),
    then falls back through city → county → jurisdiction → state.

    Args:
        query: Free-text address, city, county, jurisdiction, or state name.
        level: Optional. Pin to a specific resolver: address, city, county, jurisdiction, state.

    Returns:
        Geo results with geo_id, level, display_name.
        Use the `geo_id` value as input to shovels_permits / shovels_contractors / shovels_decisions.
    """
    client = get_client()
    return await client.resolve_geo(query=query, level=level)
