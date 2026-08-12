# SESSION HANDOFF — Shesh ecosystem

**Generated:** 2026-08-12 (live update via tools/live_update.py)
**Purpose:** Load this at the start of a new session to continue exactly
where this one stopped, without re-deriving context.

> Read this file FIRST, then `docs/AUDIT_AND_ROADMAP.md`, `TODO.md`,
> `docs/MANUAL_VERIFICATION.md`, `docs/SESSION_PROTOCOL.md`, `docs/SWARM.md`.
> The query log at `docs/queries/QUERYLOG.md` has the full decision trail.
> For next session copy-paste, read `docs/NEXT_SESSION_PROMPT.md` — it contains everything needed without re-explaining.

**NEW:** Session hopping + swarm parallelization added this session — see §11 and §12 below.
Copy `docs/NEXT_SESSION_PROMPT.md` into new Arena chat to continue — it includes GitHub profile, all repos, PAT instructions, commands.


---

## 1. What this is

**Shesh** is a local-first AI agent OS for Linux (target: CachyOS on an MSI
Sword 16 HX). It is a federation of small MCP components governed by a
policy/audit layer, with a Newelle-based voice frontend and a Rust
governance kernel (SheshAOS, in progress).

- **Naming (FINAL):** the product is **Shesh**, the kernel is **SheshAOS**.
  All repos/packages/imports are `shesh-*` / `shesh_*`. "Shesh" was the
  previous spelling and must not be reintroduced (except in the archived
  kernel repo `shesh-kernel`, which GitHub redirects).

## 2. Repositories (all under github.com/gaganjainse)

| Repo | Layer | Tests | Purpose |
|------|-------|------:|---------|
| SheshAOS | Brain | 981 (Rust) | Governance kernel (12 crates) — merge pending |
| shesh-ecosystem | — | 30 (Python) | Manifest, gates, docs, **autopilot**, this wiki source |
| shesh-audit | Brain | 20 | Hash-chained event log, GuardedMCP, Nexus bridge, secrets |
| shesh-secrets | Brain | 8 | env/gopass/keepassxc/file secret resolution |
| shesh-orchestrator | Mind | 28 | Multi-agent RLM runtime, sessions, A2A, traces |
| shesh-memory | Mind | 26 | Episodes, FTS, vector embeddings, habits, intentions, compaction |
| shesh-mind | Mind | 13 | Role-to-model router (6 GB VRAM budget) |
| shesh-harness | Mind | 14 | Self-improvement with held-out `/refine` evaluator |
| shesh-skills | Mind | 10 | Everyday tools + Markdown skills |
| shesh-calendar | Mind | 6 | iCalendar vdir reader |
| shesh-voice | Soma | — | Newelle fork + MCP overlay (wake word/STT/TTS) |
| shesh-desktop | Soma | 26 | CachyOS/Hyprland dotfiles, ambient offers |
| shesh-files | Soma | 5 | Rust watcher + classifier |
| shesh-shell | Soma | 3 | Hyprland/Quickshell MCP |
| shesh-system | Soma | 13 | Power/GPU/MUX, updates, health, maintenance |
| shesh-backup | Soma | 8 | Restic wrapper, AC-gated |
| shesh-phone | Soma | 7 | ADB control for Realme Narzo |
| shesh-containers | Soma | 5 | Podman/distrobox sandboxed exec |
| shesh-mcp-bundle | Soma | 4 | filesystem/fetch/git proxied through Guard |
| shesh-acp | Soma | 12 | Agent Client Protocol (editor integration) |

**Component tests: 182 · Ecosystem tests: 30 · Desktop ambient: 26
= 238 total, all green.**

## 3. Where the code lives on disk

- Components: `/home/user/sesha/components/shesh-*/`
- Ecosystem: `/home/user/sesha/shesh-ecosystem/` (also cloned into
  `shesh-ecosystem` under components in some checkouts — use the
  `shesh-ecosystem` repo at the workspace root)
- Each component: `pyproject.toml`, `src/shesh_<name>/`, `tests/`,
  `.github/workflows/ci.yml`, `.gitignore`
- MCP entry points are `shesh-<name>-mcp` console scripts

## 4. The autopilot (built this session — use it)

`tools/autopilot/` in shesh-ecosystem is the foolproof self-running system:

- **safety.py** — hard invariants: no red commits, no force-push, protected
  paths, rollback on failure, canonical remote check.
- **ledger.py** — durable JSONL task journal at
  `~/.local/share/shesh/autopilot/ledger.jsonl`; resumes after interruption.
- **gate.py** — runs `ruff` + `pytest` in isolation (`--confcutdir`,
  `-o addopts=`) before commit.
- **runner.py** — `process_task`: implement → gate → safe_commit → safe_push,
  with one retry + soft rollback; never pushes red.
- **cli.py** — `python -m tools.autopilot.cli {list,seed,run}`.

Before building any feature, **run the autopilot tests**:
`cd shesh-ecosystem && python3 -m pytest tests/autopilot -q`.

## 5. How to build safely (the contract) — UPDATED 2026-08-11: steal first, proper versions, no time limit

1. Pick the next pending item from `TODO.md` (or seed it:
   `python -m tools.autopilot.cli seed`).
2. **First thought = STEAL, not make tool.** Check SOURCES.md, TOOLING_CATALOG.md, manifests/upstreams.toml, awesome-hyprland, best MCP servers 2026, Rust crates (notify-rs, aya-rs). Search web for open-source things (MIT/Apache/GPL, truly free, no API key, self-hostable). If something better exists that can be stolen, upgraded, customized, specialized for our CachyOS/Hyprland/6GB VRAM system and improved — STEAL IT. Only if not found, then make yourself. What have we been learning then? Steal first. We can discard what we made if something better exists to steal. Never engage in pointless brooding.
3. Work in one component. Keep changes small and focused, but **DON'T make minimal versions/stubs that become dead code — make proper working versions** with real implementation, tests, integration, docs. We have a lot of time, freely, no limited time constraint. Who posted limited time constraint? We have a lot of time.
4. **Always** run tests in that component:
   `cd components/shesh-<x> && python3 -m pytest tests/ -q`.
5. Use `GuardedMCP` from shesh-audit for any new MCP server (auto policy +
   audit log + Nexus events).
6. Never store secrets in config — use `shesh-secrets` references
   (`env:`, `gopass:`, `file:0600`).
7. Commit with the task id in the message; push through the autopilot
   safety guards.
8. After each user message, append to `docs/queries/QUERYLOG.md` and update
   `TODO.md` statuses.
9. Archive, don't delete. No force-push to main. No root.
10. Mark hardware-only items 🟡 rather than faking success.
11. **Upgrade wrapper, not just fork and wrap:** Customize and specialize for our system and improve it — e.g., Newelle fork stripped GNOME, added Quickshell overlay, prewired MCP, 6GB-safe models, renamed Shesh (Newelle core).
12. **Integrating various systems, no conflict — cautious but enterprising:** namespace via MCP stdio, Guard, separate systemd services, separate config dirs, btrfs subvolumes, Python venvs via uv, one job per component, one process per MCP server.
13. **Style + Performance non-negotiable:** illogical-impulse look (end-4 shesh-desktop) + CachyOS performance, don't break systems, already using best customized dotfiles riced look, need good backend that integrates into look. Improve style, not change — if something better in other dotfiles (ML4W, JaKooLit, HyDE, Noctalia, Caelestia, DankMaterialShell, ekremx25, qs-hyprview, HyprPanel, rishot pill morphing), include it for functionalities, better response/animations, smooth buttery feel, better bluetooth wifi integration.

## 6. What is DONE

- ✅ All 19 repos renamed Shesh→Shesh (GitHub redirects old names)
- ✅ Governance: audit log, GuardedMCP, policy, Nexus event bridge, secrets
- ✅ Agents: orchestrator with roles, persistent sessions+cancel, A2A UDS,
  local JSONL traces, LLM planner/critic with Ollama + stubs
- ✅ Memory: episodic + FTS + vector embeddings (local hash + Ollama
  nomic-embed-text), habits/intentions/mannerisms, compaction/retention,
  semantic search MCP
- ✅ Self-improvement: held-out evaluator (must_contain/must_not_contain,
  structural checks), `refine_with_llm`
- ✅ Skills: notes/web/code/docs/reminders + 5 skills
- ✅ Calendar (iCal vdir), Containers (podman sandbox), MCP bundle
  (filesystem/fetch/git via Guard)
- ✅ System: power/GPU/MUX, restic backup, update check (read-only), health,
  maintenance/cache clean
- ✅ Phone (ADB safe-area), ACP (session/prompt/terminal/diff/cancel/perm)
- ✅ Desktop: ambient scheduler with data-aware signals, settings GUI
- ✅ Platform: manifest resolver, license gate, 3 channels, MCP config
  generator, **canary e2e covering all 16 components**, .gitignore everywhere
- ✅ Autopilot safety core (12 self-tests)
- ✅ Wiki: `docs/wiki/` (7 pages) synced to SheshAOS via
  `.github/workflows/wiki-sync.yml`
- ✅ Docs: AUDIT_AND_ROADMAP, GLOSSARY, MANUAL_VERIFICATION, TOOLING_CATALOG,
  this SESSION_HANDOFF, query log

## 7. What REMAINS (priority order)

### 🔴 Blocked (need deliberate/hardware work — do NOT auto-force)
- **shesh-kernel → SheshAOS merge.** The archived Rust kernel diverged at
  the type level. Follow `KERNEL_MERGE_PLAN.md` in SheshAOS: port leaf
  crates first (protocols, waveobj, wps, blockctl, wconfig), reconcile
  `NexusError`/TUI APIs, bring in `shesh-protocols` (ACP+MCP wire impls)
  and CLI/worker, fix upstream breaks (`russh::Error::msg` removed; `zig`
  required by terminal crate), gate on `cargo test --workspace` green.
- **Hardware validation on the physical MSI Sword 16 HX** — run through
  `docs/MANUAL_VERIFICATION.md` (display @144 Hz, NVIDIA/MUX, wake word,
  PipeWire, Quickshell render, backup restore, phone ADB, podman rootless,
  voice STT/TTS, Newelle MCP mesh).
- **Wiki one-time init** — create the first page at
  https://github.com/gaganjainse/SheshAOS/wikis so the wiki-sync Action can
  push. (GitHub has no API for this.)
- **Editor ACP testing** against real Zed/JetBrains (protocol implemented).

### 🟡 P1 (unblocked, build next)
- LLM-backed auto skill capture (Read→Execute→Reflect→Write) with deprecation
- Distrobox/Containerfile for one-command onboarding
- Installer channels with btrfs snapshot + rollback
- Local email (IMAP via vdirsyncer/neomutt); messaging bridges
  (Telegram/Signal, isolated)
- Media tools (screenshots, recording, wallpaper, audio routing)
- OTLP export of local traces
- `shesh-maint` standalone package (was started but left empty; either
  finish or fold into shesh-system — it currently duplicates
  shesh-system's maintenance tools; **decide and remove the empty dir**)
- Connect ambient signals into the live offer loop (signals.py +
  offer_for_moment exist; wire in the desktop service)
- Data-aware ambient proactivity already computes; needs GUI hookup

## 8. Known gotchas

- **Editable installs:** after any package rename, run
  `pip install -e .` in each component or imports resolve to stale names.
- **Pytest isolation:** when running a component's tests from the ecosystem
  repo, use `-p no:cacheprovider -o addopts= --confcutdir <repo>` (the gate
  does this) or parent conftest/ini pollutes results.
- **GitHub wiki** must be initialized once in the web UI before `.wiki.git`
  exists; the sync workflow skips gracefully until then.
- **GITHUB_TOKEN** cannot init a wiki; if wiki sync fails after the first
  page is created, set a `WIKI_PAT` repo secret with `repo` scope.
- **Ollama models** for the 6 GB stack: `phi4-mini`, `qwen2.5-coder:3b`,
  `moondream2`, `nomic-embed-text`.
- **Workspace budget:** do NOT install the Rust toolchain or large clones
  in the sandbox — CI has Rust. Keep `/home/user` under ~150 MB
  (clean `__pycache__`, `.egg-info`, `~/.cache`).
- The local workspace folder may be named `sesha` (typo); ignore — all
  remotes/packages are canonical `shesh-*`.

## 9. First commands for a fresh session

```bash
cd /home/user/sesha/shesh-ecosystem
export PATH="$HOME/.local/bin:$PATH"

# 1. Verify everything is green
for d in ../components/shesh-*/; do
  (cd "$d" && python3 -m pytest tests/ -q -p no:cacheprovider)
done
python3 -m pytest tests/ -q -p no:cacheprovider

# 2. Read the anchors
cat docs/SESSION_HANDOFF.md   # this file
$PAGER TODO.md docs/AUDIT_AND_ROADMAP.md docs/MANUAL_VERIFICATION.md

# 3. Continue with the next P1 from section 7
```

## 10. Design principles (don't violate these) — UPDATED 2026-08-11

- **Local-first / offline** — every tool degrades to deterministic stubs.
- **Governed** — every tool call passes the Guard; policy decides.
- **Federated** — one job per component; manifest integrates them.
- **Tested before push** — autopilot refuses red commits.
- **Small, reversible, audited** — commits, events, rollback.
- **No secrets in repos** — shesh-secrets only.
- **Shesh, not Shesh; SheshAOS, not SheshAOS.**
- **Steal first, make second** — first thought when challenged with an issue = steal from open-source (SOURCES.md, awesome-hyprland, best MCP servers 2026, Rust crates). Check if something better exists that can be stolen, upgraded, customized, specialized for our CachyOS/Hyprland/6GB VRAM system and improved. Only if not found, then make yourself. Never engage in pointless brooding — discard what we made if something better exists to steal.
- **Proper working versions, not minimal stubs** — don't make minimal versions that become dead code/stubs. Make proper working versions with real implementation, tests, integration, docs. We have a lot of time, freely, no limited time constraint.
- **Upgrade wrapper, not just fork and wrap** — customize and specialize for our system and improve it (e.g., Newelle → shesh-voice stripped GNOME, added Quickshell overlay, prewired MCP, 6GB-safe models).
- **Cautious but enterprising, no conflicts** — integrating various different systems (Hyprland + Quickshell + MCP + voice + eBPF + containers + phone ADB + OmniRoute), but no conflict between them via MCP stdio process boundaries (never in-process FFI), Guard allow/confirm/deny, separate systemd user services, separate config dirs, btrfs subvolumes, Python venvs via uv, one job per component, one process per MCP server, one policy gate.
- **Style + Performance non-negotiable** — illogical-impulse (end-4 dots-hyprland) look because love its look + CachyOS because love its performance, can't compromise, don't break systems. Already using best customized dotfiles riced look, not native Hyprland, need good backend and other systems that integrate into that look. Improve style, not change — if something better in other dotfiles, include it in our look for functionalities, better response/animations, smooth buttery feel, better bluetooth wifi integration. At end of day, it is also fork and wrapper so we should improve it, pick features/issues from every mainstream fork we are using and if useful extract and work on it. Build proper infrastructure for stealing/improving/customising so user doesn't have to write many times — manifests/upstreams.toml, tools/steal/, scripts/upstream_tracker.py, docs/STEAL_INFRASTRUCTURE.md, STYLE_PERFORMANCE.md

## 11. Session protocol — hot hopping (added 2026-08-11)

**Problem:** Arena.ai snapshots at ~128 MB / 10k files, slows after 60 min / many tool calls.
**Solution:** 60-sec handoff, zero loss.

- `tools/session_guard.py` monitors workspace size, file count, age, avg latency, uncommitted files. Logs to `~/.local/share/shesh/session_guard.jsonl`. When > thresholds (100 MB, 8000 files, 60 min, 5s avg latency), creates `docs/SESSION_HOP_ALERT.md` and prints 🚨.
- `scripts/supervise.sh` and `tools/autopilot/runner.py` call guard before each task — if hop needed, finishes current task, commits, pushes, exits instead of starting new big task.
- Handoff: `python tools/session_guard.py --handoff` generates `docs/NEXT_SESSION_PROMPT.md` (copy-paste into new Arena chat) + `dist/handoff.json`. Then `make check && git add -A && git commit -m "chore: handoff ..." && git push`.
- `docs/SESSION_PROTOCOL.md` documents full flow, `docs/NEXT_SESSION_PROMPT.md` is auto-generated template with GitHub profile, repos, PAT instructions (`GITHUB_PAT` env or `~/.config/shesh/github.pat` 0600 or `gh auth login`), commands `git pull && make check && session_guard --status`.
- `tools/github_auth.py` loads PAT securely (env > file 0600 > gh hosts.yml), refuses world-readable, never logs value.
- Ledger `~/.local/share/shesh/autopilot/ledger.jsonl` is pushed each task — next session replays `next_pending()`, rollback if interrupted.

**When to hop:** Guard says HOP, or you feel lag, or ~60 min elapsed, or `make check` starts slow.

## 12. Swarm — parallel Arena sessions via GitHub as bus (added 2026-08-11)

**Why:** Arena chats have NO connection. But you can open 3-4 Agent Mode tabs manually and want parallel work without overwrite.

**How:** GitHub repo IS the bus: `swarm/` queue/claims/heartbeats/artifacts/ledger.jsonl

- Orchestrator chat: `python tools/swarm/orchestrator.py --seed TODO.md --monitor` seeds `swarm/queue/*.json` from TODO.md ⬜ and monitors.
- Worker chats: `python tools/swarm/worker.py --component shesh-memory` polls queue, `try_claim()` via atomic `git pull --rebase + add claim + commit + push` — first push wins, second gets conflict and aborts, no overwrite.
- Branch per task `swarm/<agent-id>/<task-id>` — work isolated, `make check` gate before merge to main.
- Safety: component filter (`--component shesh-memory` vs `shesh-system`) avoids same-file edit; heartbeat every poll, orchestrator re-queues stale claims >10 min; `GuardedMCP` still enforced; no secrets in swarm files.
- Docs: `docs/SWARM.md` (architecture + actionable assessment), `swarm/README.md` (quick start), `tools/swarm/common.py/orchestrator.py/worker.py`

**Is it actionable?** Yes for 2-4 workers with component partitioning, with caveats: no real-time (45s poll), PAT needed, Arena kills background process on tab close (claim remains until re-queued), manual tab opening (Arena can't auto-spawn), too many workers increase git conflicts. Best 1 orchestrator + 2 workers.

**Next improvements:** GitHub Issues + Projects API instead of files (better atomicity), auto PR creation + Action auto-merge after gate green, dedicated `shesh-swarm` repo as pure bus (currently reuse shesh-ecosystem).

## 13. New session accomplishments (2026-08-11)

- Fixed manifest/lock drift (shesh→shesh), regenerated locks (1/16/19), Makefile, test_manifest, ruff E741, `make check` green 30 tests
- Cloned 22 repos into `src/`, verified 182 component tests
- Renamed `docs/components/shesh-*.md→shesh-*.md` and synced from `src/*/README.md`
- Created 15 ADRs `docs/adr/` + index, `docs/GETTING_STARTED.md`, `Containerfile`, `distrobox.ini`, `tools/install.sh` (btrfs snapshot+rollback), `scripts/sign_artifacts.py` (sigstore+SLSA), `scripts/export_traces_otlp.py` (OTLP), CI updated with audit guard + provenance
- Implemented session protocol (`docs/SESSION_PROTOCOL.md`, `tools/session_guard.py`, `tools/github_auth.py`, `docs/NEXT_SESSION_PROMPT.md` auto-generated)
- Implemented swarm (`docs/SWARM.md`, `swarm/README.md`, `tools/swarm/common.py`, `orchestrator.py`, `worker.py`, `swarm/queue/` 26 tasks seeded from TODO)
- Updated `TODO.md`, `QUERYLOG.md`, `AUDIT_AND_ROADMAP.md` links

## 14. Message to give next AI (copy from NEXT_SESSION_PROMPT.md)

```
You are continuing Shesh — federated local-first AI OS for CachyOS/Hyprland on MSI Sword 16 HX.
GitHub owner: gaganjainse. Main repo: shesh-ecosystem. Read docs/SESSION_HANDOFF.md FIRST, then AUDIT_AND_ROADMAP, TODO, MANUAL_VERIFICATION, SESSION_PROTOCOL, SWARM, GETTING_STARTED, queries/QUERYLOG.md
PAT: set GITHUB_PAT env or ~/.config/shesh/github.pat (0600) or gh auth login — tool tools/github_auth.py checks securely, never logs.
Run: cd /home/user && git pull origin main && make check && python tools/session_guard.py --status && ls src/ | wc -l
Then pick next ⬜ from TODO.md and continue autopilot. For swarm: orchestrator tab `python tools/swarm/orchestrator.py --monitor`, workers `python tools/swarm/worker.py --component shesh-*`
```

Paste whole `docs/NEXT_SESSION_PROMPT.md` — it contains live numbers, profile, all repos, PAT instructions, commands.

