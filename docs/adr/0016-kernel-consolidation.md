# ADR-0016: Kernel Consolidation — Merge Withdrawn, Wave Adopted as-is

**Date:** 2026-08-12
**Status:** Accepted (supersedes the staged-merge plan portion of ADR-0008)

## Context

TODO §1 carried a 🔴-blocked plan to merge the archived `shesha-kernel` (Rust,
13 crates + worker bin) into `SheshAOS` (Rust, 12 crates). Two questions were
re-opened in review on 2026-08-12:

1. Do we actually need what the merge would bring (esp. `shesh-protocols`
   — the 2,045-LOC ACP+MCP wire implementation)?
2. The kernel's `waveobj`/`wps`/`blockctl`/`wconfig` crates were the start of a
   **1:1 Rust port of Wave Terminal** (crate names mirror `wavetermdev/waveterm`
   `pkg/*` one-to-one). Is that rewrite worth finishing?

## Evidence (measured on fresh clones, 2026-08-12)

- **ACP already exists in Python:** `shesh-acp` — JSON-RPC 2.0 stdio server for
  Zed/JetBrains/Neovim, 12/12 tests green.
- **MCP already exists in Python:** 17 `shesh-*-mcp` servers + GuardedMCP policy
  wrapper (`shesh-audit`), 191 component tests green across 19/20 components.
- **Python↔Rust bridge already exists:** `shesh_audit/nexus_bridge.py` emits
  Nexus-format JSONL events into the Rust event store path.
- `shesh-protocols` in Rust would be a **third implementation of owned wires**;
  no consumer requires Rust-native ACP/MCP today.
- Wave Terminal = ~60k LOC TS (React 19/Monaco/xterm-webgl) + ~75k LOC Go,
  22k★, actively maintained. A solo Rust port is multi-year and was, by the
  author's own measure, "nowhere near Wave."
- Divergence between kernel and SheshAOS is shallow in most crates but total in
  the ones that matter (`NexusError`, TUI API); kernel has 2 extra files
  (`protocols`, worker bin) worth noting, nothing blocking.
- SeshaOS (359 LOC) was already folded into SheshAOS; redundantly live.

## Decision

- **Withdraw the kernel-merge plan.** No crate porting. `shesha-kernel` remains
  archived (ADR-0008). Close GitHub issues #7–13.
- **Archive SeshaOS** (superseded by SheshAOS; folded in per TODO).
- **Adopt stock Wave Terminal** as the mission-control surface. No rewrite, no
  heavy fork: integration via documented surfaces only (custom `widgets.json`
  widgets, `wsh` RPC, workspaces, OpenAI-compatible AI endpoint → OmniRoute or
  local Ollama). Fork `gaganjainse/waveterm` = pin + insurance, upstream-first
  patches. Wrapper/config lives in `gaganjainse/shesh-wave`.
- **SheshAOS stays the canonical Rust kernel.** `shesh-protocols` is demoted
  to P3 archive-candidate — port only if a future Rust consumer needs native
  ACP/MCP. `shesh-brain` scope unchanged.
- Rust crate prefix `sheshaaos-*` normalization deferred to the next Rust-enabled
  session (needs cargo; see ADR-0017 exception register).

## Consequences

- ✅ TODO §1 unblocked by decision instead of by labor; queue honest again.
- ✅ Terminal strategy has one owner (stock Wave), terminal-daily-driver choice
  (foot/ghostty/tmux) is orthogonal and free.
- ✅ Zero third implementation of protocol wires to maintain.
- ❌ Rust ambitions narrowed to governance kernel + salvage-optional crates.
- ❌ `shesh-protocols` Rust ACP/MCP parity postponed indefinitely.

## Links

- ADR-0008 (kernel archive), ADR-0010 (ACP+MCP), ADR-0017 (naming purge)
- shesh-ecosystem issues #7–13 (closed by this decision)
- gaganjainse/shesh-wave (Wave integration wrapper)
