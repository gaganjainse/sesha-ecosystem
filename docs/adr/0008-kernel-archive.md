# ADR-0008: Archive shesh-kernel, Don't Force Merge

**Date:** 2026-08-10
**Status:** Accepted
**Context:** SheshAOS (981 Rust tests, 12 crates) is the governance kernel. The archived `shesh-kernel` (alpha microkernel) diverged at type level: 57 compile errors, `NexusError`/`TUI` API mismatch, `russh::Error::msg` removed upstream, `zig` required by terminal crate.

## Decision
- **Do NOT force-merge** the two Rust trees — would ship broken build.
- Archive `shesh-kernel` as `shesha-kernel` (GitHub redirect) — superseded by SheshAOS.
- Document staged rebase plan in `SheshAOS/KERNEL_MERGE_PLAN.md`:
  1. Leaf crates first: protocols, waveobj, wps, blockctl, wconfig.
  2. Then ai/remote/rpc/gui/kernel/vault/tui/terminal.
  3. Reconcile `NexusError`, TUI API divergence.
  4. Bring in `sheshaos-protocols` (ACP+MCP wire impls) + CLI/worker bins.
  5. Fix upstream breaks: `russh`, `zig`.
  6. Gate: `cargo test --workspace` green on stable.
- Shesh ecosystem continues with SheshAOS Rust + Python `shesh-audit` bridge (`NexusBridge` emits EventKind JSONL).

## Consequences
- ✅ No broken main — honest audit over fake green.
- ✅ Clear path for future merge without blocking Python body.
- ✅ `SheshAOS` remains source of truth (Rust workspace).
- ❌ `shesh-brain` (packaged kernel for desktop) remains ⬜ todo until merge done.
- ❌ Two Rust histories to maintain until merge.

## Links
- `SheshAOS/KERNEL_MERGE_PLAN.md` (in SheshAOS repo)
- `docs/AUDIT_AND_ROADMAP.md` §3.1
- TODO.md §1
