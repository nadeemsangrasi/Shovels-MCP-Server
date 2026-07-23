"""
MCP tool definitions for the Shovels MCP Server.

Defines the four Shovels API tools that AI agents use to search
and retrieve permit, contractor, geo, and meta data.
"""

from typing import Optional

from src.config.settings import settings
from src.mcp.server import mcp
from src.services.shovels_client import get_client
from src.utils.errors import ShovelsClientError, format_error
from src.utils.response import build_data_meta


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


# Common permit tag taxonomy
PERMIT_TAG_TAXONOMY = (
    "Common tags: new_construction, alteration, repair, electrical, plumbing, "
    "roofing, hvac, demolition, fire_suppression, grading, foundation, framing, "
    "solar, pool, fence, sign, landscaping, commercial, residential. "
    "Note: tags describe work type, not property classification."
)


def _guess_state_code(query: str) -> Optional[str]:
    """
    Check if a query looks like a state name (full name, abbreviation, or typo).

    Returns the state code if a match is found, None otherwise.
    """
    cleaned = query.strip().lower()
    # Direct abbreviation match (e.g. "TX", "CA")
    if cleaned.upper() in STATE_ABBREVIATIONS.values():
        return cleaned.upper()
    # Full name match (e.g. "california", "Texas")
    if cleaned in STATE_ABBREVIATIONS:
        return STATE_ABBREVIATIONS[cleaned]
    # Prefix match for common typos (e.g. "taxas" -> "texas")
    for name, code in STATE_ABBREVIATIONS.items():
        if cleaned == name[:len(cleaned)] and len(cleaned) >= 3:
            return code
        # Check for single-character typos (e.g. "californa" -> "california")
        if len(cleaned) == len(name) and sum(a != b for a, b in zip(cleaned, name)) <= 2:
            return code
    return None


def _strip_nulls(data) -> dict:
    """Recursively remove null values from a response dict to reduce payload size."""
    if isinstance(data, dict):
        return {k: _strip_nulls(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [_strip_nulls(item) for item in data]
    return data


def _compact_permit(item: dict) -> dict:
    """
    Reduce a full permit record to the compact search-mode shape
    defined in the MVP spec — keeps token cost low until the agent
    fetches the full record by ID.
    Handles both nested ``address`` dict and flat top-level fields.
    """
    address = item.get("address", {})
    if isinstance(address, dict):
        city = address.get("city") or item.get("city")
        state = address.get("state") or item.get("state")
    else:
        city = item.get("city")
        state = item.get("state")
    return _strip_nulls({
        "id": item.get("id"),
        "number": item.get("number"),
        "type": item.get("type"),
        "status": item.get("status"),
        "job_value_cents": item.get("job_value_cents") or item.get("job_value"),
        "city": city,
        "state": state,
        "contractor_id": item.get("contractor_id"),
        "resource": f"shovels://permits/{item.get('id')}",
    })


def _compact_contractor(item: dict) -> dict:
    """
    Reduce a full contractor record to the compact search-mode shape.
    Handles address in both nested ``address`` dict and flat top-level fields.
    """
    address = item.get("address", {})
    if isinstance(address, dict) and address.get("city"):
        city = address.get("city")
        state = address.get("state")
    else:
        city = item.get("city")
        state = item.get("state")

    # classification can be a string or a list of one string
    classification = item.get("classification_derived")
    if isinstance(classification, list):
        classification = classification[0] if classification else item.get("classification")
    elif not classification:
        classification = item.get("classification")

    return _strip_nulls({
        "id": item.get("id"),
        "name": item.get("name") or item.get("business_name"),
        "classification": classification,
        "city": city,
        "state": state,
        "license_number": item.get("license_number") or item.get("license"),
        "resource": f"shovels://contractors/{item.get('id')}",
    })


def _compact_tool_items(items: list, tool: str) -> list:
    """
    Compact search results by tool type to reduce token payload.
    Each item gets a ``resource`` URI for full-record retrieval.
    """
    if tool == "permits":
        return [_compact_permit(item) for item in items]
    if tool == "contractors":
        return [_compact_contractor(item) for item in items]
    # Default: just strip nulls
    return [_strip_nulls(item) for item in items]


def _build_search_envelope(result: dict, tool: str) -> dict:
    """
    Convert a search result into the ``{data, meta}`` envelope
    with compact items per the progressive-disclosure design.
    """
    items = result.get("items", [])
    credits_used = int(result.get("X-Credits-Request", 0))
    credits_remaining = int(result.get("X-Credits-Remaining", 0))

    return build_data_meta(
        _compact_tool_items(items, tool),
        credits_used=credits_used,
        credits_remaining=credits_remaining,
        count=len(items),
        has_more=result.get("next_cursor") is not None,
    )


def _build_single_envelope(result: dict) -> dict:
    """
    Convert a get-by-ID result into the ``{data, meta}`` envelope
    with the full record (no compaction).

    Handles two shapes from the client:
    - Flat dict (single-ID get): ``{"id": "p1", "type": ..., "X-Credits-*": ...}``
    - List-wrapped (multi-ID get): ``{"items": [{"id": "p1"}], ...}``
    """
    credits_used = int(result.get("X-Credits-Request", 0))
    credits_remaining = int(result.get("X-Credits-Remaining", 0))

    # Multi-ID get wraps in "items" list
    if "items" in result:
        items = result["items"]
        if isinstance(items, dict):
            # Single item wrapped in a dict (some endpoints do this)
            data = _strip_nulls(items)
        elif isinstance(items, list) and len(items) == 1:
            data = _strip_nulls(items[0])
        elif isinstance(items, list) and len(items) > 1:
            # Return as list for multi-ID
            return build_data_meta(
                _strip_nulls(items),
                credits_used=credits_used,
                credits_remaining=credits_remaining,
                count=len(items),
                has_more=False,
            )
        else:
            data = _strip_nulls(items) if items else {}
    else:
        # Flat dict — single-ID get returns credits merged in
        data = _strip_nulls({k: v for k, v in result.items()
                            if not k.startswith("X-")})

    return build_data_meta(
        data,
        credits_used=credits_used,
        credits_remaining=credits_remaining,
    )


def _parse_size(limit_str: str) -> int:
    """
    Parse a ``limit`` value into a page size (1-100, default 50).

    Each MCP tool call returns at most one page (capped at 100).
    Pass ``cursor`` to get the next page.
    """
    if not limit_str or limit_str.strip() == "":
        return settings.DEFAULT_LIMIT

    if limit_str == "all":
        return 100  # max page size

    try:
        val = int(limit_str)
        if val < 1:
            val = 1
        return min(val, 100)
    except (ValueError, TypeError):
        return settings.DEFAULT_LIMIT


def _build_search_envelope(result: dict, tool: str) -> dict:
    """
    Convert a search result into the ``{data, meta}`` envelope
    with compact items per the progressive-disclosure design.
    """
    items = result.get("items", [])
    credits_used = int(result.get("X-Credits-Request", 0))
    credits_remaining = int(result.get("X-Credits-Remaining", 0))

    return build_data_meta(
        _compact_tool_items(items, tool),
        credits_used=credits_used,
        credits_remaining=credits_remaining,
        count=len(items),
        has_more=result.get("next_cursor") is not None,
        cursor=result.get("next_cursor"),
    )


# ── shovels_permits ─────────────────────────────────────

@mcp.tool()
async def shovels_permits(
    id: Optional[list[str]] = None,
    geo_id: Optional[str] = None,
    permit_from: Optional[str] = None,
    permit_to: Optional[str] = None,
    tags: Optional[list[str]] = None,
    permit_status: Optional[list[str]] = None,
    property_type: Optional[str] = None,
    min_job_value: Optional[int] = None,
    cursor: Optional[str] = None,
    include_count: bool = False,
    limit: str = "50",
    no_retry: bool = False,
) -> dict:
    """
    Search U.S. building permits by location, date, type, value;
    or fetch full records by ID.

    **Requires geo_id + permit_from + permit_to for search.**
    Pass ``id`` to fetch full records by ID instead of searching.

    💰 All monetary values in **cents** (job_value).

    🏷️ Tag taxonomy: new_construction, alteration, repair, electrical,
    plumbing, roofing, hvac, demolition, fire_suppression, solar, pool, etc.

    🏠 property_type values: commercial, residential, industrial, office,
    vacant_land, exempt, mixed_use.

    🔍 permit_status: final, in_review, active, inactive.

    Pagination: each call returns one page (max 100 records). Pass
    ``cursor`` (from ``meta.cursor`` of the previous page) to get the
    next page.  ``limit`` controls page size (1-100, default 50).

    Args:
        id: 1-50 permit IDs. Present = fetch mode (get by ID).
        geo_id: Required for search. State code, ZIP, or geo_id from shovels_geo.
        permit_from: Required for search. Start date (YYYY-MM-DD).
        permit_to: Required for search. End date (YYYY-MM-DD).
        tags: Filter by work-type tags (electrical, roofing, etc.).
        permit_status: Filter by status (final, in_review, active, inactive).
        property_type: Filter by property type.
        min_job_value: Minimum job value in cents.
        cursor: Cursor from previous page's ``meta.cursor`` to get the next page.
        include_count: Request total count in the response.
        limit: Results per page (1-100, or "all" for 100, default 50).
        no_retry: Disable automatic 429 retry.

    Returns:
        ``{data, meta}`` envelope — ``data`` is compact items,
        ``meta.cursor`` points to the next page if available.
    """
    client = get_client()

    # ── Fetch mode ────────────────────────────────────────
    if id:
        try:
            result = await client.get_permits(id)
            return _build_single_envelope(result)
        except ShovelsClientError as e:
            return format_error(str(e))

    # ── Search mode ───────────────────────────────────────
    if not geo_id:
        return format_error("geo_id is required. Use shovels_geo to resolve a location first.")
    if not permit_from:
        return format_error("permit_from is required (YYYY-MM-DD).")
    if not permit_to:
        return format_error("permit_to is required (YYYY-MM-DD).")

    try:
        page_size = _parse_size(limit)
        search_params: dict = {
            "geo_id": geo_id,
            "permit_from": permit_from,
            "permit_to": permit_to,
            "size": page_size,
        }
        if tags:
            search_params["permit_tags"] = tags
        if permit_status:
            search_params["permit_status"] = permit_status
        if property_type:
            search_params["property_type"] = property_type
        if min_job_value is not None:
            search_params["permit_min_job_value"] = min_job_value
        if cursor:
            search_params["cursor"] = cursor
        if include_count:
            search_params["include_count"] = True

        result = await client._request("GET", "permits/search", search_params, no_retry=no_retry)
        return _build_search_envelope(result, "permits")
    except ShovelsClientError as e:
        return format_error(str(e))


# ── shovels_contractors ─────────────────────────────────

@mcp.tool()
async def shovels_contractors(
    action: str = "search",
    id: Optional[list[str]] = None,
    geo_id: Optional[str] = None,
    permit_from: Optional[str] = None,
    permit_to: Optional[str] = None,
    contractor_classification: Optional[str] = None,
    contractor_name: Optional[str] = None,
    cursor: Optional[str] = None,
    metric_from: Optional[str] = None,
    metric_to: Optional[str] = None,
    property_type: Optional[str] = None,
    tag: Optional[str] = None,
    include_count: bool = False,
    limit: str = "50",
    no_retry: bool = False,
) -> dict:
    """
    Search/fetch contractors, their permits, employees, or monthly metrics.

    Mirrors ``shovels contractors search/get/permits/employees/metrics``.

    **For search:** Requires ``geo_id`` + ``permit_from`` + ``permit_to``.

    **For get:** Requires ``id``.

    **For permits:** Requires ``id`` + ``geo_id`` + ``permit_from`` + ``permit_to``.

    **For employees:** Requires ``id``.

    **For metrics:** Requires ``id`` + ``metric_from`` + ``metric_to`` + ``property_type`` + ``tag``.

    💰 Job values in **cents**.

    🏷️ Trade classifications (for ``contractor_classification``):
    electrical, plumbing, general, roofing, hvac, concrete, framing, drywall,
    painting, flooring, landscaping, masonry, fencing, solar, demolition.

    Pagination: search returns one page (max 100). Pass ``cursor`` from
    ``meta.cursor`` to get the next page.

    Args:
        action: Action to perform (search, get, permits, employees, metrics).
        id: Contractor ID(s). Required for get/permits/employees/metrics.
        geo_id: Required for search and permits.
        permit_from: Required for search and permits (YYYY-MM-DD).
        permit_to: Required for search and permits (YYYY-MM-DD).
        contractor_classification: Filter by trade classification.
        contractor_name: Filter by name (min 3 characters — trigram index).
        cursor: Cursor from previous page's ``meta.cursor`` for next page.
        metric_from: Required for metrics (YYYY-MM-DD).
        metric_to: Required for metrics (YYYY-MM-DD).
        property_type: Required for metrics.
        tag: Required for metrics.
        include_count: Request total count.
        limit: Results per page (1-100, or "all" for 100, default 50).
        no_retry: Disable automatic 429 retry.

    Returns:
        ``{data, meta}`` envelope with contractor records.
    """
    client = get_client()

    try:
        page_size = _parse_size(limit)

        if action == "search":
            if not geo_id:
                return format_error("geo_id is required for search. Use shovels_geo first.")
            if not permit_from:
                return format_error("permit_from is required (YYYY-MM-DD).")
            if not permit_to:
                return format_error("permit_to is required (YYYY-MM-DD).")

            search_params = {
                "geo_id": geo_id,
                "permit_from": permit_from,
                "permit_to": permit_to,
                "size": page_size,
            }
            if contractor_classification:
                search_params["contractor_classification_derived"] = [contractor_classification]
            if contractor_name:
                search_params["contractor_name"] = contractor_name
            if cursor:
                search_params["cursor"] = cursor
            if include_count:
                search_params["include_count"] = True

            result = await client._request("GET", "contractors/search", search_params, no_retry=no_retry)
            return _build_search_envelope(result, "contractors")

        elif action == "get":
            if not id:
                return format_error("id is required for action='get'.")
            result = await client.get_contractors(id)
            return _build_single_envelope(result)

        elif action == "permits":
            if not id:
                return format_error("id is required for action='permits'.")
            if not geo_id or not permit_from or not permit_to:
                return format_error("geo_id, permit_from, and permit_to are required for action='permits'.")
            result = await client.contractor_permits(
                id[0], geo_id, permit_from, permit_to,
                limit=limit, no_retry=no_retry,
            )
            return _build_search_envelope(result, "permits")

        elif action == "employees":
            if not id:
                return format_error("id is required for action='employees'.")
            page_size = _parse_size(limit)
            result = await client.contractor_employees(
                id[0], size=page_size, cursor=cursor, no_retry=no_retry,
            )
            return _build_single_envelope(result)

        elif action == "metrics":
            if not id:
                return format_error("id is required for action='metrics'.")
            if not all([metric_from, metric_to, property_type, tag]):
                return format_error(
                    "metric_from, metric_to, property_type, and tag are required for action='metrics'."
                )
            result = await client.contractor_metrics(
                id[0], metric_from, metric_to, property_type, tag,
                no_retry=no_retry,
            )
            return _build_single_envelope(result)

        else:
            return format_error(
                f"Unknown action '{action}'. Valid actions: search, get, permits, employees, metrics.",
            )

    except ShovelsClientError as e:
        return format_error(str(e))


# ── shovels_geo ─────────────────────────────────────────

@mcp.tool()
async def shovels_geo(
    query: str,
    level: Optional[str] = None,
    limit: str = "50",
) -> dict:
    """
    Resolve free-text place names to Shovels geo_ids.

    **Required first step** before permits/contractors search,
    since those endpoints reject free-text addresses.

    When ``level`` is omitted, tries address first (most specific),
    then falls back through city → county → jurisdiction → state.

    💡 For state-level queries, use 2-letter codes (e.g. "TX" not "Texas").
    🔍 Common typos are auto-corrected (e.g. "taxas" → "TX", "california" → "CA").

    Args:
        query: Address, city, 2-letter state code, county, or jurisdiction name.
        level: Pin to a resolver: address, city, county, jurisdiction, state.
        limit: Results per search.

    Returns:
        ``{data, meta}`` envelope with geo results.
    """
    # Validate empty query
    if not query or not query.strip():
        return format_error("query is required. Provide a location (e.g. 'TX', 'Austin, TX').")

    # Auto-correct state name typos — run for ALL queries, not just short ones
    state_code = _guess_state_code(query)
    if state_code and len(state_code) == 2:
        client = get_client()
        try:
            result = await client.resolve_geo(state_code, level="state")
            if result.get("items"):
                result["_note"] = f"Resolved '{query}' to state code '{state_code}'"
                return _build_search_envelope(result, "geo")
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

        return _build_search_envelope(result, "geo")
    except ShovelsClientError as e:
        return format_error(str(e))


# ── shovels_meta ────────────────────────────────────────

@mcp.tool()
async def shovels_meta(
    action: str = "usage",
    limit: str = "50",
) -> dict:
    """
    List valid permit tags, or check current API credit usage.

    Mirrors ``shovels tags list`` / ``shovels usage``.

    Args:
        action: Action to perform (tags or usage).
        limit: Results per page (only for action=tags).

    Returns:
        ``{data, meta}`` envelope with tags or usage info.
    """
    client = get_client()

    try:
        if action == "tags":
            try:
                limit_int = int(limit)
            except (ValueError, TypeError):
                limit_int = settings.DEFAULT_LIMIT
            result = await client.tags_list(limit=limit_int)
            return _build_search_envelope(result, "geo")

        elif action == "usage":
            result = await client.usage()
            return _build_single_envelope(result)

        else:
            return format_error(
                f"Unknown action '{action}'. Valid actions: tags, usage."
            )

    except ShovelsClientError as e:
        return format_error(str(e))


# ── MCP Resources (Progressive Disclosure) ──────────────
# These register read_resource handlers so agents can fetch
# full records by URI without loading the tool parameter schema.

@mcp.resource("shovels://permits/{permit_id}")
async def get_permit_resource(permit_id: str) -> dict:
    """
    Fetch a full permit record by its resource URI.

    Called when an agent reads shovels://permits/{permit_id}
    to get the complete record (20+ fields) without loading
    the tool parameter schema.
    """
    client = get_client()
    try:
        result = await client.get_permits([permit_id])
        return _build_single_envelope(result)
    except ShovelsClientError as e:
        return format_error(str(e))


@mcp.resource("shovels://contractors/{contractor_id}")
async def get_contractor_resource(contractor_id: str) -> dict:
    """
    Fetch a full contractor record by its resource URI.

    Called when an agent reads shovels://contractors/{contractor_id}
    to get the complete record without loading the tool parameter schema.
    """
    client = get_client()
    try:
        result = await client.get_contractors([contractor_id])
        return _build_single_envelope(result)
    except ShovelsClientError as e:
        return format_error(str(e))


