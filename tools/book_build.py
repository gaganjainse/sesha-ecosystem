#!/usr/bin/env python3
"""tools/book_build.py — generate the shesh-docs mdBook tree from canonical sources.

Architecture (docs-as-code, hybrid topology per DOCUMENTATION_POLICY.md):
canonical docs live beside their code (this repo + component clones); the
book tree is a pure projection. Nothing hand-maintained lives under generated
paths; book-native pages are declared in BOOK_OWNED and everything else under
src/ that is neither generated nor owned is deleted — loudly.

Failures are loud by design: a missing REQUIRED source aborts the build;
missing OPTIONAL sources print SKIPPED lines. That is how stale docs happen
when silent — so nothing here is silent.

Usage:
    python tools/book_build.py            # write the tree (DOCS_REPO env override)
    python tools/book_build.py --check    # verify only; exit 1 on drift (CI gate)
"""

from __future__ import annotations

import os
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_REPO = Path(os.environ.get("DOCS_REPO", "/tmp/shesh-docs"))
SRC_ROOT = Path(os.environ.get("SRC_ROOT", ROOT.parent / "src"))
BOOK = DOCS_REPO / "src"

# ---------------------------------------------------------------------------
# Mirror map: canonical source → book destination (relative to src/).
# Prefix: "eco:" = this repo, "src:" = component clone under SRC_ROOT,
# "channels:" = release-channel metadata. OPTIONAL marks sibling-layout
# sources that may be absent on a minimal checkout (announced, never silent).
# ---------------------------------------------------------------------------
MIRRORS: list[tuple[str, str, bool]] = [
    # Part I — Product
    ("eco:README.md", "product/overview.md", True),
    ("eco:docs/GETTING_STARTED.md", "product/getting-started.md", True),
    ("eco:docs/architecture/AGENTIC_BODY.md", "product/architecture/agentic-body.md", True),
    ("eco:docs/architecture/REPO_TOPOLOGY.md", "product/architecture/repo-topology.md", True),
    ("eco:docs/architecture/LANGUAGE_POLICY.md", "product/architecture/language-policy.md", True),
    ("eco:docs/architecture/MULTI_AGENT.md", "product/architecture/multi-agent.md", True),
    ("eco:docs/ACP_A2A.md", "product/architecture/acp-a2a.md", True),
    ("eco:docs/LEARNING.md", "product/concepts/learning.md", True),
    ("eco:docs/CONTAINERS_AND_VENV.md", "product/concepts/containers-venv.md", True),
    ("eco:docs/LINUX_LAYOUT.md", "product/concepts/linux-layout.md", True),
    ("channels:README.md", "product/reference/channels.md", True),
    ("eco:docs/SOURCES.md", "product/reference/upstreams.md", True),
    ("eco:docs/tutorials/organize-downloads.md", "product/tutorials/organize-downloads.md", True),
    (
        "eco:docs/tutorials/voice-settings-organizer.md",
        "product/tutorials/voice-settings-organizer.md",
        True,
    ),
    ("eco:docs/tutorials/rag-vector.md", "product/tutorials/rag-vector.md", True),
    # Part II — Factory
    ("eco:docs/WORKSPACE_SEPARATION.md", "factory/overview.md", True),
    ("eco:docs/SESSION_PROTOCOL.md", "factory/session-protocol.md", True),
    ("eco:docs/tools/session-guard.md", "factory/session-guard.md", True),
    ("eco:docs/tools/secure-pat.md", "factory/secure-pat.md", True),
    ("eco:docs/tools/github-auth.md", "factory/github-auth.md", True),
    ("eco:docs/tools/setup-worker.md", "factory/setup-worker.md", True),
    ("eco:docs/tools/llm-adapter.md", "factory/llm-adapter.md", True),
    ("eco:docs/tools/model-router.md", "factory/model-router.md", True),
    ("eco:docs/SWARM.md", "factory/swarm/README.md", True),
    ("eco:docs/EFFICIENCY.md", "factory/efficiency.md", True),
    ("eco:docs/TRAVEL_MODE.md", "factory/travel-mode.md", True),
    ("eco:docs/FOOLPROOF_SWARM_PROMPTS.md", "factory/foolproof-prompts.md", True),
    ("eco:docs/STEAL_INFRASTRUCTURE.md", "factory/steal-infrastructure.md", True),
    ("eco:docs/LIVE_UPDATE_SYSTEM.md", "factory/live-update.md", True),
    ("eco:docs/MODEL_AGNOSTIC.md", "factory/model-agnostic.md", True),
    ("src:shesh-harness/README.md", "factory/eval-harness.md", False),
    # Part III — Gateway
    ("eco:docs/OMNIROUTE_STUDY.md", "gateway/omniroute-study.md", True),
    ("src:shesh-omniroute/README.md", "gateway/shesh-omniroute.md", False),
    # Part IV — Desktop (sibling checkout; optional on minimal layouts)
    ("src:shesh-desktop/docs/SHESH/00_INDEX.md", "desktop/00-index.md", False),
    ("src:shesh-desktop/docs/SHESH/01_AUDIT.md", "desktop/01-audit.md", False),
    ("src:shesh-desktop/docs/SHESH/02_ROADMAP.md", "desktop/02-roadmap.md", False),
    ("src:shesh-desktop/docs/SHESH/03_DISK_STRUCTURE.md", "desktop/03-disk-structure.md", False),
    ("src:shesh-desktop/docs/SHESH/04_DEVICE_PROFILE.md", "desktop/04-device-profile.md", False),
    (
        "src:shesh-desktop/docs/SHESH/05_SMART_ORGANIZER_V2.md",
        "desktop/05-smart-organizer.md",
        False,
    ),
    ("src:shesh-desktop/docs/SHESH/06_SHESH_AGENT.md", "desktop/06-shesh-agent.md", False),
    ("src:shesh-desktop/docs/SHESH/07_AUTOMATIONS.md", "desktop/07-automations.md", False),
    ("src:shesh-desktop/docs/SHESH/08_ECOSYSTEM_TOOLS.md", "desktop/08-ecosystem-tools.md", False),
    ("src:shesh-desktop/docs/SHESH/09_AI_PROMPTS.md", "desktop/09-ai-prompts.md", False),
    (
        "src:shesh-desktop/docs/SHESH/10_LICENSES_AND_SOURCES.md",
        "desktop/10-licenses-sources.md",
        False,
    ),
    ("src:shesh-desktop/docs/SHESH/AMBIENT_DESIGN.md", "desktop/ambient-design.md", False),
    ("src:shesh-desktop/docs/SHESH_README.md", "desktop/shesh-readme.md", False),
    ("src:shesh-desktop/docs/SHESH/checklist.md", "desktop/checklist.md", False),
    # Part VI — Audits, roadmaps, incidents
    ("eco:docs/AUDIT_AND_ROADMAP.md", "audits/audit-and-roadmap.md", True),
    ("eco:docs/audits/AUDIT_EXHAUSTIVE.md", "audits/exhaustive-audit.md", True),
    ("eco:docs/GAP_ANALYSIS.md", "audits/gap-analysis.md", True),
    ("eco:docs/TOOLING_CATALOG.md", "audits/tooling-catalog.md", True),
    (
        "eco:docs/INCIDENTS/2026-08-11-multi-tab-swarm.md",
        "audits/incident-2026-08-11-multi-tab-swarm.md",
        True,
    ),
    (
        "eco:docs/audits/AUDIT_ECOSYSTEM_2026-08-12.json",
        "audits/AUDIT_ECOSYSTEM_2026-08-12.json",
        True,
    ),
    ("eco:docs/audits/AUDIT_EXHAUSTIVE.json", "audits/AUDIT_EXHAUSTIVE.json", True),
    # Part VII — Verification & handoff
    ("eco:docs/MANUAL_VERIFICATION.md", "verification/manual-verification.md", True),
    ("eco:docs/SESSION_HANDOFF.md", "verification/session-handoff.md", True),
    # Part VIII — Skills & policies
    ("eco:docs/skills/README.md", "skills/overview.md", True),
    ("eco:docs/skills/coding.md", "skills/coding.md", True),
    ("eco:docs/skills/web-research.md", "skills/web-research.md", True),
    ("eco:docs/skills/docs-writer.md", "skills/docs-writer.md", True),
    ("eco:docs/skills/safety-governance.md", "skills/safety-governance.md", True),
    ("eco:docs/skills/daily-briefing.md", "skills/daily-briefing.md", True),
    ("eco:docs/skills/autopilot.md", "skills/autopilot.md", True),
    ("eco:docs/skills/POLICY.md", "policies/skills-policy.md", True),
    ("eco:SECURITY.md", "policies/security-policy.md", True),
    ("eco:docs/THREAT_MODEL.md", "policies/threat-model.md", True),
    ("eco:docs/RECOVERY.md", "policies/recovery.md", True),
    ("eco:docs/policies/DEPENDENCY_POLICY.md", "policies/dependency-policy.md", True),
    ("eco:docs/policies/DOCUMENTATION_POLICY.md", "policies/documentation-policy.md", True),
    ("eco:docs/policies/FORK_GARDENING.md", "policies/fork-gardening.md", True),
    ("eco:docs/policies/JANITOR_TODO_POLICY.md", "policies/janitor-todo-policy.md", True),
    # Part IX — Queries
    ("eco:docs/queries/QUERYLOG.md", "queries/querylog.md", True),
    ("eco:docs/queries/QUERYLOG_ALL_AGENTS.md", "queries/querylog-all-agents.md", True),
    ("eco:docs/NEXT_SESSION_PROMPT.md", "queries/next-session-prompt.md", True),
    # Introduction
    ("eco:docs/GLOSSARY.md", "glossary.md", True),
    # Part XI — SheshAOS (flagship Rust AI OS)
    ("src:SheshAOS/README.md", "sheshaos/README.md", False),
    ("src:SheshAOS/HANDOVER.md", "sheshaos/handover.md", False),
    ("src:SheshAOS/docs/architecture.md", "sheshaos/architecture.md", False),
]

# Whole-directory mirrors (ADR tree).
DIR_MIRRORS = [("eco:docs/adr", "adr", True)]

# Pages the book owns (navigation glue, book-native narratives). Everything
# under src/ that is neither a generated target nor listed here is deleted.
BOOK_OWNED = {
    "SUMMARY.md",
    "introduction.md",
    "how-to-use.md",
    "product/architecture.md",
    "product/concepts.md",
    "product/tasks/overview.md",
    "product/reference/overview.md",
    "product/tutorials/overview.md",
    "gateway/overview.md",
    "desktop/overview.md",
    "portfolio/overview.md",
    "portfolio/auto-update.md",
    "projects/index.md",
}

# Fission MANUAL_VERIFICATION.md → per-section task chapters.
MV_SLUGS = {
    0: "first-boot",
    1: "accounts-keys-secrets",
    2: "mcp-mesh",
    3: "voice",
    4: "gpu-power-mux",
    5: "display-desktop",
    6: "backup",
    7: "phone",
    8: "containers",
    9: "agent-behavior",
    10: "security-audit",
    11: "canary-releases",
}

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s#]+)(#[^)]*)?\)")
GH_BLOB = "https://github.com/gaganjainse/shesh-ecosystem/blob/main/"


def resolve(src: str) -> Path:
    kind, _, rel = src.partition(":")
    if kind == "eco":
        return ROOT / rel
    if kind == "channels":
        return ROOT / "channels" / rel
    if kind == "src":
        return SRC_ROOT / rel
    raise ValueError(kind)


def canonical_rel(src: str) -> str:
    """Repo-relative path of a source, for link translation bookkeeping."""
    kind, _, rel = src.partition(":")
    return rel if kind == "eco" else f"../src/{rel}"


def build_link_map() -> dict[str, str]:
    m: dict[str, str] = {}
    for src, dst, _req in MIRRORS:
        m[canonical_rel(src)] = dst
    for src, dst, _req in DIR_MIRRORS:
        base = canonical_rel(src)
        srcdir = resolve(src)
        if srcdir.is_dir():
            for f in srcdir.rglob("*"):
                if f.is_file():
                    m[f"{base}/{f.relative_to(srcdir)}"] = str(Path(dst) / f.relative_to(srcdir))
    # Fission products: links from inside MANUAL_VERIFICATION resolve in its dir.
    m["docs/MANUAL_VERIFICATION.md"] = "verification/manual-verification.md"
    return m


def split_fences(text: str) -> list[tuple[bool, str]]:
    """(is_code, chunk) pairs so link rewriting never touches code fences."""
    parts, buf, in_code = [], [], False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            parts.append((in_code, "".join(buf)))
            buf, in_code = [], not in_code
        buf.append(line)
    parts.append((in_code, "".join(buf)))
    return parts


def translate_links(body: str, src_canonical: str, dst_book: str, link_map: dict[str, str]) -> str:
    src_dir = str(Path(src_canonical).parent)
    dst_dir = Path(dst_book).parent

    def fix(m: re.Match) -> str:
        text, url, anchor = m.group(1), m.group(2), m.group(3) or ""
        if "://" in url or url.startswith(("mailto:", "#")):
            return m.group(0)
        resolved = os.path.normpath(os.path.join(src_dir, url))
        target = link_map.get(resolved)
        if target is None:
            cross = re.match(r"^\.\./src/([^/]+)/(.+)$", resolved)
            if cross and (SRC_ROOT / cross.group(1) / cross.group(2)).exists():
                # canonical in a component repo, unmirrored: absolute URL
                repo, path = cross.group(1), cross.group(2)
                return f"[{text}](https://github.com/gaganjainse/{repo}/blob/main/{path}{anchor})"
            if (ROOT / resolved).exists():
                # canonical but not mirrored into the book: go absolute
                return f"[{text}]({GH_BLOB}{resolved}{anchor})"
            return m.group(0)  # leave; book link gate will catch real rot
        rel = os.path.relpath(target, dst_dir)
        return f"[{text}]({rel}{anchor})"

    out = []
    for is_code, chunk in split_fences(body):
        out.append(chunk if is_code else LINK_RE.sub(fix, chunk))
    return "".join(out)


def render_mirror(src: str, dst: str) -> tuple[str, str] | None:
    spath = resolve(src)
    if not spath.exists():
        return None
    raw = spath.read_text(encoding="utf-8")
    return dst, translate_links(raw, canonical_rel(src), dst, LINK_MAP)


def toml_page(title: str, src: str) -> str:
    raw = resolve(src).read_text(encoding="utf-8")
    return f"# {title}\n\n```toml\n{raw.rstrip()}\n```\n"


def fission_manual_verification() -> dict[str, str]:
    raw = (ROOT / "docs/MANUAL_VERIFICATION.md").read_text(encoding="utf-8")
    marks = [
        (m.start(), int(m.group(1)), m.group(2).strip())
        for m in re.finditer(r"(?m)^## (\d+)\.\s+(.+)$", raw)
    ]
    out: dict[str, str] = {}
    for i, (pos, num, title) in enumerate(marks):
        if num not in MV_SLUGS:
            continue
        end = marks[i + 1][0] if i + 1 < len(marks) else len(raw)
        body = raw[pos:end].split("\n", 1)[1].strip()
        body = translate_links(
            body, "docs/MANUAL_VERIFICATION.md", f"product/tasks/{MV_SLUGS[num]}.md", LINK_MAP
        )
        page = (
            f"# {num}. {title}\n\n"
            f"> Part of the [Manual Verification Checklist]"
            f"(../../verification/manual-verification.md) — section {num} "
            f"of 16.\n\n{body}\n"
        )
        out[f"product/tasks/{MV_SLUGS[num]}.md"] = page
    return out


def fission_free_providers() -> dict[str, str]:
    raw = (ROOT / "docs/OMNIROUTE_STUDY.md").read_text(encoding="utf-8")
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## (.+)$", raw)]
    want = {"Free tiers", "Big industry-used free models"}
    chunks = []
    for i, (pos, title) in enumerate(heads):
        if any(title.startswith(w) for w in want):
            end = heads[i + 1][0] if i + 1 < len(heads) else len(raw)
            chunks.append(raw[pos:end].strip())
    body = "\n\n---\n\n".join(chunks)
    body = translate_links(body, "docs/OMNIROUTE_STUDY.md", "gateway/free-providers.md", LINK_MAP)
    page = (
        "# Free providers — Groq, OpenRouter, GitHub Models, HF\n\n"
        "> Extracted from the full [OmniRoute study](omniroute-study.md); "
        "numbers re-verified 2026-06-17, refresh CI-gated.\n\n"
        f"{body}\n"
    )
    return {"gateway/free-providers.md": page}


def gen_components_readme() -> dict[str, str]:
    data = tomllib.loads((ROOT / "manifests/components.toml").read_text("utf-8"))
    comps = data.get("components", data.get("component", {}))
    if isinstance(comps, dict):
        rows = [(name, cfg) for name, cfg in sorted(comps.items())]
    else:  # list-of-tables form
        rows = [(c.get("name", "?"), c) for c in comps]
    lines = [
        "# Components — all shesh-* repos",
        "",
        "Generated from [`manifests/components.toml`](../manifest.md) — the",
        "manifest is the single source of truth; this page is a projection.",
        "",
        "| Component | Layer | Channel | Repo |",
        "|---|---|---|---|",
    ]
    for name, cfg in rows:
        layer = cfg.get("layer", "—")
        chan = cfg.get("channel", cfg.get("channels", "—"))
        lines.append(
            f"| `{name}` | {layer} | {chan} | [{name}](https://github.com/gaganjainse/{name}) |"
        )
    lines += [
        "",
        "Component READMEs are canonical in their own repos (policy:",
        "ecosystem links, never copies prose).",
        "",
    ]
    return {"product/reference/components/README.md": "\n".join(lines)}


LINK_MAP: dict[str, str] = build_link_map()


def expected_files() -> dict[str, str | None]:
    """dest → rendered content (None = handled elsewhere / dir copy)."""
    exp: dict[str, str | None] = {}
    for src, dst, req in MIRRORS:
        r = render_mirror(src, dst)
        if r is None:
            if req:
                print(f"REQUIRED doc source missing: {src}", file=sys.stderr)
                raise FileNotFoundError(src)
            print(f"SKIPPED (absent): {src}")
            exp[dst] = None  # registered target; keep any existing copy
            continue
        exp[dst] = r[1]
    for src, dst, req in DIR_MIRRORS:
        srcdir = resolve(src)
        if not srcdir.is_dir():
            if req:
                print(f"REQUIRED dir missing: {src}", file=sys.stderr)
                raise FileNotFoundError(src)
            print(f"SKIPPED (absent): {src}")
            continue
        for f in srcdir.rglob("*"):
            if f.is_file():
                rel = f.relative_to(srcdir)
                body = f.read_text(encoding="utf-8")
                exp[str(Path(dst) / rel)] = translate_links(
                    body, canonical_rel(src) + "/" + str(rel), str(Path(dst) / rel), LINK_MAP
                )
    exp["product/reference/manifest.md"] = toml_page(
        "Manifest — components.toml", "eco:manifests/components.toml"
    )
    exp["product/reference/models.md"] = toml_page(
        "Models — models.toml", "eco:manifests/models.toml"
    )
    exp.update(fission_manual_verification())
    exp.update(fission_free_providers())
    exp.update(gen_components_readme())
    return exp


def main() -> int:
    check = "--check" in sys.argv
    if not BOOK.is_dir():
        print(f"ERROR: book src missing: {BOOK} (clone shesh-docs first)", file=sys.stderr)
        return 1
    exp = expected_files()
    drift: list[str] = []

    # write / verify generated content
    written = 0
    for dst, content in sorted(exp.items()):
        path = BOOK / dst
        if content is None:
            if not path.exists():
                print(f"NOTE: optional target absent: {dst}")
            continue
        if path.exists() and path.read_text(encoding="utf-8") == content:
            continue
        drift.append(dst)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            written += 1

    # orphan sweep: anything under src/ that is neither generated nor book-owned
    orphans = []
    for f in sorted(BOOK.rglob("*")):
        if not f.is_file():
            continue
        rel = str(f.relative_to(BOOK))
        if rel not in exp and rel not in BOOK_OWNED:
            orphans.append(rel)
            if not check:
                f.unlink()
    # prune emptied dirs and report
    if not check:
        for d in sorted((p for p in BOOK.rglob("*") if p.is_dir()), key=lambda p: -len(p.parts)):
            if not any(d.iterdir()):
                d.rmdir()

    # SUMMARY integrity: every chapter target must exist
    summary = BOOK / "SUMMARY.md"
    missing = []
    if summary.exists():
        for m in LINK_RE.finditer(summary.read_text(encoding="utf-8")):
            url = m.group(2)
            if "://" in url:
                continue
            if not (BOOK / url).exists():
                missing.append(url)

    if drift or orphans or missing:
        print(
            f"{'WOULD update' if check else 'updated'}: {len(drift) or written} files; "
            f"{'WOULD remove' if check else 'removed'} {len(orphans)} orphans"
        )
        for o in orphans:
            print(f"  orphan: {o}")
        for x in missing:
            print(f"  SUMMARY target missing: {x}")
        if check:
            return 1
    print(
        f"book build {'check ' if check else ''}OK — {len(exp)} generated, "
        f"{len(BOOK_OWNED)} book-owned, {len(orphans)} orphans removed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
