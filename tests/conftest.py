"""Shared fixtures for the test suite.

Every test routes HTTP through respx against a fixed base URL so the suite
never touches the real api.bukti.ai. The sample payloads mirror real public
responses from the API and are hard-coded here rather than recorded from the
live service to keep tests deterministic.
"""

from __future__ import annotations

from typing import Any

import pytest

from bukti.client import BuktiClient

TEST_BASE_URL = "https://api.test.bukti.example"
ENTITY_ID = "agent_example"
CAPABILITY_ID = "cap_example"


PROFILE_PAYLOAD: dict[str, Any] = {
    "entity_id": ENTITY_ID,
    "entity_type": "ai_agent",
    "username": "example-agent",
    "display_name": "Example Agent",
    "domain": "software_engineering",
    "portfolio_text": "An example agent profile for testing.",
    "llm_summary": "Agent used in the bukti client test suite.",
    "profile_url": "https://bukti.ai/a/example-agent",
    "capabilities": [
        {
            "capability_id": CAPABILITY_ID,
            "name": "Example Capability",
            "evidence_score": 0.82,
            "tier": "verified",
            "evidence_count": 4,
            "source_count": 2,
            "first_observed_at": "2026-01-01T00:00:00",
            "last_observed_at": "2026-04-01T00:00:00",
            "source_platforms": ["github", "credly"],
        }
    ],
    "evidence_score_summary": {"verified": 1, "attested": 0, "self-declared": 0},
    "json_ld": {},
    "entry_path": "agent",
    "qa_passed": True,
}

CAPABILITIES_PAYLOAD: dict[str, Any] = {
    "entity_id": ENTITY_ID,
    "capabilities": [
        PROFILE_PAYLOAD["capabilities"][0],
        {
            "capability_id": "cap_minor",
            "name": "Minor Capability",
            "evidence_score": 0.28,
            "tier": "self-declared",
            "evidence_count": 1,
            "source_count": 1,
            "first_observed_at": "2026-02-01T00:00:00",
            "last_observed_at": "2026-02-01T00:00:00",
            "source_platforms": ["web"],
        },
    ],
}

PROVENANCE_PAYLOAD: dict[str, Any] = {
    "entity_id": ENTITY_ID,
    "voi_count": 3,
    "voi_ids": ["voi_1", "voi_2", "voi_3"],
    "sources": [
        {"platform": "github", "url": "https://github.com/example"},
        {"platform": "credly", "url": None},
    ],
}

CAPABILITY_PROVENANCE_PAYLOAD: dict[str, Any] = {
    "entity_id": ENTITY_ID,
    "capability_id": CAPABILITY_ID,
    "capability_name": "Example Capability",
    "evidence_count": 2,
    "tier": "verified",
    "evidence_score": 0.82,
    "first_observed_at": "2026-01-01T00:00:00",
    "last_observed_at": "2026-04-01T00:00:00",
    "source_platforms": ["github", "credly"],
    "evidence": [
        {
            "voi_id": "voi_1",
            "source_platform": "github",
            "evidence_type": "contribution_artifact",
            "observed_at": "2026-01-01T00:00:00",
            "extraction_confidence": 0.9,
            "evidence_uri": "https://github.com/example/repo",
            "evidence_text": "Merged pull request implementing feature.",
        },
        {
            "voi_id": "voi_2",
            "source_platform": "credly",
            "evidence_type": "credential_badge",
            "observed_at": "2026-04-01T00:00:00",
            "extraction_confidence": 0.95,
            "evidence_uri": None,
            "evidence_text": "Issuer-verified badge.",
        },
    ],
}


@pytest.fixture
def base_url() -> str:
    return TEST_BASE_URL


@pytest.fixture
def client(base_url: str) -> BuktiClient:
    c = BuktiClient(base_url=base_url)
    yield c
    c.close()


@pytest.fixture
def profile_payload() -> dict[str, Any]:
    return PROFILE_PAYLOAD


@pytest.fixture
def capabilities_payload() -> dict[str, Any]:
    return CAPABILITIES_PAYLOAD


@pytest.fixture
def provenance_payload() -> dict[str, Any]:
    return PROVENANCE_PAYLOAD


@pytest.fixture
def capability_provenance_payload() -> dict[str, Any]:
    return CAPABILITY_PROVENANCE_PAYLOAD
