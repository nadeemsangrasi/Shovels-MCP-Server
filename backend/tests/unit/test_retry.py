"""
Unit tests for retry utility.

Tests exponential backoff logic, retry decisions, and the decorator.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock

from src.utils.retry import (
    should_retry,
    retry_async,
    retry_sync,
    with_retry,
    RetryError,
)


class TestShouldRetry:
    """should_retry() determines if an exception triggers a retry."""

    def test_retry_on_connection_error(self):
        assert should_retry(ConnectionError("connection refused")) is True

    def test_retry_on_timeout_error(self):
        assert should_retry(TimeoutError("timed out")) is True

    def test_retry_on_asyncio_timeout(self):
        assert should_retry(asyncio.TimeoutError("timeout")) is True

    def test_no_retry_on_value_error(self):
        """Non-transient errors should not be retried."""
        assert should_retry(ValueError("bad value")) is False

    def test_no_retry_on_key_error(self):
        assert should_retry(KeyError("missing")) is False

    def test_retry_on_http_500_with_response_attr(self):
        """Check if an exception with a response.status_code in 5xx range is retried."""

        class FakeResponse:
            status_code = 503

        class FakeHTTPError(Exception):
            def __init__(self):
                self.response = FakeResponse()

        assert should_retry(FakeHTTPError()) is True

    def test_no_retry_on_http_400_with_response_attr(self):
        """4xx errors should not be retried."""

        class FakeResponse:
            status_code = 404

        class FakeHTTPError(Exception):
            def __init__(self):
                self.response = FakeResponse()

        assert should_retry(FakeHTTPError()) is False


class TestRetryAsync:
    """retry_async() retry logic tests."""

    @pytest.mark.asyncio
    async def test_succeeds_on_first_attempt(self):
        """Function that succeeds immediately should not retry."""
        mock_fn = AsyncMock(return_value="success")
        result = await retry_async(mock_fn, max_attempts=3)
        assert result == "success"
        assert mock_fn.call_count == 1

    @pytest.mark.asyncio
    async def test_retries_and_succeeds(self):
        """Function that fails twice then succeeds."""
        mock_fn = AsyncMock(side_effect=[
            ConnectionError("first fail"),
            TimeoutError("second fail"),
            "success",
        ])
        result = await retry_async(mock_fn, max_attempts=3, initial_delay=0.01)
        assert result == "success"
        assert mock_fn.call_count == 3

    @pytest.mark.asyncio
    async def test_exhausts_retries_raises_error(self):
        """Function that always fails raises RetryError."""
        mock_fn = AsyncMock(side_effect=ConnectionError("always fails"))
        with pytest.raises(RetryError):
            await retry_async(mock_fn, max_attempts=2, initial_delay=0.01)
        assert mock_fn.call_count == 2

    @pytest.mark.asyncio
    async def test_non_retryable_error_does_not_retry(self):
        """ValueError (non-transient) should not retry."""
        mock_fn = AsyncMock(side_effect=ValueError("bad input"))
        with pytest.raises(RetryError):
            await retry_async(mock_fn, max_attempts=3)
        assert mock_fn.call_count == 1

    @pytest.mark.asyncio
    async def test_custom_retry_check(self):
        """Custom retry function overrides default logic."""
        mock_fn = AsyncMock(side_effect=[ValueError("retry me"), "success"])

        # Retry on ValueError
        def custom_check(e):
            return isinstance(e, ValueError)

        result = await retry_async(
            mock_fn, max_attempts=2, initial_delay=0.01, retry_on=custom_check
        )
        assert result == "success"
        assert mock_fn.call_count == 2

    @pytest.mark.asyncio
    async def test_backoff_delay_increases(self):
        """Each retry should wait longer than the previous."""
        import time

        mock_fn = AsyncMock(side_effect=[
            ConnectionError("fail"),
            ConnectionError("fail"),
            "success",
        ])
        start = time.monotonic()
        await retry_async(mock_fn, max_attempts=3, initial_delay=0.05, backoff_factor=2.0)
        elapsed = time.monotonic() - start

        # With 0.05s initial delay, backoff 2x: ~0.05 + ~0.1 = ~0.15s
        assert elapsed >= 0.1
        assert mock_fn.call_count == 3


class TestRetrySync:
    """retry_sync() synchronous retry logic tests."""

    call_count = 0

    def _failing_fn(self, msg: str):
        self.call_count += 1
        if self.call_count < 3:
            raise ConnectionError(f"attempt {self.call_count}")
        return msg

    def test_sync_retries_and_succeeds(self):
        self.call_count = 0
        result = retry_sync(self._failing_fn, "done", max_attempts=3, initial_delay=0.01)
        assert result == "done"
        assert self.call_count == 3

    def test_sync_exhausts_retries(self):
        self.call_count = 0

        def always_fails():
            self.call_count += 1
            raise ConnectionError("fail")

        with pytest.raises(RetryError):
            retry_sync(always_fails, max_attempts=2, initial_delay=0.01)
        assert self.call_count == 2


class TestWithRetryDecorator:
    """@with_retry decorator tests."""

    @pytest.mark.asyncio
    async def test_decorator_retries_on_failure(self):
        call_count = 0

        @with_retry(max_attempts=3, initial_delay=0.01)
        async def fetch_data():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("transient")
            return "data"

        result = await fetch_data()
        assert result == "data"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_decorator_passes_args(self):
        """Decorator should pass through positional and keyword args."""

        @with_retry(max_attempts=2, initial_delay=0.01)
        async def greet(greeting: str, name: str = ""):
            return f"{greeting}, {name}!"

        result = await greet("Hello", name="World")
        assert result == "Hello, World!"
