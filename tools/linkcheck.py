#!/usr/bin/env python3
"""tools/linkcheck.py — broken relative-link checker for Markdown trees.

Adopted from the orchestrator home directory (2026-08-12).

    python3 tools/linkcheck.py [dir]    # default: ./docs

Exit 1 with a list of BROKEN targets when any `[text](relative/path.md)`
points at something that does not exist.
"""
from __future__ import annotations

import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
# Immutable/historical records (QUERYLOG, ADRs, incident/attic notes) may link
# to pages that legitimately no longer exist; living docs must not. Mirrors
# docs_index.EXEMPT_DIRS and proofread.SKIP_PARTS.
SKIP_PARTS = ("adr", "queries", "attic", "audits", "INCIDENTS", "desktop")
link_re = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]+)?\)")
n = 0
for md in root.rglob("*.md"):
    if any(part in SKIP_PARTS for part in md.parts):
        continue
    for m in link_re.finditer(md.read_text(encoding="utf-8")):
        url = m.group(1)
        if "://" in url or url.startswith("mailto:"):
            continue
        if not (md.parent / url).resolve().exists():
            print("BROKEN", md, url)
            n += 1
print("TOTAL BROKEN:", n)
sys.exit(1 if n else 0)
