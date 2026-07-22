"""
Typed error classes and formatting for the Shovels MCP Server.

Provides a structured error hierarchy mirroring the CLI's exit-code
vocabulary, and a formatting helper to produce the MVP v2 error envelope.
"""

from typing import Optional


class ShovelsClientError(Exception):
    """Raised on Shovels API errors."""


class ShovelsClientRateLimited(ShovelsClientError):
    """
    Raised when the Shovels API returns HTTP 429 (rate limited).

    Carries the Retry-After value if the header was present.
    """

    def __init__(self, message: str, retry_after: Optional[float] = None):
        super().__init__(message)
        self.retry_after = retry_after


# Maps HTTP status codes to (error_type, code) pairs.
# These match the CLI's exit-code vocabulary, delivered as JSON data
# instead of shell exit codes.
ERROR_TYPE_MAP: dict[int, tuple[str, int]] = {
    400: ("client_error", 1),
    401: ("auth_error", 2),
    403: ("auth_error", 2),
    404: ("client_error", 1),
    422: ("validation_error", 1),
    429: ("rate_limited", 3),
}

# Error types that are not tied to a single status code
ERROR_TYPE_SERVER_ERROR = ("server_error", 4)
ERROR_TYPE_NETWORK_ERROR = ("network_error", 5)
ERROR_TYPE_CREDIT_EXHAUSTED = ("credit_exhausted", 3)


def format_error(
    message: str,
    status_code: Optional[int] = None,
    error_type: Optional[str] = None,
    code: Optional[int] = None,
    credits_remaining: Optional[int] = None,
) -> dict:
    """
    Build a structured error response matching the MVP v2 error envelope.

    When ``status_code`` is given and maps to a known ``(error_type, code)``
    pair, those values are used unless explicitly overridden by passing
    ``error_type`` or ``code``.

    Special case: HTTP 429 with ``credits_remaining=0`` is promoted to
    ``credit_exhausted``.

    Returns::

        {"error": str, "code": int, "error_type": str}
    """
    # Try to look up known types from the map
    resolved_type, resolved_code = ERROR_TYPE_SERVER_ERROR  # fallback
    if status_code is not None:
        if status_code == 429 and credits_remaining is not None and credits_remaining <= 0:
            resolved_type, resolved_code = ERROR_TYPE_CREDIT_EXHAUSTED
        else:
            resolved_type, resolved_code = ERROR_TYPE_MAP.get(
                status_code, ERROR_TYPE_SERVER_ERROR
            )

    return {
        "error": message,
        "code": code if code is not None else resolved_code,
        "error_type": error_type if error_type is not None else resolved_type,
    }


__all__ = [
    "ShovelsClientError",
    "ShovelsClientRateLimited",
    "ERROR_TYPE_MAP",
    "ERROR_TYPE_SERVER_ERROR",
    "ERROR_TYPE_NETWORK_ERROR",
    "ERROR_TYPE_CREDIT_EXHAUSTED",
    "format_error",
]
