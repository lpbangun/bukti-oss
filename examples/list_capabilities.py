"""List every capability on a profile grouped by tier.

Run:
    python examples/list_capabilities.py
"""

from __future__ import annotations

from collections import defaultdict

from bukti import BuktiClient

ENTITY_ID = "agent_0be6d7cce0e8"


def main() -> None:
    with BuktiClient() as bukti:
        caps = bukti.list_capabilities(ENTITY_ID)

    by_tier: dict[str, list[str]] = defaultdict(list)
    for cap in caps:
        line = f"  {cap.name}  ({cap.evidence_score:.2f}, {cap.evidence_count} ev.)"
        by_tier[cap.tier].append(line)

    for tier in ("verified", "attested", "self-declared"):
        rows = by_tier.get(tier, [])
        if not rows:
            continue
        print(f"{tier.upper()} ({len(rows)})")
        for row in rows:
            print(row)


if __name__ == "__main__":
    main()
