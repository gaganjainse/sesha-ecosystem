# Shesha — Master TODO & Roadmap

The single anchored list of everything to do. Status: ✅ done · 🟡 in progress ·
⬜ todo · 🔴 blocked · 💡 future. Groups correspond to the Agentic Body layers
(Brain / Mind / Soma) and to platform work. Check this before starting anything
new; update it on every change so we don't drift.

Last updated: 2026-08-09

---

## Status vs original plan (honest audit)
- ✅ shesha-ecosystem created & pushed
- ✅ All 12 components split into own repos (beyond the original 3)
- ✅ shesha-voice: Newelle fork renamed + MCP overlay (was missing)
- 🟡 shesha-audit standalone done; **NexusAOS Rust bridge now added** (Python→shared JSONL)
- ✅ Arch/Fedora/Ubuntu canary CI; CachyOS is Arch-based so covered
- 🔴 shesha-kernel merge remains blocked on Rust type reconciliation

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
- ✅ NexusAOS event-store bridge (NexusBridge in shesha-audit; Guard emits Nexus-format events)
- 💡 Future: eBPF telemetry with Aya (Rust) for system/performance sensing

## 2. Mind (deliberation / AM)  🟡
- ✅ `shesha-memory` — episodic/semantic/intention/mannerism/habit memory + token-bounded context assembly (15 tests)
- ✅ `shesha-harness` — Continual Harness: immutable base prompt, evidence-backed `/refine`, rollback (7 tests)
- ✅ `shesha-orchestrator` — multi-agent RLM runtime, roles, A2A-lite bus, budgets (9 tests)
- ✅ `shesha-skills` — everyday MCP tools + 5 markdown skills (10 tests)
- ✅ `shesha-ambient` (in desktop) — polite catch-up scheduler + warm proactivity (20 tests)
- ✅ **`shesha-mind`** — role-to-model router with VRAM budget (13 tests)
- ⬜ **`shesha-brain`** — packaged nexusaos-kernel for desktop; routes tool calls through policy
- 🟡 LLM planner wired in shesha-mind; orchestrator planner uses LLMAgents (real model via Ollama when available, stubs offline)
- ✅ A2A over Unix socket — UDS broker with role routing (3 tests); then optional remote (opt-in)
- ✅ Persistent/background agent sessions — SessionManager with start/get/list/cancel (25 tests)
- ✅ Real refine loop: held-out evaluator + Ollama responder (refine_with_llm MCP)
- 🟡 Skill capture framework exists; automatic Read→Execute→Reflect→Write capture remains
- ✅ Episodic compaction/summarization retention (compact_memory MCP)
- ✅ RAG embeddings + vector store (local hash embedder offline, Ollama nomic-embed-text supported; semantic_search MCP; 6 tests)
- 💡 Future: skill marketplace / sharing evolved skills (open-space.cloud style, opt-in)

## 3. Soma (body / AS)  🟡
- ✅ `shesha-files` — Rust watcher + Python classifier (5 tests)
- ✅ `shesha-shell` — Hyprland/Quickshell MCP (3 tests)
- ✅ `shesha-system` — power/GPU/MUX/backup/status MCP (7 tests)
- ✅ `shesha-acp` — editor↔agent ACP server (7 tests)
- ✅ `shesha-voice` — Newelle fork for wake/STT/TTS
- ✅ `shesha-desktop` — CachyOS/Hyprland dotfiles, Sesha settings GUI
- ✅ **`shesha-phone`** — ADB control with safe-bounds tapping (7 tests)
- ✅ shesha-backup restic wrapper with verify
- ✅ `shesha-maintenance`: clean_system_caches, check_system_updates, system_health (6 tests)
- ✅ `shesha-update-check`: check_system_updates (read-only)
- ✅ `shesha-health`: system_health (disk/units/load/temps/caches)
- 🟡 Package mature third-party MCPs behind policy: filesystem/fetch/git shipped as shesha-mcp-bundle (4 tests); Playwright/GitHub/SQLite remain
- ✅ Calendar: local-first iCal vdir MCP (shesha-calendar); email/CalDAV sync remains via vdirsyncer
- ⬜ Messaging bridges (Telegram/Signal) as isolated, opt-in services
- ⬜ Media: screenshots, screen recording, wallpaper, audio routing
- ✅ Container control MCP (podman/distrobox) for sandboxed tasks (5 tests)
- 🔴 Hardware tests: Hyprland@144, NVIDIA MUX, wake word, PipeWire, Quickshell render — must run on the MSI or canary VM
- 💡 Future: accessibility (a11y), eBPF kernel tuning

## 4. Protocols & integration  🟡
- ✅ MCP (agent↔tools) across all components
- ✅ ACP server skeleton; need real editor sessions/diffs
- ✅ A2A-lite bus in orchestrator
- 🟡 ACP: session streaming + cancel + permission responses done; terminal bridge + diffs remain
- ✅ MCP server config generator from manifest — servers.json + Zed/Newelle configs (9 servers, 5 tests)
- ⬜ ACP tested against Zed and JetBrains
- ✅ Local JSONL trace recorder + session tracing (recent_traces MCP; 3 tests)

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
