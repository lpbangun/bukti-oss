"""Exception types raised by the Bukti client."""

from __future__ import annotations


class BuktiError(Exception):
    """Base class for all errors raised by the Bukti client."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class BuktiNotFoundError(BuktiError):
    """Raised when the requested entity or capability does not exist (HTTP 404)."""


class BuktiAuthError(BuktiError):
    """Raised when authentication or authorization fails (HTTP 401/403)."""


class BuktiRateLimitError(BuktiError):
    """Raised when the caller exceeds the server's rate limit (HTTP 429)."""


class BuktiServerError(BuktiError):
    """Raised for 5xx responses from the Bukti API after retries are exhausted."""
