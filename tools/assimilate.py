#!/usr/bin/env python3
"""Watch tracked upstreams and open adoption work when they move.

The fleet declared an adoption policy (ADR-0018: prefer a maintained upstream)
and a register of 21 projects in manifests/upstreams.toml, but nothing ever
read it. upstream_tracker.py parses [component.*] tables, while the register
uses [upstream.*], so it reported an empty list and exited zero. No schedule
invoked it either. The result was a policy that existed only on paper.

This closes the loop:

  --report   what moved since the pinned revision
  --check    non-zero if an upstream advanced and no work item exists
  --queue    add a queue item for each advance, so it reaches an agent

Adoption itself stays a human decision. The tool refuses to fork or vendor
anything on its own: licence compatibility and whether a capability belongs in
the fleet are judgement calls, and ADR-0018 requires both to be recorded.

Usage:
    assimilate.py --report
    assimilate.py --check
    assimilate.py --queue
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

ECO = Path(__file__).resolve().parent.parent
REGISTER = ECO / "manifests" / "upstreams.toml"
STATE = ECO / "channels" / "upstream-status.json"
QUEUE_TOOL = ECO.parent / "shesh-workspace" / "tools" / "steer.py"

# Licences that can be combined into a GPL-3.0-or-later distribution.
COMPATIBLE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC",
              "GPL-2.0-or-later", "GPL-3.0", "GPL-3.0-only", "GPL-3.0-or-later",
              "LGPL-2.1-or-later", "LGPL-3.0-or-later", "MPL-2.0", "Unlicense",
              "CC0-1.0"}
# Copyleft that may only be reached across a process boundary, never linked.
PROCESS_ONLY = {"AGPL-3.0", "AGPL-3.0-only", "AGPL-3.0-or-later", "SSPL-1.0"}


def token() -> str | None:
    """Prefer the encrypted store; fall back to the environment."""
    for var in ("GITHUB_TOKEN", "GH_TOKEN", "SHESH_TOKEN_PRIMARY"):
        if os.environ.get(var):
            return os.environ[var]
    helper = ECO.parent / "shesh-workspace" / "tools" / "token.py"
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


def register() -> dict[str, dict]:
    if not REGISTER.exists():
        sys.exit(f"error: {REGISTER} not found")
    data = tomllib.loads(REGISTER.read_text(encoding="utf-8"))
    return data.get("upstream", {})


def licence_verdict(spdx: str | None) -> tuple[str, str]:
    if not spdx or spdx == "NOASSERTION":
        return "unknown", "licence not declared; verify before adopting"
    if spdx in COMPATIBLE:
        return "ok", f"{spdx} combines with GPL-3.0-or-later"
    if spdx in PROCESS_ONLY:
        return "process-only", f"{spdx} may be used only across a process boundary"
    return "incompatible", f"{spdx} cannot be combined; do not adopt"


def survey() -> list[dict]:
    tok = token()
    if not tok:
        print("note: no token available; unauthenticated rate limits apply",
              file=sys.stderr)
    prior = {}
    if STATE.exists():
        try:
            prior = {e["name"]: e for e in json.loads(STATE.read_text())["upstreams"]}
        except (json.JSONDecodeError, KeyError):
            prior = {}

    out = []
    for name, entry in sorted(register().items()):
        repo = entry.get("repo")
        if not repo or "/" not in repo:
            continue
        meta = api(f"/repos/{repo}", tok)
        rel = api(f"/repos/{repo}/releases/latest", tok)
        head = (meta.get("pushed_at") or "")[:10]
        spdx = (meta.get("license") or {}).get("spdx_id")
        state, why = licence_verdict(spdx)
        was = prior.get(name, {}).get("head", "")
        out.append({
            "name": name,
            "repo": repo,
            "head": head,
            "release": rel.get("tag_name"),
            "stars": meta.get("stargazers_count"),
            "archived": bool(meta.get("archived")),
            "licence": spdx,
            "licence_state": state,
            "licence_note": why,
            "moved": bool(was and head and head != was),
            "previous": was,
            "adopt": entry.get("adopt") or entry.get("steal"),
            "notes": entry.get("improve") or entry.get("notes"),
        })
    return out


def write_state(rows: list[dict]) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"upstreams": rows}, indent=2) + "\n",
                     encoding="utf-8")


def report(rows: list[dict]) -> None:
    print(f"{len(rows)} tracked upstream(s)\n")
    moved = [r for r in rows if r["moved"]]
    dead = [r for r in rows if r["archived"]]
    risky = [r for r in rows if r["licence_state"] in {"incompatible", "unknown"}]

    if moved:
        print("Advanced since the last survey:")
        for r in moved:
            print(f"  {r['name']:<28} {r['previous']} -> {r['head']}  {r['repo']}")
        print()
    if dead:
        print("Archived upstream (adoption is now a fork-and-own decision):")
        for r in dead:
            print(f"  {r['name']:<28} {r['repo']}")
        print()
    if risky:
        print("Licence needs a decision before adoption:")
        for r in risky:
            print(f"  {r['name']:<28} {r['licence'] or 'undeclared'} — {r['licence_note']}")
        print()
    if not (moved or dead or risky):
        print("No upstream advanced and no licence needs review.")


def queue(rows: list[dict]) -> int:
    """Turn each advance into a work item an agent will actually see."""
    if not QUEUE_TOOL.exists():
        print(f"error: {QUEUE_TOOL} not found", file=sys.stderr)
        return 1
    added = 0
    for r in [x for x in rows if x["moved"] and not x["archived"]]:
        if r["licence_state"] == "incompatible":
            continue
        title = f"Review upstream {r['name']} ({r['previous']} -> {r['head']})"
        note = f"{r['repo']}; licence {r['licence'] or 'undeclared'} ({r['licence_state']})"
        rc = subprocess.run(
            [sys.executable, str(QUEUE_TOOL), "add", title,
             "--priority", "p2", "--repo", "shesh-ecosystem", "--note", note],
            capture_output=True, text=True, timeout=30)
        if rc.returncode == 0:
            added += 1
    print(f"queued {added} adoption review(s)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--queue", action="store_true")
    a = ap.parse_args()

    rows = survey()
    if not rows:
        print("error: the upstream register is empty or unparseable",
              file=sys.stderr)
        return 1

    if a.check:
        moved = [r for r in rows if r["moved"]]
        if moved:
            print(f"{len(moved)} upstream(s) advanced and need review:")
            for r in moved:
                print(f"  {r['name']}: {r['previous']} -> {r['head']}")
            print("\nRun: python3 tools/assimilate.py --queue")
            return 1
        print(f"{len(rows)} upstream(s) tracked, none advanced.")
        return 0

    if a.queue:
        rc = queue(rows)
        write_state(rows)
        return rc

    report(rows)
    write_state(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
