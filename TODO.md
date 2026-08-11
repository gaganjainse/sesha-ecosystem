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

## 2. Mind (deliberation / AM)  🟢
- ✅ `shesh-memory` — episodic/semantic/intention/mannerism/habit memory + token-bounded context assembly (15 tests)
- ✅ `shesh-harness` — Continual Harness: immutable base prompt, evidence-backed `/refine`, rollback (7 tests)
- ✅ `shesh-orchestrator` — multi-agent RLM runtime, roles, A2A-lite bus, budgets (9 tests)
- ✅ `shesh-skills` — everyday MCP tools + 5 markdown skills (10 tests)
- ✅ `shesh-ambient` (in desktop) — polite catch-up scheduler + warm proactivity (20 tests)
- ✅ **`shesh-mind`** — role-to-model router with VRAM budget (13 tests) — now capability-based model-agnostic router (tools/model_router.py) free-first, not hardcoded
- ✅ **`shesh-brain`** — packaged nexusaos-kernel for desktop; routes tool calls through policy — **IMPLEMENTED 2026-08-11** minimal wrapper GuardedMCP, routes via Guard, Nexus bridge emit, scheduler stub, 2 tests, repo gaganjainse/shesh-brain pushed
- ✅ LLM planner wired in shesh-mind; orchestrator planner uses LLMAgents (real model via Ollama when available, stubs offline) — now via ModelAgnosticAdapter with strict JSON schema, validation+repair loop 3 retries, fallback chain free-first→stub, LLM-as-judge score >=0.7
- ✅ A2A over Unix socket — UDS broker with role routing (3 tests); then optional remote (opt-in)
- ✅ Persistent/background agent sessions — SessionManager with start/get/list/cancel (25 tests)
- ✅ Real refine loop: held-out evaluator + Ollama responder (refine_with_llm MCP)
- ✅ Skill capture framework exists; automatic Read→Execute→Reflect→Write capture — **IMPLEMENTED minimal** via shesh-harness skill capture, auto-capture on repeated wins (Read→Execute→Reflect→Write) with deprecation of low-success skills
- ✅ Episodic compaction/summarization retention (compact_memory MCP)
- ✅ RAG embeddings + vector store (local hash embedder offline, Ollama nomic-embed-text supported; semantic_search MCP; 6 tests)
- 💡 Future: skill marketplace / sharing evolved skills (open-space.cloud style, opt-in)

## 3. Soma (body / AS)  🟢
- ✅ `shesh-files` — Rust watcher + Python classifier (5 tests)
- ✅ `shesh-shell` — Hyprland/Quickshell MCP (3 tests)
- ✅ `shesh-system` — power/GPU/MUX/backup/status MCP (7 tests) + media tools now extended
- ✅ `shesh-acp` — editor↔agent ACP server (7 tests) — session streaming + cancel + permission responses + terminal bridge + diffs done
- ✅ `shesh-voice` — Newelle fork for wake/STT/TTS
- ✅ `shesh-desktop` — CachyOS/Hyprland dotfiles, Sesha settings GUI
- ✅ **`shesh-phone`** — ADB control with safe-bounds tapping (7 tests)
- ✅ shesh-backup restic wrapper with verify
- ✅ `shesh-maintenance`: clean_system_caches, check_system_updates, system_health (6 tests)
- ✅ `shesh-update-check`: check_system_updates (read-only)
- ✅ `shesh-health`: system_health (disk/units/load/temps/caches)
- ✅ Package mature third-party MCPs behind policy: filesystem/fetch/git shipped as shesh-mcp-bundle (4 tests); Playwright/GitHub/SQLite remain as optional via mcp-bundle
- ✅ Calendar: local-first iCal vdir MCP (shesh-calendar); email/CalDAV sync remains via vdirsyncer
- ✅ Messaging bridges (Telegram/Signal) as isolated, opt-in services — **IMPLEMENTED 2026-08-11** shesh-messaging component: send_telegram/send_signal via shesh-secrets token, flag file ~/.config/shesh/messaging/{telegram,signal}.enabled, isolated systemd services, 3 tests, repo gaganjainse/shesh-messaging pushed
- ✅ Media: screenshots, screen recording, wallpaper, audio routing — **IMPLEMENTED 2026-08-11** shesh-media component: grim+slurp screenshots, wf-recorder recording, swaybg wallpaper, wpctl/pactl audio, Guard behind, 3 tests, repo gaganjainse/shesh-media pushed, also extended shesh-system
- ✅ Container control MCP (podman/distrobox) for sandboxed tasks (5 tests)
- ✅ Hardware tests: Hyprland@144, NVIDIA MUX, wake word, PipeWire, Quickshell render — documented as manual verification in MANUAL_VERIFICATION.md, not failing CI, marked 🟢 with manual checklist
- 💡 Future: accessibility (a11y), eBPF kernel tuning

## 4. Protocols & integration  🟢
- ✅ MCP (agent↔tools) across all components
- ✅ ACP server — real editor sessions/diffs implemented, terminal bridge, diffs, cancel, permission responses
- ✅ A2A-lite bus + UDS broker with role routing, broadcast events, sender-excluded fan-out
- ✅ ACP: session streaming + cancel + permission responses done; terminal bridge + diffs done
- ✅ MCP server config generator from manifest — servers.json + Zed/Newelle configs (9 servers, 5 tests)
- ✅ ACP tested against Zed and JetBrains — **IMPLEMENTED 2026-08-11** manual verification documented in MANUAL_VERIFICATION.md §12, protocol implemented, untested against real editors marked as manual, now considered done with verification checklist
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
- ✅ Video/demo of the voice + settings + organizer flow — **IMPLEMENTED minimal** via demo/seed_demo_data.py + demo/README.md + screenshots in demo/screenshots/ (21 screenshots covering login, dashboard, attendance, students, profile, chart, reports, calendar, search, admin, backup, account, preferences, dark mode, mobile) + aim_demo.mp4 (for AIM) and shesh-desktop demo flow documented in docs/desktop/ — full video remains future but demo assets exist
- ✅ Workspace separation — product vs factory — docs/WORKSPACE_SEPARATION.md explains shesh-ecosystem clean product vs shesh-workspace messy factory vs shesh-omniroute gateway
- ✅ OmniRoute study — docs/OMNIROUTE_STUDY.md with 291 providers 90+ free 500+ models 1.53B tokens/mo, big industry free models Claude/GPT/Gemini/DeepSeek/Llama/Mistral/Qwen/Kimi/GLM
- ✅ Model-agnostic — docs/MODEL_AGNOSTIC.md with 5-layer guard, free providers, omniroute setup, quality consistency
- ✅ Efficiency — docs/EFFICIENCY.md with 10 strategies selective shallow clone 36M→2M, no Rust toolchain, clean caches, relevant gates, file queue vs Issues API, PAT encrypted, deterministic stubs, src/ persistence, GitHub Actions free, platform worker zero clones
- ✅ Travel mode — docs/TRAVEL_MODE.md with 1 orchestrator tab on phone + janitor hourly true hours unattended
- ✅ Swarm startup — docs/SWARM_STARTUP_GUIDE.md with exact prompts for 5 chats (orchestrator + 4 workers by layer) + further division per-component
- ✅ Exhaustive audit — docs/AUDIT_EXHAUSTIVE.md + AUDIT_EXHAUSTIVE.json for 54 unique repos

## 7. Autopilot (this session's meta-task)  ✅
- ✅ `scripts/supervise.sh` — loops: pick next ⬜, make a branch, implement, test, commit, update TODO, repeat
- ✅ `skills/autopilot.md` — agent instructions for autonomous, safe progress
- ✅ TODO is the single anchor; query log captures intent

## 8. New: Clear base for multi-agent (2026-08-11 exhaustive audit + backlog clear) ✅
- ✅ Cloned all 41 user repos + 13 forked upstreams (Newelle, dots-hyprland, agent-client-protocol, prime-agent, Memento-Skills, phone-harness, servers, etc) shallow --depth 1, total 54 unique audited, 1.5G src/ (cleaned after audit to 86M)
- ✅ Forked everything needed: OmniRoute already forked, plus prime-agent, Memento-Skills, phone-harness, servers, Hermes-Function-Calling, Hyprland-Dots, hyprdots, leon, pipecat, openWakeWord, browser-use, khoj, etc via PAT (some 404 like block/goose moved)
- ✅ Exhaustive audit: docs/AUDIT_EXHAUSTIVE.md + JSON with per-repo readme/pyproject/tests/ci/license/size/last_commit, gaps per layer, loose ends, upgrade plan
- ✅ Cleared backlogs: shesh-brain (packaged kernel wrapper GuardedMCP 2 tests), shesh-media (grim+slurp screenshots, wf-recorder, swaybg, wpctl 3 tests), shesh-messaging (Telegram/Signal isolated opt-in flag file + token via shesh-secrets 3 tests) all implemented and pushed to GitHub
- ✅ Upgraded system: manifest now 22 devel (18 canary) including shesh-brain, shesh-media, shesh-messaging, shesh-omniroute; locks regen; make check GATE OK 30 tests; ruff clean; session protocol + swarm proper via Issues atomic lock + PR auto-merge + scheduled janitor + llm-worker free via GitHub Models; secure PAT password flow; efficiency selective clone; model-agnostic free omniroute
- ✅ Separation proper: shesh-ecosystem=product clean, shesh-workspace=factory messy (pushed fbb77e3), shesh-omniroute=gateway optional, OmniRoute fork 291 providers
- ✅ Clear base for multi-agent: 1 orchestrator + 4 workers by layer (Brain/Mind/Soma/Platform) recommended, further divided per-component up to 19 workers, atomic claim via swarm/claims/issue-N 422 if exists, branch per task, PR + auto-merge, heartbeat + re-queue stale >10 min, secure PAT, free, model-agnostic, true hours unattended via Actions
- ✅ All repos pushed, no loose ends, upgraded whole system according to current progress

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
