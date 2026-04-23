"""CLI smoke tests using Click's CliRunner."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from bukti import __version__
from bukti.cli import cli
from bukti.models import (
    Capability,
    CapabilityProvenance,
    Evidence,
    Profile,
)


def _sample_profile() -> Profile:
    return Profile(
        entity_id="agent_example",
        entity_type="ai_agent",
        username="example-agent",
        display_name="Example Agent",
        domain="software_engineering",
        portfolio_text="Agent used in CLI tests.",
        llm_summary="A short summary.",
        profile_url="https://bukti.ai/a/example-agent",
        capabilities=[_sample_capability()],
    )


def _sample_capability() -> Capability:
    return Capability(
        capability_id="cap_example",
        name="Example Capability",
        evidence_score=0.82,
        tier="verified",
        evidence_count=4,
        source_count=2,
        source_platforms=["github", "credly"],
    )


def _sample_capability_provenance() -> CapabilityProvenance:
    return CapabilityProvenance(
        entity_id="agent_example",
        capability_id="cap_example",
        capability_name="Example Capability",
        evidence_count=1,
        tier="verified",
        evidence_score=0.82,
        source_platforms=["github"],
        evidence=[
            Evidence(
                voi_id="voi_1",
                source_platform="github",
                evidence_type="contribution_artifact",
                observed_at="2026-01-01T00:00:00",
                extraction_confidence=0.9,
                evidence_text="Merged PR.",
            )
        ],
    )


def test_version_command() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_profile_command_text_output() -> None:
    runner = CliRunner()
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.get_profile.return_value = _sample_profile()
    with patch("bukti.cli.BuktiClient", return_value=mock_client):
        result = runner.invoke(cli, ["profile", "agent_example"])
    assert result.exit_code == 0
    assert "Example Agent" in result.output


def test_profile_command_json_output() -> None:
    runner = CliRunner()
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.get_profile.return_value = _sample_profile()
    with patch("bukti.cli.BuktiClient", return_value=mock_client):
        result = runner.invoke(cli, ["--json", "profile", "agent_example"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["entity_id"] == "agent_example"


def test_capabilities_command() -> None:
    runner = CliRunner()
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.list_capabilities.return_value = [_sample_capability()]
    with patch("bukti.cli.BuktiClient", return_value=mock_client):
        result = runner.invoke(cli, ["capabilities", "agent_example"])
    assert result.exit_code == 0
    assert "Example Capability" in result.output
    assert "verified" in result.output


def test_provenance_command() -> None:
    runner = CliRunner()
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.get_capability_provenance.return_value = _sample_capability_provenance()
    with patch("bukti.cli.BuktiClient", return_value=mock_client):
        result = runner.invoke(cli, ["provenance", "agent_example", "cap_example"])
    assert result.exit_code == 0
    assert "Example Capability" in result.output
    assert "contribution_artifact" in result.output


def test_profile_command_handles_error() -> None:
    from bukti.exceptions import BuktiNotFoundError

    runner = CliRunner()
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.get_profile.side_effect = BuktiNotFoundError("nope", status_code=404)
    with patch("bukti.cli.BuktiClient", return_value=mock_client):
        result = runner.invoke(cli, ["profile", "ghost"])
    assert result.exit_code == 1
    assert "error" in result.output.lower()
