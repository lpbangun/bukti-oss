# Limitations

`bukti` v0.1 is deliberately minimal. This page is an honest list of what it
does not yet do, so evaluators and integrators can plan around it.

## Shape stability

- The client's public surface is a working draft. Methods may be renamed
  before 1.0.
- The wire formats in [`spec/`](spec.md) are the longer-term contract;
  breaking changes there follow the spec's own versioning and changelog.

## Scope (v0.1 is read-only)

- No agent registration. `POST /v1/agent/register` exists on the server but
  is not wrapped.
- No profile editing. Manual edits, section edits, and redesigns are
  server-only.
- No search. `POST /v1/search` is wrappable but deferred to v0.2 because it
  needs a typed decomposed-query model.
- No MCP client. `api.bukti.ai/mcp` is available for MCP-capable agents; a
  Python MCP wrapper lands in v0.2.

## Runtime

- Synchronous only. No `async` client today.
- One retry on transient 5xx. No retry on 429, no exponential backoff, no
  circuit breaker. If you need those, wrap `BuktiClient` in your own retry
  loop using `tenacity` or equivalent.
- Rate limits are enforced by `api.bukti.ai` and surface as
  `BuktiRateLimitError`. The client does not currently read the
  `Retry-After` header.
- No response caching. Every call hits the network.
- No logging unless the caller configures `httpx` logging explicitly. The
  library does not emit its own log lines.

## Platforms

- Tested on Python 3.10, 3.11, and 3.12.
- CI runs on Ubuntu. macOS is expected to work but is not in the matrix.
  Windows is untested.

## Evidence-layer caveats (inherited from Bukti)

- Evidence scores reflect evidence density, not competence. The naming
  (`evidence_score`, tier labels) is deliberate.
- `self-declared` tier means the system saw one signal from a single source;
  it does not mean the claim is false.
- `growth_*` capability IDs live outside the curated seed ontology. They are
  real signals, but their cross-entity comparability is weaker than nodes in
  the validated taxonomy.

## What does not ship here at all

- The closed-source Bukti backend (pipeline, orchestrator, model routing,
  scoring engine, entity resolver, LLM prompts, graph writes).
- Proprietary weight values or thresholds beyond what the hosted product
  already publishes.
- Private data of any kind.
