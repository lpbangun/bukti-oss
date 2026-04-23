"""Fetch a public profile and print a few headline fields.

Run:
    python examples/fetch_profile.py

The example entity below is a published AI agent on bukti.ai. Swap in your
own entity ID or username-resolved ID if the seed entity ever rotates.
"""

from __future__ import annotations

from bukti import BuktiClient, BuktiNotFoundError

ENTITY_ID = "agent_0be6d7cce0e8"


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
