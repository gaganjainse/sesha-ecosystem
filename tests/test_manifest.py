"""Tests for the Shesha ecosystem manifest resolver and gates.

These run entirely offline with no hardware dependencies. They are the first
line of defense: a malformed manifest, incompatible license, or duplicate
capability must fail before anything is promoted.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
MANIFEST = ROOT / "manifests" / "components.toml"

sys.path.insert(0, str(SCRIPTS))

import resolve_manifest as rm


@pytest.fixture()
def manifest_data():
    return rm.load_manifest(MANIFEST)


def test_manifest_is_valid(manifest_data):
    errors = rm.validate(manifest_data["component"])
    assert errors == [], f"manifest validation failed: {errors}"


def test_ecosystem_metadata_present(manifest_data):
    eco = manifest_data["ecosystem"]
    assert eco["name"] == "sesha"
    assert eco["schema_version"] >= 1
    assert "body_doc" in eco


def test_every_component_has_body_layer(manifest_data):
    valid = {"brain", "mind", "soma"}
    for name, c in manifest_data["component"].items():
        assert c["layer"] in valid, f"{name} has bad layer {c['layer']}"


def test_no_duplicate_capabilities(manifest_data):
    errors = rm.validate(manifest_data["component"])
    dup = [e for e in errors if "already provided" in e]
    assert not dup, f"duplicate capabilities: {dup}"


def test_all_licenses_are_compatible(manifest_data):
    for name, c in manifest_data["component"].items():
        assert c["license"] in rm.COMPATIBLE_LICENSES, (
            f"{name} has incompatible license {c['license']!r}; use separate_service "
            f"for {sorted(rm.SERVICE_ONLY_LICENSES)}"
        )


def test_each_component_has_upstream_or_is_ours(manifest_data):
    for name, c in manifest_data["component"].items():
        repo = c["repo"]
        # Our own components may not need an upstream, but brain/mind lineage
        # components should declare their upstream for the audit trail.
        if c["layer"] in {"brain", "mind"}:
            assert "upstream" in c, f"{name}: brain/mind components need an upstream"
        assert repo.startswith("gaganjainse/") or "/" in repo


def test_resolve_writes_deterministic_lock(tmp_path, manifest_data):
    out = tmp_path / "shesha.lock"
    components = manifest_data["component"]
    lock1 = rm.resolve(components, "canary")
    out.write_text(json.dumps(lock1, indent=2, sort_keys=True))
    # Resolve twice -> identical bytes (determinism)
    lock2 = rm.resolve(components, "canary")
    assert lock1 == lock2
    data = json.loads(out.read_text())
    assert data["count"] >= 3
    assert "shesha-files" in data["components"]


def test_channel_filters_correctly(manifest_data):
    components = manifest_data["component"]
    stable = rm.resolve(components, "stable")
    canary = rm.resolve(components, "canary")
    devel = rm.resolve(components, "devel")
    assert stable["count"] <= canary["count"] <= devel["count"]
    # Stable should never include devel/canary components
    for c in stable["components"].values():
        assert c["channel"] == "stable"


def test_cli_resolver_runs(tmp_path):
    out = tmp_path / "out.lock"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "resolve_manifest.py"),
         "--manifest", str(MANIFEST), "--out", str(out), "--channel", "canary"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(out.read_text())
    assert data["count"] > 0
    assert "sha256" in data


def test_cli_rejects_incompatible_license(tmp_path):
    bad = tmp_path / "bad.toml"
    bad.write_text(
        '[ecosystem]\nname="x"\nschema_version=1\nstable_channel="stable"\n'
        '[component.evil]\nlayer="soma"\nrepo="x/y"\nversion="1"\n'
        'license="SSPL-1.0"\nchannel="canary"\nprovides=["bad"]\n'
    )
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "resolve_manifest.py"),
         "--manifest", str(bad), "--out", str(tmp_path / "o.lock")],
        capture_output=True, text=True,
    )
    assert r.returncode != 0
    assert "not GPL-3-compatible" in r.stderr


def test_three_body_layers_present(manifest_data):
    layers = {c["layer"] for c in manifest_data["component"].values()}
    # The whole point of the project: brain + mind + soma.
    assert {"brain", "mind", "soma"} <= layers
