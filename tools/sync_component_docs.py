#!/usr/bin/env python3
"""Sync every component README into docs/components/<name>.md.

Canonical source is each component repo's README.md; docs/components/ is a
pure projection. Run without args to copy, with --check to verify no drift
(the CI gate). Missing component checkouts are skipped with a note, mirroring
book_build's OPTIONAL-SKIPPED policy — but if a component IS checked out and
its README differs, --check fails loudly.

Usage:
  python tools/sync_component_docs.py [--check] [--src-root DIR]
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_SRC = ROOT / ".." / "components"  # siblings (canary layout)
FALLBACK_SRC = ROOT / ".." / "src"  # dev machine layout (/home/user/src)

# Markdown link: [text](url) with optional trailing #anchor. Same shape as
# book_build's LINK_RE so translation behaves identically.
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)#]+)(#[^)]+)?\)")


def translate_links(body: str, repo: str, readme: pathlib.Path) -> str:
    """Rewrite repo-relative links to absolute GitHub blob URLs.

    docs/components/*.md live in the ecosystem repo, so a relative link
    written for the component repo (e.g. docs/SETUP.md, LICENSE) would rot
    here. Component-root-relative paths become blob URLs on the component
    repo's default branch; absolute URLs, anchors, and mailto: pass through.
    """
    base = f"https://github.com/gaganjainse/{repo}/blob/main/"
    repo_root = readme.parent.resolve()  # directory containing README.md
    # .resolve() matters: via the fallback src path the parent contains
    # '..' segments and relative_to() below would spuriously fail,
    # leaving links untranslated (raw relative links rot in the mirror).

    def fix(m: re.Match) -> str:
        text, url, anchor = m.group(1), m.group(2), m.group(3) or ""
        if "://" in url or url.startswith(("mailto:", "#", "/")):
            return m.group(0)
        resolved = pathlib.Path(os.path.normpath(repo_root / url))
        # only rewrite links that stay inside the component repo
        try:
            rel = resolved.relative_to(repo_root).as_posix()
        except ValueError:
            return m.group(0)
        return f"[{text}]({base}{rel}{anchor})"

    out = []
    in_code = False
    for line in body.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        out.append(line if in_code else LINK_RE.sub(fix, line))
    return "".join(out)


def _component_repos() -> dict[str, str]:
    """Map component-docs filename -> repo basename, deduped by repo.

    Since the shesh-core consolidation (ADR-0019) one repo backs 16 organs, so
    keying by component name would mirror the same README 16 times. Key by repo
    basename instead: one docs/components/<repo>.md per actual repo.
    """
    data = tomllib.loads((ROOT / "manifests/components.toml").read_text("utf-8"))
    comps = data.get("component", {})
    repos: dict[str, str] = {}
    for name, comp in comps.items():
        if not name.startswith("shesh-"):
            continue
        repo = comp.get("repo", "")
        if not repo:
            continue
        basename = repo.split("/")[-1]
        repos.setdefault(basename, basename)
    return repos


def _find_readme(src_root: pathlib.Path, repo: str) -> pathlib.Path | None:
    for base in (src_root, FALLBACK_SRC):
        cand = base / repo / "README.md"
        if cand.is_file():
            return cand
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="verify no drift, exit 1 if stale")
    ap.add_argument("--src-root", type=pathlib.Path, default=DEFAULT_SRC)
    args = ap.parse_args()

    out_dir = ROOT / "docs" / "components"
    out_dir.mkdir(parents=True, exist_ok=True)

    stale: list[str] = []
    missing: list[str] = []
    synced = 0
    for name, repo in sorted(_component_repos().items()):
        readme = _find_readme(args.src_root, repo)
        if readme is None:
            missing.append(name)
            continue
        target = out_dir / f"{name}.md"
        content = translate_links(readme.read_text("utf-8"), name, readme)
        if target.exists() and target.read_text("utf-8") == content:
            continue
        if args.check:
            stale.append(name)
        else:
            target.write_text(content)
            synced += 1

    for name in missing:
        print(f"SKIPPED (no checkout): {name}")
    if synced:
        print(f"synced {synced} component READMEs -> {out_dir}")
    if stale:
        print("STALE (README drift — run python tools/sync_component_docs.py):")
        for name in stale:
            print(f"  - {name}")
        return 1
    if not args.check and not synced:
        print("all component READMEs already current")
    print(f"components checked: {len(_component_repos())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
