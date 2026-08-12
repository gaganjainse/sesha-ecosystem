# Incident post-mortem — 2026-08-11: five-tab swarm collision

**Status:** mitigated same-day; controls landed in PRs #37, #38, #39, #40.

## What happened

Five parallel agent tabs (orchestrator + brain/mind/soma/platform workers) plus
GitHub Actions drove one swarm bus for a day. Net effect: real bugs got found and
fixed, but also: duplicate/noise issues seeded (#19–34), placeholder "work" PRs
merged to main (5 commits: marker files from a stub `do_work`), claim/PR closure
cross-talk via the shared issue/PR number space, and a PAT exposed in a transcript.

## Root causes (each now has a control)

1. **Worker placebo** — `do_work()` marker-filed every claim and auto-merge
   closed real issues. → Workers now fail closed without `--executor` and release
   claims (`release_issue_claim`) — #39.
2. **Loose TODO seeder** — any line containing ⬜/🟡 became an issue. → Strict
   bullet parser + blocked-ancestor inheritance — #38.
3. **Shared working tree with daemon commits** — heartbeat commits raced manual
   rebases. → daemons isolated to their own clone via `tools/swarm/daemon.sh`;
   orchestrator refuses swarm commits off-main — #40.
4. **Gate gaps** — ruff didn't cover `tools/` locally (29 pre-existing errors);
   workflow used forbidden `gh pr review --approve`. → fixed on main same day
   (68a0df5, 17ef93c); local `make check` and CI now match.
5. **Session guard self-nuke** — `--status` past 60 min deleted the plain PAT
   under running daemons. → read-only status; explicit `--handoff` only — #40.
6. **Credential hygiene** — PAT visible in a tool transcript. → rotation task
   opened (owner action), askpass-style auth in workers — #39.

## What was good

- Atomic claim refs, auto-merge gate, heartbeat bus and hop protocol all behaved
  under multi-agent load once the above were fixed. The incident was the best
  stress test the system has had; findings became code the same day.

## Residue

- 5 placeholder commits remain in main's history (no force-push, by policy).
  They are harmless inert markers under `swarm/artifacts/` — content removed in
  d9dc459; this note is the institutional memory.
