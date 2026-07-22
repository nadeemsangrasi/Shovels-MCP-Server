"""
MCP tool definitions for the Shovels MCP Server.

Defines the four Shovels API tools that AI agents use to search
and retrieve permit, contractor, decision, and geo data.
"""

from typing import Optional

from src.mcp.server import mcp
from src.services.shovels_client import get_client, ShovelsClientError


# ── Helpers ──────────────────────────────────────────────

STATE_ABBREVIATIONS = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY",
}

# Decision categories as returned by the Shovels API (not user-guess names)
DECISION_CATEGORIES = [
    "spot_rezoning", "area_rezoning", "zoning_code_modification",
    "economic_development_incentives", "land_use_planning", "final_plat",
    "project_amendments", "city_properties", "variance", "conditional_use_permit",
]

# Common permit tag taxonomy
PERMIT_TAG_TAXONOMY = (
    "Common tags: new_construction, alteration, repair, electrical, plumbing, "
    "roofing, hvac, demolition, fire_suppression, grading, foundation, framing, "
    "solar, pool, fence, sign, landscaping, commercial, residential. "
    "Note: tags describe work type, not property classification."
)


def _guess_state_code(query: str) -> Optional[str]:
    """
    Check if a query looks like a misspelled state name and return the code.

    Returns the state code if a fuzzy match is found, None otherwise.
    """
    cleaned = query.strip().lower()
    # Direct abbreviation match
    if cleaned.upper() in STATE_ABBREVIATIONS.values():
        return cleaned.upper()
    # Full name match (including common misspellings)
    # Simple Levenshtein-like check: try exact first, then prefix match
    if cleaned in STATE_ABBREVIATIONS:
        return STATE_ABBREVIATIONS[cleaned]
    # Prefix match for common typos (e.g. "taxas" -> "texas")
    for name, code in STATE_ABBREVIATIONS.items():
        if cleaned == name[:len(cleaned)] and len(cleaned) >= 3:
            return code
        # Check for single-character typos
        if len(cleaned) == len(name) and sum(a != b for a, b in zip(cleaned, name)) == 1:
            return code
    return None


def _strip_nulls(data) -> dict:
    """Recursively remove null values from a response dict to reduce payload size."""
    if isinstance(data, dict):
        return {k: _strip_nulls(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [_strip_nulls(item) for item in data]
    return data


def _compact_items(items: list) -> list:
    """
    Return a compact version of each item — strips nulls and keeps key fields.
    """
    return [_strip_nulls(item) for item in items]


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
    property_type: Optional[str] = None,
    cursor: Optional[str] = None,
    size: int = 20,
) -> dict:
    """
    Search U.S. building permits.

    **Search mode**: Requires geo_id + permit_from + permit_to.
    Pass `permits_status`, `permit_tags`, `property_type` etc. to filter results.

    💰 All monetary values in **cents** (job_value, fees).

    🏷️ Tag taxonomy: new_construction, alteration, repair, electrical, plumbing,
    roofing, hvac, demolition, fire_suppression, solar, pool, etc.

    🏠 property_type values: commercial, residential, industrial, office,
    vacant_land, exempt, mixed_use.

    Args:
        geo_id: **Required.** State code (e.g. "TX"), ZIP (e.g. "78746"), or geo_id from shovels_geo.
        permit_from: **Required.** Start date (YYYY-MM-DD).
        permit_to: **Required.** End date (YYYY-MM-DD).
        ids: Permit IDs from a previous search — fetches full details.
        permit_tags: Filter by work-type tags (electrical, roofing, new_construction, etc.).
        permit_status: Filter by status: final, in_review, inactive, active.
        permit_min_job_value: Minimum job value in cents.
        contractor_classification_derived: Filter by contractor trade classification.
        property_type: Filter by property type: commercial, residential, industrial, office, vacant_land, exempt, mixed_use.
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
            return {"error": str(e), "note": "Direct ID lookup may not be supported for all permit IDs. Use search with geo_id + dates instead."}

    # Search mode — validate required params
    if not geo_id:
        return {"error": "geo_id is required. Use shovels_geo to resolve a location first."}
    if not permit_from:
        return {"error": "permit_from is required (YYYY-MM-DD)."}
    if not permit_to:
        return {"error": "permit_to is required (YYYY-MM-DD)."}

    try:
        result = await client.search_permits(
            geo_id=geo_id,
            permit_from=permit_from,
            permit_to=permit_to,
            permit_tags=permit_tags,
            permit_status=permit_status,
            permit_min_job_value=permit_min_job_value,
            contractor_classification_derived=contractor_classification_derived,
            property_type=property_type,
            cursor=cursor,
            size=min(size, 100),
        )
        # Compact: strip null fields to reduce payload
        if "items" in result:
            result["items"] = _compact_items(result["items"])
        return result
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

    🏷️ Trade classifications (for contractor_classification_derived):
    electrical, plumbing, general, roofing, hvac, concrete, framing, drywall,
    painting, flooring, landscaping, masonry, fencing, solar, demolition.

    Args:
        geo_id: **Required.** State code (e.g. "TX"), ZIP, or geo_id from shovels_geo.
        permit_from: **Required.** Start date (YYYY-MM-DD).
        permit_to: **Required.** End date (YYYY-MM-DD).
        ids: Contractor IDs from a previous search — fetches full details.
        contractor_classification_derived: Filter by trade (electrical, plumbing, general, roofing, etc.).
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
            return {"error": str(e), "note": "Direct ID lookup may not be supported for all contractor IDs. Use search with geo_id + dates instead."}

    # Search mode — validate required params
    if not geo_id:
        return {"error": "geo_id is required. Use shovels_geo to resolve a location."}
    if not permit_from:
        return {"error": "permit_from is required (YYYY-MM-DD)."}
    if not permit_to:
        return {"error": "permit_to is required (YYYY-MM-DD)."}

    try:
        result = await client.search_contractors(
            geo_id=geo_id,
            permit_from=permit_from,
            permit_to=permit_to,
            contractor_classification_derived=contractor_classification_derived,
            contractor_name=contractor_name,
            contractor_min_total_job_value=contractor_min_total_job_value,
            cursor=cursor,
            size=min(size, 100),
        )
        if "items" in result:
            result["items"] = _compact_items(result["items"])
        return result
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

    📋 Valid category values (not English names — use these exact strings):
    spot_rezoning, area_rezoning, zoning_code_modification,
    economic_development_incentives, land_use_planning, final_plat,
    project_amendments, city_properties, variance, conditional_use_permit.

    ℹ️ `decision_q` is capped at 100 characters — longer queries are truncated.

    Args:
        geo_id: **Required.** State or place geo_id only (ZIP not supported).
        decision_from: **Required.** Start date (YYYY-MM-DD).
        decision_to: **Required.** End date (YYYY-MM-DD).
        ids: Decision IDs from a previous search — fetches full details.
        category: Filter by exact API category (see valid values in description).
        decision_q: Text search (max 100 chars; longer input truncated).
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
            return {"error": str(e), "note": "Direct ID lookup may not be supported for all decision IDs. Use search with geo_id + dates instead."}

    # Search mode — validate required params
    if not geo_id:
        return {"error": "geo_id is required. Use shovels_geo to resolve a location."}
    if not decision_from:
        return {"error": "decision_from is required (YYYY-MM-DD)."}
    if not decision_to:
        return {"error": "decision_to is required (YYYY-MM-DD)."}

    # Truncate decision_q with a warning
    decision_q_clean = None
    q_warning = None
    if decision_q:
        if len(decision_q) > 100:
            q_warning = f"decision_q truncated from {len(decision_q)} to 100 characters"
            decision_q_clean = decision_q[:100]
        else:
            decision_q_clean = decision_q

    try:
        result = await client.search_decisions(
            geo_id=geo_id,
            decision_from=decision_from,
            decision_to=decision_to,
            category=category,
            decision_q=decision_q_clean,
            cursor=cursor,
            size=min(size, 100),
        )
        if "items" in result:
            result["items"] = _compact_items(result["items"])
        if q_warning:
            result["_warning"] = q_warning
        return result
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

    💡 For state-level queries, use 2-letter codes (e.g. "TX" not "Texas").
    🔍 Common typos are auto-corrected (e.g. "taxas" → "TX", "california" → "CA").

    Args:
        query: Address, city, 2-letter state code, county, or jurisdiction name.
        level: Pin to a resolver: address, city, county, jurisdiction, state.

    Returns:
        Geo results with geo_id — use as input to other tools.
    """
    # Validate empty query
    if not query or not query.strip():
        return {"error": "query is required. Provide a location (e.g. 'TX', 'Austin, TX')."}

    # Auto-correct state name typos
    state_code = _guess_state_code(query)
    if state_code and (level == "state" or (level is None and len(query) <= 5)):
        # If they seem to be asking for a state, use state level directly
        client = get_client()
        try:
            result = await client.resolve_geo(state_code, level="state")
            if result.get("items"):
                result["_note"] = f"Resolved '{query}' to state code '{state_code}'"
                return result
        except ShovelsClientError:
            pass

    client = get_client()
    try:
        result = await client.resolve_geo(query=query, level=level)

        # Surface a helpful note when query fell through to address
        if level is None and result.get("level_matched") == "address" and result.get("items"):
            result["_note"] = (
                "Resolved to address level (most specific). "
                "For broader results, try level='jurisdiction' or level='state'."
            )

        return result
    except ShovelsClientError as e:
        return {"error": str(e)}
