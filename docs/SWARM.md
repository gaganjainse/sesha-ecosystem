# SWARM — Multi-Session Parallel Work via GitHub as Bus

> **TL;DR:** Open 1 orchestrator chat + 2-3 worker chats in Arena.ai. They coordinate ONLY through GitHub (`swarm/` folder) using atomic `git push` for locking. No direct chat-to-chat connection, no overwriting, no manual maintenance beyond opening chats.

## Why we need it

- **Single session slowdown:** Arena workspace snapshot 128 MB / 10k files — shesh-ecosystem with 22 cloned repos hits ~60-100 MB quickly, tool calls get slow after 60 min, context overflows. You've experienced needing to change sessions.
- **Big project:** 19 components, 40 docs, 238 tests — one session can't finish TODO in time, but serial hopping loses flow.
- **Solution:** Parallel sessions, each working on different component, coordinated via GitHub.

## Architecture

### GitHub as command center

We repurpose `shesh-ecosystem` repo itself (could also be dedicated `shesh-swarm` repo) as message bus:

```
swarm/
  queue/       → tasks from TODO.md ⬜
  claims/      → who owns which task (atomic push)
  heartbeats/  → agent alive
  artifacts/   → done/failed result
  ledger.jsonl → append-only event log
```

This is **the only connection** between Arena chats — no WebSocket, no shared memory.

### Claim protocol (no overwrite)

```python
# worker.py try_claim()
1. git pull --rebase origin main
2. check if swarm/claims/<task>.json exists → if yes, abort
3. create swarm/claims/<task>.json {task_id, my_agent_id}
4. git add + commit + push origin main
5. if push fails (remote changed) → pull --rebase, check again — if file now exists with other agent_id, we lost race, abort. Retry next task.
6. if push succeeds → we own task
```

GitHub push is atomic — first writer wins. Second gets `! [rejected] main -> main (fetch first)` and must rebase, seeing other's claim.

### Branch per task (no crash)

Worker does:

```bash
git checkout -b swarm/<agent-id>/<task-id>
# edit src/shesh-memory/ or docs/ etc
make check   # gate — ruff + pytest + license + locks
# if green
git add -A && git commit -m "feat(shesh-memory): implement ..."
git push origin swarm/<agent-id>/<task-id>
# then merge to main via:
git checkout main && git merge --no-ff swarm/<agent-id>/<task-id> && git push
# and write artifact + mark queue task done
```

If two workers edit same file, merge conflict → second worker's `git pull --rebase` fails, must resolve manually — no silent overwrite.

### Orchestrator vs workers

- **Orchestrator** (`tools/swarm/orchestrator.py`): seeds queue from `TODO.md` ⬜, monitors heartbeats, re-queues stale claims (>10 min no heartbeat), dashboard, updates TODO when artifacts done.
- **Worker** (`tools/swarm/worker.py --component X`): polls queue, filters by component, claims, works, pushes.

You open **one orchestrator chat** + **N worker chats** (N=2-3 recommended). You don't maintain them beyond opening tabs — they auto-poll GitHub every 45-60s.

## Is it actionable? Honest assessment

| Question | Answer |
|----------|--------|
| Can Arena Agent Mode chats talk directly? | **No** — isolated sandboxes, no shared memory, no API to spawn another Agent Mode. GitHub is only bus. |
| Can we avoid overwriting? | **Yes** — branch per task + atomic claim push + gate before merge. If workers touch different components (shesh-memory vs shesh-system), zero conflict. If same file `manifests/components.toml`, last merge wins but git conflict forces manual rebase, not silent loss. |
| Do I need to maintain workers? | **Minimal** — you open 2-3 tabs, paste worker prompt (from `docs/NEXT_SESSION_PROMPT.md` + `--component X`), leave them. They heartbeat to `swarm/heartbeats/`. If you close tab, orchestrator detects stale claim after 10 min and re-queues. |
| Can one chat be orchestrator? | **Yes** — orchestrator is just another Arena chat running `orchestrator.py --monitor`. It doesn't control workers, only watches GitHub and seeds tasks. Workers don't need orchestrator to keep working (they poll queue). |
| Does everything work through GitHub repo as workspace? | **Yes** — that's the design. Workspace is ephemeral, GitHub is persistent. Every change pushed to `main`. Next session `git pull` recovers everything. `src/` clones are gitignored locally but their READMEs synced to `docs/components/` which IS committed. |
| Limitations? | 1. No real-time — poll 45s delay. 2. PAT needed for push — must set `GITHUB_PAT` or `~/.config/shesh/github.pat` 0600. 3. Arena kills background `start_process` when tab closed — worker loop stops, but claim remains until orchestrator re-queues. 4. Too many workers (>4) increases git push conflicts. 5. Can't auto-scale workers — you manually open tabs. |

**Verdict:** Actionable for 2-4 parallel sessions with component partitioning. Not a true Kubernetes, but best possible given Arena constraints.

## How to start swarm (copy-paste)

### Prerequisites (once)

```bash
# PAT for push — choose one, secure
echo "ghp_..." > ~/.config/shesh/github.pat
chmod 600 ~/.config/shesh/github.pat
# or
export GITHUB_PAT=ghp_...
# or
gh auth login

# Ensure git
git config --global user.name "Gagan Jain"
git config --global user.email "gagan.jain.se@gmail.com"
```

### Orchestrator (tab 1)

```
Read docs/SESSION_HANDOFF.md FIRST, then docs/SWARM.md

You are orchestrator for shesh-ecosystem, GitHub gaganjainse/shesh-ecosystem
PAT in GITHUB_PAT env or ~/.config/shesh/github.pat

cd /home/user && git pull origin main && python tools/session_guard.py --status
python tools/swarm/orchestrator.py --seed TODO.md --dashboard
python tools/swarm/orchestrator.py --monitor
```

Leave open.

### Worker memory (tab 2)

```
Read docs/SESSION_HANDOFF.md FIRST, then docs/SWARM.md

You are worker for shesh-memory, GitHub gaganjainse/shesh-ecosystem
PAT same

cd /home/user && git pull && python tools/swarm/worker.py --component shesh-memory --poll 45
```

### Worker system (tab 3)

```
... worker for shesh-system
python tools/swarm/worker.py --component shesh-system
```

## Session hopping WITH swarm

Swarm + session protocol combine:

1. Each worker runs `session_guard.py --tick` before task — if hop needed, finishes task, pushes, and exits
2. You close that worker tab, open new one, paste worker prompt again — it pulls and continues from queue, no overlap because claim already completed and artifact exists
3. Orchestrator also hops via same protocol — new orchestrator tab picks up ledger

No central server to maintain.

## Files

- `tools/swarm/common.py` — gen_agent_id, list_tasks, try_claim, heartbeat, complete_task
- `tools/swarm/orchestrator.py` — seed TODO → queue, dashboard, monitor stale claims
- `tools/swarm/worker.py` — poll, claim, do_work (calls autopilot runner when available), gate, push artifact
- `tools/github_auth.py` — secure PAT loader (env > file 0600 > gh hosts.yml, refuses world-readable)
- `tools/session_guard.py` — hop detection + NEXT_SESSION_PROMPT generation
- `swarm/` — queue, claims, heartbeats, artifacts, ledger.jsonl
- `docs/SESSION_PROTOCOL.md` — 60-sec handoff
- `docs/NEXT_SESSION_PROMPT.md` — auto-generated paste for next session

## Security

- PAT never logged, never committed — `github_auth.py` redacts `ghp_****`
- `github.pat` must be 0600, else tool refuses
- No token in `swarm/` files — only agent_id
- Provenance via `scripts/sign_artifacts.py` — SHA256 + SLSA, optional sigstore cosign keyless

## Next improvements

- Switch from file queue to GitHub Issues + labels `component:shesh-memory`, `P0` — better atomicity via API, but needs `gh` or PAT with issues write
- Auto PR creation per task + GitHub Action auto-merge after `make check` green
- Use `gh` Projects board for dashboard instead of `dashboard()` print
- Dedicated `shesh-swarm` repo as pure bus (currently we reuse shesh-ecosystem to avoid new repo)
