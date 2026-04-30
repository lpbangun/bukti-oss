"""Synchronous HTTP client for the Bukti public API.

The client wraps the read-only surface at https://api.bukti.ai: profile
retrieval, capability listing, and provenance. It is deliberately thin — no
caching, no retry strategy beyond a single retry on transient 5xx responses,
no logging unless the caller configures it.
"""

from __future__ import annotations

from types import TracebackType
from typing import Any

import httpx

from bukti.exceptions import (
    BuktiAuthError,
    BuktiError,
    BuktiNotFoundError,
    BuktiRateLimitError,
    BuktiServerError,
)
from bukti.models import (
    Capability,
    CapabilityProvenance,
    Profile,
    Provenance,
)

DEFAULT_BASE_URL = "https://api.bukti.ai"
DEFAULT_TIMEOUT = 30.0


class BuktiClient:
    """Minimal synchronous client for the Bukti read-only API.

    Example:
        >>> with BuktiClient() as bukti:
        ...     profile = bukti.get_profile("agent_example_01")
        ...     print(profile.display_name)

    Args:
        base_url: API root. Override for staging or self-hosted deployments.
        api_key: Optional bearer-style key. Sent as ``X-API-Key``. Most
            read-only endpoints do not require a key today.
        timeout: Per-request timeout in seconds.
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        api_key: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        headers = {
            "Accept": "application/json",
            "User-Agent": "bukti-python/0.1.0",
        }
        if api_key:
            headers["X-API-Key"] = api_key
        self._http = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

    def __enter__(self) -> BuktiClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        """Release the underlying HTTP connection pool."""
        self._http.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = path if path.startswith("/") else f"/{path}"

        try:
            response = self._http.request(method, url, **kwargs)
        except httpx.RequestError as exc:
            raise BuktiError(f"Network error calling {url}: {exc}") from exc

        if 500 <= response.status_code < 600:
            try:
                response = self._http.request(method, url, **kwargs)
            except httpx.RequestError as exc:
                raise BuktiServerError(
                    f"Network error on retry to {url}: {exc}",
                    status_code=response.status_code,
                ) from exc

        return self._handle_response(response, url)

    @staticmethod
    def _handle_response(response: httpx.Response, url: str) -> dict[str, Any]:
        status = response.status_code
        if 200 <= status < 300:
            try:
                return response.json()
            except ValueError as exc:
                raise BuktiError(f"Invalid JSON from {url}: {exc}", status_code=status) from exc

        detail = BuktiClient._extract_detail(response)
        message = f"{status} {detail}" if detail else f"HTTP {status} from {url}"

        if status == 404:
            raise BuktiNotFoundError(message, status_code=status)
        if status in (401, 403):
            raise BuktiAuthError(message, status_code=status)
        if status == 429:
            raise BuktiRateLimitError(message, status_code=status)
        if 500 <= status < 600:
            raise BuktiServerError(message, status_code=status)
        raise BuktiError(message, status_code=status)

    @staticmethod
    def _extract_detail(response: httpx.Response) -> str:
        try:
            body = response.json()
        except ValueError:
            return response.text.strip()[:200]
        if isinstance(body, dict):
            for key in ("detail", "message", "error"):
                value = body.get(key)
                if isinstance(value, str) and value:
                    return value
        return ""

    def get_profile(self, entity_id: str) -> Profile:
        """Fetch a published profile by entity ID.

        Draft profiles are visible only to their owner and return 404 to
        everyone else.

        Raises:
            BuktiNotFoundError: if the profile does not exist or is not public.
        """
        data = self._request("GET", f"/v1/profile/{entity_id}")
        return Profile.model_validate(data)

    def list_capabilities(self, entity_id: str) -> list[Capability]:
        """Return all capabilities surfaced on a profile with tier and score."""
        data = self._request("GET", f"/v1/profile/{entity_id}/capabilities")
        caps = data.get("capabilities", []) if isinstance(data, dict) else []
        return [Capability.model_validate(c) for c in caps]

    def get_provenance(self, entity_id: str) -> Provenance:
        """Return the aggregate evidence manifest for a profile."""
        data = self._request("GET", f"/v1/profile/{entity_id}/provenance")
        return Provenance.model_validate(data)

    def get_capability_provenance(self, entity_id: str, capability_id: str) -> CapabilityProvenance:
        """Return the full VOI chain backing one capability on one profile."""
        data = self._request(
            "GET",
            f"/v1/profile/{entity_id}/capabilities/{capability_id}/provenance",
        )
        return CapabilityProvenance.model_validate(data)
