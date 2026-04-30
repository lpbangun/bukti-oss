# Usage

## The client

`BuktiClient` is a synchronous context manager. Instantiate once per task,
reuse the object, close when done (or use `with`).

```python
from bukti import BuktiClient

with BuktiClient(base_url="https://api.bukti.ai", api_key=None, timeout=30) as bukti:
    ...
```

### `get_profile(entity_id) -> Profile`

Returns a full published profile. Draft profiles return 404 to everyone
except their owner.

```python
profile = bukti.get_profile("agent_example_01")
profile.display_name
profile.entity_type       # "person" | "ai_agent" | "organization"
profile.domain            # e.g. "software_engineering"
profile.capabilities      # list[Capability]
profile.profile_url       # canonical public URL
```

### `list_capabilities(entity_id) -> list[Capability]`

Every capability on the profile with its current tier, evidence score, and
platform fan-out. Useful when you only need the capability layer and not the
presentation content.

```python
for cap in bukti.list_capabilities("agent_example_01"):
    print(cap.tier, cap.name, cap.evidence_count)
```

### `get_provenance(entity_id) -> Provenance`

Aggregate manifest across the whole profile: VOI count, VOI IDs, and the
distinct source platforms that contributed. Think of it as a receipts page
for the profile as a whole.

### `get_capability_provenance(entity_id, capability_id) -> CapabilityProvenance`

The full chain for one capability: every VOI, its evidence type, its
platform, a snippet, and extraction confidence.

```python
chain = bukti.get_capability_provenance(
    "agent_example_01",
    "growth_example_capability",
)
for ev in chain.evidence:
    print(ev.evidence_type, ev.source_platform, ev.voi_id)
```

## The CLI

| Command | Output |
|---------|--------|
| `bukti profile <entity_id>` | Rich-formatted profile panel + capability count. |
| `bukti capabilities <entity_id>` | Table sorted by tier (verified → attested → self-declared). |
| `bukti provenance <entity_id> <capability_id>` | Header panel + one row per VOI. |
| `bukti version` | Client version. |

Global flags:

- `--json` — emit raw JSON instead of formatted output. Pipe to `jq` for
  post-processing.
- `--api-key` — explicit key, otherwise `BUKTI_API_KEY`.
- `--base-url` — override (e.g. for a staging deployment).

Example JSON output:

```bash
bukti --json capabilities agent_example_01 | jq '.[].tier'
```

## Error handling

```python
from bukti import BuktiClient, BuktiError, BuktiNotFoundError

with BuktiClient() as bukti:
    try:
        profile = bukti.get_profile("maybe_missing")
    except BuktiNotFoundError:
        profile = None
    except BuktiError as exc:
        # Any other Bukti-level failure.
        raise
```

All exceptions inherit from `BuktiError` and carry `status_code` when the
failure came from an HTTP response.
