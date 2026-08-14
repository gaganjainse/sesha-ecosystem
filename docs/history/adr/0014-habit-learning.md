# ADR-0014: Habit Learning is Frequentist with Decay, Not Opaque Weights

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** learning, habits, interpretability

## Context
We want system to learn habits/intentions/mannerisms from observed behavior ("learns my habits"). Options:
- Opaque neural weights — not inspectable, not reversible, needs training data.
- Frequentist counting with decay — inspectable, reversible, simple.

User is technical, wants inspectable/reversible, not black-box.

## Decision
- **Habits** are learned via frequency + corroboration + decay in `shesh-memory`:
  - Event: "User runs `check_system_updates` after boot 5 days in a row at 9am".
  - Counter increments; if corroborated (3+ times), promoted to candidate habit in `habits.md`.
  - Decay: if not seen for 30 days, weight decays, eventually archived.
  - User reviews candidate habits via `/refine` or settings GUI — not auto-applied as "always allow".
- **Intentions** are explicit: "You told me to remind about backup daily" → `intentions.md`, not inferred.
- **Mannerisms** are style snippets collected from user's edits/approvals, ranked by frequency.
- All stored as Markdown — human-readable, git-tracked, rollback possible.

No embedding-only learning; no opaque vector.

## Consequences
- ✅ Inspectable — `cat ~/.local/share/shesh/memory/habits.md`.
- ✅ Reversible — delete line or rollback via harness.
- ✅ Decay prevents stale habits.
- ❌ Less expressive than neural — but sufficient for desktop habits.
- ❌ Needs corroboration threshold tuning (currently 3 occurrences).

## Links
- `docs/LEARNING.md`, `shesh-memory/src/habits.py`
- D13
