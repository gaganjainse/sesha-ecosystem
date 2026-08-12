# ADR-0018: Adopt-vs-Build Decisions & the 2026-08-12 Excision

**Date:** 2026-08-12
**Status:** Accepted
**Tags:** strategy, dependencies, architecture, cleanup

## Context

The renovation surfaced a recurring question — build our own or adopt the
web-best? — plus a barrel of pre-commit archaeology: crates, directories and
fallback paths that the already-adopted architecture had made dead weight but
that nobody had physically removed. This ADR records each adopt-vs-build call
and the resulting excision.

## Decisions

### 1. MCP servers: adopt standalone `fastmcp` 3, drop the official `mcp` shim

`mcp` 1.29.0 bundles a FastMCP re-implementation whose settings model carries
an unresolved forward reference — every `FastMCP(...)` construction raises a
`pydantic-settings` `IncompleteFieldDefinitionWarning`. `mcp` 2.0.0 deletes
`mcp.server.fastmcp` entirely, making our unbounded `mcp>=1.0` a resolver
landmine. Options were: (a) suppress the warning, (b) pin `mcp<2` forever,
(c) migrate to upstream-maintained `fastmcp>=3.4.7,<4`. **Chosen: (c).**
The warning is a real bug in the shim, not noise; the standalone package is
where FastMCP development actually happens. 20 component repos migrated;
every suite passes under `pytest -W error` (warnings-as-errors), which is now
the policy, not an option.

### 2. Guard enforcement: fail-fast, never silent fallback

Components carried `try: from shesh_audit… except ImportError: _MCP = FastMCP`.
Worse, several imported `shesh_audit.guard` — a module that **never existed** —
so the fallback fired on every run and tools ran unguarded while ADR-0015
claimed total coverage. **Chosen: direct imports + declared dependencies.**
A missing guard now crashes the server at startup. Internal deps install in
CI via `git+https://github.com/gaganjainse/<repo>.git@main` until packages
are published to PyPI (publication tracked as a user action).

### 3. Terminal & mission control: adopt Wave, excise the pretenders

ADR-0016 adopted stock Wave Terminal. Leftovers from the abandoned port were
still workspace members — and were breaking CI: `shesh-terminal`'s build
script requires a Zig toolchain (ADR-0001 forbids Zig/FFI in the main build),
its "native Zig VT100 parser" is a 71-line line/byte counter whose only
caller was a demo `shesh pty` printout, and `PtyManager` had zero callers
(blockctl uses `portable-pty` directly). `shesh-gui` had zero consumers;
`shesh-tui` only fed the CLI default. Top-level `zig/` was an orphaned
pre-Rust kernel attempt. The dead `tests/` crate advertised six criterion
benches that had never executed (not a workspace member; hardcoded paths from
an old machine). **Chosen: excise all of it.** SheshAOS is 9 crates + a
headless `shesh` CLI; three *real* criterion benches cover event store,
WaveObj store, and broker hot paths; workspace is pure Rust again.

### 4. LLM supply: local Ollama models, retire GitHub Models routing

The swarm LLM worker's dependency on GitHub Models free tier was replaced by
the local stack (Ollama phi4-mini/qwen2.5-coder per GETTING_STARTED), with
OmniRoute as the OpenAI-compatible front. Rationale: ratelimits made CI
non-deterministic; local is deterministic and zero-cost.

### 5. Lint gates: tool-native, not grep

The "no unwrap/expect in production code" gate was a grep that could not see
`#[cfg(test)]` scope — it flagged only false positives. **Chosen:** every
crate carries `[lints] workspace = true`; `clippy -D warnings` with
`clippy.toml`'s `allow-*-in-tests` is the enforcement. That immediately found
two real production unwraps the grep never could, now fixed.

## Consequences

- ✅ Workspace is smaller, honest, and green under stricter gates than before.
- ✅ Zig toolchain requirement eliminated from the main build (bootstrap + CI).
- ✅ Dependency graph is generated from `cargo metadata`/pyprojects
  (`tools/depgraph.py` + `docs/architecture/DEPENDENCY_GRAPH.md`); a CI
  freshness gate makes doc drift a build failure.
- ❌ `shesh pty`/`shesh tui` go away — breakage accepted, no grandfathering.
- ❌ PyPI publication of `shesh-*` packages remains an open user action;
  until then CI tracks `main` of internal deps.

## Links

- ADR-0001 (language policy), ADR-0015 (guard, updated), ADR-0016 (Wave)
- `docs/architecture/DEPENDENCY_GRAPH.md`, `tools/depgraph.py`
