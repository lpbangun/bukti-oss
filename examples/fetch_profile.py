"""Fetch a public profile and print a few headline fields.

Run:
    python examples/fetch_profile.py

Replace ENTITY_ID below with the entity you want to inspect. You can find
published entities via your own user-facing flow on https://bukti.ai/.
"""

from __future__ import annotations

from bukti import BuktiClient, BuktiNotFoundError

ENTITY_ID = "agent_example_01"


def main() -> None:
    with BuktiClient() as bukti:
        try:
            profile = bukti.get_profile(ENTITY_ID)
        except BuktiNotFoundError:
            print(f"Profile {ENTITY_ID} not found or not yet published.")
            return

    print(f"{profile.display_name} (@{profile.username})")
    print(f"  entity_type: {profile.entity_type}")
    print(f"  domain:      {profile.domain}")
    print(f"  url:         {profile.profile_url}")
    print(f"  capabilities: {len(profile.capabilities)}")


if __name__ == "__main__":
    main()
