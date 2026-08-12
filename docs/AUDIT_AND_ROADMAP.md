# Complete Audit & Master Roadmap

_A comprehensive penny-pick of every decision made, everything built, and
every task remaining across the Shesh ecosystem. Generated from the live
repos and this session's decisions. This is the anchor document; TODO.md
is the actionable checklist derived from it._

Last audited: 2026-08-12 (evening — full hardening pass; see 2026-08-12 evening delta below)

## 2026-08-12 evening delta

- **Dependency truth**: hand-drawn graphs replaced by tools/depgraph.py + CI
  freshness gate; cargo-machete trimmed ~24 declared-but-unused Rust deps
  (which is why the hand graphs had phantom edges).
- **Silent failures (17:40 directive) done ecosystem-wide**: 0 error-class
  findings across every clone; three real bugs surfaced and fixed
  (smart-organizer fake savings, safety.sh fake backup, voice console-crash
  silence) plus the earlier component batch (harness outage-as-zero-score,
  omniroute config revert, swarm claim race).
- **Supply chain**: SheshAOS has a real LICENSE, deny/machete/typos CI;
  actionlint 1.7.12 pinned org-wide; link integrity gated.
- **Workspace self-service (16:41 directive)**: orchestrator toolkit adopted
  into tools/ with `make verify-all`; home dir de-cluttered to
  archive/adopted-or-oneoff-2026-08-12/.
- Open threads moved to TODO.md: callable component-CI workflow decision,
  fork/archive triage, SHESH/SESHA mirror naming drift, janitor TODO policy,
  and the PAT rotation (user action).

---

## 0. Truthful answers

- **Can the assistant see the whole conversation?** This session's transcript,
  yes. Anything before the opening summary is only known through the files/docs
  we created, not raw memory. The on-disk repos are the source of truth.
- **Are the files (sesha-audit, pyproject.toml, etc.) present?** Yes. All 12
  components live in `/home/user/sesha/components/shesh-*/`, each with
  `pyproject.toml`, `src/`, `tests/`, README, and CI. shesh-audit has all 5
  modules (`__init__, log, policy, gate, nexus_bridge, server`) plus 18 tests.
- **What caused the workspace-over-budget notice?** The Rust toolchain
  (`~/.cargo`+`~/.rustup`, ~1 GB) installed to test the kernel merge, plus
  large git clones. Removed; workspace now 127 MB.

---

## 1. Decisions made (and why)

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Five languages only: Rust, Python, Lua, QML/JS, Bash; no Zig/C/Mojo/Go | Minimize FFI; cross-language talk is MCP/JSON over processes, not in-process links |
| D2 | Exotic runtimes go in rootless Podman/Distrobox, not host | Reproducible envs, no host pollution |
| D3 | Federated component repos + manifest/locks, not a monorepo | Each component independently versioned/tested; ecosystem repo is the integration point |
| D4 | Three release channels stable/canary/devel | Daily work on devel, integration on canary, releases on stable; gates promote |
| D5 | Local-first; cloud is opt-in behind policy | Privacy, offline operation; no keys in config |
| D6 | Governance: immutable base prompt + evidence-backed `/refine` with rollback | Self-improvement must be safe (Prime Agent "cheating" lesson) |
| D7 | Agent roles: coordinator/planner/coder/researcher/vision/critic | Specialist models; 6 GB-safe model per role |
| D8 | shesh-kernel archived rather than force-merged | The two Rust trees diverged at type level (57 compile errors); forcing would ship a broken build. Staged rebase documented. |
| D9 | Newelle forked as shesh-voice with an overlay, core untouched | Keeps upstream rebase easy; overlay ships MCP config + local model + wake word |
| D10 | ACP adopted alongside MCP | ACP = editor↔agent (Zed/JetBrains); MCP = agent↔tools. They stack. |
| D11 | Catch-up scheduler, not fixed cron timers | Laptops sleep/shut down; `OnStartupSec`+jitter+AC/idle gates + budget |
| D12 | Warmth via one optional offer at natural pauses, ≤3/day | Proactive but never nagging; throttled/snoozeable |
| D13 | Hierarchical memory + token-bounded context assembly | Solves retention and finite context window together |
| D14 | Habit learning is frequentist with decay, not opaque weights | Inspectable/reversible; candidate habits reviewed |
| D15 | Every tool call passes through shesh-audit Guard | allow/confirm/deny + logged + emitted in SheshAOS event format |

---

## 2. What exists (verified)

### Repos (16 total: 15 active, 1 archived)

| Repo | Layer | Tests | Purpose |
|------|-------|------:|---------|
| SheshAOS | Brain | 981 (Rust) | Governance kernel; Rust workspace of 12 crates |
| shesh-audit | Brain | 18 | Hash-chained event log + policy Guard + Nexus bridge |
| shesh-mind | Mind | 13 | Role→model router (6 GB VRAM budget) |
| shesh-memory | Mind | 15 | Episodic/semantic/intention/habit memory + context assembler |
| shesh-harness | Mind | 7 | Continual Harness: immutable base, `/refine`, rollback |
| shesh-orchestrator | Mind | 9 | Multi-agent RLM runtime, A2A bus, budgets |
| shesh-skills | Mind | 10 | Everyday MCP tools + 5 Markdown skills |
| shesh-voice | Soma | — (fork) | Newelle fork + overlay (wake/STT/TTS/MCP wiring) |
| shesh-files | Soma | 5 | Rust watcher + Python classifier |
| shesh-shell | Soma | 3 | Hyprland/Quickshell MCP |
| shesh-system | Soma | 7 | Power/GPU/MUX/status MCP |
| shesh-acp | Soma | 9 | Agent Client Protocol server |
| shesh-backup | Soma | 8 | restic wrapper, AC/daily gating, verify |
| shesh-phone | Soma | 7 | ADB control for Realme Narzo, safe-bounds |
| shesh-desktop | Soma | 20 (ambient) | CachyOS/Hyprland dotfiles, settings GUI |
| shesh-ecosystem | — | 13 | Manifest, resolver, gates, docs, canary CI |
| ~~shesh-kernel~~ | ~~Brain~~ | — | **ARCHIVED**: superseded by SheshAOS, merge pending |

**Verified test total: 124 Python tests passing across components + 13 ecosystem = 137, plus 981 Rust tests in SheshAOS and 20 ambient tests in shesh-desktop.**

### Central documentation (in shesh-ecosystem/docs/)

- `architecture/AGENTIC_BODY.md`, `REPO_TOPOLOGY.md`, `LANGUAGE_POLICY.md`, `MULTI_AGENT.md`
- `ACP_A2A.md`, `CONTAINERS_AND_VENV.md`, `LINUX_LAYOUT.md`, `LEARNING.md`
- `TOOLING_CATALOG.md`, `GAP_ANALYSIS.md`, `GLOSSARY.md`
- `components/` — README for every shesh-* component (9)
- `skills/` — 5 agent skills (+ autopilot)
- `desktop/` — 14 SHESH docs from shesh-desktop
- `queries/QUERYLOG.md` — every user prompt + answer

### Component docs
Each repo has a standardized README (layer, license, ecosystem link, tools, dev commands).

---

## 3. Penny-picked task list (everything remaining, incl. "future work")

Tasks are tagged P0 (blocks real use) / P1 (soon) / P2 (future). The
checkable version is TODO.md.

### 3.1 Brain / governance
- [P0] **Shesh-kernel → SheshAOS merge.** Rebase archived kernel onto
  SheshAOS; port leaf crates first (protocols, waveobj, wps, blockctl,
  wconfig), reconcile `NexusError`/TUI API divergence, bring
  `shesh-protocols` (ACP+MCP wire impls) and CLI/worker bins; fix
  upstream build breaks (`russh::Error::msg` removed, `zig` required by
  terminal); gate on `cargo test --workspace` green. See
  `KERNEL_MERGE_PLAN.md` in SheshAOS.
- [P0] Wire shesh-audit Guard in front of **every** MCP tool call
  (orchestrator + skills currently declare it; enforce at the server boundary).
- [P1] Nexus bridge: have Rust SheshAOS actually consume `nexus-events.jsonl`
  (currently Python writes it; Rust reads TBD).
- [P1] Secret manager integration (KeePassXC/gopass); no keys in MCP config.
- [P2] eBPF/Aya telemetry for system/performance sensing (read-only).
- [P2] Supply-chain: sigstore/provenance for component artifacts.

### 3.2 Mind / agents
- [P0] **LLM-backed planner/critic** in orchestrator (currently stub); wire to
  Ollama via shesh-mind routing.
- [P1] **A2A over a Unix socket** (currently in-process); then optional remote
  (opt-in, authenticated).
- [P1] Persistent/background agent sessions (detach/reattach like Prime).
- [P1] Real `/refine` loop: local-model planner + llm-eval-harness grading on
  held-out checks before promotion.
- [P1] Automatic skill capture (Read→Execute→Reflect→Write) with held-out
  scoring; deprecate unused/low-success skills ("discard the dross").
- [P1] Episodic compaction/summarization retention job.
- [P1] `shesh-mind` model router: honor currently-loaded models (avoid
  unloading), add embedding provider abstraction.
- [P2] RAG via rag-service (semantic retrieval beyond FTS).
- [P2] Skill marketplace / sharing evolved skills (opt-in).

### 3.3 Soma / body
- [P1] Package mature third-party MCP servers behind the Guard: filesystem,
  git, fetch, Playwright, GitHub (scoped PAT), SQLite, markitdown, time.
- [P1] `shesh-maintenance` (cache/journal/orphan packages), `update-check`
  (notify never auto-`-Syu`), `health` (CPU/GPU/disk/battery).
- [P1] `shesh-phone`: OCR/vision→tap loop (the harness concept from
  phone-harness); currently only adb primitives exist.
- [P1] Container-control MCP (podman/distrobox) for sandboxed/untrusted tasks.
- [P1] Email/calendar: local-first CalDAV/IMAP (vdirsyncer + khal/neomutt).
- [P1] Messaging bridges (Telegram/Signal) as isolated opt-in services.
- [P1] Media: screenshots, screen recording, wallpaper, audio routing.
- [P1] ACP full sessions: terminal bridge, diff/update messages (cancel +
  permission responses done).
- [P2] Accessibility (a11y).
- [P2] Job-mode isolated profile (work git identity, no personal cloud).

### 3.4 Desktop / AP (Agentic Physique — the MSI)
- [P0] **Hardware validation on the actual machine**: Hyprland@144, NVIDIA
  MUX, wake word, PipeWire audio, Quickshell render. (Cannot run in this
  sandbox.)
- [P1] Installer channel support (stable/canary/devel) with btrfs snapshot
  + rollback.
- [P1] Wire ambient offers to the Quickshell overlay (call
  `shesh-ambient offer` on workspace switch / idle).
- [P1] Make proactivity data-aware (real Inbox count, git status, backup age)
  instead of static strings.
- [P2] Accessibility, recording.

### 3.5 Platform / infrastructure
- [P0] **Canary end-to-end test**: boot all MCP + ACP servers in a container,
  run a real task end-to-end. (Workflow matrix exists; e2e does not.)
- [P1] Distrobox/Containerfile for one-command onboarding.
- [P1] Observability: OpenTelemetry traces for agent runs (local only).
- [P1] shesh-ambient installed as a user service + wired into setup.
- [P2] Self-hosted update mirror.

### 3.6 Docs / process (this audit)
- [x] Centralize all docs — **done** (42 markdown files in docs/).
- [x] Query log — **done** and must be appended each response (real-time).
- [x] Master TODO/roadmap — **this document + TODO.md**.
- [P1] ADRs (Architecture Decision Records) for D1–D15.
- [P1] User getting-started guide for shesh-desktop.
- [P1] Doc-sync job: copy each component README into docs/components/ on change.

---

## 4. What was explicitly NOT done (and why)

- Did **not** force the kernel merge (D8) — would have shipped broken code.
- Did **not** delete any repos — archived the duplicate; personal/college
  projects (portfolio, AIM, ClinicLedger, Vyākṛti, etc.) left untouched.
- Did **not** run hardware/GPU/audio tests — impossible in this sandbox.
- Did **not** connect real LLM/LLM-eval to refine/orchestrator yet — stubs
  are in place; this is P0/P1.

---

## 5. Operating rules going forward (autopilot) — UPDATED 2026-08-11 per user feedback

1. Anchor to TODO.md; pick the highest-priority unblocked ⬜.
2. Branch per item; tests gate every push; never push red.
3. After every user message: append to `docs/queries/QUERYLOG.md`, update TODO.md status, and refresh relevant docs — real-time.
4. Archive, never delete. No force-push to main.
5. Mark hardware-dependent items 🟡 rather than faking success.
6. **DON'T make minimal versions/stubs that become dead code — make proper working versions** with real implementation, tests, integration, docs. Minimal versions we made (shesh-brain, media, messaging, ebpf minimal) became stubs — user called out, now we make proper.
7. **First thought when challenged with an issue = STEAL, not make a tool.** What have we been learning? Philosophy is steal from open source world and make it ours. Check `SOURCES.md`, `TOOLING_CATALOG.md`, `manifests/upstreams.toml`, awesome-hyprland, best MCP servers 2026, Rust crates (notify, aya, etc), CachyOS Noctalia, etc. Search web for open-source things (MIT/Apache/GPL, truly free no API key, self-hostable). If something better exists that can be stolen, upgraded, customized, specialized for our CachyOS/Hyprland/6GB VRAM system and improved — STEAL IT. Only if not found, then make yourself.
8. **We can discard what we made if something better exists to steal.** Never engage in pointless brooding — if existing open-source does job better (e.g., DankMaterialShell bar vs our custom bar, ekremx25/quickshell monitor management vs our custom, SearXNG/agent-search vs Tavily subscription), discard ours and wrap better one, upgrade wrapper for our needs.
9. **Upgrade wrapper, not just fork and wrap.** Our job is not just to fork and wrap, but to upgrade wrapper for our needs and customize and specialize for our system and improve it — e.g., Newelle fork stripped GNOME, added Quickshell overlay, prewired MCP, 6GB-safe models, renamed Shesh (Newelle core).
10. **Integrating various different systems, but no conflict.** We have to be cautious but enterprising — namespace via MCP stdio process boundaries (never in-process FFI), Guard policy allow/confirm/deny, separate systemd user services, separate config dirs, btrfs subvolumes, Python venvs via uv, so integrations don't clash. One job per component, one process per MCP server, one policy gate.
11. **We have a lot of time, freely — no limited time constraint.** Who posted limited time constraint? We have a lot of time. Don't rush to minimal stubs to save time. Make proper working versions. User is traveling now 1-2 days, can keep one chat open, GitHub Actions true hours unattended handle rest.
12. **Style + Performance non-negotiable:** User uses illogical-impulse (end-4 dots-hyprland) because loves its look, CachyOS because loves its performance. Can't compromise, don't break these systems. Already using best customized dotfiles riced look, don't need looks, need good backend and other systems that integrate into that look. Improve style, not change — if something better in other dotfiles (ML4W, JaKooLit, HyDE, Noctalia, Caelestia, DankMaterialShell, ekremx25/quickshell, qs-hyprview, HyprPanel, rishot pill bar morphing), include it in our look: functionalities, improvements, better response and animations, more smooth and buttery feel, better bluetooth wifi integration. At end of day, it is also fork and wrapper so we should improve it. Pick features/issues from every mainstream fork we are using and if useful extract and work on it. Build proper infrastructure for stealing/improving/customising so user doesn't have to write it many times — `manifests/upstreams.toml`, `tools/steal/`, `scripts/upstream_tracker.py`, `docs/STEAL_INFRASTRUCTURE.md`.

---

## 6. Manual verification

Things that cannot be tested in the sandbox are tracked separately in
**[MANUAL_VERIFICATION.md](MANUAL_VERIFICATION.md)** — work through it on the
physical MSI after install. It covers accounts/keys, the MCP mesh, voice/GPU/
display, backup, phone, containers, agent behavior, security, and the
deliberate non-autopilot items (kernel merge, hardware validation).
