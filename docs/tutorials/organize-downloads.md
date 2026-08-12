# Tutorial — organize Downloads with Smart Organizer v2

Status: living · last verified 2026-08-13
Full reference: [05_SMART_ORGANIZER_V2](https://github.com/gaganjainse/shesh-desktop/blob/main/docs/SHESH/05_SMART_ORGANIZER_V2.md)
in shesh-desktop.

The organizer turns `~/Downloads` from a pile into routed folders. Pipeline:
Rust watcher (notices new files) → Python classifier (decides destination) →
Bash apply layer (**the only mover** — the layers that decide never move
files themselves).

## Walkthrough

1. **Dry-run first.** Classification output shows the proposed destination
   per file with the rule that fired. Nothing moves until the apply layer
   confirms.
2. **Override with the rules file.** The user-editable rules file beats every
   heuristic — your rule always wins over the classifier.
3. **Go continuous.** Enable the systemd units (canonical unit files ship in
   the repo — no here-doc installs) to watch Downloads around the clock.

## Verify it works

- [ ] Drop a known-type file (e.g. a `.pdf`) into Downloads and see it land
      in the expected folder within seconds.
- [ ] Edit the rules file with an obvious override; confirm it preempts the
      classifier on the next matching file.
- [ ] Check the apply layer logged each move (moves without log lines are a
      bug — report them).

This corresponds to [MANUAL_VERIFICATION §5](../MANUAL_VERIFICATION.md)
(desktop section) on the hardware checklist.
