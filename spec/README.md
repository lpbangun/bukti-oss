> **Status:** This is the Bukti Protocol specification (v0.1 draft), the open contract that the `bukti` Python client in the parent directory implements. For the runnable client, see the [top-level README](../README.md). The methodology behind the protocol is published at [docs.bukti.ai](https://docs.bukti.ai). The specification stands on its own as an implementation-agnostic standard any third party can implement.

# Bukti Protocol

**An open specification for evidence-backed capability claims about people, AI agents, and organizations.**

> Status: public draft · v0.1 · shapes are implementable today, with breaking changes expected before 1.0.

---

## What this is

This is the **Bukti Protocol** — the portable, implementation-agnostic specification for how capability evidence can be expressed, aggregated, and exchanged across systems.

It exists because the current state of "professional credibility" on the internet is fragmented: resumes are self-reported, skills lists are unranked, and AI agents have no way to discover one another by what they can actually do. Bukti (the product at [bukti.ai](https://bukti.ai)) is one implementation of this protocol — a platform that ingests evidence from public artifacts (repositories, credentials, publications, project links) and produces evidence-ranked capability profiles for humans, AI agents, and organizations.

The protocol itself is not the product. It is the set of shapes, vocabularies, and interop surfaces a third party would need to:

- publish evidence-backed capability profiles that other systems (including LLM agents) can consume,
- query and verify evidence claims made by any compliant implementation,
- interoperate with Bukti and other capability-intelligence platforms on a shared contract.

The reasoning behind each design choice — why the tier vocabulary is what it is, why VOIs are immutable, why bi-temporality, what the system explicitly does not verify — is documented at **[docs.bukti.ai](https://docs.bukti.ai)**.

---

## Why it exists

The Bukti product at [bukti.ai](https://bukti.ai) ships three things that exist today:

1. A **reference implementation** of the protocol (closed-source — the product).
2. A **public discovery surface** that any LLM or agent can consume today: `skill.md`, `llms.txt`, JSON-LD on every profile page, A2A Agent Cards, and MCP tools mounted at `/mcp`. See the *Cross-reference* section below.
3. A **vocabulary** for evidence types, confidence tiers, and capability ontology — currently embedded in the product, which makes integration brittle for third parties.

The protocol splits that vocabulary out. Once the spec exists, any system that ingests or emits capability evidence can be "Bukti-compatible" without depending on Bukti the platform.

---

## What the protocol covers (and what it doesn't)

### In scope for v0.1

| Component | What is specified |
|---|---|
| **VOI — Verified Outcome Instance** | The atomic, immutable unit of evidence. Every capability claim is backed by one or more VOIs. Field-level JSON Schema defining `entity_id`, `capability_id`, `evidence_type`, `evidence_text`, `evidence_uri`, `source_platform`, `extraction_confidence`, `observed_at`, `recorded_at`, `supersedes_id`. |
| **Evidence type enumeration** | The 8 canonical evidence types: `behavioral_artifact`, `task_outcome`, `peer_attestation`, `contribution_artifact`, `publication_artifact`, `credential_badge`, `indirect_attestation`, `self_reported`. Normative meaning of each. |
| **Confidence tier vocabulary** | The three normative tier strings: `verified`, `attested`, `self-declared`. The *meaning* of each tier (aggregation of independent sources + evidence density + recency) is specified; the numeric thresholds and aggregation formula an implementer chooses are **not** mandated — only the semantics. |
| **Entity model** | `person`, `ai_agent`, `organization` entity types. Agent-specific operational metadata (runtime, modalities, cost per call, latency, MCP endpoint). |
| **Bi-temporal metadata** | Every claim carries valid-time and transaction-time. Corrections via append-only supersedes chains — never mutation. |
| **MCP tool contract** | The six Model Context Protocol tools a compliant implementation exposes: `search`, `verify`, `capability_provenance`, `profile`, `context`, `register`. Input and output schemas for each. |
| **REST surface** | Core endpoints for profile retrieval, capability listing, per-capability provenance drill-down, and agent registration. JSON body shapes. |
| **Ontology crosswalk** | Mapping between the O*NET Content Model (CC-BY-4.0 public base) and the domain-extension and growth-tier node naming conventions. |
| **Profile discovery surfaces** | Conventions for `llms.txt`, `skills.md` frontmatter, `agent.md`, and schema.org JSON-LD shapes (Person / SoftwareApplication / Organization with `hasCredential[]` links to provenance). |

### Explicitly out of scope for v0.1

The protocol does **not** prescribe:
- Specific evidence weight values or aggregation formula parameters (implementations choose).
- LLM model choices, extraction prompts, or routing logic.
- Graph database technology or storage layout.
- Entity resolution / deduplication heuristics.
- Pipeline orchestration (ingestion is an implementation concern).
- Cryptographic attestation or signing — see *Open questions for v0.1* below.

If an implementer wants to produce Bukti-compatible profiles without ever invoking an LLM, the protocol must make that possible. It will.

---

## Cross-reference: what's live on [bukti.ai](https://bukti.ai) today

The following are publicly callable or crawlable on the production platform right now. They are the interop surfaces the protocol will formalize:

| Surface | Live URL | Spec section (forthcoming) |
|---|---|---|
| Public discovery index for LLMs | `https://bukti.ai/llms.txt` | `docs/llms-txt.md` |
| Robots / AI-crawler policy | `https://bukti.ai/robots.txt` | — |
| Profile sitemap | `https://bukti.ai/sitemap.xml` | `docs/discovery.md` |
| Platform A2A agent card | `https://api.bukti.ai/.well-known/agent-card.json` | `docs/a2a.md` |
| Platform OpenClaw skill | `https://api.bukti.ai/skill.md` | `docs/openclaw.md` |
| Per-profile JSON-LD | inline in HTML `<head>` on `/p/{username}`, `/a/{username}`, `/b/{username}` | `docs/json-ld.md` |
| Per-profile skills.md | `https://api.bukti.ai/v1/profile/{id}/skills.md` | `docs/skills-md.md` |
| Per-profile agent.md | `https://api.bukti.ai/v1/profile/{id}/agent.md` | `docs/agent-md.md` |
| Per-profile JSON | `https://api.bukti.ai/v1/profile/{id}` | `docs/rest.md` |
| Capability provenance | `https://api.bukti.ai/v1/profile/{id}/capabilities/{cap_id}/provenance` | `docs/rest.md` |
| MCP server | `https://api.bukti.ai/mcp` (standard MCP handshake) | `docs/mcp.md` |
| Agent registration | `POST https://api.bukti.ai/v1/agent/register` | `docs/rest.md` |

The bukti.ai marketing site advertises the platform as **"A2A + MCP compliant"** with agent access via **"Chat prompt · MCP config · REST API · CLI"**. The three evidence tiers are surfaced publicly on the site as **Verified** / **Attested** / **Declared** — the protocol normalizes the third to `self-declared` for interop clarity (the shorter "Declared" is a UI label, not the wire value).

The site's published docs page names these evidence sources: **Resume, GitHub repositories, Publications, Credly badges, Project links, Benchmark results, Real-world usage data, Peer attestations**. The protocol maps each of these to one or more of the 8 evidence-type enum values.

---

## Repository layout

```
bukti-protocol/
├── README.md                 ← this file
├── LICENSE                   ← Apache-2.0 (see Licensing)
├── CONTRIBUTING.md           ← how to propose changes (forthcoming)
├── CHANGELOG.md              ← versioned changes to the spec (forthcoming)
├── docs/                     ← normative specification, one concern per file
│   ├── overview.md           ← entry point (forthcoming)
│   ├── voi.md                ← VOI object + evidence types (forthcoming)
│   ├── entity.md             ← Entity / AI agent / Organization (forthcoming)
│   ├── capability.md         ← Capability node + ontology crosswalk (forthcoming)
│   ├── tiers.md              ← confidence tier vocabulary + semantics (forthcoming)
│   ├── temporal.md           ← bi-temporal metadata (forthcoming)
│   ├── rest.md               ← REST API surface (forthcoming)
│   ├── mcp.md                ← MCP tool contract (forthcoming)
│   ├── a2a.md                ← A2A Agent Card extensions (forthcoming)
│   ├── openclaw.md           ← skill.md / OpenClaw integration (forthcoming)
│   ├── discovery.md          ← llms.txt, sitemap, JSON-LD (forthcoming)
│   ├── skills-md.md          ← skills.md frontmatter schema (forthcoming)
│   ├── agent-md.md           ← agent.md format (forthcoming)
│   └── json-ld.md            ← schema.org JSON-LD shapes (forthcoming)
├── schemas/                  ← machine-readable JSON Schemas
│   ├── voi.schema.json       ← (forthcoming)
│   ├── entity.schema.json    ← (forthcoming)
│   └── ...
└── examples/                 ← minimal compliant payloads for each shape
    └── ...
```

---

## Design principles

1. **Evidence is the primitive.** The protocol is built around VOIs, not around profiles, skills, or scores. A profile is a read-side projection of its VOIs. A score is a derived number over its VOIs. VOIs are what travel.
2. **Immutable append-only.** VOIs are never modified. Corrections are expressed by emitting a new VOI whose `supersedes_id` points at the earlier one. This makes evidence auditable over time.
3. **Bi-temporal by default.** Every claim carries both when-it-was-observed and when-it-was-recorded. Retrospective corrections don't rewrite history.
4. **Human- and machine-parseable equally.** A profile is simultaneously a human-readable portfolio, a schema.org JSON-LD document for search crawlers, a skills.md text file for LLM context injection, and an MCP-queryable graph for tool-enabled agents. Each surface is co-equal; one is not a degraded version of another.
5. **Vocabulary is normative; scoring is not.** The protocol mandates the shape of evidence, the evidence-type enum, and the tier vocabulary. The exact aggregation formula and weight values an implementer uses are not part of the spec — compliant systems can differ on scoring as long as they report tier, source count, and evidence count transparently.
6. **Vendor-agnostic.** No field in the spec will reference a specific LLM, database, or SaaS vendor.
7. **Three entity types, one protocol.** Humans, AI agents, and organizations share the same core schema. Agent- and org-specific extensions are additive.
8. **Citation and invocation are equal first-class modes.** LLMs that cite cached snapshots and agents that call live endpoints are both valid consumers. The protocol supports both without privileging either. (See `docs/discovery.md`.)

---

## What is open-sourced here (and what isn't)

### Open-sourced

- **Schema definitions.** JSON Schema for every object in the protocol (VOI, Entity, Capability, Provenance, Agent Card extensions).
- **Vocabulary.** The 8-value evidence type enum, the 3-tier confidence vocabulary, the capability ID prefix conventions.
- **Interop contracts.** The MCP tool input/output schemas, the REST endpoint shapes, the JSON-LD templates, the skills.md / agent.md format.
- **Ontology crosswalk.** Mapping between O*NET (CC-BY-4.0 base) and Bukti domain-extension IDs. Domain extensions authored by Bukti are released under the repository license below.
- **Methodology document.** The high-level reasoning behind the design — why VOIs are immutable, why bi-temporality, why evidence types are enumerated and not free-form. Enough to let a third party re-derive the shape if they disagreed with a specific field.
- **Reference examples.** Minimal compliant payloads for every shape.

### Not open-sourced (stays in the closed product)

- The specific aggregation formula a hosted implementation uses, including any numeric weights, thresholds, and decay parameters.
- LLM extraction, QA, and routing logic.
- Entity resolution and deduplication heuristics.
- Pipeline orchestration.
- Graph data and user content.
- The Bukti frontend.

The boundary is: *shapes and vocabularies* are public; *weights, prompts, formulas, and orchestration* are private. A third party implementing the protocol must be able to produce Bukti-compatible output without access to any of the private pieces.

---

## Relationship to existing standards

Bukti Protocol builds on, rather than replaces, several existing standards:

- **O*NET Content Model** (CC-BY-4.0, U.S. Department of Labor) — the seed layer of the capability ontology is the O*NET skill/knowledge/ability taxonomy. Bukti extends with domain-specific child nodes.
- **schema.org** — profile JSON-LD uses standard types (`Person`, `SoftwareApplication`, `Organization`, `EducationalOccupationalCredential`). No custom vocabulary where schema.org has coverage.
- **A2A (Agent-to-Agent)** — agent cards served at `/.well-known/agent-card.json` are A2A-compliant. Bukti-specific fields use the `x_bukti_*` extension prefix (a rename to a neutral prefix is a v0.1 open question).
- **MCP (Model Context Protocol)** — the tool server at `/mcp` is standard FastMCP. The 6 tools in the spec are registered using the MCP conventions; nothing in the handshake deviates.
- **Open Badges 3.0** — the `credential_badge` evidence type is designed to accept Open Badges 3.0 Verifiable Credentials as input without transformation. Bukti treats OB3.0 badges as first-class, issuer-verified evidence.
- **llms.txt** — the emerging convention for LLM-readable site indexing.

The protocol explicitly does **not** reinvent any of these. It adds the layer above: an evidence-aggregation model that ties disparate signals (O*NET-coded capabilities + OB3.0 badges + GitHub contributions + schema.org profiles) into a single queryable, tier-ranked, bi-temporal record.

---

## Open questions for v0.1 (to be resolved before public release)

The following are genuinely open and I am tracking them. Contributions welcome once the repo goes public.

1. **Cryptographic attestation.** The protocol has no signature primitive today. Options: (a) no attestation in v0.1 and declare it out of scope, (b) adopt W3C Verifiable Credentials wholesale, (c) define a minimal `attestation` optional field on VOIs. Leaning toward option (b) for `peer_attestation` and `credential_badge` types, with a lightweight optional field for others.
2. **Canonical VOI hashing.** `raw_signal_hash` exists on VOIs but has no mandated algorithm. Decide: canonical hashing scheme (so implementers dedup identically) or drop the field.
3. **Source platform vocabulary.** Currently free-form strings (`github`, `credly`, `upload`, `web_link`, `self_description`). Decide: closed enum vs. open-with-prefix-for-extensions.
4. **Organization entity.** Defined in enum, not implemented anywhere. Keep for forward-compat or defer to v0.2.
5. **Aggregate score publishing.** Is `evidence_score` (0–1 float) part of the public shape, or only tier + counts? The product surfaces it on `/v1/profile/{id}/capabilities` today, but some argue a protocol should leave the number private.
6. **A2A extension prefix.** Rename `x_bukti_*` to `x_protocol_*` or contribute these upstream to A2A.
7. **Timezone strictness.** Require UTC with offset in all ISO-8601 datetimes, or accept any timezone-aware format.
8. **Tailored views.** Out of scope for v0.1; tracked for later.

---

## Licensing

The protocol documentation and JSON schemas in this repository are licensed under the **Apache License, Version 2.0** — see `LICENSE`. Apache-2.0 includes a patent grant, which is standard for protocol specifications.

The O*NET Content Model used as the seed layer of the ontology is © U.S. Department of Labor and is licensed under CC-BY-4.0. Attribution is carried into any ontology export.

Open Badges 3.0 is a W3C specification and is not covered by this license.

Reference implementations of the protocol — if they are ever extracted from the closed product — will be released separately under a compatible license.

---

## Status and versioning

- **Current version:** `0.1.0-draft` (no tagged release yet).
- **Stability:** nothing is stable until `1.0.0`. Expect shape changes between drafts.
- **Semver:** the spec follows semver once tagged — MAJOR for breaking shape changes, MINOR for additive fields or new objects, PATCH for clarifications.

---

## Maintainers

Single maintainer at the v0.1 stage; governance is documented in [`CONTRIBUTING.md`](./CONTRIBUTING.md).

Questions: open a GitHub issue on this repository, or see the maintainer's contact on [bukti.ai](https://bukti.ai).
