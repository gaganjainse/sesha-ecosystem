# Query Log

Every prompt from the user and the assistant's response, with links to docs
created or updated. Newest first. This anchors the project to the user's actual
intent and prevents drift.

---

## Q: "Don't ask me everything now — make a supervisor/agent that supervises you and continues automatically... Add ALL docs to shesha-ecosystem/docs, save all prompts + answers in a query doc, update docs regularly, create a complete todo list including future work."

**Answer:** Created this query log, the central TODO, the `supervisor` runbook, and
gathered all 40 docs into `docs/` (architecture, desktop, components, skills). Added
an autopilot loop (`scripts/supervise.sh`) and an agent skill
(`skills/autopilot.md`) so work continues without re-asking. Everything links back
to TODO.md.

**Docs:** [TODO.md](../TODO.md), [SUPERVISOR.md](../SUPERVISOR.md),
[skills/autopilot.md](../skills/autopilot.md)

---

## Q: "Rename everything to Shesha (from Sesha), even repos. Unarchive personal projects; only merge/delete duplicates. Do shesha-kernel → SheshaAOS merge and continue."

**Answer:** Renamed all `sesha-*` repos to `shesha-*`, `NexusAOS`→`SheshaAOS`,
`nexus-kernel`→`shesha-kernel`, `Auto-desktopenv`→`shesha-desktop` (GitHub redirects
in place). Personal projects were never archived. Folded the archived `SeshaOS`
stub into SheshaAOS. Attempted the kernel merge and found it cannot be forced
(178 commits ahead but type-diverged: 57 compile errors; base has pre-existing
russh/zig build issues) — documented a staged crate-by-crate plan instead of
pushing a broken build. Fixed a stranded rebrand where the bin dir was never
renamed.

**Docs:** [KERNEL_MERGE_PLAN](https://github.com/gaganjainse/SheshaAOS/blob/main/KERNEL_MERGE_PLAN.md),
[GLOSSARY.md](../GLOSSARY.md)

---

## Q: "We also need ACP servers, multiple agents. Research what's missing for a full ecosystem, not a demo. Steal tools and skills from the web."

**Answer:** Researched MCP/ACP/A2A and the Prime Agent RLM/Continual Harness.
Built `shesha-acp` (Agent Client Protocol server for Zed/JetBrains) and documented
the multi-agent model (coordinator/planner/coder/researcher/vision/critic) in
MULTI_AGENT.md. Cataloged mature third-party MCP servers to package rather than
rebuild (filesystem, git, fetch, playwright, github, memory, markitdown).

**Docs:** [ACP_A2A.md](../ACP_A2A.md), [architecture/MULTI_AGENT.md](../architecture/MULTI_AGENT.md),
[TOOLING_CATALOG.md](../TOOLING_CATALOG.md)

---

## Q: "There is nothing for web/coding/docs/normal things. We need many tools and skills. Deep research what we're missing."

**Answer:** Built `shesha-skills` — MCP tools for notes (markdown vault),
web search (keyless DuckDuckGo HTML) + fetch, git/github inspection, pandoc
document conversion, and reminders — plus Markdown skills: coding, web-research,
docs-writer, safety-governance, daily-briefing.

**Docs:** [components/shesha-skills.md](../components/shesha-skills.md),
[skills/](../skills/)

---

## Q: "The system should learn my intentions/habits/mannerisms and improve. Memory retention and context window are issues. Resolve this properly."

**Answer:** Built `shesha-memory`: hierarchical memory (working/episodic/
semantic/intentions/mannerisms/habits), habit learning with corroboration +
decay, and a token-bounded `ContextAssembler` that prioritizes
mannerisms→intentions→facts→habits→skills→working→relevant→recent and trims the
lowest priority first so prompts never overflow the window.

**Docs:** [LEARNING.md](../LEARNING.md), [components/shesha-memory.md](../components/shesha-memory.md)

---

## Q: "You hardcoded the system; it should learn intentions/habits and improve. Also memory/context window issues."

(Combined with the above — led to shesha-memory and the self-improvement design.)

---

## Q: "You assume the system is 24/7 live; it isn't. Don't boot mid-work. Be active/helpful/warm, not passive."

**Answer:** Built `shesha-ambient` (in shesha-desktop): a catch-up scheduler
(OnStartupSec + jitter, not fixed wall-clock; heavy jobs need AC+idle; budget
bounds), a courtesy policy that defers during fullscreen/calls/high-CPU/low
battery, and a proactivity engine that makes one optional offer at a natural
pause (45s–15m idle), throttled to ≤3/day, snoozeable.

**Docs:** [desktop/AMBIENT_DESIGN.md](../desktop/AMBIENT_DESIGN.md)

---

## Q: "I got a workspace-over-budget notification. Proceed to phase 2."

**Answer:** Cleaned heavy caches/venvs, then split out three standalone
component repos — `shesha-files` (Rust watcher + classifier), `shesha-shell`
(Hyprland MCP), `shesha-system` (power/GPU/backup MCP) — each with its own
tests and CI, replacing the monolithic tools dir.

**Docs:** [architecture/REPO_TOPOLOGY.md](../architecture/REPO_TOPOLOGY.md)

---

## Q: "Integrate everything so I can change settings in the GUI, not code. Don't break the style. Test each setting/function in a container."

**Answer:** Added a `shesha` config object to end-4's existing Quickshell
settings system and a matching **Sesha settings page** (`SeshaConfig.qml`) in
the same widget style as General/Bar/Services. A `Sesha.qml` service applies
toggles to systemd units and hyprctl. All changes are in the dotfiles repo.

**Docs:** [desktop/06_SESHA_AGENT.md](../desktop/06_SESHA_AGENT.md)

---

## Q: "Choose the languages we use; minimize FFI overhead/complexity/debugging/security risks."

**Answer:** Five core languages, each for one job — Rust (brain/kernel/watchers),
Python 3.11+ (AI glue/MCP), Lua (Hyprland config only), QML/JS (Quickshell UI),
Bash 5+ (installer/glue). No Zig/C/Mojo/Go; cross-language talk is MCP/JSON
over process boundaries, never in-process FFI. Exotic runtimes go in rootless
Podman/Distrobox.

**Docs:** [architecture/LANGUAGE_POLICY.md](../architecture/LANGUAGE_POLICY.md),
[CONTAINERS_AND_VENV.md](../CONTAINERS_AND_VENV.md)

---

## Q (earlier): "Fix the bugs and make it a real system, not a demo."

**Answer:** Audited and fixed: undefined AUR_HELPER, missing `bc` dep, MSI DMI
content check, RAM-detected zram, MCP iterating real files, license (MIT→GPL-3),
typos, redirect order; added real system tools, device profile, FHS/XDG layout,
rootless Podman + uv environments, and the federated ecosystem manifest with
quality gates and canary CI.

**Docs:** [desktop/01_AUDIT.md](../desktop/01_AUDIT.md),
[GAP_ANALYSIS.md](../GAP_ANALYSIS.md)

---

## Q (autopilot): "Start the work on autopilot."

**Answer:** Began autonomous work per the supervisor. Implemented
`shesha-mind` — the model router: maps roles (primary/planner/coder/researcher/
vision/critic/embedding) to 6 GB-safe Ollama models with VRAM budgeting, a
fallback chain, session planning that minimizes distinct loaded models, and an
injectable Ollama client. MCP tools `select_model`/`plan_session`/`list_roles`/
`set_model_for_role`/`list_installed_models`. 13 offline tests, ruff clean,
pushed to gaganjainse/shesha-mind and added to the ecosystem manifest.

**Docs:** [components/shesha-mind.md](../components/shesha-mind.md), TODO.md

---

## Q (autopilot cont.): (continue)

**Answer:** Added a reusable `Guard` to shesha-audit that any MCP server imports
to check + log each tool action against policy (allow/confirm/deny). 4 new tests
(15 total). This is the integration point that makes the Brain govern every Soma
tool call. Next: ACP full session support (streaming, permissions, diffs).

---

## Q (autopilot cont. 2): (continue)

**Answer:** Built `shesha-mind` model router (13 tests) and shipped it. Added a
reusable policy `Guard` to shesha-audit (15 tests). Extended shesha-acp with
session/cancel and permission-response, and fixed an incomplete package rename.
All pushed; component READMEs centralized in docs/components.

**Docs:** components/shesha-mind.md, components/shesha-audit.md, components/shesha-acp.md

---

## Q (autopilot cont. 3): (continue)

**Answer:** Built `shesha-backup` (restic wrapper with AC+daily gating,
snapshot verification, and explicit prune; 8 offline tests) and pushed.
Extended ACP with session cancel + permission responses and fixed an incomplete
package rename. The Brain policy Gate is now reusable across components.

**Docs:** components/shesha-backup.md, components/shesha-acp.md

---

## Q (autopilot cont. 4): (continue)

**Answer:** Built `shesha-phone` (ADB wrapper with safe-area bounds, taps/
swipes/text/screenshots, injectable runner; 7 tests) for the Realme Narzo target.
All component READMEs synced to docs/components. Ecosystem now has 15 components
across Brain/Mind/Soma with 138 tests.

---

## Q: "Have you done these? Are phases in pipeline? Search the whole chat for dropped items."

**Answer:** Honest audit: items 1 (ecosystem), 2 (component split — all 12),
and 5 (Arch canary) were done. Item 3 (shesha-voice) was MISSING — the Newelle
fork was never renamed or given an overlay; fixed now (renamed to shesha-voice,
added MCP config + default model + wake word). Item 4 was partial: shesha-audit
existed standalone but the **NexusAOS event-store bridge was missing**; added a
NexusBridge that emits events in the Rust EventKind format from the Guard.
Added a TODO status section so nothing is silently dropped.

**Docs:** components/shesha-voice.md, GLOSSARY, TODO (Status vs original plan)

---

## Q: "Okay then do the work"

**Answer:** Implemented P0: enforce the shesha-audit Guard at every MCP
boundary. Added `GuardedMCP(FastMCP)` in shesha-audit — a middleware that
policy-checks every tool call before execution, denies protected paths, logs
each decision + result, and emits SheshaAOS-format Nexus events. Wired it into
all 8 MCP servers (shell, system, skills, memory, harness, orchestrator, mind,
backup) with a graceful fallback to plain FastMCP if audit isn't installed,
and added shesha-audit as a dependency. 2 new middleware tests (20 total in
audit); full suite: 113 component tests green. Renamed packages to shesha_* on
the way through.

**Docs:** TODO.md, components/shesha-audit.md

---

## Q: "Okay" / "Continue" (autopilot)

**Answer:** Implemented P0: LLM-backed planner/critic in shesha-orchestrator.
New `LLMAgents` calls Ollama (model chosen per role by shesha-mind); the planner
parses strict JSON steps, role agents execute, the critic returns an
approved/notes verdict. Balanced JSON extraction (fenced + brace scan). All
fall back to deterministic stubs on bad JSON/offline; `execute(use_llm=False)`
forces stubs; `llm_status()` reports live vs fallback. 9 new tests (18 total),
pushed; shesha-mind added as a dependency.

**Docs:** components/shesha-orchestrator.md, TODO.md

---

## Q: "Continue" (autopilot)

**Answer:** Implemented P0 canary e2e test (`scripts/e2e-canary.sh`): installs
all 12 components, imports every server module, verifies the audit Guard denies
protected paths, memory assembles a bounded context, orchestrator enforces its
budget and runs 3 stub steps, ACP does a session/prompt round-trip, and backup
reports status. Wired into daily canary CI. Fixed two false imports along the
way (shesha-files is a flat `classifier` module; shesha-memory has no `log.py`).
All 3 P0s now done; remaining 🔴 items are the kernel merge (needs careful Rust
work) and hardware tests (need the physical MSI).

**Docs:** scripts/e2e-canary.sh, .github/workflows/canary.yml, TODO.md

---

## Q: "Continue" (autopilot)

**Answer:** Built `scripts/generate_mcp_config.py` — reads the manifest and
emits canonical `servers.json` plus Zed (`context_servers`) and Newelle
(`mcp-servers`) configs filtered by channel. Correctly excludes non-MCP
components (desktop fork, voice fork, ACP) and maps each repo to its console
script. 5 new tests (18 ecosystem tests total); wired into the repo. This
connects all the components into a working MCP mesh instead of isolated
servers.

**Docs:** scripts/generate_mcp_config.py, components connected via generated config

---

## Q: "Continue" / interruptions (autopilot)

**Answer:** Added system maintenance/health/update tools to shesha-system:
`check_system_updates` (read-only, never auto -Syu), `clean_system_caches`
(user/pacman/journal, opt-in with sudo noted), `system_health` (disk, failed
units, load, temps, cache sizes). Robust df parsing. 6 new tests (13 total).
Also shipped the MCP config generator earlier (9 servers, Zed/Newelle outputs).

**Docs:** components/shesha-system.md, TODO.md

---

## Q: "Continue in Autocomplete mode"

**Answer:** Built the A2A Unix-socket transport: a 0600-permission UDS broker
with line-delimited JSON, role-based routing, broadcast events, and
sender-excluded fan-out, plus `serve/send/listen`. In-process bus stays for
tests. 3 new tests (21 total). Also added system maintenance/health/update
tools and the MCP config generator in prior ticks.

**Docs:** architecture/MULTI_AGENT.md, components/shesha-orchestrator.md

---

## Q: "Continue" / fix busy-and-overflow issues

**Answer:** Shipped `shesha-mcp-bundle`: proxies upstream filesystem/fetch/git
MCP servers (npx/uvx) through the Guard, with tool prefixing (fs_*, fetch_*,
git_*), handshake, skip-if-missing, and 4 offline tests. Added A2A Unix socket
and system maintenance/health tools in prior ticks.

**Infra note on interruptions/memory:** the "AI service busy" errors are
upstream rate/load — mitigated by batching tool calls and smaller commits.
Container overflow came from the Rust toolchain + large clones; removed
~/.cargo, ~/.rustup, target/, and caches, and keep work in the components/
tree (not gh-mirror).

---

## Q: "Continue in Autocomplete mode"

**Answer:** Added persistent reattachable sessions to shesha-orchestrator:
a `SessionManager` runs Orchestrator executions in background threads, tracks
goal/status/trace/result/error, and exposes MCP tools start_session/get_session/
list_sessions/cancel_session. Cancellation is checked before/after each step;
failures are recorded. 4 new tests (25 total). Also fixed the A2A handshake-once
bug and JSON-RPC result unwrapping along the way.

**Docs:** components/shesha-orchestrator.md, TODO.md

---

## Q: "Continue where you left off" (autopilot)

**Answer:** Added persistent reattachable sessions to the orchestrator
(SessionManager + start/get/list/cancel MCP tools, 25 tests) and built
`shesha-containers` (unprivileged podman/distrobox sandboxed execution with
--cap-drop=ALL/--network=none/pids-limit, plus list/pull/set_engine; 5 tests).
Both pushed; ecosystem manifest/TODO updated.

**Docs:** components/shesha-containers.md, TODO.md

---

## Q: 👍 (continue)

**Answer:** Built episodic memory compaction (`shesha-memory`): summarizes old
episodes into semantic.md in batches, trims to a retention window, with an
injectable summarizer (LLM in prod) and `compact_memory` MCP tool (5 new tests,
20 total). Also shipped shesha-containers (sandboxed podman MCP) and persistent
sessions earlier this run.

**Docs:** components/shesha-memory.md, TODO.md

---

## Q: "Start, I am ready anytime"

**Answer:** Implemented the held-out evaluator for /refine (shesha-harness):
structural validation + weighted must_contain/must_not_contain checks scored
0..1 against a min_score gate, with the refinement applied as system context
during replay. Added make_ollama_responder() for local model scoring, wired it
into propose_and_apply via a responder, and exposed refine_with_llm MCP. 7 new
tests (14 total). Also shipped episodic compaction and data-aware ambient
signals earlier this run.

**Docs:** components/shesha-harness.md, TODO.md

---

## Q: "Okay" (continue)

**Answer:** Built semantic retrieval for shesha-memory: pluggable Embedder
(local deterministic hash for offline, Ollama nomic-embed-text for real
semantics), a SQLite VectorStore with cosine search, and MCP tools
semantic_search/index_memory. 6 new tests (26 total). Also shipped the
held-out /refine evaluator earlier this run.

**Docs:** components/shesha-memory.md, TODO.md

---

## Q: "Continue on autocomplete, don't stop"

**Answer:** Shipped: data-aware ambient signals wired into offer_for_moment;
shesha-calendar (iCal vdir MCP, 6 tests); ACP terminal/exec + fs/diff with
confirmation for dangerous commands (3 tests); local JSONL trace recorder
wired into sessions with recent_traces MCP (3 tests). Ecosystem manifest,
TODO, and query log updated.

**Docs:** components/*.md, TODO.md

---

## Q: "Continue on autocomplete, don't stop"

**Answer:** Shipped: local JSONL trace recorder + session tracing; ACP
terminal/exec and fs/diff with confirmation; shesha-calendar (iCal vdir MCP);
extended canary e2e to cover all 15 components; shesha-secrets multi-backend
resolver (env/gopass/keepassxc/file, refuses world-readable files). All
tested and pushed.

**Docs:** components/*.md, scripts/e2e-canary.sh, TODO.md

---

## Q: "Make a document of every manual thing I need to check myself, from the
start of the session; divide into sections; update it regularly."

**Answer:** Created `docs/MANUAL_VERIFICATION.md` — 12 sections: first boot,
accounts/keys/secrets, MCP mesh, voice, GPU/power/MUX, display, backup, phone,
containers, agent behavior, security/audit, canary/releases, plus the deliberate
non-autopilot items (kernel merge, hardware validation) and a one-command health
check. Linked it from AUDIT_AND_ROADMAP. Will keep it current each run.

**Docs:** MANUAL_VERIFICATION.md (new), AUDIT_AND_ROADMAP.md
