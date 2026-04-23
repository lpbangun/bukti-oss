# Contributing to Bukti Protocol

> **Private-draft phase.** This repository is not yet public. Once it is, this file will be expanded. For now it records the intended governance model so a future public contributor can understand how proposals will be handled.

## Scope

This repository is for the Bukti Protocol specification only — the shapes, vocabularies, and interop contracts described in `README.md`. It is **not** a place for:
- Bugs in the bukti.ai product — those belong to the closed product repo.
- Feature requests for the bukti.ai product.
- Questions about a specific implementation — see `docs/` or open a discussion once the repo is public.

## Types of contribution welcome

1. **Clarifications.** A field description is ambiguous; a worked example would help.
2. **Open-question input.** `README.md` lists the open questions for v0.1. Reasoned input on any of them is welcome.
3. **Additional examples.** Minimal compliant payloads for edge cases.
4. **Ontology contributions.** Proposals for new domain-extension capability IDs, with justification against the O*NET base.
5. **Errata.** Typos, broken links, schema validation errors.
6. **Compatibility reports.** "I implemented the spec. Here's what I found."

## Types of change that need discussion before a PR

- **Breaking shape changes.** Adding, removing, or retyping a field on any object. Open an issue first.
- **New evidence types.** The 8-value enum is intentionally small. Additions require justification that the new type is not expressible as a combination of existing ones.
- **Tier vocabulary changes.** The three tiers are normative. Additions or renames need strong justification.
- **New interop surfaces.** Proposing a new REST endpoint or MCP tool.

## How to propose a change

1. Open an issue describing what you want to change and why. Include a concrete motivating example.
2. Wait for a maintainer reply. If the proposal is in-scope, a maintainer will either work on it or invite a PR.
3. Send a PR referencing the issue. Keep PRs small and focused on one concern.
4. A maintainer will merge, request changes, or decline with a reason.

## Style guide for spec documents

- One concern per file under `docs/`. Don't grow files beyond ~500 lines — split instead.
- Field tables use the columns: Field · Type · Required · Description · Notes.
- Use `string`, `integer`, `number`, `boolean`, `array`, `object`, `null`, `datetime` as type names. Avoid language-specific types.
- Every normative statement uses MUST / SHOULD / MAY per RFC 2119. Don't sprinkle them decoratively.
- Every example is a complete, valid payload. No ellipses, no placeholders. Show the whole thing.
- Every reference to an external standard links to its canonical source.

## Versioning

- The spec follows semver once tagged.
- Draft versions use the `0.x.y-draft` pattern. No compatibility guarantees during draft.
- Changes land in `CHANGELOG.md` with the exact version they appear in.

## License

Contributions are licensed under the same Apache-2.0 license as the repository. By sending a PR, you agree your contribution is licensed under Apache-2.0 and that you have the right to license it that way.
