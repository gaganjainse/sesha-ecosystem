# ADR-0012: Warm Proactivity at Natural Pauses

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** ambient, ux, proactivity

## Context
Previous assistant was binary: passive (never helps) or interrupting (breaks flow during work). User ask: "Be active/helpful/warm, not passive." But nagging is worse than silence — notification fatigue.

We need helpfulness without annoyance: one optional, context-aware offer when user naturally pauses, with data behind it.

## Decision
Proactivity engine in `shesh-ambient`:

- **Trigger**: natural pause = 45s–15m idle, NOT while typing, fullscreen, gaming, call, high-CPU, low-battery.
- **Frequency**: ≤3 offers/day, 30-min cooldown, snoozeable.
- **Content**: one optional offer, grounded in real signals:
  - `check_system_updates` pending?
  - git repos dirty?
  - backup age > 24h?
  - inbox count?
  - "You have 3 unsynced notes" etc.
  - Not static strings.
- **Presentation**: Quickshell overlay, dismiss with Esc, "don't ask today" option.
- **Warmth**: mannerisms from `shesh-memory` (user's preferred tone) injected via ContextAssembler.

Data-aware signals wired in `signals.py` + `offer_for_moment()`.

## Consequences
- ✅ Helpful without nagging — max 3/day.
- ✅ Offers are actionable (real Inbox, real git status).
- ✅ Snooze + cooldown respects user.
- ❌ Need real data probes — `signals.py` must not be expensive (use cache).
- ❌ GUI hookup needed — ambient service → Quickshell overlay (wiring todo).

## Links
- `docs/desktop/AMBIENT_DESIGN.md`
- `shesh-desktop/tools/shesh-ambient/signals.py`
