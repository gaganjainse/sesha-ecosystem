# Dependency Policy — rolling with the river, never drowning in it

CachyOS (our OS) is rolling-release. Packages we depend on move under us
weekly. Policy: **design for motion** — stay near latest in a controlled way,
with gates that catch breakage early and a written protocol for when they do.

## The rules

1. **Near-latest by default.** Python deps pin minimums + a curated ceiling
   (`fastmcp>=3.4.7,<4`); ceilings lift deliberately, not accidentally.
2. **Automation moves versions, humans approve.** Dependabot (pip +
   github-actions, weekly, grouped) opens the PRs; CI gates answer "is it
   safe"; a human/session merges. Pins without a mover = rot; movers without
   gates = roulette. We have both.
3. **Conflict protocol (user-specified):** a new release breaks us → land the
   rest, hold the offender back ONE version with a dated comment naming the
   failure. Still broken next cycle → hold again, max twice. Fundamental
   break (upstream removed the behavior) → **replace the dependency**;
   never indefinite pinning, never impulsive forking. All three outcomes are
   recorded in TODO.md as they happen.
4. **Deprecation watch:** no dependency on a project archived upstream (gap
   check quarterly), no Python/Rust stdlib-deprecated APIs (pytest `-W error`
   and clippy enforce continuously — warnings are CI failures here).
5. **New dependencies are a decision, not an accident:** check SOURCES.md /
   steal-first rule first; record in manifests/components.toml for ecosystem
   components; license must be declared (scripts/check_licenses.py gates).
6. **Rust:** `cargo update` is a deliberate act run at the quarterly review
   with the full gate chain (deny, machete, clippy -D warnings, tests);
   Cargo.lock is committed so runners and machines agree.

## Rolling-resilience design (what "resistant, not break" means concretely)

- **canary.yml + scheduled full-matrix CI** = early warning: upstream drift
  breaks the canary first, not the user.
- **Tests warnings-as-errors fleet-wide** (`pytest -W error`): deprecation
  warnings are tomorrow's breakage, caught at deprecation time.
- **The desktop never hard-depends on a specific glibc/pacman behavior**:
  components probe (`shutil.which`, capability flags) and fail *loudly and
  honestly* rather than fabricate (SF-audited).
- **shesh-backup + RECOVERY.md**: pre-upgrade snapshots are the rollback; the
  runbook is the restore. `tools/dr_check.sh` verifies readiness.
- **Kernel/driver moves (CachyOS + NVIDIA class):** vendor quirks stay behind
  the shesh-system capability layer, so a kernel change degrades one tool
  honestly instead of crashing a stack.

## Better-alternative reviews

Quarterly review asks per dependency: is there a maintained, license-clean,
measurably better alternative we should steal? Adoptions recorded as ADRs.
The bar for switching: maintained momentum, real gain, migration cost < gain
within a month of engineering time.
