# Changelog

All notable changes to this repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the client package follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
The Bukti Protocol specification in `spec/` has its own changelog at
`spec/CHANGELOG.md` and is versioned independently.

## [0.1.0] — Initial release

### Added
- `bukti` Python client (`BuktiClient`) with read-only methods for profile,
  capability listing, and capability-level provenance against
  `https://api.bukti.ai`.
- `bukti` CLI with subcommands: `profile`, `capabilities`, `provenance`,
  `version`.
- Runnable examples under `examples/` for the three main client methods.
- Pytest suite covering happy paths, every error type, the single-retry 5xx
  behavior, and CLI subcommand output.
- MkDocs site (Material theme) covering setup, usage, architecture,
  limitations, and specification pointers.
- Bukti Protocol specification v0.1-draft vendored under `spec/` (see
  `spec/CHANGELOG.md`).

### Notes
- v0.1 is read-only. Agent registration, search decomposition, and the MCP
  client are deferred to a later release.
- API shapes may change before the client reaches 1.0. Pin to `0.1.x` for
  today's stability guarantees.
