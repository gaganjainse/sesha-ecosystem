#!/usr/bin/env python3
"""Generate MCP client configs from the ecosystem manifest.

Reads manifests/components.toml and writes per-client configuration files
so all the shesh-* MCP servers are wired into editors/assistants:

  ~/.config/shesh/mcp/servers.json   - canonical list (consumed by our servers)
  ~/.config/shesh/mcp/newelle.json   - Newelle MCP integration
  ~/.config/shesh/mcp/zed.json       - Zed editor context_servers

The generator is idempotent and only enables components on the requested
channel. It never overwrites secrets; server commands use the installed
console_scripts (shesh-*-mcp).
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

import tomllib  # Python 3.11+

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "shesh" / "mcp"

# Map repo -> MCP command name (the console_script each package installs)
SERVER_COMMANDS = {
    "shesh-desktop": None,  # dotfiles fork, not an MCP server
    "shesh-voice": None,  # Newelle fork, not an MCP server
    "shesh-audit": "shesh-audit-mcp",
    "shesh-system": "shesh-system-mcp",
    "shesh-shell": "shesh-shell-mcp",
    "shesh-files": None,  # folded into shesh-core; classifier library, no MCP console script
    "shesh-skills": "shesh-skills-mcp",
    "shesh-memory": "shesh-memory-mcp",
    "shesh-mind": "shesh-mind-mcp",
    "shesh-harness": "shesh-harness-mcp",
    "shesh-orchestrator": "shesh-orchestrator-mcp",
    "shesh-backup": "shesh-backup-mcp",
    "shesh-acp": None,  # ACP is not an MCP server
}


@dataclass
class Component:
    name: str
    repo: str
    channel: str
    provides: list[str] = field(default_factory=list)
    enabled: bool = True


def load_components(manifest: Path) -> list[Component]:
    with manifest.open("rb") as f:
        data = tomllib.load(f)
    out: list[Component] = []
    for name, spec in data.get("component", {}).items():
        out.append(Component(
            name=name,
            repo=spec.get("repo", ""),
            channel=spec.get("channel", "devel"),
            provides=list(spec.get("provides", [])),
        ))
    return out


def select(components: list[Component], channel: str) -> list[Component]:
    rank = {"stable": 0, "canary": 1, "devel": 2}
    max_rank = rank.get(channel, 2)
    return [c for c in components
            if c.enabled and rank.get(c.channel, 2) <= max_rank]


def canonical_servers(chosen: list[Component]) -> dict:
    servers = {}
    for c in chosen:
        cmd = SERVER_COMMANDS.get(c.name, f"{c.name}-mcp")
        if cmd is None:
            continue
        servers[c.name] = {"command": cmd, "args": []}
    return {"mcpServers": servers}


def zed_config(canonical: dict) -> dict:
    return {
        "context_servers": {
            name: {"command": spec["command"], "args": spec["args"]}
            for name, spec in canonical["mcpServers"].items()
        }
    }


def newelle_config(canonical: dict) -> dict:
    # Newelle stores mcp-servers as a JSON-encoded string of {name: command}
    servers = {name: spec["command"] for name, spec in canonical["mcpServers"].items()}
    return {"mcp-servers": json.dumps(servers)}


def write(path: Path, data: dict, *, dry_run: bool) -> None:
    text = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if dry_run:
        print(f"# {path}\n{text}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        print(f"wrote {path}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve()
    ap.add_argument("--manifest", type=Path,
                    default=here.parents[1] / "manifests" / "components.toml")
    ap.add_argument("--channel", choices=["stable", "canary", "devel"],
                    default="canary")
    ap.add_argument("--servers", type=str, default="",
                    help="comma-separated component names to enable (default: all on the channel)")
    ap.add_argument("--out", type=Path, default=DEFAULT_CONFIG_DIR)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    components = load_components(args.manifest)
    chosen = select(components, args.channel)
    if args.servers:
        allow = {s.strip() for s in args.servers.split(",") if s.strip()}
        chosen = [c for c in chosen if c.name in allow]
        dropped = sorted({c.name for c in select(components, args.channel)} - allow)
        if dropped:
            print(f"# disabled by --servers: {', '.join(dropped)}")
    canonical = canonical_servers(chosen)

    write(args.out / "servers.json", canonical, dry_run=args.dry_run)
    write(args.out / "zed.json", zed_config(canonical), dry_run=args.dry_run)
    write(args.out / "newelle.json", newelle_config(canonical), dry_run=args.dry_run)

    print(f"# {len(canonical['mcpServers'])} MCP servers enabled on '{args.channel}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
