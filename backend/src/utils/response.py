"""
Response envelope helpers for the Shovels MCP Server.

Transforms raw Shovels API responses into the MVP v2 ``data``/``meta``
envelope that mirrors the CLI output contract.
"""

from typing import Any, Optional


def build_data_meta(
    data: Any,
    credits_used: int = 0,
    credits_remaining: int = 0,
    count: Optional[int] = None,
    has_more: bool = False,
) -> dict:
    """
    Wrap API response data in the ``{data, meta}`` envelope.

    When *data* is a list, it's treated as a search result page and the
    ``meta`` block includes ``count`` and ``has_more``.

    When *data* is a single dict, the ``meta`` block only carries credit info.

    Args:
        data: Response payload (list for search, dict for single record).
        credits_used: Credits consumed by this request.
        credits_remaining: Credits remaining on the API key.
        count: Explicit count (defaults to ``len(data)`` for lists).
        has_more: Whether additional pages are available.

    Returns:
        Envelope dict with ``data`` and ``meta`` keys.
    """
    if isinstance(data, list):
        return {
            "data": data,
            "meta": {
                "count": count if count is not None else len(data),
                "has_more": has_more,
                "credits_used": credits_used,
                "credits_remaining": credits_remaining,
            },
        }

    # Single-object response (get-by-ID, usage)
    return {
        "data": data,
        "meta": {
            "credits_used": credits_used,
            "credits_remaining": credits_remaining,
        },
    }


__all__ = ["build_data_meta"]
