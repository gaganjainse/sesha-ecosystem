# Shesha — Master TODO & Roadmap

The single anchored list of everything to do. Status: ✅ done · 🟡 in progress ·
⬜ todo · 🔴 blocked · 💡 future. Groups correspond to the Agentic Body layers
(Brain / Mind / Soma) and to platform work. Check this before starting anything
new; update it on every change so we don't drift.

Last updated: 2026-08-09

---

## 0. Project identity & naming ✅
- ✅ Sesha → **Shesha** (शेष) across all repos/code/docs
- ✅ Glossary: AOS (Agentic OS), AB (Agentic Body), AM (Agentic Mind), AI (Agentic Intelligence), AS (Agentic Soma), AP (Agentic Physique)
- ✅ 12 active + 2 archived repos, all lowercase `shesha-*`, GitHub redirects in place
- ✅ Central docs gathered into `shesha-ecosystem/docs/` (40 docs)
- ✅ Query log started (`docs/queries/QUERYLOG.md`)

## 1. Brain (governance / AOS)  🟡
- ✅ `shesha-audit` — hash-chained append-only event log + allow/confirm/deny policy (11 tests)
- ✅ `SheshaAOS` — Rust governance kernel rebranded; SeshaOS folded in
- 🔴 **shesha-kernel → SheshaAOS merge** — type-diverged, do NOT force. See `KERNEL_MERGE_PLAN.md`.
  - ⬜ Rebase archived shesha-kernel onto SheshaAOS main
  - ⬜ Port leaf crates first (protocols, waveobj, wps, blockctl, wconfig)
  - ⬜ Then ai/remote/rpc/gui/kernel/vault/tui/terminal
  - ⬜ Reconcile `NexusError`/TUI API divergence
  - ⬜ Bring in `sheshaaos-protocols` (ACP+MCP wire impl) and CLI/worker bins
  - ⬜ Fix pre-existing upstream build breaks: `russh::Error::msg` removed; `zig` required by terminal
  - ⬜ Gate: `cargo test --workspace` green on stable
- ✅ Wire `shesha-audit` as the policy gate in front of every MCP tool call (Guard helper in shesha-audit; components import it)
- ⬜ NexusAOS event-store bridge so Rust brain and Python soma share one audit log
- 💡 Future: eBPF telemetry with Aya (Rust) for system/performance sensing

## 2. Mind (deliberation / AM)  🟡
- ✅ `shesha-memory` — episodic/semantic/intention/mannerism/habit memory + token-bounded context assembly (15 tests)
- ✅ `shesha-harness` — Continual Harness: immutable base prompt, evidence-backed `/refine`, rollback (7 tests)
- ✅ `shesha-orchestrator` — multi-agent RLM runtime, roles, A2A-lite bus, budgets (9 tests)
- ✅ `shesha-skills` — everyday MCP tools + 5 markdown skills (10 tests)
- ✅ `shesha-ambient` (in desktop) — polite catch-up scheduler + warm proactivity (20 tests)
- ✅ **`shesha-mind`** — role-to-model router with VRAM budget (13 tests)
- ⬜ **`shesha-brain`** — packaged nexusaos-kernel for desktop; routes tool calls through policy
- ⬜ LLM-backed planner/critic in orchestrator (currently stub); wire to Ollama
- ⬜ A2A over Unix socket (currently in-process); then optional remote (opt-in)
- ⬜ Persistent/background agent sessions (detach/reattach like Prime)
- ⬜ Real `refine` loop: planner uses local model, evaluator plugs into `llm-eval-harness`
- ⬜ Auto-skill capture (Read→Execute→Reflect→Write) with held-out scoring; deprecate unused skills
- ⬜ Episodic compaction/summarization job (retention policy)
- ⬜ RAG via `rag-service` (semantic retrieval beyond FTS) — optional embeddings
- 💡 Future: skill marketplace / sharing evolved skills (open-space.cloud style, opt-in)

## 3. Soma (body / AS)  🟡
- ✅ `shesha-files` — Rust watcher + Python classifier (5 tests)
- ✅ `shesha-shell` — Hyprland/Quickshell MCP (3 tests)
- ✅ `shesha-system` — power/GPU/MUX/backup/status MCP (7 tests)
- ✅ `shesha-acp` — editor↔agent ACP server (7 tests)
- ✅ `shesha-voice` — Newelle fork for wake/STT/TTS
- ✅ `shesha-desktop` — CachyOS/Hyprland dotfiles, Sesha settings GUI
- ⬜ **`shesha-phone`** — ADB harness for Realme Narzo (OCR/vision→tap)
- ⬜ `sesha-backup` real restic implementation + verify
- ⬜ `sesha-maintenance` script (cache, journal, orphan packages)
- ⬜ `sesha-update-check` (notify, never auto `-Syu`)
- ⬜ `sesha-health` telemetry (CPU/GPU/disk/battery)
- ⬜ Package mature third-party MCPs behind policy: filesystem, git, fetch, Playwright, GitHub, SQLite, markitdown
- ⬜ Email/calendar: local-first CalDAV/IMAP (vdirsyncer+khal/neomutt)
- ⬜ Messaging bridges (Telegram/Signal) as isolated, opt-in services
- ⬜ Media: screenshots, screen recording, wallpaper, audio routing
- ⬜ Container control MCP (podman/distrobox) for sandboxed tasks
- 🔴 Hardware tests: Hyprland@144, NVIDIA MUX, wake word, PipeWire, Quickshell render — must run on the MSI or canary VM
- 💡 Future: accessibility (a11y), eBPF kernel tuning

## 4. Protocols & integration  🟡
- ✅ MCP (agent↔tools) across all components
- ✅ ACP server skeleton; need real editor sessions/diffs
- ✅ A2A-lite bus in orchestrator
- 🟡 ACP: session streaming + cancel + permission responses done; terminal bridge + diffs remain
- ⬜ MCP server config generator (from manifest) + `~/.config/shesha/mcp/`
- ⬜ ACP tested against Zed and JetBrains
- ⬜ OpenTelemetry traces (local) for agent runs

## 5. Platform / infrastructure  🟡
- ✅ uv projects with lockfiles; rootless Podman + Distrobox guidance
- ✅ Ecosystem manifest resolver with license gate + 3 channels (stable/canary/devel)
- ✅ Canary multi-distro CI (arch/fedora/ubuntu) workflow
- ✅ Cross-component test suites (100+ tests total)
- ⬜ **Canary end-to-end test**: boot all MCP/ACP servers in a container, run a real task
- ⬜ Distrobox/Containerfile for reproducible onboarding
- ⬜ Installer channel support (stable/canary/devel) with btrfs snapshot + rollback
- ⬜ Secret manager (KeePassXC/gopass) — no keys in config
- ⬜ Supply-chain: sigstore/provenance for artifacts
- ⬜ Integrate `shesha-audit` into CI release gates
- 💡 Future: self-hosted update mirror

## 6. Docs & knowledge  🟡
- ✅ Architecture docs (Body, topology, languages, containers, Linux layout, multi-agent, ACP/A2A, learning)
- ✅ Gap analysis + tooling catalog + attribution
- ✅ Per-component READMEs standardized
- ⬜ Keep `docs/queries/QUERYLOG.md` appended on every user prompt (autopilot does this)
- ⬜ Doc synchronization: when a component changes, copy its README into `docs/components/`
- ⬜ Architecture Decision Records (ADRs) for each protocol decision
- ⬜ User-facing getting-started guide for shesha-desktop
- ⬜ Video/demo of the voice + settings + organizer flow

## 7. Autopilot (this session's meta-task)  ✅
- ✅ `scripts/supervise.sh` — loops: pick next ⬜, make a branch, implement, test, commit, update TODO, repeat
- ✅ `skills/autopilot.md` — agent instructions for autonomous, safe progress
- ✅ TODO is the single anchor; query log captures intent

---

## How to work (autopilot rules)
1. Read TODO.md top-to-bottom; pick the highest-priority ⬜ not blocked.
2. Create a branch `feat/<thing>`.
3. Implement with tests; never push red.
4. Update the relevant doc and this TODO (flip ⬜→✅/🟡).
5. Append the user's prompt + a one-paragraph answer to QUERYLOG.md.
6. Commit in small Conventional-Commit chunks; push; open PR if non-trivial.
7. If blocked (🔴), document why in the linked doc and move on.
8. Do not delete repos; archive instead. Do not force-push to main.
