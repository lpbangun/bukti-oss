"""Show the Verified Outcome Instance (VOI) chain for one capability.

Run:
    python examples/get_provenance.py
"""

from __future__ import annotations

from bukti import BuktiClient

ENTITY_ID = "agent_0be6d7cce0e8"


def main() -> None:
    with BuktiClient() as bukti:
        caps = bukti.list_capabilities(ENTITY_ID)
        if not caps:
            print(f"No capabilities on {ENTITY_ID}.")
            return
        top = caps[0]
        chain = bukti.get_capability_provenance(ENTITY_ID, top.capability_id)

    print(f"{chain.capability_name}  [{chain.tier} @ {chain.evidence_score:.2f}]")
    print(f"  sources: {', '.join(chain.source_platforms) or '(none)'}")
    for ev in chain.evidence:
        print(f"  - {ev.evidence_type} via {ev.source_platform} ({ev.voi_id})")
        if ev.evidence_text:
            snippet = ev.evidence_text.replace("\n", " ")
            print(f"      {snippet[:120]}")


if __name__ == "__main__":
    main()
