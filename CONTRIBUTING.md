# Contributing

Thanks for the interest. This repository has two layers and they accept
changes a little differently.

## The client and CLI (`src/bukti/`, `tests/`, `examples/`, `docs/`)

Normal OSS flow. If the change is small (a typo, a bug fix with a test), open
a PR. For anything larger (a new client method, an error-handling change, a
CLI subcommand), open an issue first so we can agree on the shape before you
write code.

What we ask of every PR:

- Tests pass locally: `pytest`.
- Lint is clean: `ruff check src/ tests/`.
- New code has docstrings and type hints.
- No secrets, no copied backend code, no hard-coded credentials.

## The protocol specification (`spec/`)

The specification has its own governance, described in
[`spec/CONTRIBUTING.md`](./spec/CONTRIBUTING.md). Spec changes go through that
process. Breaking shape changes require an issue discussion first; we keep
the normative surface small on purpose.

## Scope — what does NOT belong here

- The closed-source Bukti backend. Bug reports for `api.bukti.ai` go to the
  maintainers privately.
- Feature requests for the hosted `bukti.ai` product.
- Integration adapters to third-party platforms. Those can live in their own
  repositories and depend on this package.

## License of contributions

By opening a PR you agree your contribution is licensed under the Apache
License 2.0 (see `LICENSE`) and that you have the right to license it that
way. The same applies to spec contributions.

## Code style

- Python: ruff (config in `pyproject.toml`). Line length 120. No `# type:
  ignore` without a reason on the same line.
- Docstrings: concise. One sentence for simple functions, a short block with
  an Args/Raises section for anything public-facing.
- No `print()` in library code. The CLI uses Click + Rich; the client does
  not log unless a caller configures it.
