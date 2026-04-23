"""Command-line interface for the Bukti client.

Usage:
    bukti profile <entity_id>
    bukti capabilities <entity_id>
    bukti provenance <entity_id> <capability_id>
    bukti version
"""

from __future__ import annotations

import json
import sys
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bukti import __version__
from bukti.client import DEFAULT_BASE_URL, BuktiClient
from bukti.exceptions import BuktiError

_TIER_ORDER = {"verified": 0, "attested": 1, "self-declared": 2}


def _make_client(ctx: click.Context) -> BuktiClient:
    opts = ctx.obj or {}
    return BuktiClient(
        base_url=opts.get("base_url", DEFAULT_BASE_URL),
        api_key=opts.get("api_key"),
    )


def _emit_json(payload: Any) -> None:
    click.echo(json.dumps(payload, indent=2, default=str))


def _fail(message: str, exit_code: int = 1) -> None:
    click.echo(f"error: {message}", err=True)
    sys.exit(exit_code)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--api-key", envvar="BUKTI_API_KEY", default=None, help="API key (defaults to $BUKTI_API_KEY).")
@click.option("--base-url", default=DEFAULT_BASE_URL, show_default=True, help="API base URL.")
@click.option("--json", "as_json", is_flag=True, help="Emit raw JSON instead of formatted output.")
@click.pass_context
def cli(ctx: click.Context, api_key: str | None, base_url: str, as_json: bool) -> None:
    """Bukti — capability intelligence from the command line."""
    ctx.ensure_object(dict)
    ctx.obj.update({"api_key": api_key, "base_url": base_url, "json": as_json})


@cli.command()
@click.argument("entity_id")
@click.pass_context
def profile(ctx: click.Context, entity_id: str) -> None:
    """Show a profile by entity ID."""
    as_json = ctx.obj.get("json", False)
    try:
        with _make_client(ctx) as client:
            result = client.get_profile(entity_id)
    except BuktiError as exc:
        _fail(str(exc))

    if as_json:
        _emit_json(result.model_dump())
        return

    console = Console()
    header = f"[bold]{result.display_name or result.entity_id}[/bold]"
    if result.username:
        header += f"  [dim]@{result.username}[/dim]"
    body_lines = [
        header,
        f"[dim]entity_id:[/dim] {result.entity_id}",
        f"[dim]entity_type:[/dim] {result.entity_type}    [dim]domain:[/dim] {result.domain}",
    ]
    if result.profile_url:
        body_lines.append(f"[dim]url:[/dim] {result.profile_url}")
    if result.llm_summary:
        body_lines.append("")
        body_lines.append(result.llm_summary)
    elif result.portfolio_text:
        body_lines.append("")
        body_lines.append(result.portfolio_text[:500])
    console.print(Panel("\n".join(body_lines), border_style="cyan"))
    console.print(
        f"[dim]{len(result.capabilities)} capabilities · "
        f"run `bukti capabilities {result.entity_id}` for detail[/dim]"
    )


@cli.command()
@click.argument("entity_id")
@click.pass_context
def capabilities(ctx: click.Context, entity_id: str) -> None:
    """List capabilities for a profile, sorted by tier."""
    as_json = ctx.obj.get("json", False)
    try:
        with _make_client(ctx) as client:
            caps = client.list_capabilities(entity_id)
    except BuktiError as exc:
        _fail(str(exc))

    if as_json:
        _emit_json([c.model_dump() for c in caps])
        return

    caps_sorted = sorted(
        caps,
        key=lambda c: (_TIER_ORDER.get(c.tier, 99), -c.evidence_score),
    )

    console = Console()
    table = Table(title=f"Capabilities for {entity_id}", show_lines=False)
    table.add_column("Capability")
    table.add_column("Tier")
    table.add_column("Score", justify="right")
    table.add_column("Evidence", justify="right")
    table.add_column("Sources")

    tier_style = {"verified": "green", "attested": "yellow", "self-declared": "dim"}
    for cap in caps_sorted:
        tier_color = tier_style.get(cap.tier, "white")
        table.add_row(
            cap.name or cap.capability_id,
            f"[{tier_color}]{cap.tier}[/{tier_color}]",
            f"{cap.evidence_score:.2f}",
            str(cap.evidence_count),
            ", ".join(cap.source_platforms) or "-",
        )
    console.print(table)


@cli.command()
@click.argument("entity_id")
@click.argument("capability_id")
@click.pass_context
def provenance(ctx: click.Context, entity_id: str, capability_id: str) -> None:
    """Show the evidence chain for one capability on one profile."""
    as_json = ctx.obj.get("json", False)
    try:
        with _make_client(ctx) as client:
            result = client.get_capability_provenance(entity_id, capability_id)
    except BuktiError as exc:
        _fail(str(exc))

    if as_json:
        _emit_json(result.model_dump())
        return

    console = Console()
    header = (
        f"[bold]{result.capability_name}[/bold]  "
        f"[dim]{result.capability_id}[/dim]\n"
        f"tier: {result.tier}   score: {result.evidence_score:.2f}   "
        f"evidence: {result.evidence_count}"
    )
    console.print(Panel(header, border_style="cyan"))

    if not result.evidence:
        console.print("[dim]No evidence records returned.[/dim]")
        return

    table = Table(show_lines=False)
    table.add_column("VOI")
    table.add_column("Type")
    table.add_column("Platform")
    table.add_column("Observed")
    table.add_column("Snippet")
    for ev in result.evidence:
        snippet = (ev.evidence_text or "").strip().replace("\n", " ")
        if len(snippet) > 80:
            snippet = snippet[:77] + "..."
        table.add_row(
            ev.voi_id,
            ev.evidence_type,
            ev.source_platform,
            (ev.observed_at or "-")[:10],
            snippet or "-",
        )
    console.print(table)


@cli.command()
def version() -> None:
    """Print the client version."""
    click.echo(f"bukti {__version__}")


def main(args: list[str] | None = None) -> None:
    """Entry point registered as the ``bukti`` console script."""
    cli.main(args=args, prog_name="bukti", standalone_mode=True)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
