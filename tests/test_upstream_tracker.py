"""Offline tests for upstream_tracker (network calls mocked)."""
from __future__ import annotations

import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import upstream_tracker as ut  # noqa: E402


def test_gh_get_handles_failure(monkeypatch):
    def fake_urlopen(*_a, **_k):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    result = ut.gh_get("owner/repo")
    assert "_error" in result


def test_track_reads_manifest_components(monkeypatch, tmp_path):
    manifest = tmp_path / "c.toml"
    manifest.write_text(
        '[ecosystem]\nname="sesha"\nschema_version=1\nstable_channel="stable"\n'
        '[component.a]\nlayer="soma"\nrepo="gaganjainse/a"\nversion="1"\n'
        'license="MIT"\nchannel="canary"\nprovides=["x"]\n'
        'upstream={name="X", repo="owner/x", ref="v1"}\n'
        '[component.b]\nlayer="brain"\nrepo="gaganjainse/b"\nversion="1"\n'
        'license="MIT"\nchannel="canary"\nprovides=["y"]\n'
    )

    def fake_gh(_repo):
        return {"default_branch": "main", "stargazers_count": 10,
                "open_issues_count": 2, "archived": False}

    def fake_rel(_repo):
        return {"tag": "v2", "published": "2026-01-01"}

    monkeypatch.setattr(ut, "gh_get", fake_gh)
    monkeypatch.setattr(ut, "latest_release", fake_rel)
    monkeypatch.setattr(ut.time, "sleep", lambda *_: None)

    report = ut.track(manifest)
    assert "a" in report["components"]
    assert report["components"]["a"]["latest_release"] == "v2"
    # component without an upstream table is skipped
    assert "b" not in report["components"]
