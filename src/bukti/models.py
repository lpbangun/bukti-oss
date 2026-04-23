"""Pydantic models for public Bukti API responses.

These mirror the shapes documented in the Bukti Protocol specification (see
`spec/`). Only the fields needed by the client's read-only v0.1 surface are
modeled here; extra fields from the API are ignored rather than rejected so
minor server-side additions do not break clients.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ConfidenceTier = Literal["verified", "attested", "self-declared"]
"""Human-facing confidence tier assigned to a capability.

Bukti aggregates evidence rather than scoring competence, so profiles surface
tiers (and evidence counts) rather than raw numbers to end users.
"""

EvidenceType = Literal[
    "behavioral_artifact",
    "task_outcome",
    "peer_attestation",
    "contribution_artifact",
    "publication_artifact",
    "credential_badge",
    "indirect_attestation",
    "self_reported",
]
"""The eight evidence categories the protocol distinguishes.

See `spec/docs/` for each type's intended semantics. ``self_reported`` is the
enum value for the evidence category; ``self-declared`` (with hyphen) is the
tier label shown when aggregate evidence does not clear the attested threshold.
"""

EntityType = Literal["person", "ai_agent", "organization"]
"""The three entity types Bukti profiles."""


class _Model(BaseModel):
    """Base model that tolerates unknown fields from server responses."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class Capability(_Model):
    """A single capability claim attached to an entity."""

    capability_id: str = Field(..., description="Ontology identifier (O*NET, domain extension, or growth_* node).")
    name: str = Field(..., description="Human-readable capability name.")
    evidence_score: float = Field(..., description="Aggregate evidence score in [0, 1]. Field is labeled evidence_score, not confidence, to signal the methodology.")
    tier: ConfidenceTier = Field(..., description="Tier assigned by the scoring engine.")
    evidence_count: int = Field(0, description="Number of underlying Verified Outcome Instances (VOIs).")
    source_count: int = Field(0, description="Number of distinct source platforms contributing evidence.")
    first_observed_at: str | None = Field(None, description="Earliest ISO-8601 timestamp across contributing evidence.")
    last_observed_at: str | None = Field(None, description="Latest ISO-8601 timestamp across contributing evidence.")
    source_platforms: list[str] = Field(default_factory=list, description="Platforms contributing evidence (e.g., github, credly, web).")


class Source(_Model):
    """A platform or URL that contributed evidence to a profile."""

    platform: str = Field(..., description="Short platform identifier (e.g., github, credly, web).")
    url: str | None = Field(None, description="Canonical source URL if available.")


class Profile(_Model):
    """A published Bukti profile.

    The full response carries presentation tokens, portfolio copy, and
    JSON-LD for agents and crawlers; only the identity and capability layer
    is modeled here as a stable contract. The raw response stays accessible
    on the client for callers that need to read newer fields.
    """

    entity_id: str = Field(..., description="Opaque stable identifier for the entity.")
    entity_type: str = Field("human", description="One of person, ai_agent, organization (legacy: 'human').")
    username: str | None = Field(None, description="Vanity handle if the profile has been claimed.")
    display_name: str = Field("", description="Human-readable name for display.")
    domain: str = Field("general", description="Primary domain (e.g., education, software_engineering).")
    portfolio_text: str = Field("", description="Long-form portfolio prose suitable for rendering.")
    llm_summary: str = Field("", description="Short machine-readable summary for LLM context injection.")
    profile_url: str = Field("", description="Canonical public URL.")
    capabilities: list[Capability] = Field(default_factory=list, description="All capabilities surfaced on the profile.")
    evidence_score_summary: dict[str, Any] = Field(default_factory=dict, description="Aggregate score breakdown by tier.")


class Evidence(_Model):
    """One Verified Outcome Instance (VOI) — the atomic evidence unit."""

    voi_id: str = Field(..., description="Stable identifier for this evidence record.")
    source_platform: str = Field(..., description="Where the evidence was observed.")
    evidence_type: EvidenceType = Field(..., description="One of the eight evidence categories.")
    observed_at: str | None = Field(None, description="ISO-8601 timestamp when the evidence was observed (valid time).")
    extraction_confidence: float = Field(0.0, description="Extractor's per-record confidence in [0, 1].")
    evidence_uri: str | None = Field(None, description="Canonical URI for the evidence if one exists.")
    evidence_text: str = Field("", description="Short textual snippet describing the evidence.")


class Provenance(_Model):
    """Aggregate evidence manifest for a whole profile."""

    entity_id: str
    voi_count: int = Field(0, description="Total number of VOIs backing this profile.")
    voi_ids: list[str] = Field(default_factory=list, description="IDs of every backing VOI.")
    sources: list[Source] = Field(default_factory=list, description="Distinct source platforms contributing evidence.")


class CapabilityProvenance(_Model):
    """Full evidence chain for a single capability on a profile."""

    entity_id: str
    capability_id: str
    capability_name: str
    evidence_count: int = 0
    tier: ConfidenceTier = "self-declared"
    evidence_score: float = 0.0
    first_observed_at: str | None = None
    last_observed_at: str | None = None
    source_platforms: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list, description="Individual VOIs backing the capability.")
