"""Bukti — Python client and CLI for capability intelligence.

The client is a thin wrapper over the public HTTP API at https://api.bukti.ai.
It implements the Bukti Protocol, whose open specification lives in ../spec/.
"""

from bukti.client import BuktiClient
from bukti.exceptions import (
    BuktiAuthError,
    BuktiError,
    BuktiNotFoundError,
    BuktiRateLimitError,
    BuktiServerError,
)
from bukti.models import (
    Capability,
    CapabilityProvenance,
    Evidence,
    Profile,
    Provenance,
    Source,
)

__version__ = "0.1.0"

__all__ = [
    "BuktiClient",
    "BuktiError",
    "BuktiNotFoundError",
    "BuktiAuthError",
    "BuktiRateLimitError",
    "BuktiServerError",
    "Profile",
    "Capability",
    "Provenance",
    "CapabilityProvenance",
    "Evidence",
    "Source",
    "__version__",
]
