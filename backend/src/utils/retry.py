"""
Retry helper with exponential backoff for the SkillClaw MCP Server.

Provides utilities for retrying failed operations with configurable
backoff strategies, useful for handling transient errors in external APIs.
"""

import asyncio
import time
from typing import TypeVar, Callable, Any, Optional
from functools import wraps
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RetryError(Exception):
    """Raised when all retry attempts are exhausted."""

    def __init__(self, message: str, last_exception: Optional[Exception] = None):
        super().__init__(message)
        self.last_exception = last_exception


def should_retry(exception: Exception) -> bool:
    """
    Determine if an exception should trigger a retry.

    Args:
        exception: The exception that occurred

    Returns:
        True if the operation should be retried, False otherwise
    """
    # Retry on common transient errors
    retry_exceptions = (
        ConnectionError,
        TimeoutError,
        asyncio.TimeoutError,
    )

    if isinstance(exception, retry_exceptions):
        return True

    # Check for HTTP 5xx errors (if using httpx)
    if hasattr(exception, "response"):
        response = getattr(exception, "response")
        if hasattr(response, "status_code"):
            return 500 <= response.status_code < 600

    return False


async def retry_async(
    func: Callable[..., Any],
    *args: Any,
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 60.0,
    retry_on: Optional[Callable[[Exception], bool]] = None,
    **kwargs: Any,
) -> T:
    """
    Retry an async function with exponential backoff.

    Args:
        func: Async function to retry
        *args: Positional arguments for func
        max_attempts: Maximum number of attempts (default: 3)
        initial_delay: Initial delay in seconds (default: 1.0)
        backoff_factor: Multiplier for delay after each attempt (default: 2.0)
        max_delay: Maximum delay between attempts (default: 60.0)
        retry_on: Optional function to determine if exception should trigger retry
        **kwargs: Keyword arguments for func

    Returns:
        Result of the function call

    Raises:
        RetryError: If all attempts are exhausted
    """
    retry_check = retry_on or should_retry
    delay = initial_delay
    last_exception = None

    for attempt in range(1, max_attempts + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e

            if attempt == max_attempts or not retry_check(e):
                logger.error(
                    f"All retry attempts exhausted for {func.__name__}",
                    extra={
                        "function": func.__name__,
                        "attempts": attempt,
                        "error": str(e),
                    },
                )
                raise RetryError(
                    f"Failed after {attempt} attempts: {str(e)}",
                    last_exception=e,
                )

            logger.warning(
                f"Attempt {attempt}/{max_attempts} failed for {func.__name__}, retrying in {delay}s",
                extra={
                    "function": func.__name__,
                    "attempt": attempt,
                    "max_attempts": max_attempts,
                    "delay": delay,
                    "error": str(e),
                },
            )

            await asyncio.sleep(delay)
            delay = min(delay * backoff_factor, max_delay)

    # Should never reach here, but for type safety
    raise RetryError("Unexpected retry loop exit", last_exception=last_exception)


def retry_sync(
    func: Callable[..., Any],
    *args: Any,
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 60.0,
    retry_on: Optional[Callable[[Exception], bool]] = None,
    **kwargs: Any,
) -> T:
    """
    Retry a synchronous function with exponential backoff.

    Args:
        func: Synchronous function to retry
        *args: Positional arguments for func
        max_attempts: Maximum number of attempts (default: 3)
        initial_delay: Initial delay in seconds (default: 1.0)
        backoff_factor: Multiplier for delay after each attempt (default: 2.0)
        max_delay: Maximum delay between attempts (default: 60.0)
        retry_on: Optional function to determine if exception should trigger retry
        **kwargs: Keyword arguments for func

    Returns:
        Result of the function call

    Raises:
        RetryError: If all attempts are exhausted
    """
    retry_check = retry_on or should_retry
    delay = initial_delay
    last_exception = None

    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e

            if attempt == max_attempts or not retry_check(e):
                logger.error(
                    f"All retry attempts exhausted for {func.__name__}",
                    extra={
                        "function": func.__name__,
                        "attempts": attempt,
                        "error": str(e),
                    },
                )
                raise RetryError(
                    f"Failed after {attempt} attempts: {str(e)}",
                    last_exception=e,
                )

            logger.warning(
                f"Attempt {attempt}/{max_attempts} failed for {func.__name__}, retrying in {delay}s",
                extra={
                    "function": func.__name__,
                    "attempt": attempt,
                    "max_attempts": max_attempts,
                    "delay": delay,
                    "error": str(e),
                },
            )

            time.sleep(delay)
            delay = min(delay * backoff_factor, max_delay)

    # Should never reach here, but for type safety
    raise RetryError("Unexpected retry loop exit", last_exception=last_exception)


def with_retry(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 60.0,
    retry_on: Optional[Callable[[Exception], bool]] = None,
):
    """
    Decorator for adding retry logic to async functions.

    Args:
        max_attempts: Maximum number of attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay after each attempt
        max_delay: Maximum delay between attempts
        retry_on: Optional function to determine if exception should trigger retry

    Example:
        @with_retry(max_attempts=3, initial_delay=1.0)
        async def fetch_data():
            # ... code that might fail transiently
            pass
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await retry_async(
                func,
                *args,
                max_attempts=max_attempts,
                initial_delay=initial_delay,
                backoff_factor=backoff_factor,
                max_delay=max_delay,
                retry_on=retry_on,
                **kwargs,
            )

        return wrapper

    return decorator
