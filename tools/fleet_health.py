#!/usr/bin/env python3
"""Report the CI status of every repository, and fail if main is red.

"No red reaches main" needs something that looks. This checks the default
branch of every repository in the fleet and exits non-zero if any is failing,
so the rule is enforced rather than hoped for.

Usage:
    fleet_health.py              # table of every repository
    fleet_health.py --check      # non-zero if any main is red
    fleet_health.py --json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ECO = Path(__file__).resolve().parent.parent
FLEET = ECO.parent
OWNER = "gaganjainse"


def token() -> str | None:
    for var in ("GITHUB_TOKEN", "GH_TOKEN", "SHESH_TOKEN_PRIMARY"):
        if os.environ.get(var):
            return os.environ[var]
    helper = FLEET / "shesh-workspace" / "tools" / "token.py"
    if helper.exists() and os.environ.get("SHESH_PAT_PASSWORD"):
        r = subprocess.run([sys.executable, str(helper), "get", "primary"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    return None


def api(path: str, tok: str | None) -> dict:
    cmd = ["curl", "-s", "--max-time", "25",
           "-H", "Accept: application/vnd.github+json"]
    if tok:
        cmd += ["-H", f"Authorization: Bearer {tok}"]
    cmd.append(f"https://api.github.com{path}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(r.stdout or "{}")
    except (subprocess.SubprocessError, OSError, json.JSONDecodeError):
        return {}


def repos() -> list[str]:
    """Every locally checked-out repository with a git remote."""
    out = []
    for p in sorted(FLEET.iterdir()):
        if (p / ".git").is_dir():
            out.append(p.name)
    return out


def survey() -> list[dict]:
    tok = token()
    rows = []
    for name in repos():
        meta = api(f"/repos/{OWNER}/{name}", tok)
        if meta.get("message") == "Not Found":
            rows.append({"repo": name, "state": "missing", "archived": None})
            continue
        branch = meta.get("default_branch", "main")
        runs = api(f"/repos/{OWNER}/{name}/actions/runs"
                   f"?branch={branch}&per_page=1", tok)
        wr = (runs.get("workflow_runs") or [{}])[0]
        rows.append({
            "repo": name,
            "branch": branch,
            "archived": bool(meta.get("archived")),
            "state": wr.get("conclusion") or wr.get("status") or "no runs",
            "workflow": wr.get("name"),
            "url": wr.get("html_url"),
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = survey()
    if a.json:
        print(json.dumps(rows, indent=2))
        return 0

    red = [r for r in rows if r["state"] in {"failure", "timed_out",
                                             "startup_failure"}]
    running = [r for r in rows if r["state"] in {"queued", "in_progress"}]

    if not a.check:
        for r in sorted(rows, key=lambda x: x["repo"]):
            flag = "archived" if r.get("archived") else ""
            print(f"  {r['state']:<15} {r['repo']:<20} {flag}")
        print(f"\n{len(rows)} repositories, {len(red)} red, {len(running)} running")

    if red:
        print("\nRed on the default branch:")
        for r in red:
            print(f"  {r['repo']}: {r['workflow']} — {r['url']}")
        print("\nNo red may sit on main. Fix or revert.")
        return 1

    if a.check:
        print(f"{len(rows)} repositories, none red"
              + (f", {len(running)} still running" if running else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
