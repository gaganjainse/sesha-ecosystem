# Shesh — Master TODO & Roadmap

The single anchored list of everything to do. Status: ✅ done · 🟡 in progress ·
⬜ todo · 🔴 blocked · 💡 future. Groups correspond to the Agentic Body layers
(Brain / Mind / Soma) and to platform work. Check this before starting anything
new; update it on every change so we don't drift.

Last updated: 2026-08-11 (new session: cloned all 22 component repos, fixed manifest/lock drift shesha→shesh, regenerated locks, renamed docs/components, fixed Makefile + test_manifest, created 15 ADRs, getting-started guide, Containerfile + distrobox.ini + installer with btrfs snapshot/rollback, synced component READMEs)

## New session accomplishments (2026-08-11)
- ✅ Fixed manifest/lock drift: regenerated channels/*.lock from shesh-* manifest (was stale shesha-* from rename commit 0d4f0f1), updated Makefile Shesha→Shesh, fixed test_manifest to accept shesh name, fixed ruff lint E741 in autopilot tests, make check green (30 tests)
- ✅ Cloned all component repos into /home/user/src (22 repos: shesh-* + SheshaAOS + SeshaOS + shesha-kernel + NexusAOS + shesh-desktop) — offline tests verified (182 component tests where deps present)
- ✅ Doc sync: renamed docs/components/shesha-*.md → shesh-*.md and synced content from src/*/README.md (17 components)
- ✅ ADRs: created docs/adr/ with 15 ADRs for D1–D15 (languages, containers, federated repos, channels, local-first, refine governance, agent roles, kernel archive, voice overlay, ACP+MCP, catchup scheduler, warm proactivity, hierarchical memory, habit learning, Guard policy) + index README
- ✅ Getting-started: created docs/GETTING_STARTED.md (developer quick start, full CachyOS install, Ollama 6GB stack, Rust/uv/Podman, pipx component install, voice, secrets, backup, phone, containers, everyday use, canary promotion, hardware checks, troubleshooting)
- ✅ Platform onboarding: Containerfile (Arch-based reproducible dev container), distrobox.ini, tools/install.sh with --channel stable|canary|devel, btrfs snapshot creation + rollback docs, pipx upgrade loop, MCP config generation
- ✅ Supply-chain + observability: scripts/sign_artifacts.py (sigstore keyless stub, SHA256 + SLSA provenance, offline-first), scripts/export_traces_otlp.py (local JSONL → OTLP JSON, optional HTTP endpoint), CI updated with audit guard sanity + supply-chain provenance step, .gitignore updated for dist/ and src/
- ✅ QUERYLOG updated for this session (4 new Q/A: AIM vs shesh-ecosystem correction, session handoff, new session full order)





---

## Status vs original plan (honest audit)
- ✅ shesh-ecosystem created & pushed
- ✅ All 12 components split into own repos (beyond the original 3)
- ✅ shesh-voice: Newelle fork renamed + MCP overlay (was missing)
- 🟡 shesh-audit standalone done; **NexusAOS Rust bridge now added** (Python→shared JSONL)
- ✅ Arch/Fedora/Ubuntu canary CI; CachyOS is Arch-based so covered
- 🔴 shesh-kernel merge remains blocked on Rust type reconciliation

## 0. Project identity & naming ✅
- ✅ Sesha → **Shesh** (शेष) across all repos/code/docs
- ✅ Glossary: AOS (Agentic OS), AB (Agentic Body), AM (Agentic Mind), AI (Agentic Intelligence), AS (Agentic Soma), AP (Agentic Physique)
- ✅ 12 active + 2 archived repos, all lowercase `shesh-*`, GitHub redirects in place
- ✅ Central docs gathered into `shesh-ecosystem/docs/` (40 docs)
- ✅ Query log started (`docs/queries/QUERYLOG.md`)

## 1. Brain (governance / AOS)  🟡
- ✅ `shesh-audit` — hash-chained append-only event log + allow/confirm/deny policy (11 tests)
- ✅ `SheshAOS` — Rust governance kernel rebranded; SeshaOS folded in
- 🔴 **shesh-kernel → SheshAOS merge** — type-diverged, do NOT force. See `KERNEL_MERGE_PLAN.md`.
  - ⬜ Rebase archived shesh-kernel onto SheshAOS main
  - ⬜ Port leaf crates first (protocols, waveobj, wps, blockctl, wconfig)
  - ⬜ Then ai/remote/rpc/gui/kernel/vault/tui/terminal
  - ⬜ Reconcile `NexusError`/TUI API divergence
  - ⬜ Bring in `sheshaos-protocols` (ACP+MCP wire impl) and CLI/worker bins
  - ⬜ Fix pre-existing upstream build breaks: `russh::Error::msg` removed; `zig` required by terminal
  - ⬜ Gate: `cargo test --workspace` green on stable
- ✅ Wire `shesh-audit` as the policy gate in front of every MCP tool call (Guard helper in shesh-audit; components import it)
- ✅ NexusAOS event-store bridge (NexusBridge in shesh-audit; Guard emits Nexus-format events)
- 💡 Future: eBPF telemetry with Aya (Rust) for system/performance sensing

## 2. Mind (deliberation / AM)  🟡
- ✅ `shesh-memory` — episodic/semantic/intention/mannerism/habit memory + token-bounded context assembly (15 tests)
- ✅ `shesh-harness` — Continual Harness: immutable base prompt, evidence-backed `/refine`, rollback (7 tests)
- ✅ `shesh-orchestrator` — multi-agent RLM runtime, roles, A2A-lite bus, budgets (9 tests)
- ✅ `shesh-skills` — everyday MCP tools + 5 markdown skills (10 tests)
- ✅ `shesh-ambient` (in desktop) — polite catch-up scheduler + warm proactivity (20 tests)
- ✅ **`shesh-mind`** — role-to-model router with VRAM budget (13 tests)
- ⬜ **`shesh-brain`** — packaged nexusaos-kernel for desktop; routes tool calls through policy
- 🟡 LLM planner wired in shesh-mind; orchestrator planner uses LLMAgents (real model via Ollama when available, stubs offline)
- ✅ A2A over Unix socket — UDS broker with role routing (3 tests); then optional remote (opt-in)
- ✅ Persistent/background agent sessions — SessionManager with start/get/list/cancel (25 tests)
- ✅ Real refine loop: held-out evaluator + Ollama responder (refine_with_llm MCP)
- 🟡 Skill capture framework exists; automatic Read→Execute→Reflect→Write capture remains
- ✅ Episodic compaction/summarization retention (compact_memory MCP)
- ✅ RAG embeddings + vector store (local hash embedder offline, Ollama nomic-embed-text supported; semantic_search MCP; 6 tests)
- 💡 Future: skill marketplace / sharing evolved skills (open-space.cloud style, opt-in)

## 3. Soma (body / AS)  🟡
- ✅ `shesh-files` — Rust watcher + Python classifier (5 tests)
- ✅ `shesh-shell` — Hyprland/Quickshell MCP (3 tests)
- ✅ `shesh-system` — power/GPU/MUX/backup/status MCP (7 tests)
- ✅ `shesh-acp` — editor↔agent ACP server (7 tests)
- ✅ `shesh-voice` — Newelle fork for wake/STT/TTS
- ✅ `shesh-desktop` — CachyOS/Hyprland dotfiles, Sesha settings GUI
- ✅ **`shesh-phone`** — ADB control with safe-bounds tapping (7 tests)
- ✅ shesh-backup restic wrapper with verify
- ✅ `shesh-maintenance`: clean_system_caches, check_system_updates, system_health (6 tests)
- ✅ `shesh-update-check`: check_system_updates (read-only)
- ✅ `shesh-health`: system_health (disk/units/load/temps/caches)
- 🟡 Package mature third-party MCPs behind policy: filesystem/fetch/git shipped as shesh-mcp-bundle (4 tests); Playwright/GitHub/SQLite remain
- ✅ Calendar: local-first iCal vdir MCP (shesh-calendar); email/CalDAV sync remains via vdirsyncer
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

## 5. Platform / infrastructure  🟢
- ✅ uv projects with lockfiles; rootless Podman + Distrobox guidance
- ✅ Ecosystem manifest resolver with license gate + 3 channels (stable/canary/devel)
- ✅ Canary multi-distro CI (arch/fedora/ubuntu) workflow
- ✅ Cross-component test suites (100+ tests total)
- ✅ Canary end-to-end test covers all 15 components
- ✅ Distrobox/Containerfile for reproducible onboarding — Containerfile (Arch + podman + uv), distrobox.ini, make check green in container
- ✅ Installer channel support (stable/canary/devel) with btrfs snapshot + rollback — tools/install.sh with --channel, --dry-run, --check, snapshot to /.snapshots/pre-shesh-<channel>-<date>, rollback instructions, verified
- ✅ Secret manager: env/gopass/keepassxc/file backends (shesh-secrets; 8 tests)
- ✅ Supply-chain: sigstore/provenance for artifacts — scripts/sign_artifacts.py (keyless cosign when COSIGN_KEYLESS set, otherwise SHA256 + SLSA provenance.json), SLSA statement emitted, CI step added
- ✅ Integrate `shesh-audit` into CI release gates — audit guard sanity check in ci.yml, provenance + OTLP sample generation
- ✅ OTLP traces: scripts/export_traces_otlp.py for local JSONL → OTLP JSON export (opt-in HTTP endpoint), local-only observability
- 💡 Future: self-hosted update mirror + sigstore Rekor transparency log verification

## 6. Docs & knowledge  🟢
- ✅ Architecture docs (Body, topology, languages, containers, Linux layout, multi-agent, ACP/A2A, learning)
- ✅ Gap analysis + tooling catalog + attribution
- ✅ Per-component READMEs standardized — synced from src repos (17 components) + renamed shesha→shesh
- ✅ Keep `docs/queries/QUERYLOG.md` appended on every user prompt (autopilot does this) — updated this session
- ✅ Doc synchronization: when a component changes, copy its README into `docs/components/` — done this session, needs automation job next
- ✅ Architecture Decision Records (ADRs) for each protocol decision — 15 ADRs in docs/adr/ + index
- ✅ User-facing getting-started guide for shesh-desktop — docs/GETTING_STARTED.md with full install, Ollama stack, voice, secrets, backup, phone, troubleshooting
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
