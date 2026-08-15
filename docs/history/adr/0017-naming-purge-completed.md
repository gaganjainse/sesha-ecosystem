# ADR-0017: Naming Purge Completed — No Grandfathering

**Date:** 2026-08-12
**Status:** Accepted (completes ADR-0001's naming policy)

## Context

ADR-0001/§Naming made **Shesh** / `shesh-*` / `shesh_*` the only spelling and
banned reintroducing "Shesh". In practice, 8 component packages plus desktop-layer
scripts kept the banned spelling in distribution names, import packages, runtime
data dirs, env vars, QML config namespaces and prose. The owner ruled on
2026-08-12: **no grandfathering — purge everywhere, breakage accepted.**

## Executed rename (verified with tests, same-day)

| Repo | Change surface | Tests | Commit |
|---|---|---|---|
| shesh-audit | dist/import `shesh_audit`→`shesh_audit`; data dir migration | 20/20 | 7bab045 |
| shesh-backup | + `~/.local/state/shesh→shesh` migration | 8/8 | b5e00ee |
| shesh-files | + env `SHESH_*`→`SHESH_*` | 5/5 | 1bf458f |
| shesh-mcp-bundle | dist/import | 4/4 | 56550a2 |
| shesh-phone | dist/import | 7/7 | 6a9cdd539bfec22a925cab654fb96b831c3feba5 |
| shesh-shell | dist/import | 3/3 | 7c46a00 |
| shesh-skills | dist/import | 10/10 | e3de7a7 |
| shesh-system | dist/import | 13/13 | 303f245 |
| shesh-desktop | tools/, sdata/, profiles/, QML namespace `options.shesh→shesh`, wake word "Hey Shesh", docs/ | 26/26 | …3b025778aaed6ee6336eb50546b0f04577b2b21e |

Data-dir migrations are one-shot auto-rename-on-first-run (not grandfathering:
the legacy name ceases to exist). Cross-repo consumers (e.g. shesh-media's
`from shesh_audit.guard import GuardedMCP`) now resolve the canonical name.

## Exception register (deliberate, documented — not drift)

1. **Forks tracking upstream keep upstream internals**: `shesh-voice` (Newelle)
   keeps `newelle` module layout; `shesh-desktop` keeps upstream dotfile dirs.
   Renaming fork internals would destroy upstream diffability.
2. **Historical references** to `shesha-kernel` (the archived repo's real name)
   remain as-is in ADRs/handoff docs.
3. **Rust crate prefix `sheshaaos-*`** (inside SheshAOS) — normalize when Rust
   work resumes; unverifiable in a cargo-less lane today.

## Consequences

- ✅ One spelling everywhere a user/agent looks: `shesh`.
- ✅ Future greps, tooling, and agent prompts have zero ambiguity.
- ❌ Local checkouts/installs from before 2026-08-12 must re-clone or run the
  rename tooling; entry-point names changed (`shesh-audit-mcp`→`shesh-audit-mcp`).

## Erratum (2026-08-15): no-op arrows in the table above

The "Executed rename" table was authored **after** the purge completed, so the
left-hand side of several `→` arrows shows the already-canonical name and the
arrows read as no-ops. The actual pre-purge spelling on the left was the banned
`sesha` form. For clarity:

| Row | Actual change (pre-purge → post-purge) |
|---|---|
| shesh-audit | import package `sesha_audit` → `shesh_audit`; data dir `~/.local/state/sesha` → `…/shesh` |
| shesh-backup | data dir `~/.local/state/sesha` → `~/.local/state/shesh` |
| shesh-files | env prefix `SESHA_*` → `SHESH_*` |
| shesh-desktop | QML namespace `options.sesha` → `options.shesh` |
| entry points | console scripts `sesha-audit-mcp` → `shesh-audit-mcp` (and siblings) |

This record is immutable; the erratum is appended rather than editing the
original rows.
