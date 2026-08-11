#!/usr/bin/env bash
# supervise.sh — autonomous work loop for an AI agent on Shesh.
#
# Usage:
#   scripts/supervise.sh            # one tick (pick next todo, implement, commit)
#   scripts/supervise.sh --loop     # repeat until no actionable todos
#   scripts/supervise.sh --dry-run  # show what it would do, change nothing
#
# It does NOT replace the agent's judgment: it enforces the workflow from
# TODO.md — pick the next unblocked item, work on a branch, test, document,
# commit, and update TODO + QUERYLOG. Safety: never force-push, never delete
# repos, stop on test failure.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LOOP=0; DRY=0
for arg in "$@"; do case "$arg" in
  --loop) LOOP=1 ;; --dry-run) DRY=1 ;; esac done

log(){ printf '\033[36m[supervise]\033[0m %s\n' "$*"; }

next_todo() {
  # Print the first ⬜ line in TODO.md that isn't under a 🔴 heading.
  awk '
    /🔴/{block=1} /^## /&&!/🔴/{block=0}
    /⬜/ && !block {print; exit}
  ' TODO.md
}

run() {
  if [ "$DRY" = 1 ]; then echo "DRY: $*"; else "$@"; fi
}

tick() {
  # --- Session guard check FIRST ---
  if [ -f tools/session_guard.py ]; then
    python3 tools/session_guard.py --tick || true
    if [ -f docs/SESSION_HOP_ALERT.md ]; then
      log "🚨 SESSION HOP ALERT exists — recommend handoff before new task"
      cat docs/SESSION_HOP_ALERT.md | head -n 20
      # Don't start new big task if hop needed — finish and exit
      if grep -q "HOP RECOMMENDED" docs/SESSION_HOP_ALERT.md 2>/dev/null; then
        log "Hop needed — not starting new task, generating handoff"
        python3 tools/session_guard.py --handoff || true
        return 1
      fi
    fi
  fi

  local item
  item="$(next_todo || true)"
  if [ -z "$item" ]; then
    log "No actionable todos found."
    return 1
  fi
  log "Next: $item"
  local branch
  branch="feat/auto-$(date +%s)"
  run git checkout -b "$branch" 2>/dev/null || run git checkout "$branch"

  # The actual implementation is done by the agent (human or LLM) invoking this
  # script as part of its tool loop. This script enforces the gates AFTER work:
  if [ "$DRY" = 0 ]; then
    log "Running gates..."
    if [ -d tests ]; then python3 -m pytest tests/ -q || { echo "tests failed"; return 2; }; fi
    python3 -m ruff check scripts/ tests/ 2>/dev/null || true
  fi

  # Append to query log (agent fills in the answer).
  local today; today="$(date -u +%Y-%m-%d)"
  if [ "$DRY" = 0 ]; then
    cat >> docs/queries/QUERYLOG.md <<EOF

---

## Autopilot tick ($today)

Worked on: ${item}
(Branch: $branch — fill in outcome + doc links.)
EOF
  fi

  log "Commit + update TODO status for: $item"
  run git add -A
  run git commit -q -m "wip: ${item//✅/}" || true
  log "Tick complete on branch $branch. Push when ready."
}

if [ "$LOOP" = 1 ]; then
  while tick; do sleep 1; done
else
  tick
fi
