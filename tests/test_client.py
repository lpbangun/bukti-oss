"""Tests for the synchronous Bukti HTTP client."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
import respx

from bukti import (
    BuktiAuthError,
    BuktiClient,
    BuktiNotFoundError,
    BuktiRateLimitError,
    BuktiServerError,
)
from tests.conftest import CAPABILITY_ID, ENTITY_ID


@respx.mock
def test_get_profile_happy_path(base_url: str, client: BuktiClient, profile_payload: dict[str, Any]) -> None:
    route = respx.get(f"{base_url}/v1/profile/{ENTITY_ID}").mock(
        return_value=httpx.Response(200, json=profile_payload)
    )
    profile = client.get_profile(ENTITY_ID)
    assert route.called
    assert profile.entity_id == ENTITY_ID
    assert profile.display_name == "Example Agent"
    assert len(profile.capabilities) == 1
    assert profile.capabilities[0].tier == "verified"


@respx.mock
def test_list_capabilities_happy_path(base_url: str, client: BuktiClient, capabilities_payload: dict[str, Any]) -> None:
    respx.get(f"{base_url}/v1/profile/{ENTITY_ID}/capabilities").mock(
        return_value=httpx.Response(200, json=capabilities_payload)
    )
    caps = client.list_capabilities(ENTITY_ID)
    assert len(caps) == 2
    assert {c.tier for c in caps} == {"verified", "self-declared"}


@respx.mock
def test_get_provenance_happy_path(base_url: str, client: BuktiClient, provenance_payload: dict[str, Any]) -> None:
    respx.get(f"{base_url}/v1/profile/{ENTITY_ID}/provenance").mock(
        return_value=httpx.Response(200, json=provenance_payload)
    )
    prov = client.get_provenance(ENTITY_ID)
    assert prov.voi_count == 3
    assert {s.platform for s in prov.sources} == {"github", "credly"}


@respx.mock
def test_get_capability_provenance_happy_path(
    base_url: str, client: BuktiClient, capability_provenance_payload: dict[str, Any]
) -> None:
    respx.get(
        f"{base_url}/v1/profile/{ENTITY_ID}/capabilities/{CAPABILITY_ID}/provenance"
    ).mock(return_value=httpx.Response(200, json=capability_provenance_payload))
    chain = client.get_capability_provenance(ENTITY_ID, CAPABILITY_ID)
    assert chain.evidence_count == 2
    assert chain.evidence[0].source_platform == "github"


@respx.mock
def test_not_found_raises(base_url: str, client: BuktiClient) -> None:
    respx.get(f"{base_url}/v1/profile/ghost").mock(
        return_value=httpx.Response(404, json={"detail": "Profile not found: ghost"})
    )
    with pytest.raises(BuktiNotFoundError) as exc:
        client.get_profile("ghost")
    assert exc.value.status_code == 404


@respx.mock
def test_auth_error_raises(base_url: str, client: BuktiClient) -> None:
    respx.get(f"{base_url}/v1/profile/x").mock(
        return_value=httpx.Response(401, json={"detail": "unauthorized"})
    )
    with pytest.raises(BuktiAuthError):
        client.get_profile("x")


@respx.mock
def test_rate_limit_raises(base_url: str, client: BuktiClient) -> None:
    respx.get(f"{base_url}/v1/profile/x").mock(
        return_value=httpx.Response(429, json={"detail": "slow down"})
    )
    with pytest.raises(BuktiRateLimitError):
        client.get_profile("x")


@respx.mock
def test_server_error_retries_once_then_raises(base_url: str, client: BuktiClient) -> None:
    route = respx.get(f"{base_url}/v1/profile/x").mock(
        return_value=httpx.Response(503, json={"detail": "unavailable"})
    )
    with pytest.raises(BuktiServerError):
        client.get_profile("x")
    assert route.call_count == 2


@respx.mock
def test_server_error_retry_succeeds(base_url: str, client: BuktiClient, profile_payload: dict[str, Any]) -> None:
    route = respx.get(f"{base_url}/v1/profile/{ENTITY_ID}").mock(
        side_effect=[
            httpx.Response(502),
            httpx.Response(200, json=profile_payload),
        ]
    )
    profile = client.get_profile(ENTITY_ID)
    assert profile.entity_id == ENTITY_ID
    assert route.call_count == 2


def test_context_manager_closes(base_url: str) -> None:
    with BuktiClient(base_url=base_url) as c:
        assert c._http.is_closed is False
    assert c._http.is_closed is True


def test_api_key_sent_as_header(base_url: str) -> None:
    client = BuktiClient(base_url=base_url, api_key="sekret")
    try:
        assert client._http.headers.get("X-API-Key") == "sekret"
    finally:
        client.close()
