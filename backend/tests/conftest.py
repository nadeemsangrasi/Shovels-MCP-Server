"""
Shared test fixtures for the Shovels MCP Server test suite.

Provides mock API credentials and HTTP transport helpers.
"""

import os
import pytest
from typing import Optional
from httpx import Request, Response
from src.services.shovels_client import reset_client, clear_request_api_key


@pytest.fixture(autouse=True)
def mock_env():
    """
    Ensure SHOVELS_API_KEY is set for all tests.
    Resets the ShovelsClient singleton and request API key context before each test.
    """
    # Backup original env
    original_key = os.environ.get("SHOVELS_API_KEY")
    os.environ["SHOVELS_API_KEY"] = "test-api-key"

    # Reset client singleton and request key context so each test starts fresh
    reset_client()
    clear_request_api_key()

    yield

    # Restore original env
    if original_key is not None:
        os.environ["SHOVELS_API_KEY"] = original_key
    else:
        os.environ.pop("SHOVELS_API_KEY", None)


def mock_response(
    json_data: dict,
    status_code: int = 200,
    headers: Optional[dict] = None,
) -> Response:
    """
    Build a mock httpx.Response with optional credit headers.

    Args:
        json_data: JSON body the response should contain
        status_code: HTTP status code (default 200)
        headers: Additional response headers

    Returns:
        An httpx.Response ready to return from a mock transport
    """
    default_headers = {
        "X-Credits-Request": "1",
        "X-Credits-Limit": "250",
        "X-Credits-Remaining": "249",
    }
    if headers:
        default_headers.update(headers)

    return Response(
        status_code=status_code,
        json=json_data,
        headers=default_headers,
    )


def mock_error_response(status_code: int = 401, detail: str = "Unauthorized") -> Response:
    """
    Build a mock error response from the Shovels API.

    Args:
        status_code: HTTP error status code
        detail: Error detail message

    Returns:
        A non-OK httpx.Response
    """
    return Response(
        status_code=status_code,
        json={"detail": detail},
        headers={
            "X-Credits-Request": "1",
            "X-Credits-Limit": "250",
            "X-Credits-Remaining": "249",
        },
    )
