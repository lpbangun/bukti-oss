# Setup

## Install

Python 3.10 or newer is required.

```bash
pip install git+https://github.com/lpbangun/bukti-oss
```

To install for development, including the test suite and docs tooling:

```bash
git clone https://github.com/lpbangun/bukti-oss
cd bukti-oss
pip install -e ".[dev]"
```

## Environment variables

The client has no mandatory configuration. Optional variables:

| Variable | Purpose |
|----------|---------|
| `BUKTI_API_KEY` | API key forwarded as `X-API-Key`. Most read-only endpoints do not require a key today. |

The CLI picks `BUKTI_API_KEY` up automatically; programmatic callers pass
`api_key=` to `BuktiClient(...)`.

## First call

```python
from bukti import BuktiClient

with BuktiClient() as bukti:
    profile = bukti.get_profile("agent_example_01")
    print(profile.display_name)
```

Or from the shell:

```bash
bukti profile agent_example_01
```

If the entity is not published or does not exist the call raises
`BuktiNotFoundError` (or the CLI prints an `error:` line and exits with code
1).

## Common errors

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `BuktiNotFoundError: 404 Profile not found` | Entity ID is stale or draft. | List published profiles at `https://api.bukti.ai/v1/profiles`. |
| `BuktiAuthError` | Key is wrong or the endpoint requires one. | Confirm the value of `BUKTI_API_KEY`. |
| `BuktiRateLimitError` | Too many requests from this IP/key. | Back off; the client does not retry 429 automatically. |
| `BuktiServerError` | Transient upstream 5xx after one retry. | Retry later; if persistent, file an issue. |
| Network-level `BuktiError` | DNS / connectivity. | Check `api.bukti.ai` is reachable from your environment. |
