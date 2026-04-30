# Bukti

The `bukti` Python package is a thin client for the Bukti capability
intelligence platform. It wraps the public HTTP API at
[`api.bukti.ai`](https://api.bukti.ai) and implements the open Bukti
Protocol specification that lives in [`spec/`](https://github.com/lpbangun/bukti-oss/tree/main/spec).

Use these docs to:

- [Install and make your first call.](setup.md)
- [Browse the client and CLI surface.](usage.md)
- [See how the layers fit together.](architecture.md)
- [Understand what v0.1 does not do.](limitations.md)
- [Read the methodology that motivates the protocol.](methodology.md)
- [Jump into the protocol specification.](spec.md)

## Who this is for

- **Python developers** who want to query Bukti profiles, capabilities, and
  evidence chains from a script, a notebook, or a backend service.
- **Agent developers** who want an evidence-grounded signal about other
  agents (cost, latency, modality, capability provenance).
- **Protocol implementers** who want to build a compatible client in another
  language, or a compatible server — both of which the specification covers.

## Minimum example

```python
from bukti import BuktiClient

with BuktiClient() as bukti:
    profile = bukti.get_profile("agent_example_01")
    for cap in profile.capabilities:
        print(f"{cap.tier:<12} {cap.name}  ({cap.evidence_score:.2f})")
```

That is the whole library in miniature. Everything else is variations on
this: list every capability, fetch the underlying VOIs for one capability,
or scan the provenance manifest for a whole profile.
