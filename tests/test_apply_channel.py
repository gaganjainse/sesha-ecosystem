"""Tests for the channel applier (btrfs snapshot logic is mocked)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import apply_channel as ac  # noqa: E402


def test_on_btrfs_detects_filesystem(monkeypatch):
    import shutil

    monkeypatch.setattr(shutil, "which", lambda x: "/usr/bin/btrfs")
    monkeypatch.setattr(
        ac,
        "_run",
        lambda cmd, check=True: type(
            "R", (), {"returncode": 0, "stdout": "btrfs\n", "stderr": ""}
        )(),
    )
    assert ac.on_btrfs(Path("/")) is True


def test_on_btrfs_false_without_command(monkeypatch):
    monkeypatch.setattr(__import__("shutil"), "which", lambda x: None)
    assert ac.on_btrfs(Path("/")) is False


def test_apply_refuses_on_non_btrfs(tmp_path, monkeypatch):
    monkeypatch.setattr(ac, "on_btrfs", lambda p: False)
    monkeypatch.setattr(ac, "resolve_lock", lambda c: tmp_path / f"{c}.lock")
    (tmp_path / "stable.lock").write_text('{"components": {}}')
    rc = ac.apply("stable", take_snapshot=True)
    assert rc == 2


def test_apply_writes_state(tmp_path, monkeypatch):
    monkeypatch.setattr(ac, "on_btrfs", lambda p: False)
    monkeypatch.setattr(ac, "resolve_lock", lambda c: tmp_path / f"{c}.lock")
    (tmp_path / "canary.lock").write_text(
        '{"components": {"shesh-audit": {"repo": "gaganjainse/shesh-audit", "version": "0.1.0"}}}'
    )
    # No snapshot on non-btrfs -> skip via --no-snapshot path
    rc = ac.apply("canary", take_snapshot=False)
    assert rc == 0


def test_resolve_lock_builds_when_missing(tmp_path, monkeypatch):
    import contextlib

    called = {}

    def fake_run(cmd, check=True):
        called.update(cmd=cmd)
        return type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr(ac, "ROOT", tmp_path)
    monkeypatch.setattr(ac, "_run", fake_run)
    (tmp_path / "channels").mkdir()
    (tmp_path / "manifests" / "components.toml").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "manifests" / "components.toml").write_text("[component]\n")
    # resolve_lock should call resolve_manifest.py
    with contextlib.suppress(Exception):
        ac.resolve_lock("devel")
    assert "resolve_manifest.py" in " ".join(called.get("cmd", []))
