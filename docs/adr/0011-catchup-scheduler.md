# ADR-0011: Catch-Up Scheduler, Not Fixed Cron Timers

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** scheduling, laptop, ambient

## Context
Laptop sleeps, shuts down, runs on battery. Fixed wall-clock timers (`02:00 daily`) misfire: job runs at boot mid-work, or misses backup window entirely. User complaint: "You assume 24/7 live; it isn't. Don't boot mid-work."

We need scheduling that respects laptop lifecycle, power, and user attention.

## Decision
Adopt **catch-up scheduler** (systemd timer with `OnStartupSec` + `OnCalendar` + jitter):

- `shesh-ambient` in `shesh-desktop` defines:
  - `OnStartupSec=5m` + `RandomizedDelaySec=2h` — jobs run soon after boot, not during boot storm.
  - Heavy jobs (backup, maintenance) need `ConditionACPower=true` + `idle` gate (no fullscreen/call/high-CPU).
  - Budget bounds: max runtime, CPU quota `IOSchedulingClass=idle`.
  - Courtesy policy: defer if fullscreen/game/call/low battery.
- Daily backup timer: `daily` + `Persistent=true` — if missed, runs at next boot.
- Proactive offers (ambient) not timer-driven: at natural pauses (45s–15m idle), throttled ≤3/day.

Not cron, not systemd `OnCalendar` alone.

## Consequences
- ✅ Laptop-friendly — no mid-work boot storm.
- ✅ Missed jobs eventually run (catch-up).
- ✅ AC + idle gating prevents battery drain.
- ❌ More complex than cron — need systemd user timers + ambient scheduler logic.
- ❌ Jitter makes exact timing non-deterministic — documented.

## Links
- `docs/desktop/AMBIENT_DESIGN.md`, `docs/desktop/07_AUTOMATIONS.md`
- `shesh-desktop/tools/shesh-ambient/`
