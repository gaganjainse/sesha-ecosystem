# ADR-0015: Every Tool Call Passes Through shesh-audit Guard

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** governance, security, audit, policy

## Context
Agent can propose destructive actions: `rm`, write to `.ssh`, MUX switch, package `-Syu`, ADB tap outside safe area. We need governance that cannot be bypassed by a component forgetting to check.

SheshAOS is the Rust governance kernel (append-only event store, policy engine). But Python MCP servers are where tools execute.

We need a single choke point: every tool call checked, logged, emitted in SheshAOS format.

## Decision
- **`shesh-audit`** provides:
  - `AuditLog`: hash-chained append-only log (`events.jsonl`) + `verify_integrity()` that detects tampering.
  - `Policy`: allow/confirm/deny rules — read-only tools allow, protected paths deny, everything else confirm. Runtime-extensible (first match wins).
  - `Guard`: `check(actor, tool, args) -> Decision` + logs decision.
  - `GuardedMCP(FastMCP)`: middleware that policy-checks every MCP tool call before execution, denies protected paths, logs decision + result, emits Nexus-format event via `NexusBridge`.
  - `NexusBridge`: writes `nexus-events.jsonl` in SheshAOS EventKind format — Rust kernel can later consume.
- All Python components import `GuardedMCP`:
  ```python
  try:
      from shesh_audit.guard import GuardedMCP
  except ImportError:
      from mcp.server.fastmcp import FastMCP as GuardedMCP  # graceful fallback
  ```
- Protected paths: `~/.ssh`, `~/.gnupg`, `Vaults/`, `~/Documents/Job`, job folders, etc. — denied regardless of confirmation.

MCP entry point `shesh-*-mcp` auto-wraps.

## Consequences
- ✅ No tool bypasses governance — middleware enforced at server boundary.
- ✅ Audit trail: every decision + result + hash chain.
- ✅ Nexus bridge: Python→Rust event flow (`nexus-events.jsonl`).
- ✅ Fallback to plain FastMCP if audit not installed (dev).
- ❌ Policy must be kept fast — checked on every call (currently in-memory, <1ms).
- ❌ Confirm UX needs GUI/voice wiring — currently returns confirm status.

## Links
- `docs/components/shesh-audit.md`, `policies/SKILLS_POLICY.md`
- `shesh-audit` (20 tests), `shesh-audit/src/guard.py`
- D6, D5, D1 (Rust kernel)
