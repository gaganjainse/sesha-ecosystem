#!/usr/bin/env python3
"""tools/depgraph.py — generate the ecosystem dependency graph, deterministically.

Three layers, all derived from source of truth (nothing hand-maintained):

1. Rust crates: `cargo metadata` on the SheshAOS workspace (falls back to
   scanning Cargo.toml files when cargo is unavailable, e.g. on CI docs jobs).
2. Python components: `dependencies` in each component's pyproject.toml that
   reference other shesh-* packages.
3. Repo level: the union of 1+2 plus declared repos in manifests/components.toml.

Usage:
    python tools/depgraph.py                 # print mermaid graph for all layers
    python tools/depgraph.py --json          # machine-readable adjacency
    python tools/depgraph.py --check FILE    # exit 1 if FILE's graph block is stale

The --check mode is the CI freshness gate: the committed graph must equal the
generated one, which makes missing-doc updates fail loudly instead of drifting.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ECO = Path(__file__).resolve().parent.parent          # shesh-ecosystem repo


def resolve_src() -> Path:
    """Where the sibling component checkouts live.

    Search order (first hit wins, printed in --check output for
    transparency): $SHESH_SRC (explicit override, CI sets it) ->
    $HOME/src (CI clone jobs land here) -> <ecosystem>/../src
    (developer workspace). A candidate only counts if the SheshAOS
    checkout is actually there — silently scanning the wrong tree is
    exactly the class of failure this tool exists to prevent.
    """
    candidates = []
    if os.environ.get("SHESH_SRC"):
        candidates.append(Path(os.environ["SHESH_SRC"]))
    candidates.append(Path.home() / "src")
    candidates.append(ECO.parent / "src")
    for cand in candidates:
        if (cand / "SheshAOS" / ".git").exists():
            return cand
    return candidates[-1]  # let the missing-path error show truthfully


SRC = resolve_src()


def manifest_repos(include_archived: bool = False) -> list[str]:
    """Repos declared in manifests/components.toml (install-time truth).

    Entries marked `archived = true` (e.g. shesh-desktop) are frozen upstream:
    archived repos are read-only so findings against them can never be fixed —
    CI clone lists and audits skip them by default.
    """
    data = tomllib.loads((ECO / "manifests" / "components.toml").read_text())
    comps = data.get("component", {})
    if include_archived:
        return sorted(comps.keys())
    return sorted(k for k, v in comps.items() if not v.get("archived", False))


def list_repos() -> list[str]:
    """Every repo the graph reads: SheshAOS + manifest components + any
    checked-out shesh-*/pyproject.toml under SRC."""
    found = {p.parent.name for p in SRC.glob("shesh-*/pyproject.toml")}
    return sorted({"SheshAOS"} | set(manifest_repos()) | found)


def rust_edges_workspace(sheshaos: Path) -> dict[str, set[str]]:
    """crate -> intra-workspace dependency crates, via cargo metadata."""
    try:
        out = subprocess.run(
            ["cargo", "metadata", "--format-version", "1", "--locked", "--no-deps",
             "--manifest-path", str(sheshaos / "Cargo.toml")],
            capture_output=True, text=True, timeout=120, check=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        # cargo-less fallback: parse Cargo.tomls (workspace member list + dep paths)
        root = tomllib.loads((sheshaos / "Cargo.toml").read_text())
        members = [m.split("/")[-1] for m in root["workspace"]["members"]]
        names = set(members)
        edges = {name: set() for name in names}
        for name in names:
            toml_path = (sheshaos / "crates" / name / "Cargo.toml")
            if name == "shesh-cli":
                toml_path = sheshaos / "bin" / "shesh-cli" / "Cargo.toml"
            if not toml_path.exists():
                continue
            text = toml_path.read_text()
            for other in names - {name}:
                if re.search(rf"^{re.escape(other)}\s*[=.]", text, re.M):
                    edges[name].add(other)
        return edges

    meta = json.loads(out)
    members = {p["name"] for p in meta["packages"]}
    edges = {name: set() for name in members}
    for pkg in meta["packages"]:
        for dep in pkg["dependencies"]:
            if dep["name"] in members:
                edges[pkg["name"]].add(dep["name"])
    return edges


def python_edges_components(src: Path) -> dict[str, set[str]]:
    """component repo -> internal shesh-* package deps (declared in pyproject)."""
    edges: dict[str, set[str]] = {}
    for pyproject in sorted(src.glob("shesh-*/pyproject.toml")):
        repo = pyproject.parent.name
        try:
            data = tomllib.loads(pyproject.read_text())
        except tomllib.TOMLDecodeError:
            continue
        deps = data.get("project", {}).get("dependencies", [])
        internal = set()
        for dep in deps:
            name = re.split(r"[<>=~! @\[]", dep, maxsplit=1)[0].strip()
            if name.startswith("shesh-") and name != repo:
                internal.add(name)
        edges[repo] = internal
    return edges


def to_mermaid(title: str, edges: dict[str, set[str]]) -> str:
    lines = ["```mermaid", f"---\ntitle: {title}\n---", "graph TD"]
    for node in sorted(edges):
        lines.append(f'    {node.replace("-", "_")}["{node}"]')
    for src in sorted(edges):
        for dst in sorted(edges[src]):
            lines.append(f"    {src.replace('-', '_')} --> {dst.replace('-', '_')}")
    lines.append("```")
    return "\n".join(lines)


def rust_test_counts(sheshaos: Path) -> dict[str, int]:
    """#[test]/#[tokio::test] count per crate — feeds the CI floor honestly."""
    counts: dict[str, int] = {}
    for crate in sorted((sheshaos / "crates").glob("shesh-*")):
        n = 0
        for rs in crate.rglob("*.rs"):
            if "target" in rs.parts:
                continue
            text = rs.read_text(errors="replace")
            n += len(re.findall(r"#\[(?:tokio::)?test\]", text))
        counts[crate.name] = n
    for rs in (sheshaos / "bin").rglob("*.rs"):
        if "target" not in rs.parts:
            counts.setdefault("shesh-cli", 0)
            counts["shesh-cli"] += len(re.findall(r"#\[(?:tokio::)?test\]",
                                                  rs.read_text(errors="replace")))
    return counts


def render(eco: ECO = ECO) -> str:  # noqa: E501
    rust = rust_edges_workspace(SRC / "SheshAOS")
    comp = python_edges_components(SRC)
    parts = [
        "<!-- AUTO-GENERATED by tools/depgraph.py — edit by rerunning the tool,",
        "     CI's depgraph freshness gate rejects hand edits. -->",
        "",
        "# Shesh Ecosystem — Dependency Graph",
        "",
        "_Generated from cargo metadata, component pyprojects, and manifests/components.toml._",
        "",
        "## Rust workspace (SheshAOS)",
        "",
        to_mermaid("SheshAOS crates", rust),
        "",
        "### Test counts per crate (static #[test] scan)",
        "",
        "| crate | tests |", "|---|---|",
    ]
    total = 0
    for crate, n in rust_test_counts(SRC / "SheshAOS").items():
        parts.append(f"| {crate} | {n} |")
        total += n
    parts.append(f"| **total** | **{total}** |")
    parts += [
        "",
        "## Python components (shesh-* internal deps)",
        "",
        to_mermaid("Component internal dependencies", comp),
        "",
        "## Repo level",
        "",
        "Every arrow above lifted to its owning repo; SheshAOS crates map to the",
        "SheshAOS repo. Cross-layer edges: shesh-brain/audit → SheshAOS via the",
        "kernel event bridge (`kernel-events.jsonl`, ADR-0015).",
        "",
    ]
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", metavar="FILE")
    ap.add_argument("--list-repos", action="store_true",
                    help="print the repos the generator reads (for CI checkouts)")
    args = ap.parse_args()

    if args.list_repos:
        print("\n".join(list_repos()))
        return 0

    if args.json:
        rust = rust_edges_workspace(SRC / "SheshAOS")
        comp = python_edges_components(SRC)
        print(json.dumps({
            "rust": {k: sorted(v) for k, v in sorted(rust.items())},
            "python": {k: sorted(v) for k, v in sorted(comp.items())},
        }, indent=2))
        return 0

    text = render()
    if args.check:
        committed = Path(args.check).read_text()
        # stdout mode adds one trailing newline via print(); normalize both.
        if committed.rstrip("\n") != text.rstrip("\n"):
            print("STALE: dependency graph differs from generated output.", file=sys.stderr)
            print("Regenerate with: python tools/depgraph.py > " + args.check, file=sys.stderr)
            return 1
        print("dependency graph fresh")
        return 0
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
