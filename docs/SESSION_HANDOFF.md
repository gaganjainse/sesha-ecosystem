# SESSION HANDOFF — Shesh ecosystem

**Generated:** 2026-08-10
**Purpose:** Load this at the start of a new session to continue exactly
where this one stopped, without re-deriving context.

> Read this file FIRST, then `docs/AUDIT_AND_ROADMAP.md`, `TODO.md`, and
> `docs/MANUAL_VERIFICATION.md`. The query log at
> `docs/queries/QUERYLOG.md` has the full decision trail.

---

## 1. What this is

**Shesh** is a local-first AI agent OS for Linux (target: CachyOS on an MSI
Sword 16 HX). It is a federation of small MCP components governed by a
policy/audit layer, with a Newelle-based voice frontend and a Rust
governance kernel (SheshAOS, in progress).

- **Naming (FINAL):** the product is **Shesh**, the kernel is **SheshAOS**.
  All repos/packages/imports are `shesh-*` / `shesh_*`. "Shesha" was the
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

## 5. How to build safely (the contract)

1. Pick the next pending item from `TODO.md` (or seed it:
   `python -m tools.autopilot.cli seed`).
2. Work in one component. Keep changes small and focused.
3. **Always** run tests in that component:
   `cd components/shesh-<x> && python3 -m pytest tests/ -q`.
4. Use `GuardedMCP` from shesh-audit for any new MCP server (auto policy +
   audit log + Nexus events).
5. Never store secrets in config — use `shesh-secrets` references
   (`env:`, `gopass:`, `file:0600`).
6. Commit with the task id in the message; push through the autopilot
   safety guards.
7. After each user message, append to `docs/queries/QUERYLOG.md` and update
   `TODO.md` statuses.
8. Archive, don't delete. No force-push to main. No root.
9. Mark hardware-only items 🟡 rather than faking success.

## 6. What is DONE

- ✅ All 19 repos renamed Shesha→Shesh (GitHub redirects old names)
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
  `NexusError`/TUI APIs, bring in `sheshaos-protocols` (ACP+MCP wire impls)
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

## 10. Design principles (don't violate these)

- **Local-first / offline** — every tool degrades to deterministic stubs.
- **Governed** — every tool call passes the Guard; policy decides.
- **Federated** — one job per component; manifest integrates them.
- **Tested before push** — autopilot refuses red commits.
- **Small, reversible, audited** — commits, events, rollback.
- **No secrets in repos** — shesh-secrets only.
- **Shesh, not Shesha; SheshAOS, not SheshaAOS.**
