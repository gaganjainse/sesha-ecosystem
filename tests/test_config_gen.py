"""Tests for the MCP config generator."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from generate_mcp_config import (  # noqa: E402
    canonical_servers, load_components, newelle_config, select, zed_config,
)


MANIFEST = """
[ecosystem]
name = "shesh"
schema_version = 1

[component.shesh-audit]
repo = "gaganjainse/shesh-audit"
license = "GPL-3.0"
channel = "canary"
provides = ["audit"]

[component.shesh-system]
repo = "gaganjainse/shesh-system"
license = "GPL-3.0"
channel = "canary"
provides = ["power"]

[component.shesh-acp]
repo = "gaganjainse/shesh-acp"
license = "GPL-3.0"
channel = "canary"
provides = ["acp"]

[component.shesh-experimental]
repo = "gaganjainse/shesh-experimental"
license = "GPL-3.0"
channel = "devel"
provides = ["experimental"]
"""


@pytest.fixture()
def manifest(tmp_path):
    p = tmp_path / "components.toml"
    p.write_text(MANIFEST)
    return p


def test_loads_components(manifest):
    comps = load_components(manifest)
    names = {c.name for c in comps}
    assert {"shesh-audit", "shesh-system", "shesh-acp"} <= names


def test_select_respects_channel(manifest):
    comps = load_components(manifest)
    canary = select(comps, "canary")
    assert "shesh-experimental" not in {c.name for c in canary}
    devel = select(comps, "devel")
    assert "shesh-experimental" in {c.name for c in devel}


def test_canonical_skips_acp_and_maps_commands(manifest):
    comps = select(load_components(manifest), "canary")
    servers = canonical_servers(comps)["mcpServers"]
    assert "shesh-audit" in servers
    assert servers["shesh-audit"]["command"] == "shesh-audit-mcp"
    # ACP is not an MCP server -> excluded
    assert "shesh-acp" not in servers


def test_zed_config_shape(manifest):
    comps = select(load_components(manifest), "canary")
    z = zed_config(canonical_servers(comps))
    assert "context_servers" in z
    assert "shesh-system" in z["context_servers"]
    assert z["context_servers"]["shesh-system"]["command"] == "shesh-system-mcp"


def test_newelle_config_encodes_json_string(manifest):
    comps = select(load_components(manifest), "canary")
    n = newelle_config(canonical_servers(comps))
    import json
    decoded = json.loads(n["mcp-servers"])
    assert "shesh-audit" in decoded
    assert decoded["shesh-audit"] == "shesh-audit-mcp"
