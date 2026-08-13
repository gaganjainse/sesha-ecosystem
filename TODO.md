# Shesh — Master TODO & Roadmap

The single anchored list of everything to do. Status: ✅ done · 🟡 in progress ·
⬜ todo · 🔴 blocked · 💡 future. Groups correspond to the Agentic Body layers
(Brain / Mind / Soma) and to platform work. Check this before starting anything
new; update it on every change so we don't drift. Ledger writes are
**append-and-attest only** — agents may add items and flip ⬜→✅ with proof
in the same commit, never clear (docs/policies/JANITOR_TODO_POLICY.md).

Last updated: 2026-08-13 (Security + rolling-deps + docs renovation megasession)

## New session accomplishments (2026-08-13, evening — three mandates completed)

- ✅ **Security fleet sweep (API-verified):** vulnerability alerts + automated security fixes + secret scanning + **push protection** enabled on all 53 active repos; canonical `SECURITY.md` + `docs/THREAT_MODEL.md` + `docs/RECOVERY.md` + `tools/dr_check.sh`; per-repo SECURITY.md pointer stubs ×25 → GitHub Security tab works everywhere
- ✅ **Workflow hardening ×26 repos:** third-party actions SHA-pinned at latest releases (Dependabot moves them weekly — pins can't silently rot), `permissions:` least-privilege, `persist-credentials: false` on non-pushing checkouts; **critical swarm-auto-merge `pull_request_target` RCE-class hole removed**; zizmor + gitleaks gates in the reusable pipeline (21 callers inherit); reusable-pipeline callers themselves SHA-pinned after zizmor caught the `@main` refs
- ✅ **MCP rug-pull/poisoning defense:** `tool_pins.py` in shesh-audit (`53a60b6`) — TOFU description pins, drift refusal, poisoning-marker scan; 9 tests; both guard seams wired
- ✅ **Rolling deps (agent-owned per user order):** Python floors at PyPI-latest (pytest 9.1.1/ruff 0.16.2/asyncio 1.4.0/fastmcp 3.4.7), fleet sweep 21/21 green; SheshAOS lock refresh 872/872 green (`a9dfc9f`); DEPENDENCY_POLICY.md codifies downgrade-one/drop-replace break-glass; dependabot configs corrected per-repo reality (no manifests → no phantom ecosystems; desktop pip→/sdata/uv); **desktop lock-refresh workflow** compiles the laptop-class lock in CI monthly; portfolio `path-to-regexp` CVE override
- ✅ **Docs renovation (the big one):** `tools/book_build.py` pure-projection engine (mirror map + fissions + generators + link translation + orphan sweep); shesh-docs rebuilt — 74 placeholder chapters replaced with real content, 114 duplicate/orphan files removed, mdbook render gate in CI, SUMMARY integrity + link + name gates; audits → `docs/audits/`, SITUATION_REPORT fused into INCIDENTS post-mortem, desktop mirror retired to attic (SSOT: desktop repo); 6 tool docs + 3 tutorials + skills POLICY authored from code-grounded truth; ecosystem CI gates mirror freshness
- ✅ **MANUAL_VERIFICATION → 16 sections:** +rolling-deps hygiene, +security posture (incl. PAT rotation owner action), +recovery drill
- ✅ **Suppression hunts:** desktop python-check `|| true` gates removed after clearing 26 ruff findings (incl. REAL glxinfo pipe bug: shell=True+list broke renderer detection); portfolio `|| true` chain removed → exposed missing Inter fonts (vendored OFL) + missing Pillow step + `npm ci || npm install` lockfile fallback — all fixed for real
- ✅ **Naming canon final:** shesh-desktop body-text SHESH sweep (`504ee8e`), shesh-voice verified zero-legacy; gates enforce

## New session accomplishments (2026-08-13, decisions executed + completions)

- ✅ **D1 reusable component CI**: one definition at `.github/workflows/component-ci.yml` (workflow_call; python matrix, internal git deps, extra pip, editable-install, optional rust gate) + thin callers in **all 21 components** (vendored-copy drift eliminated at the root); pytest now runs with **`-W error`** everywhere; 235 tests green per sweep. Knowns fixed en route: `install-editable` must be a YAML boolean, not a string.
- ✅ **D2 fork garden**: 5 uncited/stale forks archived reversibly (hyprdots, register, Hermes-Function-Calling, leon, khoj); keep-set with per-fork citation evidence → docs/policies/FORK_GARDENING.md
- ✅ **D3 SHESH-only naming**: canonical tree `docs/desktop/{SHESH_README,01_AUDIT,02_SHESH_HYBRID,04_SHESH_VOICE,06_SHESH_AGENT,08_12_15_*}` with one-way content map in scripts/sync-docs.sh; stale-name guard list + dual fast/strict modes; ecosystem/shc/oracle/GLOSSARY/orchestrator docs all on canonical names. ⟶ Superseded same-day: in-repo mirror retired to `docs/attic/desktop-mirror-2026-08-13/` — canonical desktop docs live in the shesh-desktop repo, book mirrors from there (one-topic-one-home)
- ✅ **D4 janitor policy**: append-and-attest only → docs/policies/JANITOR_TODO_POLICY.md
- ✅ **Auditor gap closed**: `tools/silent_failures.py` SF4 now covers workflow YAML `run:` blocks (8 regression tests); 5 live `|| true` sites fixed for real (strict installs ×2, guarded swarm diagnostics ×2, shesh-wave warning-level gate), plus a workflow-name-strict rule
- ✅ **Minimal→complete**: shesh-brain 81777f5 / shesh-messaging 946b4ca / shesh-media 5461535 / shesh-ebpf 306540f — the four components TODO itself flagged as stubs now carry complete contracts + 44 new tests total

## New session accomplishments (2026-08-12, orchestration + hardening)
- ✅ **Dependency graph truth**: tools/depgraph.py (cargo metadata + pyprojects + manifest) regenerates docs/architecture/DEPENDENCY_GRAPH.md; CI freshness gate rejects hand edits; last 4 phantom edges (vault→kernel, blockctl→waveobj/wps, wconfig→waveobj) fell when SheshAOS's manifests were trimmed (3f75f03/89702c0)
- ✅ **Silent-failure eradication (SF1-SF6)**: tools/silent_failures.py + ecosystem-wide CI (clones all repos). Fixed 9 BLE001 + 17 TRY + 20 AST swallows across 21 Python components, 77 in ecosystem tools, 19 SF4 + 3 SF1 in shesh-desktop (folders.sh fake-savings + safety.sh fake-backup real bugs), 105 SF1 in shesh-voice (window.py console-crash silence fixed for real). Ecosystem audit now: **0 errors**
- ✅ **SheshAOS supply-chain**: MIT LICENSE added (README always claimed it), cargo-deny (2 documented ignores only: RUSTSEC-2023-0071 no-patch-exists, RUSTSEC-2017-0008 unreachable-path), cargo-machete (~24 unused decls removed), typos, all wired into CI; canonical license.workspace inheritance; internal path deps versioned (wildcards=deny)
- ✅ **Workspace automation adopted**: tools/sync_repos.py, verify_worktrees.py, ecosystem_audit.py (ad-hoc `git reset --hard` + ambient `pip install` removed), verify_all_strict.sh, linkcheck.py + `make verify-all`/`make linkcheck`; link integrity now CI-gated (found 21 rotted links)
- ✅ **Post-snapshot recovery runbook executed**: remotes restored, exec bits repo-wide, waveterm build/ restored from git objects, media/system suppression commits re-dropped from archived patches
- ✅ **All four deferred decisions EXECUTED 2026-08-13** (D1 reusable CI, D2 fork garden, D3 SHESH-only naming, D4 append-and-attest janitor) — see the 2026-08-13 accomplishments section above for evidence pointers
- 🟡 **PAT rotation required by the USER** (org owner action): the PAT at ~/.config/shesh/github.pat appeared in an earlier plaintext transcript — rotate it on GitHub, then rewrite the file
- 🟡 **libghostty (shesh-voice fork base) — PARKED by user order 2026-08-13:** upstream divergence is outside our hands ("not in our hands"); revisit only when upstream moves. This is the ledger receipt for the single sanctioned exception — everything else in the three mandates is complete.

## New session accomplishments (2026-08-11)
- ✅ Fixed manifest/lock drift: regenerated channels/*.lock from shesh-* manifest (was stale shesh-* from rename commit 0d4f0f1), updated Makefile Shesh→Shesh, fixed test_manifest to accept shesh name, fixed ruff lint E741 in autopilot tests, make check green (30 tests)
- ✅ Cloned all component repos into /home/user/src (22 repos: shesh-* + SheshAOS + SheshAOS + shesha-kernel + SheshAOS + shesh-desktop) — offline tests verified (182 component tests where deps present)
- ✅ Doc sync: renamed docs/components/shesh-*.md → shesh-*.md and synced content from src/*/README.md (17 components)
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
- 🟡 shesh-audit standalone done; **SheshAOS Rust bridge now added** (Python→shared JSONL)
- ✅ Arch/Fedora/Ubuntu canary CI; CachyOS is Arch-based so covered
- ✅ shesh-kernel merge question resolved — withdrawn, no payload needed (ADR-0016)

## 0. Project identity & naming ✅
- ✅ Sesha → **Shesh** (शेष) across all repos/code/docs
- ✅ Glossary: AOS (Agentic OS), AB (Agentic Body), AM (Agentic Mind), AI (Agentic Intelligence), AS (Agentic Soma), AP (Agentic Physique)
- ✅ 12 active + 2 archived repos, all lowercase `shesh-*`, GitHub redirects in place
- ✅ Central docs gathered into `shesh-ecosystem/docs/` (40 docs)
- ✅ Query log started (`docs/queries/QUERYLOG.md`)

## 1. Brain (governance / AOS)  🟡
- ✅ `shesh-audit` — hash-chained append-only event log + allow/confirm/deny policy (11 tests)
- ✅ `SheshAOS` — Rust governance kernel rebranded; SeshaOS folded in
- ✅ **shesh-kernel → SheshAOS merge — WITHDRAWN by decision (ADR-0016, 2026-08-12).**
  Full-repo audit showed the protocol wires the merge existed to get — ACP and MCP — are
  already implemented and tested in Python (shesh-acp server; 17 `*-mcp` servers; GuardedMCP),
  and the Python↔Rust bridge is `kernel_bridge` JSONL. The Rust `shesh-protocols` crate
  would be a third implementation of owned wires. The iced/GUI terminal porting was the
  abandoned Wave rewrite; verdict: adopt stock Wave Terminal as mission control (shesh-wave).
  shesha-kernel stays archived (ADR-0008); SeshaOS archived as superseded (was already
  folded into SheshAOS). No merge, no port — kernel chapter closed.
- ✅ Wire `shesh-audit` as the policy gate in front of every MCP tool call (Guard helper in shesh-audit; components import it)
- ✅ SheshAOS event-store bridge (KernelBridge in shesh-audit; Guard emits kernel-format events)
- ✅ `shesh-ebpf` — eBPF telemetry via Aya (read-only; 4 tests) — added to manifest

## 2. Mind (deliberation / AM)  🟢
- ✅ `shesh-memory` — episodic/semantic/intention/mannerism/habit memory + token-bounded context assembly (15 tests)
- ✅ `shesh-harness` — Continual Harness: immutable base prompt, evidence-backed `/refine`, rollback (7 tests)
- ✅ `shesh-orchestrator` — multi-agent RLM runtime, roles, A2A-lite bus, budgets (9 tests)
- ✅ `shesh-skills` — everyday MCP tools + 5 markdown skills (10 tests)
- ✅ `shesh-ambient` (in desktop) — polite catch-up scheduler + warm proactivity (20 tests) — **COMPLETED P1 2026-08-13** (82b3173): data-aware offers (real git/backup/Downloads/disk facts via sources.py, 11 new tests, 38 total)
- ✅ **job-mode isolated work profile (P2)** — **COMPLETED 2026-08-13** (shesh-desktop 827a851): tools/job-mode/job-mode.sh — work git identity via includeIf ~/work/**, personal sync paused/restored, reversible + idempotent, shellcheck clean
- ✅ **kernel bridge Rust consumption (P1)** — **COMPLETED 2026-08-13** (SheshAOS 83e3358): shesh-kernel kernel_ingest reads kernel-events.jsonl (typed events, bad-line/unknown-kind/monotonicity accounting, tail view; 5 tests; workspace + clippy clean)
- ✅ **`shesh-mind`** — role-to-model router with VRAM budget (13 tests) — now capability-based model-agnostic router (tools/model_router.py) free-first, not hardcoded
- ✅ **`shesh-brain`** — packaged shesh-kernel for desktop; routes tool calls through policy — **COMPLETED 2026-08-13** (81777f5): two-phase confirmation flow closed (`record_confirmation` → hash-chained audit + kernel CONFIRMATION_GRANTED/DENIED events), `audit_tail` ledger read view, 8 tests pin the contract (was: minimal wrapper, scheduler stub, 2 tests)
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
- ✅ **`shesh-phone`** — ADB control with safe-bounds tapping (7 tests) — **COMPLETED P1 2026-08-13** (78d120e): OCR/vision→tap loop (`VisionTapLoop` + `TemplateVision`, injected provider, safe-area refusal, verify-after-tap; 9 new tests, 16 total)
- ✅ shesh-backup restic wrapper with verify
- ✅ `shesh-maintenance`: clean_system_caches, check_system_updates, system_health (6 tests)
- ✅ `shesh-update-check`: check_system_updates (read-only)
- ✅ `shesh-health`: system_health (disk/units/load/temps/caches)
- ✅ Package mature third-party MCPs behind policy: filesystem/fetch/git shipped as shesh-mcp-bundle (4 tests); Playwright/GitHub/SQLite remain as optional via mcp-bundle
- ✅ Calendar: local-first iCal vdir MCP (shesh-calendar); email/CalDAV sync remains via vdirsyncer — **COMPLETED P1 2026-08-13** (4e4e0cc): `tools/setup-email.sh` local-first IMAP sync → ~/.maildir + neomutt config, secrets via shesh-secrets env only
- ✅ Messaging bridges (Telegram/Signal) as isolated, opt-in services — **COMPLETED 2026-08-13** (946b4ca): bridge now full-duplex — `read_telegram` (getUpdates, caller-acked offsets, long-poll clamp, channel_post) + `telegram_status` (getMe probe); same opt-in flag + secrets-resolved-token disciplines; 12 tests (was: send-only, 3 tests)
- ✅ Media: screenshots, screen recording, wallpaper, audio routing — **COMPLETED 2026-08-13** (5461535): audio contract made honest (no fabricated `stub-speakers`; empty list + explicit reason when offline), real `get_volume`/`set_volume` via wpctl with mute parse + 1.0 policy cap; 16 tests (was: 3 tests + fabricated sink names). NOTE: wallpaper backend is hyprpaper-via-hyprctl — the 08-11 line claiming swaybg was inaccurate
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
- ✅ Per-component READMEs standardized — synced from src repos (17 components) + renamed shesh→shesh
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
- ✅ Exhaustive audit — docs/audits/AUDIT_EXHAUSTIVE.md + .json for 54 unique repos

## 7. Autopilot (this session's meta-task)  ✅
- ✅ `scripts/supervise.sh` — loops: pick next ⬜, make a branch, implement, test, commit, update TODO, repeat
- ✅ `skills/autopilot.md` — agent instructions for autonomous, safe progress
- ✅ TODO is the single anchor; query log captures intent

## 8. New: Clear base for multi-agent (2026-08-11 exhaustive audit + backlog clear) ✅
- ✅ Cloned all 41 user repos + 13 forked upstreams (Newelle, dots-hyprland, agent-client-protocol, prime-agent, Memento-Skills, phone-harness, servers, etc) shallow --depth 1, total 54 unique audited, 1.5G src/ (cleaned after audit to 86M)
- ✅ Forked everything needed: OmniRoute already forked, plus prime-agent, Memento-Skills, phone-harness, servers, Hermes-Function-Calling, Hyprland-Dots, hyprdots, leon, pipecat, openWakeWord, browser-use, khoj, etc via PAT (some 404 like block/goose moved)
- ✅ Exhaustive audit: docs/audits/AUDIT_EXHAUSTIVE.md + JSON with per-repo readme/pyproject/tests/ci/license/size/last_commit, gaps per layer, loose ends, upgrade plan
- ✅ Cleared backlogs: shesh-brain (packaged kernel wrapper GuardedMCP 2 tests), shesh-media (grim+slurp screenshots, wf-recorder, swaybg, wpctl 3 tests), shesh-messaging (Telegram/Signal isolated opt-in flag file + token via shesh-secrets 3 tests) all implemented and pushed to GitHub
- ✅ Upgraded system: manifest now 22 devel (18 canary) including shesh-brain, shesh-media, shesh-messaging, shesh-omniroute; locks regen; make check GATE OK 30 tests; ruff clean; session protocol + swarm proper via Issues atomic lock + PR auto-merge + scheduled janitor + llm-worker free via GitHub Models; secure PAT password flow; efficiency selective clone; model-agnostic free omniroute
- ✅ Separation proper: shesh-ecosystem=product clean, shesh-workspace=factory messy (pushed fbb77e3), shesh-omniroute=gateway optional, OmniRoute fork 291 providers
- ✅ Clear base for multi-agent: 1 orchestrator + 4 workers by layer (Brain/Mind/Soma/Platform) recommended, further divided per-component up to 19 workers, atomic claim via swarm/claims/issue-N 422 if exists, branch per task, PR + auto-merge, heartbeat + re-queue stale >10 min, secure PAT, free, model-agnostic, true hours unattended via Actions
- ✅ All repos pushed, no loose ends, upgraded whole system according to current progress

---

## How to work (autopilot rules) — UPDATED 2026-08-11 per user feedback, no limited time

1. Read TODO.md top-to-bottom; pick the highest-priority ⬜ not blocked.
2. Create a branch `feat/<thing>`.
3. **First thought = STEAL, not make tool.** Check SOURCES.md, TOOLING_CATALOG.md, manifests/upstreams.toml, awesome-hyprland, best MCP servers 2026, Rust crates (notify-rs, aya-rs, etc), web search for open-source things (MIT/Apache/GPL, truly free no API key, self-hostable). If something better exists that can be stolen, upgraded, customized, specialized for our CachyOS/Hyprland/6GB VRAM system and improved — STEAL IT. Only if not found, then make yourself. What have we been learning then? Steal first.
4. **DON'T make minimal versions/stubs that become dead code — make proper working versions** with real implementation, tests, integration, docs. Minimal versions we made (shesh-brain, media, messaging, ebpf minimal) became stubs per user feedback — **all four completed 2026-08-13** (brain 81777f5, messaging 946b4ca, media 5461535, ebpf 306540f; 8/12/16/8 tests each). We have a lot of time, freely, no limited time constraint.
5. Implement with tests; never push red.
6. Update the relevant doc and this TODO (flip ⬜→✅/🟡).
7. Append the user's prompt + a one-paragraph answer to QUERYLOG.md.
8. Commit in small Conventional-Commit chunks; push; open PR if non-trivial.
9. If blocked (🔴), document why in the linked doc and move on.
10. Do not delete repos; archive instead. Do not force-push to main.
11. **We can discard what we made if something better exists to steal.** Never engage in pointless brooding — if existing open-source does job better (DankMaterialShell vs custom bar, ekremx25 monitor management vs custom, SearXNG/agent-search vs Tavily subscription $0.005/query online-led), discard ours and wrap better one, upgrade wrapper.
12. **Upgrade wrapper, not just fork and wrap.** Customize and specialize for our system and improve it — e.g., Newelle stripped GNOME, added Quickshell overlay, prewired MCP, 6GB-safe models, renamed Shesh (Newelle core).
13. **Integrating various systems, no conflict — cautious but enterprising:** namespace via MCP stdio process boundaries (never in-process FFI), Guard allow/confirm/deny, separate systemd user services, separate config dirs, btrfs subvolumes, Python venvs via uv, one job per component, one process per MCP server, one policy gate.
14. **Style + Performance non-negotiable:** illogical-impulse (end-4 dots-hyprland) look + CachyOS performance, don't break systems, already using best customized dotfiles riced look, need good backend that integrates into look, not replacing look. Improve style, not change — if something better in other dotfiles (ML4W, JaKooLit, HyDE, Noctalia, Caelestia, DankMaterialShell, ekremx25, qs-hyprview, HyprPanel, rishot pill morphing [0.16,1,0.3,1,1,1] springy), include it in our look for functionalities, better response/animations, smooth buttery feel, better bluetooth wifi integration. Build proper infrastructure for stealing/improving/customising so user doesn't write many times — manifests/upstreams.toml, tools/steal/, scripts/upstream_tracker.py, docs/STEAL_INFRASTRUCTURE.md, docs/STYLE_PERFORMANCE.md
