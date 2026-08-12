# Janitor TODO Policy — append-and-attest only (Decision D4)

**Decision:** D4-A (the MUST option). The janitor / swarm agents may only
*grow* the TODO ledger or *attest* completions. They may never clear it.

## Rules

1. **Add freely.** Janitor runs may append new findings as ⬜ items with the
   discovering commit/run reference.
2. **Flip ⬜ → ✅ only with evidence in the same commit.** The flip commit
   message must name the PR or commit that proves the work (e.g. `done by
   c85ea43`). A bare flip without a pointer is reverted by review.
3. **Never delete, never "clear".** No janitor run may remove items, rewrite
   sections, or downscope wording. Ambiguity is an oracle question, not an
   edit permission.
4. **Stale items** stay in the ledger until an orchestrator session moves
   them under an `## Archive` heading with an explicit `archive:`-prefixed
   commit message explaining why each item is obsoleted.
5. **Auditable.** Every TODO.md mutation by an automated agent carries its
   run URL in the commit trailer (`Swarm-Run: …`), enforced by review, so
   the ledger's history is reconstructable end to end.

## Why not seed-and-clear

A janitor that both seeds and clears controls the *denominator* of done.
Completion numbers become unfalsifiable, and silently dropped items are
exactly the silent-failure class `tools/silent_failures.py` exists to gate
(SF1–SF4). Attest-only keeps the ledger monotone and every ✅ provable.

*Orchestrated ac 2026-08-13 (Decision D4, user-chosen MUST option).*
