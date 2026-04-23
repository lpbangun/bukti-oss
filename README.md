# Bukti — Python client, CLI, and open protocol for capability intelligence

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

## What this is

[Bukti](https://bukti.ai) is a capability intelligence platform. It turns
public artifacts (repositories, credentials, publications, project write-ups)
into evidence-backed capability claims about people, AI agents, and
organizations, and exposes those claims over HTTP, MCP, and A2A-compliant
surfaces.

This repository is the open layer of Bukti. It contains the Python client and
CLI that wrap the public HTTP API, plus the open specification the client
implements.

## Two layers

This repository contains two layers. The `src/bukti/` package and CLI are the
runnable client: install with pip and start querying. The [`spec/`](./spec/)
directory contains the Bukti Protocol, the open specification this client
implements. Both are Apache 2.0 licensed. If you are here to use Bukti from
Python, start below. If you are here to understand or implement the protocol
yourself, see [`spec/`](./spec/).

The Bukti backend that serves `api.bukti.ai` is closed-source and is not part
of this repository.

## Install

```bash
pip install git+https://github.com/bukti-ai/bukti
```

(PyPI publication lands in a later release. Pin to a commit SHA in production
for now.)

## Quickstart — Python

```python
from bukti import BuktiClient

with BuktiClient() as bukti:
    profile = bukti.get_profile("agent_0be6d7cce0e8")
    print(profile.display_name, "-", len(profile.capabilities), "capabilities")
```

## Quickstart — CLI

```bash
bukti profile agent_0be6d7cce0e8
bukti capabilities agent_0be6d7cce0e8
```

## CLI reference

| Command | Purpose |
|---------|---------|
| `bukti profile <entity_id>` | Pretty-printed profile summary. |
| `bukti capabilities <entity_id>` | Table of capabilities grouped by tier. |
| `bukti provenance <entity_id> <capability_id>` | Evidence chain (VOIs) for one capability. |
| `bukti version` | Print the client version. |

Global flags: `--api-key` (or `BUKTI_API_KEY` env var), `--base-url`,
`--json` (machine-readable output).

## Python API reference

`BuktiClient` is a thin synchronous wrapper with four public methods:
`get_profile`, `list_capabilities`, `get_provenance`,
`get_capability_provenance`. Each returns a Pydantic model matching the
shapes in [`spec/`](./spec/). See [`docs/usage.md`](./docs/usage.md) for full
method signatures and examples.

## Architecture

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
                                            │      spec/           │
                                            │  (open, Apache-2.0)  │
                                            └──────────────────────┘
```

The client is a thin HTTP wrapper over `api.bukti.ai`. The server is the
closed-source Bukti platform. The open specification in `spec/` defines the
wire contract the client implements; any third party can write a compatible
client or a compatible server.

## Limitations

v0.1 is a minimum-useful release. Honest list of what it does not do:

- **API may change before 1.0.** Shapes in `spec/` are the stable contract
  going forward; the client surface may rename methods before 1.0.
- **Synchronous only.** An async variant is planned.
- **Read-only.** Agent registration, manual profile edits, and search
  decomposition are exposed by `api.bukti.ai` but not yet wrapped.
- **No MCP client.** The hosted `/mcp` surface works today for MCP-capable
  agents. A Python MCP client wrapper lands in v0.2.
- **Rate limits** enforced by `api.bukti.ai` apply. `BuktiRateLimitError`
  surfaces 429 responses; the client does not currently retry them.
- **Tested on Python 3.10–3.12 on Linux and macOS.** Windows is not part of
  the test matrix; contributions welcome.
- **Retries are minimal.** One retry on transient 5xx, nothing else.

## The protocol

The full specification lives in [`spec/`](./spec/). It covers the VOI
(Verified Outcome Instance) evidence primitive, the three entity types
(person, AI agent, organization), the confidence tiering vocabulary, the
capability ontology (O\*NET + domain extensions), and the interop surfaces
(REST, MCP, A2A, OpenClaw, discovery files). The spec versions and ships
independently of the client.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Client changes follow the normal
PR flow. Specification changes follow [`spec/CONTRIBUTING.md`](./spec/CONTRIBUTING.md).

## License

Apache License 2.0 for both layers. See [LICENSE](./LICENSE) and
[NOTICE](./NOTICE) (the latter carries O\*NET attribution for the seed
ontology extended in `spec/`).

## Links

- [bukti.ai](https://bukti.ai)
- Specification: [`spec/`](./spec/)
- Issues: file them against this repository.
