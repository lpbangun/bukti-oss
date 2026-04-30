# Architecture

```
┌──────────┐     ┌──────────────┐     HTTPS      ┌───────────────┐
│  bukti   │ ──▶ │ BuktiClient  │ ─────────────▶ │ api.bukti.ai  │
│  (CLI)   │     │  (Pydantic)  │                │  (closed)     │
└──────────┘     └──────────────┘                └───────────────┘
      ▲                                                  │
      │                                                  │ implements
      └───── implements ────────────────────────────────▶│
                                                          │
                                            ┌──────────────────────┐
                                            │   Bukti Protocol     │
                                            │       spec/          │
                                            │  (open, Apache-2.0)  │
                                            └──────────────────────┘
```

## Layers

**CLI (`src/bukti/cli.py`).** Click + Rich. Parses flags, picks an output
mode (rich or JSON), constructs a `BuktiClient`, hands results to a
formatter, maps `BuktiError` to a non-zero exit code.

**Client (`src/bukti/client.py`).** Synchronous HTTP wrapper on `httpx`.
Every method takes primitive arguments and returns a Pydantic model. One
retry on transient 5xx; everything else surfaces as a typed exception.

**Models (`src/bukti/models.py`).** Pydantic v2 mirrors of the public API
response shapes. Extra fields from the server are ignored, so additive API
changes do not break pinned clients.

**Server (`api.bukti.ai`).** Closed-source. Runs the pipeline that turns
public artifacts into VOIs (Verified Outcome Instances) and serves the
public read surface. This repository has no backend code.

**Specification (`spec/`).** Implementation-agnostic description of the wire
formats the client depends on. Anyone can implement it.

## Request path

1. Caller invokes `bukti.get_profile("agent_example_01")` (or the
   equivalent CLI command).
2. Client assembles `GET /v1/profile/agent_example_01` against the
   configured base URL.
3. Server returns JSON; `Profile.model_validate(...)` parses it.
4. Client returns the typed object; CLI formats it.

## What the server does that the client does not

Only the hosted Bukti backend runs the ingestion pipeline, the evidence
scoring engine, the ontology mapper, the entity resolver, and the
profile-generation LLMs. The client only consumes the published output. The
protocol specification describes the output format; it does not describe the
backend's internal implementation.
