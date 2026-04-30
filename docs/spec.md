# Specification

The Bukti Protocol specification lives in [`spec/`](https://github.com/lpbangun/bukti-oss/tree/main/spec)
at the root of the repository. This page is a pointer and a summary; the
specification itself is the normative source.

## What the spec covers

- **[`spec/README.md`](https://github.com/lpbangun/bukti-oss/tree/main/spec)** — top-level overview, design principles, cross-reference from spec sections to live `bukti.ai` surfaces, and the in-scope / out-of-scope lists.
- **[`spec/docs/`](https://github.com/lpbangun/bukti-oss/tree/main/spec/docs)** — normative specification files (one concern per file: VOI, Entity, Capability, tiers, temporal semantics, REST, MCP, A2A, OpenClaw, discovery files, `skills.md`, `agent.md`, JSON-LD).
- **[`spec/schemas/`](https://github.com/lpbangun/bukti-oss/tree/main/spec/schemas)** — machine-readable JSON Schema definitions (`$schema` = draft 2020-12) for every object in the protocol.
- **[`spec/examples/`](https://github.com/lpbangun/bukti-oss/tree/main/spec/examples)** — minimal compliant payloads for every object and every interop surface.
- **[`spec/CONTRIBUTING.md`](https://github.com/lpbangun/bukti-oss/tree/main/spec/CONTRIBUTING.md)** — governance, style guide, and the list of change types that require discussion before a PR.
- **[`spec/CHANGELOG.md`](https://github.com/lpbangun/bukti-oss/tree/main/spec/CHANGELOG.md)** — independent version history for the specification.

## Relationship to this client

The client in `src/bukti/` implements the read-only subset of the spec's
REST surface. The Pydantic models in `src/bukti/models.py` mirror the shapes
defined normatively in `spec/schemas/`. When the two disagree, `spec/` is
the source of truth; file an issue.

## Versioning

The client and the specification version independently:

| Artifact | Version today | Versioning rule |
|----------|---------------|-----------------|
| `bukti` Python client | 0.1.0 | Semver; breaking changes require a major bump once at 1.0. |
| Bukti Protocol | 0.1.0-draft | Semver; draft suffix while shapes are still being finalized. |

## How to read the spec for an implementation

1. Start with `spec/README.md` for the mental model.
2. Read the VOI, Entity, Capability, and tiers documents (in that order) for
   the core objects.
3. Read whichever interop surface documents you need (REST, MCP, A2A,
   OpenClaw, discovery).
4. Validate any payloads you produce against `spec/schemas/*.schema.json`.
5. Compare against `spec/examples/*.json` for complete reference payloads.
