# SESSION HANDOFF — Shesh ecosystem

**Generated:** 2026-08-12 (live update via tools/live_update.py) ·
**State-refresh:** 2026-08-13 evening — see §0 first.
**Purpose:** Load this at the start of a new session to continue exactly
where this one stopped, without re-deriving context.

> Read this file FIRST, then `docs/history/AUDIT_AND_ROADMAP.md`, `TODO.md`,
> `docs/MANUAL_VERIFICATION.md`, `docs/SESSION_PROTOCOL.md`, `docs/SWARM.md`.
> The query log at `docs/history/queries/QUERYLOG.md` has the full decision trail.
> For next session copy-paste, read `docs/NEXT_SESSION_PROMPT.md` — it contains everything needed without re-explaining.

Copy `docs/NEXT_SESSION_PROMPT.md` into a new Arena chat to continue — it includes GitHub profile, all repos, PAT instructions, commands.

---

## 0.1 Federation consolidation (2026-08-13) — ADR-0019
16 sub-service shesh-* modules folded into the new `shesh-core` monorepo
(16 packages + 15 unchanged console-script names, 175 tests). Kept as services:
shesh-memory, shesh-orchestrator, shesh-harness, shesh-phone, shesh-omniroute
(now depend on `shesh-core>=0.1`). 17 folded repos archived. Manifest organs
unchanged (23); their repo field points at shesh-core; locks regenerated
(stable 1 / canary 19 / devel 23). fetch-components.sh clones once + symlinks.

## 0.2 One-link install hardened (2026-08-13) — before user's PC reset
`bash <(curl -s .../shesh-desktop/main/tools/bootstrap.sh)` now installs the WHOLE
stack (desktop + device profile + shesh-core MCP + policy + configs). Fixed:
setup exec bit (100755), bootstrap flag passthrough (setup ignores unknown flags —
bootstrap owns --device/--skip-* now), empty mcp_servers dir, install-shesh-stack
canary default + shared venv + correct units. Guard policy is config-driven via
~/.config/shesh/policy.json (Settings → Shesh → Governance).

## 0. Current position — 2026-08-13 (fleet-wide rolling dependency update)

**Rolling deps (one job, latest everywhere):** SheshAOS `ab27cd8` (8 crates to
latest majors, 877/877 tests, clippy/fmt/deny clean); portfolio `cd94afb`
(TS7 reverted→6.x per conflict protocol, upstream needs astro API);
vyakrti-ide `a79f152` (react 19, zustand 5, monaco 0.56); waveterm `f6ca6e8`
+ `639f381` (lock resync + ai/@ai-sdk bump cleared undici 12 alerts);
pipecat `fe1962a` (uv lock -U). Remaining honest (waveterm docs workspace):
image-size no upstream patch; sharp/serialize-javascript/uuid constrained by
Docusaurus pins (override destabilizes install — documented). Python 23
components + Actions already at latest. Full detail: QUERYLOG 2026-08-13.

**Nexus→Shesh rename (complete):** SheshAOS `nexus_ingest` →
`kernel_ingest` (`363900b`); ecosystem living docs swept (`006c3e7`) —
kernel_bridge/kernel-events.jsonl/KernelBridge/KernelError everywhere;
AUDIT_AND_ROADMAP P1 flipped ✅; immutable history untouched.

**Nexus → Shesh/Kernel rename (complete):** SheshAOS `nexus_ingest` →
`kernel_ingest` (`363900b`); ecosystem living docs swept (`006c3e7`) —
kernel_bridge/kernel-events.jsonl/KernelBridge/KernelError everywhere;
AUDIT_AND_ROADMAP P1 flipped ✅; immutable history untouched.

**Pending-item completion (this turn):** a11y spec + checker + reference
fixes (ecosystem `61b66a3`, shesh-desktop `d885c16` — 381-element baseline,
on-machine long tail); skill marketplace primitives (shesh-harness
`b00407b` — export/import JSON manifests, 7 tests); RAG confirmed covered
in-component (shesh-memory semantic_search, 33 tests); self-hosted update
mirror (shesh-desktop `3237048` — update-mirror.sh, dry-run safe);
eBPF boundary honest + shesh-ebpf verified (8 tests).

Roadmap completion (earlier): every sandbox-feasible P1/P2 item is done —
shesh-phone vision→tap loop (`78d120e`), ambient data-aware proactivity
(`82b3173`), job-mode profile P2 (`827a851`), kernel bridge Rust ingest
(SheshAOS `83e3358`+`1ddf28b`+`363900b`), email/IMAP setup (shesh-calendar
`4e4e0cc`). Remaining honest: P0 hardware validation (needs the MSI
machine), real eBPF (needs kernel privs), a11y long tail (on-machine QML
pass), hosted marketplace + Rekor (💡Future). See QUERYLOG 2026-08-13.

Latest closures (new session, continued):
- **Canary P0 e2e — GREEN on arch/fedora/ubuntu** (`4b0af81` → `f3b4a3c`):
  was red 3 consecutive days. Fixed gate-in-container `/src` hardcode,
  missing component clones (fetch-components.sh), e2e install order +
  non-Python skip + stale kernel_bridge import, snapshot-checkout git root
  discovery (self-contained tests + pure-path fallback), INDEX regen.
- **Component README auto-sync** (`126a478`, `f3b4a3c`): new
  tools/sync_component_docs.py (link translation to blob URLs) + CI
  freshness job; 23 drifted files synced; linkcheck 0 broken.
- **Failure-memory offline loop** (`shesh-memory 4103d05`): 7 new tests;
  exposed + fixed 2 real habit-learner bugs (volume-bias promotion,
  double-decay). 33/33 tests.
- **Dependabot fleet:** merged 5 open PRs (vyakrti-ide postcss, pipecat h2,
  waveterm js-yaml/mermaid/nanoid); Vyakrti Rust CI fixed (drive-letter
  path guard, `65e520e`); dompurify CVE closed via npm override in
  waveterm/vyakrti-ide/Vyakrti (all alerts closed, builds green).
- **pipecat transformers — FIXED** (`ea9e3af` + `a65576b`): the HIGH RCE
  advisories (GHSA-fgcw-684q-jj6r et al.) required transformers ≥5.5.0, but
  the `speechmatics` extra pulled `speechmatics-voice[smart]` which pins
  transformers `<5` — unsatisfiable when combined with local-smart-turn.
  Verified the STT service never imports the smart modules (cloud API only),
  so dropped `[smart]` from the extra (documented; opt-in note added) →
  bumped lock transformers 4.57.6 → **5.15.0**. Follow-up: mcp
  1.27.2 → 1.28.1 (`5a8037e`, GHSA-vj7q-gjh5-988w WebSocket Host/Origin).
  **pipecat: 0 open dependabot alerts.** (pipecat is a mirror fork — not a
  Shesh component; fixes are upstreamable.)
- **shesh-voice Flatpak Build — verified GREEN** (was unconfirmed).
- **Known-good tips:** ecosystem `39ed0cf`, shesh-docs `0357778`,
  shesh-desktop `668e07fc`, portfolio `c7673c2`, SheshAOS `a9dfc9f`,
  shesh-voice `8a6fd42`, shesh-wave `987da7b`, AIM `6afe02a`,
  ClinicLedger `b04adf7`, ClinicLedger-Template `30be902`, Vyakrti `637bb2f`,
  waveterm `2fb3842`, vyakrti-ide `01de4fb`, shesh-memory `4103d05`.

CI closure (earlier same session):

- **shesh-desktop lock-refresh — GREEN** (`9f46a15`): the `789e282`
  girepository fix from the prior session never landed on main (parallel
  race). Re-applied with the verified noble package
  (`libgirepository-2.0-dev` + `gobject-introspection` + `libglib2.0-dev`),
  dispatched → success → bot committed fresh lock `668e07fc`. The stale
  desktop lock that was blocking dependabot security runs is gone.
- **portfolio Auto-Update — GREEN** (`cd30013` + `c7673c2`): prettier
  normalize step after regeneration (root cause of run 31653325256), then
  the AI-OS repo rename (→ SeshAOS) broke the generator's priority lookup
  (only 7 curated → ≥8 test failed). Generator renamed; 8 curated,
  22/22 tests, run 31663621988 + CI green.
- **Fleet poll (60 repos):** 173 GREEN / 0 PENDING / 16 RED. 13 reds are
  dependabot-PR or stale-SHA runs (pre-fix SHAs, re-verified — see QUERYLOG
  entry); shesh-workspace janitor red is a stale run of a workflow removed
  at tip (20ec93e); the last two genuinely-red main branches (AIM,
  ClinicLedger/ClinicLedger-Template) were then fixed — see below.
- **AIM CI — GREEN** (`6afe02a`): tests patched a non-existent module attr
  (`app.fetch_settings_map`; app.py imports it lazily) → repointed the 5
  patch sites at `repositories.system_repository.fetch_settings_map`.
  101/101 tests, flake8/py_compile clean.
- **ClinicLedger CI — GREEN in progress** (`f17d3f9` + `6131bf3`): gradle
  pin `9.5` → `9.6.1` (full version string required); missing
  `gradle-wrapper.jar` restored (the blanket `*.jar` .gitignore rule had
  swallowed it — negation exception added).
- **ClinicLedger-Template CI — GREEN in progress** (`85cb9c3` + `134e050` +
  `30be902`): same gradle pin → `9.5.0`; same wrapper-jar restore; plus the
  POSIX `gradlew` script itself was never committed (only `gradlew.bat`) —
  restored with exec bit.
- **Known-good tips:** ecosystem `7670f90`, shesh-docs `82f62e2`,
  shesh-desktop `668e07fc`, portfolio `c7673c2`, SheshAOS `a9dfc9f`,
  shesh-voice `8a6fd42`, shesh-wave `987da7b`, AIM `6afe02a`.
- **Fresh-session gotchas (Arena snapshot exclusions):** `.git/config`
  (origin remote) and `~/.git-credentials` are not persisted → re-add
  remote, credential helper, identity each session; reinstall
  cryptography/ruff/node24.

Remaining honest leftovers (owner-side / sanctioned): PAT rotation
(transcript exposure), libghostty park, optional cross-repo docs auto-push
secret — see MANUAL_VERIFICATION §13 and TODO.md.

### Prior session (2026-08-13): security + rolling deps + docs renovation — record

Three user mandates landed that session, all pushed and gate-verified:

- **Security / attack resistance / recovery (research-backed, cited in-repo):**
  push protection + secret scanning on all 53 active repos (API-verified);
  every third-party Action SHA-pinned at latest releases with weekly
  Dependabot moves; `pull_request_target` RCE pattern removed from
  swarm-auto-merge; zizmor + gitleaks gates in the reusable pipeline;
  MCP rug-pull/tool-poisoning defense (`tool_pins.py`, TOFU + drift
  refusal) landed in shesh-audit (`53a60b6`); canonical
  `SECURITY.md` + `docs/THREAT_MODEL.md` + `docs/RECOVERY.md` +
  `tools/dr_check.sh`.
- **Rolling dependencies (owned by the agent now):** Python floors at
  current majors (pytest 9.1.1, ruff 0.16.2, pytest-asyncio 1.4.0, fastmcp
  3.4.7 — PyPI-latest on 2026-08-13); fleet sweep 21/21 green; SheshAOS
  Cargo.lock refreshed (`a9dfc9f`, 872/872 tests + clippy/deny/machete
  clean); conflict protocol codified in `docs/policies/DEPENDENCY_POLICY.md`
  (downgrade-by-one → drop-and-replace).
- **Docs renovation:** shesh-docs is now a pure projection —
  `tools/book_build.py` (mirror map + fissions + generators + link
  translation + orphan sweep), 74 placeholders replaced with real content,
  114 orphan/duplicate files removed, mdbook render gate in CI; audits moved
  to `docs/history/audits/`, SITUATION_REPORT fused into the INCIDENTS post-mortem,
  desktop mirror retired to `docs/history/attic/` (canonical = shesh-desktop repo).
- **Naming:** SHESH-only canon enforced fleet-wide including shesh-desktop
  body text (`504ee8e`); shesh-voice verified zero-legacy.
- **Owner-side leftovers (cannot be done by the agent):** rotate the GitHub
  PAT (transcript exposure 2026-08-11/12); optional Actions secret if
  cross-repo docs auto-push is wanted later. Both listed in
  `docs/MANUAL_VERIFICATION.md` §13.

Tips: ecosystem `210972e`→(this refresh), shesh-docs `ce643f3`, shesh-desktop
`504ee8e`, SheshAOS `a9dfc9f`, shesh-audit `78c9d86`. CI poll for the day's
pushes is the first job of the next session if not appended below.

---

## 1. What this is

**Shesh** is a local-first AI agent OS for Linux (target: CachyOS on an MSI
Sword 16 HX). It is a federation of small MCP components governed by a
policy/audit layer, with a Newelle-based voice frontend and a Rust
governance kernel (SheshAOS, in progress).

- **Naming (FINAL, canon):** the product/OS is **SHESH**, the kernel project
  is **SheshAOS**. All repos/packages/imports are `shesh-*` / `shesh_*`;
  env vars `SHESH_*`. Legacy spellings survive only in immutable-history
  classes (ADR/QUERYLOG/audits/attic) and real frozen artifacts — exact list
  in [ADR-0017](history/adr/0017-naming-purge-completed.md). Gates: rename sweep +
  shesh-docs name gate (living docs must not even enumerate the old tokens —
  the gate caught this paragraph doing so; fixed).

## 2. Repositories (all under github.com/gaganjainse)

| Repo | Layer | Tests | Purpose |
|------|-------|------:|---------|
| SheshAOS | Brain | 872 (Rust) | Governance kernel — merge pending |
| shesh-ecosystem | — | 61 (Python) | Manifest, gates, docs, **autopilot**, this wiki source |
| shesh-audit | Brain | 29 | Hash-chained event log, GuardedMCP, tool pins, kernel bridge, secrets |
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

**Component tests: 235+ (2026-08-13 sweep) · Ecosystem tests: 61 · Desktop
ambient: 26 · SheshAOS: 872 — all green.**

## 3. Where the code lives on disk

- Components: `/home/user/src/shesh-*/  (canonical layout; `sesha` dir names on older machines are the known legacy typo — see below)`
- Ecosystem: `/home/user/shesh-ecosystem/` (canonical) — also cloned into
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
   audit log + kernel events).
6. Never store secrets in config — use `shesh-secrets` references
   (`env:`, `gopass:`, `file:0600`).
7. Commit with the task id in the message; push through the autopilot
   safety guards.
8. After each user message, append to `docs/history/queries/QUERYLOG.md` and update
   `TODO.md` statuses.
9. Archive, don't delete. No force-push to main. No root.
10. Mark hardware-only items 🟡 rather than faking success.
11. **Upgrade wrapper, not just fork and wrap:** Customize and specialize for our system and improve it — e.g., Newelle fork stripped GNOME, added Quickshell overlay, prewired MCP, 6GB-safe models, renamed Shesh (Newelle core).
12. **Integrating various systems, no conflict — cautious but enterprising:** namespace via MCP stdio, Guard, separate systemd services, separate config dirs, btrfs subvolumes, Python venvs via uv, one job per component, one process per MCP server.
13. **Style + Performance non-negotiable:** illogical-impulse look (end-4 shesh-desktop) + CachyOS performance, don't break systems, already using best customized dotfiles riced look, need good backend that integrates into look. Improve style, not change — if something better in other dotfiles (ML4W, JaKooLit, HyDE, Noctalia, Caelestia, DankMaterialShell, ekremx25, qs-hyprview, HyprPanel, rishot pill morphing), include it for functionalities, better response/animations, smooth buttery feel, better bluetooth wifi integration.

## 6. What is DONE

- ✅ All 19 repos renamed Shesh→Shesh (GitHub redirects old names)
- ✅ Governance: audit log, GuardedMCP, policy, kernel event bridge, secrets
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
  `KernelError`/TUI APIs, bring in `shesh-protocols` (ACP+MCP wire impls)
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
cd /home/user/shesh-ecosystem
export PATH="$HOME/.local/bin:$PATH"

# 1. Verify everything is green
for d in ../components/shesh-*/; do
  (cd "$d" && python3 -m pytest tests/ -q -p no:cacheprovider)
done
python3 -m pytest tests/ -q -p no:cacheprovider

# 2. Read the anchors
cat docs/SESSION_HANDOFF.md   # this file
$PAGER TODO.md docs/history/AUDIT_AND_ROADMAP.md docs/MANUAL_VERIFICATION.md

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
- Created 15 ADRs `docs/history/adr/` + index, `docs/GETTING_STARTED.md`, `Containerfile`, `distrobox.ini`, `tools/install.sh` (btrfs snapshot+rollback), `scripts/sign_artifacts.py` (sigstore+SLSA), `scripts/export_traces_otlp.py` (OTLP), CI updated with audit guard + provenance
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

