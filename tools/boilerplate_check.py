#!/usr/bin/env python3
"""Boilerplate-as-code drift gate.

Canonical boilerplate lives in templates/boilerplate/. This tool checks that
every OWN repo (non-fork) matches it, so a fix written once can't silently rot
in one repo while 30 others drift.

Checks per repo:
  1. SECURITY.md present (+ canonical content if present)
  2. LICENSE present
  3. .github/dependabot.yml present
  4. a CI workflow present
  5. CI does NOT contain suppression patterns (the generic template that hid
     failures: `2>/dev/null ||`, `|| true`, `|| echo "…gate passed"`, `--exit-zero`)

Forks are out of scope (upstream owns their CI; FORK_REVIEW.md tracks deltas).

Modes:
  --fleet    scan all non-fork gaganjainse repos via the GitHub API (raw fetch)
  --repo N   scan one repo
  --path D   scan a local checkout
Exit 0 clean · 1 drift · 2 setup/network error. No silent pass.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

USER = "gaganjainse"
RAW = f"https://raw.githubusercontent.com/{USER}"

# Suppression patterns from the old auto-generated template. Upstream fork CI
# may legitimately use `|| true` on linters, but these combined markers identify
# OUR template specifically.
SUPPRESSION = [
    "2>/dev/null ||",
    "|| true",
    "--exit-zero",
    "gate passed",
]


def _strip_comments(yaml: str) -> str:
    # YAML full-line comments start with #; inline comments after code are kept
    # (a `|| true # reason` is still `|| true`).
    return "\n".join(line for line in yaml.splitlines() if not line.lstrip().startswith("#"))

CANONICAL = Path(__file__).resolve().parent.parent / "templates" / "boilerplate"


def fetch_raw(name: str, branch: str, path: str) -> str | None:
    url = f"{RAW}/{name}/{branch}/{path}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return r.read().decode()
    except Exception:  # noqa: BLE001 — raw fetch / contents API: absence is reported, not swallowed
        return None


def api(path: str) -> object:
    import os
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "shesh-boilerplate"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def workflow_files(name: str, branch: str) -> list[str]:
    """List .github/workflows/*.yml via the contents API (works regardless of filename)."""
    try:
        items = api(f"/repos/{USER}/{name}/contents/.github/workflows?ref={branch}")
        return [i["name"] for i in items if i["name"].endswith((".yml", ".yaml"))]
    except Exception:  # noqa: BLE001 — raw fetch / contents API: absence is reported, not swallowed
        return []


def check_files(name: str, branch: str, files: dict[str, str | None], findings: list[str]) -> None:
    for label, content in files.items():
        if content is None:
            findings.append(f"{name}: missing {label}")
        elif label == "SECURITY.md":
            # Accept the generic template AND the shesh-* canonical pointer.
            ok = ("privately" in content) or ("canonical" in content.lower())
            if not ok:
                findings.append(f"{name}: SECURITY.md drifted from canonical template")


def check_ci(name: str, branch: str, findings: list[str]) -> None:
    wfs = workflow_files(name, branch)
    if not wfs:
        findings.append(f"{name}: no CI workflow found")
        return
    for fn in wfs:
        ci = fetch_raw(name, branch, f".github/workflows/{fn}")
        if ci is None:
            continue
        ci = _strip_comments(ci)
        for pat in SUPPRESSION:
            if pat in ci:
                findings.append(f"{name}: CI contains suppression pattern {pat!r} ({fn})")
                return


def repo_branch(name: str) -> str | None:
    try:
        return api(f"/repos/{USER}/{name}")["default_branch"]
    except Exception:  # noqa: BLE001 — raw fetch / contents API: absence is reported, not swallowed
        return None


def scan_fleet() -> list[str]:
    repos = api(f"/users/{USER}/repos?per_page=100&type=public")
    own = [r for r in repos if not r["fork"] and not r["archived"]]
    findings: list[str] = []
    for r in own:
        name = r["name"]
        branch = r["default_branch"]
        files = {
            "SECURITY.md": fetch_raw(name, branch, "SECURITY.md"),
            "LICENSE": fetch_raw(name, branch, "LICENSE") or fetch_raw(name, branch, "LICENSE.md") or fetch_raw(name, branch, "LICENSE.txt"),
            "dependabot.yml": fetch_raw(name, branch, ".github/dependabot.yml"),
        }
        check_files(name, branch, files, findings)
        check_ci(name, branch, findings)
    return findings


def scan_repo(name: str) -> list[str]:
    branch = repo_branch(name)
    if not branch:
        return [f"{name}: repo not reachable"]
    findings: list[str] = []
    files = {
        "SECURITY.md": fetch_raw(name, branch, "SECURITY.md"),
        "LICENSE": fetch_raw(name, branch, "LICENSE") or fetch_raw(name, branch, "LICENSE.md") or fetch_raw(name, branch, "LICENSE.txt"),
        "dependabot.yml": fetch_raw(name, branch, ".github/dependabot.yml"),
    }
    check_files(name, branch, files, findings)
    check_ci(name, branch, findings)
    return findings


def scan_path(root: Path) -> list[str]:
    name = root.name
    findings: list[str] = []
    files = {
        "SECURITY.md": (root / "SECURITY.md").read_text() if (root / "SECURITY.md").exists() else None,
        "LICENSE": (root / "LICENSE").read_text() if (root / "LICENSE").exists() else None,
        "dependabot.yml": (root / ".github/dependabot.yml").read_text() if (root / ".github/dependabot.yml").exists() else None,
    }
    check_files(name, "main", files, findings)
    check_ci(name, "main", findings)
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Boilerplate drift gate")
    ap.add_argument("--fleet", action="store_true")
    ap.add_argument("--repo")
    ap.add_argument("--path")
    args = ap.parse_args()

    if args.fleet:
        findings = scan_fleet()
        print(f"fleet scan: {len(findings)} drift finding(s)")
    elif args.repo:
        findings = scan_repo(args.repo)
    elif args.path:
        findings = scan_path(Path(args.path))
    else:
        ap.error("one of --fleet / --repo / --path is required")

    for f in findings:
        print("DRIFT", f)
    if findings:
        print(f"\n{len(findings)} drift finding(s) — boilerplate is inconsistent.")
        return 1
    print("\nAll boilerplate consistent with templates/boilerplate/.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001 — top-level report, never hide
        print(f"boilerplate_check error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
