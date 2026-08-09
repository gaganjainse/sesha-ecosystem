#!/usr/bin/env python3
"""Track upstream repos for our forks.

Reads manifests/components.toml and, for every component with an ``upstream``
table, fetches the latest release/tag and open issue count from the GitHub API
(no auth required for public repos within rate limits). Produces a JSON report
under ``channels/upstream-status.json`` and prints a human-readable summary.

This powers the weekly "upstream advanced" bot: if upstream moved past our pin,
we open a rebase PR on the fork, run its tests, and promote only if green.

Usage:
    python scripts/upstream_tracker.py [--manifest manifests/components.toml]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

GITHUB = "https://api.github.com/repos/{repo}"
UA = "sesha-ecosystem-tracker/0.1"


def gh_get(repo: str) -> dict:
    """GET a GitHub repo's JSON, returning {} on failure (offline/rate-limit)."""
    url = GITHUB.format(repo=repo)
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/vnd.github+json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        return {"_error": str(e)}


def latest_release(repo: str) -> dict:
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read())
            return {"tag": d.get("tag_name"), "published": d.get("published_at")}
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        return {"_error": str(e)}


def track(manifest: Path) -> dict:
    with manifest.open("rb") as f:
        data = tomllib.load(f)

    report = {"generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "components": {}}
    for name, c in data.get("component", {}).items():
        up = c.get("upstream")
        if not up:
            continue
        repo = up["repo"]
        # Normalize GitHub shorthand.
        if repo.startswith("http"):
            repo = "/".join(repo.rstrip("/").split("/")[-2:])
        info = gh_get(repo)
        rel = latest_release(repo)
        report["components"][name] = {
            "upstream_repo": repo,
            "pinned_ref": up.get("ref"),
            "upstream_default_branch": info.get("default_branch"),
            "upstream_stars": info.get("stargazers_count"),
            "upstream_open_issues": info.get("open_issues_count"),
            "latest_release": rel.get("tag"),
            "latest_release_published": rel.get("published"),
            "archived": info.get("archived"),
            "error": info.get("_error") or rel.get("_error"),
        }
        # be polite to the API
        time.sleep(0.5)
    return report


def summarize(report: dict) -> None:
    print(f"Upstream status — {report['generated']}")
    for name, c in report["components"].items():
        if c.get("error"):
            print(f"  ⚠ {name}: {c['upstream_repo']} -> {c['error']}")
            continue
        moved = ""
        if c["pinned_ref"] and c["latest_release"] and c["pinned_ref"] != c["latest_release"]:
            moved = f"  ⬆ pinned {c['pinned_ref']} -> {c['latest_release']}"
        print(f"  • {name:18} {c['upstream_repo']:32} "
              f"⭐{c['upstream_stars']} issues={c['upstream_open_issues']}{moved}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", default="manifests/components.toml", type=Path)
    ap.add_argument("--out", default="channels/upstream-status.json", type=Path)
    args = ap.parse_args()

    report = track(args.manifest)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    summarize(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
