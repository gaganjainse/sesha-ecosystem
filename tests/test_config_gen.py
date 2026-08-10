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
name = "shesha"
schema_version = 1

[component.shesha-audit]
repo = "gaganjainse/shesha-audit"
license = "GPL-3.0"
channel = "canary"
provides = ["audit"]

[component.shesha-system]
repo = "gaganjainse/shesha-system"
license = "GPL-3.0"
channel = "canary"
provides = ["power"]

[component.shesha-acp]
repo = "gaganjainse/shesha-acp"
license = "GPL-3.0"
channel = "canary"
provides = ["acp"]

[component.shesha-experimental]
repo = "gaganjainse/shesha-experimental"
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
    assert {"shesha-audit", "shesha-system", "shesha-acp"} <= names


def test_select_respects_channel(manifest):
    comps = load_components(manifest)
    canary = select(comps, "canary")
    assert "shesha-experimental" not in {c.name for c in canary}
    devel = select(comps, "devel")
    assert "shesha-experimental" in {c.name for c in devel}


def test_canonical_skips_acp_and_maps_commands(manifest):
    comps = select(load_components(manifest), "canary")
    servers = canonical_servers(comps)["mcpServers"]
    assert "shesha-audit" in servers
    assert servers["shesha-audit"]["command"] == "shesha-audit-mcp"
    # ACP is not an MCP server -> excluded
    assert "shesha-acp" not in servers


def test_zed_config_shape(manifest):
    comps = select(load_components(manifest), "canary")
    z = zed_config(canonical_servers(comps))
    assert "context_servers" in z
    assert "shesha-system" in z["context_servers"]
    assert z["context_servers"]["shesha-system"]["command"] == "shesha-system-mcp"


def test_newelle_config_encodes_json_string(manifest):
    comps = select(load_components(manifest), "canary")
    n = newelle_config(canonical_servers(comps))
    import json
    decoded = json.loads(n["mcp-servers"])
    assert "shesha-audit" in decoded
    assert decoded["shesha-audit"] == "shesha-audit-mcp"
