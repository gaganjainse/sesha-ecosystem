#!/usr/bin/env python3
"""Shesh-ecosystem proofread gate — canon scan (fleet) + optional grammar.

The résumé-specific version lives in the portfolio repo
(scripts/check-resume-consistency.mjs + check-resume-grammar.mjs). This is the
FLEET version: it scans one repo or every public gaganjainse repo for the same
class of drift — retired names (NexusAOS / Nexus bridge / nexus-kernel / SeshaOS)
that must never appear in living docs — and can optionally grammar-check prose
via the LanguageTool public API.

Modes:
  --repo NAME      scan one repo (README + description + docs/) via GitHub API
  --path DIR       scan a local checkout (default: this repo's own root)
  --fleet          scan all public gaganjainse repos (README + description)
  --grammar        also run LanguageTool on prose (advisory unless --strict)
  --strict         grammar findings block too (canon findings always block)
  --max N          fleet cap (default 120)

Immutable records (ADRs, QUERYLOG, audits, changelogs, attic/incident/archive
notes) are skipped on purpose — the Nexus→Shesh rename canon applies to living
docs only; history stays history.

Exit 0 clean · 1 violations · 2 setup/network error. No silent pass.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"
USER = "gaganjainse"

# Retired names that must not appear in living docs.
# "nexus*" and "sesha*" variants are retired everywhere, matched
# case-insensitively. (The SheshAOS docs slug was renamed seshaos -> sheshaos on
# 2026-08-13, so no lowercase "seshaos" is legitimate anymore.)
FORBIDDEN_CI = [
    r"\bnexusaos\b",
    r"\bnexus-aos\b",
    r"\bnexus_kernel\b",
    r"\bnexus-kernel\b",
    r"\bnexus kernel\b",
    r"\bnexus bridge\b",
    r"\bseshaos\b",
    r"\bsesha\b",
    r"\bsesha os\b",
]
FORBIDDEN_CS = [
    r"\bSeshaOS\b",
    r"\bSesha OS\b",
]
FORBIDDEN_RE_CI = re.compile("|".join(FORBIDDEN_CI), re.IGNORECASE)
FORBIDDEN_RE_CS = re.compile("|".join(FORBIDDEN_CS))

# Living docs only — skip immutable/historical records.
SKIP_PARTS = (
    "adr", "querylog", "audit", "changelog", "attic", "incident",
    "archive", "handoff", "next_session", "history", "todo",
)
README_NAMES = ("README.md", "README", "README.rst", "readme.md")

LT_URL = "https://api.languagetool.org/v2/check"


def api(path: str, token: str | None) -> object:
    req = urllib.request.Request(
        API + path,
        headers={"User-Agent": "shesh-proofread", "Accept": "application/vnd.github+json"},
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_raw(name: str, branch: str, path: str) -> str | None:
    url = f"{RAW}/{USER}/{name}/{branch}/{path}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:  # noqa: BLE001 — network fetch must not abort a fleet scan; absence is reported
        return None


# A forbidden term inside a code span is often the true name of something that
# still exists — a crate directory, a binary, a package. Renaming the prose
# without renaming the artefact would make the document wrong, so a backticked
# occurrence is reported only when nothing of that name is on disk.
CODE_SPAN = re.compile(r"`[^`\n]*`")


def _code_spans(text: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in CODE_SPAN.finditer(text)]


def scan_text(text: str, source: str, violations: list[str],
              known_names: set[str] | None = None) -> None:
    spans = _code_spans(text)
    for m in list(FORBIDDEN_RE_CI.finditer(text)) + list(FORBIDDEN_RE_CS.finditer(text)):
        if known_names and any(a <= m.start() and m.end() <= b for a, b in spans):
            span = next(text[a + 1:b - 1] for a, b in spans
                        if a <= m.start() and m.end() <= b)
            if span.strip().strip("-/") in known_names:
                continue
        ctx = text[max(0, m.start() - 25): m.end() + 25].replace("\n", " ")
        violations.append(f"{source}: forbidden term {m.group(0)!r} → \"…{ctx}…\"")


def is_skippable(path: str) -> bool:
    low = path.lower()
    return any(p in low for p in SKIP_PARTS)


def scan_repo(name: str, token: str | None, deep: bool) -> list[str]:
    """Scan one repo's description + README (+ docs/ when deep)."""
    violations: list[str] = []
    meta = api(f"/repos/{USER}/{name}", token)
    branch = meta.get("default_branch", "main")
    desc = meta.get("description") or ""
    if desc:
        scan_text(desc, f"{name} (description)", violations)
    tree_paths: list[str] = []
    tree_meta = api(f"/repos/{USER}/{name}/git/trees/{branch}?recursive=1", token)
    if isinstance(tree_meta, dict):
        tree_paths = [i.get("path", "") for i in tree_meta.get("tree", [])]
    known = {
        p.split("/")[1] for p in tree_paths
        if p.count("/") >= 1 and p.split("/")[0] in ("crates", "bin", "src", "packages")
    }
    for rn in README_NAMES:
        text = fetch_raw(name, branch, rn)
        if text:
            scan_text(text, f"{name}/{rn}", violations, known)
            break
    if deep:
        for p in tree_paths:
            if p.endswith(".md") and not is_skippable(p):
                t = fetch_raw(name, branch, p)
                if t:
                    scan_text(t, f"{name}/{p}", violations, known)
    return violations


def on_disk_names(root: Path) -> set[str]:
    """Directory and binary names present in a checkout.

    A forbidden term is allowed inside a code span when it names one of these,
    because the document is then stating a fact about the tree. Renaming such a
    reference without renaming the directory makes the document wrong.
    """
    names: set[str] = set()
    for sub in ("crates", "bin", "src", "packages"):
        d = root / sub
        if d.is_dir():
            names |= {c.name for c in d.iterdir() if c.is_dir()}
    return names


def scan_path(root: Path) -> list[str]:
    violations: list[str] = []
    known = on_disk_names(root)
    for p in root.rglob("*.md"):
        rel = str(p.relative_to(root))
        if is_skippable(rel):
            continue
        scan_text(p.read_text(encoding="utf-8", errors="replace"), rel, violations,
                  known)
    return violations


def grammar_check(text: str, label: str) -> list[str]:
    body = urllib.parse.urlencode({"text": text[:15000], "language": "en-US"}).encode()
    req = urllib.request.Request(LT_URL, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    notes = []
    for m in data.get("matches", []):
        cat = (m.get("rule") or {}).get("category", {}).get("id", "UNKNOWN")
        notes.append(f"[{cat}] {label}: {m.get('message')}")
    return notes


def main() -> int:
    ap = argparse.ArgumentParser(description="Shesh ecosystem proofread gate")
    ap.add_argument("--repo", help="scan one repo by name")
    ap.add_argument("--path", help="scan a local checkout path")
    ap.add_argument("--fleet", action="store_true", help="scan all public gaganjainse repos")
    ap.add_argument("--grammar", action="store_true", help="also run LanguageTool on prose")
    ap.add_argument("--strict", action="store_true", help="grammar findings are blocking")
    ap.add_argument("--max", type=int, default=120, help="fleet repo cap")
    args = ap.parse_args()

    import os
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT")

    if not (args.repo or args.path or args.fleet):
        args.path = str(Path(__file__).resolve().parent.parent)

    violations: list[str] = []
    grammar_notes: list[str] = []

    if args.path:
        root = Path(args.path)
        violations = scan_path(root)
        print(f"scanned local path {root}")
    elif args.fleet:
        repos = api(f"/users/{USER}/repos?per_page=100&type=public", token)
        names = [r["name"] for r in repos if not r.get("archived") and not r.get("fork")]
        names = names[: args.max]
        print(f"fleet scan: {len(names)} repos")
        for name in names:
            try:
                v = scan_repo(name, token, deep=False)
                if v:
                    violations.extend(v)
                    print(f"  {name}: {len(v)} violation(s)")
            except Exception as e:  # noqa: BLE001 — per-repo scan error is appended + surfaced
                violations.append(f"{name}: scan error {type(e).__name__}: {e}")
        if args.grammar:
            for name in names:
                for rn in README_NAMES:
                    branch = api(f"/repos/{USER}/{name}", token).get("default_branch", "main")
                    text = fetch_raw(name, branch, rn)
                    if text:
                        grammar_notes.extend(grammar_check(text, name))
                        break
    elif args.repo:
        violations = scan_repo(args.repo, token, deep=True)
        print(f"scanned repo {args.repo} (deep)")
        if args.grammar:
            branch = api(f"/repos/{USER}/{args.repo}", token).get("default_branch", "main")
            for rn in README_NAMES:
                text = fetch_raw(args.repo, branch, rn)
                if text:
                    grammar_notes.extend(grammar_check(text, args.repo))
                    break

    print()
    for v in violations:
        print("CANON", v)
    for g in grammar_notes:
        print("GRAMMAR", g)

    n_v = len(violations)
    n_g = len(grammar_notes)
    print(f"\n{len(names) if args.fleet else 1} repos · {n_v} canon violation(s) · {n_g} grammar note(s)")

    if n_v:
        print("CANON violations block the gate.")
        return 1
    if args.strict and n_g:
        print("--strict: grammar notes block the gate.")
        return 1
    print("Clean.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001 — top-level: report, never hide
        print(f"proofread error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
