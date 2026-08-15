#!/usr/bin/env python3
"""Push shared boilerplate to every repository from one source of truth.

The 2026-08-15 audit found the same file diverging across repositories: two
different setup-python pins, five copies of one ruff comment, inconsistent
gitignores, missing agent files. Anything copied by hand drifts. This copies it
by rule instead.

Usage:
    python3 tools/sync_fleet.py            # apply
    python3 tools/sync_fleet.py --check    # exit non-zero if anything drifted
"""
from __future__ import annotations

import argparse
import difflib
import os
import sys

FLEET_DEFAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PRODUCT = [
    "shesh-core", "shesh-memory", "shesh-orchestrator", "shesh-harness",
    "shesh-phone", "shesh-omniroute", "shesh-skills", "shesh-voice",
    "shesh-desktop", "shesh-aos",
]
# Superseded under ADR-0019. They ship nothing, but their workflows still run,
# so they must carry the same action pins as everything else.
TOMBSTONES = [
    "shesh-acp", "shesh-audit", "shesh-backup", "shesh-brain", "shesh-calendar",
    "shesh-containers", "shesh-ebpf", "shesh-files", "shesh-mcp-bundle",
    "shesh-media", "shesh-messaging", "shesh-mind", "shesh-secrets",
    "shesh-shell", "shesh-system", "shesh-wave", "shesh-kernel",
]

ALL_REPOS = PRODUCT + ["shesh-ecosystem", "shesh-workspace", "shesh-docs",
                       "shesh-docs-archive"] + TOMBSTONES

# One pin, fleet-wide, and every pin is a full commit SHA.
#
# A tag is mutable: whoever controls the upstream repository can repoint it at
# different code, so `@v4` is a supply-chain hole. The zizmor unpinned-uses
# audit enforces this and will fail the build on a tag. An earlier revision of
# this file rewrote 86 SHA pins down to `@v4` and broke every workflow that
# runs the audit; do not reintroduce a tag here.
#
# To move a pin: resolve the tag to its SHA and record which release it is.
#   gh api repos/<owner>/<repo>/git/ref/tags/<tag> --jq .object.sha
ACTION_PINS = {
    # v4, resolved 2026-08-15
    "actions/checkout": "actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
    # v7.0.0
    "actions/setup-python": "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
}

# A pin must be a 40-character hex SHA, never a tag or branch.
PIN_RE = __import__("re").compile(r"@[0-9a-f]{40}$")

SECURITY_MD = """# Security Policy

The canonical security posture for the Shesh fleet — vulnerability reporting,
supported versions, threat model, and recovery runbooks — is maintained in the
[ecosystem security policy](https://github.com/gaganjainse/shesh-ecosystem/blob/main/SECURITY.md).

Report vulnerabilities through the process documented there. This repository
follows the fleet-wide policy and carries no local exceptions.
"""

CONTRIBUTING_MD = """# Contributing

Fleet-wide conventions, the build gate, and judgment boundaries are defined once
in [AGENTS.md](https://github.com/gaganjainse/shesh-ecosystem/blob/main/AGENTS.md).
Read that first.

## Before you start

```bash
make check          # or: pytest -q && ruff check .
```

A red gate on arrival is not yours to build on. Fix it or report it.

## Making a change

1. Branch as `feat/<slug>` or `fix/<slug>`. Never work on `main`.
2. Read the files you intend to change.
3. Keep the change small; one logical change per commit.
4. Add a test with a fix.
5. Run the gate before committing.
6. Use a Conventional Commit message: `feat:`, `fix:`, `docs:`, `refactor:`,
   `chore(ci):`.

## What blocks a merge

- A failing gate.
- A credential in the diff.
- A new dependency without justification and a licence check.
- A documented claim that the code does not support.
- A test weakened to make a change pass.

## Where things live

Product code ships to users and passes the release gate. Build tooling lives in
`shesh-workspace` and does not. Documentation lives in `shesh-docs`; this
repository's README stays canonical for how to build and run it.

See [HANDOFF.md](https://github.com/gaganjainse/shesh-ecosystem/blob/main/HANDOFF.md)
for the full work loop.
"""

CHANGELOG_MD = """# Changelog

Notable changes to this component. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Metadata, lint configuration, and ignore rules standardised across the fleet.

## [0.1.0]

Initial release.
"""

AGENTS_STUB = """# AGENTS.md

Fleet-wide conventions, judgment boundaries, and the build gate are defined once
in the ecosystem repository:

**https://github.com/gaganjainse/shesh-ecosystem/blob/main/AGENTS.md**

Read that first, then
[HANDOFF.md](https://github.com/gaganjainse/shesh-ecosystem/blob/main/HANDOFF.md)
for where to continue work.

This file records only what differs in `{repo}`.

## This repository

`{role}`

See [README.md](README.md) for what this component does, how to build it, and
how to run its tests.

## Local notes

- Run this repository's own suite before committing. The ecosystem gate covers
  integration, not these units.
- The README is canonical here. Do not copy its content into `shesh-docs`;
  link to it.
"""

ROLES = {
    "shesh-core": "Product. Consolidated Brain and Soma tool servers.",
    "shesh-memory": "Product. Hierarchical memory and habit learning.",
    "shesh-orchestrator": "Product. Multi-agent runtime and session management.",
    "shesh-harness": "Product. Continual refinement of supplemental agent state.",
    "shesh-phone": "Product. Android device control over ADB.",
    "shesh-omniroute": "Product. Optional network model gateway, off by default.",
    "shesh-skills": "Product. Agent Skills library and everyday tool server.",
    "shesh-voice": "Product. Speech input and output.",
    "shesh-desktop": "Product. Desktop shell and device profile.",
    "SheshAOS": "Product. The Rust governance kernel.",
    "shesh-ecosystem": "Composition. Manifest, lockfiles, and release gates.",
    "shesh-workspace": "Factory. Build tooling. Never installed by a user.",
    "shesh-docs": "Documentation. Published, not installed.",
    "shesh-docs-archive": "Record. Superseded material, not maintained.",
}


def sync_file(path: str, content: str, check: bool, drift: list) -> bool:
    existing = None
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            existing = fh.read()
    if existing == content:
        return False
    if check:
        drift.append(path)
        if existing is not None:
            d = list(difflib.unified_diff(
                existing.splitlines(), content.splitlines(),
                fromfile=path, tofile="canonical", lineterm="", n=1))
            for line in d[:8]:
                print(f"    {line}")
        return True
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return True


def pin_actions(fleet: str, check: bool, drift: list) -> int:
    """One action pin fleet-wide, and every pin is a SHA."""
    bad = [a for a, pin in ACTION_PINS.items() if not PIN_RE.search(pin)]
    if bad:
        msg = (f"refusing to sync: {', '.join(bad)} pinned to a tag, not a "
               f"40-character SHA; a tag is mutable and fails unpinned-uses")
        raise SystemExit(msg)
    n = 0
    for repo in ALL_REPOS:
        wf = os.path.join(fleet, repo, ".github", "workflows")
        if not os.path.isdir(wf):
            continue
        for f in sorted(os.listdir(wf)):
            if not f.endswith((".yml", ".yaml")):
                continue
            p = os.path.join(wf, f)
            with open(p, encoding="utf-8") as fh:
                s = orig = fh.read()
            for action, pin in ACTION_PINS.items():
                s = _repin(s, action, pin)
            if s != orig:
                n += 1
                if check:
                    drift.append(p)
                else:
                    with open(p, "w", encoding="utf-8") as fh:
                        fh.write(s)
    return n


def _repin(text: str, action: str, pin: str) -> str:
    import re
    return re.sub(rf"uses:\s*{re.escape(action)}@[^\s#]+", f"uses: {pin}", text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fleet", default=FLEET_DEFAULT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    drift: list[str] = []
    wrote = 0

    for repo in ALL_REPOS:
        root = os.path.join(args.fleet, repo)
        if not os.path.isdir(root):
            continue

        if sync_file(os.path.join(root, "SECURITY.md"), SECURITY_MD, args.check, drift):
            wrote += 1
        if sync_file(os.path.join(root, "CONTRIBUTING.md"), CONTRIBUTING_MD, args.check, drift):
            wrote += 1

        # MIS-1: a changelog everywhere, created once and then owned locally.
        cl = os.path.join(root, "CHANGELOG.md")
        if not os.path.exists(cl) and sync_file(cl, CHANGELOG_MD, args.check, drift):
            wrote += 1

        # Agent files: the canonical one is hand-written; the rest are stubs.
        if repo != "shesh-ecosystem":
            stub = AGENTS_STUB.format(repo=repo, role=ROLES.get(repo, "Component."))
            if sync_file(os.path.join(root, "AGENTS.md"), stub, args.check, drift):
                wrote += 1

    pinned = pin_actions(args.fleet, args.check, drift)

    if args.check:
        if drift:
            print(f"\n{len(drift)} file(s) drifted from the canonical source:")
            for p in drift:
                print(f"  {os.path.relpath(p, args.fleet)}")
            print("\nRun: python3 tools/sync_fleet.py")
            return 1
        print("Fleet boilerplate is in sync.")
        return 0

    print(f"synced {wrote} file(s); re-pinned actions in {pinned} workflow(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
