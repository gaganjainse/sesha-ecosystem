# Gap Analysis — from demo to full ecosystem

> Rigorous audit (2026-08-09) of what exists vs what a real, evolving, world-integrated
> AI operating environment needs. Each gap is rated P0 (blocker), P1 (soon), P2 (later), with
> a concrete home component. This is the backlog that makes Shesh self-improving rather than static.

Legend: ✅ exists · 🟡 partial · ❌ missing

---

## 1. Protocols (the "nervous system")

| Need | Status | Gap / action |
|---|---|---|
| MCP (agent→tools) | ✅ | 3 servers live + shesh-skills |
| **ACP (editor→agent)** | ❌ **P0** | Need a `shesh-acp` server so Shesh runs inside Zed/JetBrains/Neovim with file/terminal/diff/permission UX. MCP and ACP stack, not compete. |
| **A2A (agent→agent)** | ❌ P1 | Multi-agent coordination across trust boundaries; adopt Google A2A rather than inventing. |
| JSON-RPC (brain internal) | ✅ in SheshAOS | `shesh-rpc` already used; wire Brain↔Soma over it. |
| Event stream / audit | 🟡 | Log exists conceptually; need `shesh-audit` component (append-only, hash-chained, queryable). |
| Streaming (voice/UI) | 🟡 | Newelle streams TTS/STT; our MCP servers are request/response; add SSE/streaming for long tasks. |

## 2. Agent topology (the "mind")

| Need | Status | Gap / action |
|---|---|---|
| Single primary agent | ✅ Newelle |
| **Specialist subagents** | ❌ **P0** | coder/planner/reviewer/vision roles (SheshOS thesis). Build `shesh-orchestrator` with RLM-style `rlm("subtask")` spawning child agents. |
| **Role-based crews** | ❌ P1 | Researcher→writer→reviewer pipelines (CrewAI model) for docs/research. |
| **Persistent/background agents** | ❌ P1 | Daemon-backed sessions that survive disconnect (Prime Agent pattern); long goals + heartbeats. |
| Agent-to-agent messaging | ❌ P1 | Direct message bus between running agents. |
| Human-in-the-loop | 🟡 | Policy asks for destructive actions; need ACP permission UX + approvals queue. |
| Multiple model routing | 🟡 | `shesh-mind` declared; implement router (planner/coder/vision selection by task). |

## 3. Self-evolution (the "learn & discard dross" requirement)

| Need | Status | Gap / action |
|---|---|---|
| Immutable base prompt | ✅ principle |  |
| **Continual Harness (CRUD state)** | ❌ **P0** | Mutable supplemental prompts/skills/memories/subagent specs as durable state the agent can refine. Port Prime Agent's pattern. |
| **`/refine` evidence loop** | ❌ **P0** | Read trajectory → propose smallest evidence-backed edit → apply at turn boundary → record trigger/outcome. Never mutate base. |
| Rollback of refinements | ❌ P1 | Refinement history with IDs; revert bad harness updates. |
| **Automatic skill creation** | ❌ P1 | "Read→Execute→Reflect→Write" (Memento-Skills); turn repeated wins into reusable skills. |
| Frontier-based skill evolution | ❌ P2 | EvoSkill/GEPA: mutate skill/prompt, score on held-out tasks, keep top-N. |
| Discard/deprecation | ❌ P1 | Track skill usage/success; auto-archive low-value ones ("discard the dross"). |
| Reflection on failure | ❌ P1 | Failure traces → proposed fixes (Memento pattern). |
| Eval harness for changes | ❌ P1 | Wire `llm-eval-harness` so refinements are graded before promotion (canary gate). |
| Memory (episodic/semantic) | 🟡 | `shesh-memory` declared; build RAG + entity memory + Chroma/vector store. |

## 4. World integration ("integrate, don't isolate")

| Need | Status | Gap / action |
|---|---|---|
| Web search | ✅ shesh-skills (keyless DDG) |
| Web fetch | ✅ |
| Browser automation | ❌ P1 | Package Playwright MCP (sandboxed) for JS sites/testing. |
| GitHub | 🟡 | `github_view` read-only; add GitHub MCP (issues/PRs/CI) with PAT, scoped. |
| Email/calendar/contacts | ❌ P1 | Local-first CalDAV/IMAP (`vdirsyncer`/`khal`/`neomutt`), not cloud-locked. |
| Messaging (Telegram/WhatsApp/Signal) | ❌ P2 | Optional bridges; treat as separate services. |
| Phone (Realme Narzo) | 🟡 declared | `shesh-phone` ADB harness needs implementation. |
| Editor/IDE | ❌ **P0** | ACP server (above). |
| Docs conversion (PDF/Office) | ✅ pandoc |
| Obsidian/notes | ✅ notes vault |
| Containers/sandboxing | ❌ P1 | `shesh-containers`: podman/distrobox control for untrusted code. |
| Cloud fallback | 🟡 policy exists | OmniRoute/LiteLLM proxy behind explicit opt-in. |

## 5. Soma/desktop completeness

| Need | Status | Gap / action |
|---|---|---|
| Power/GPU/MUX | ✅ shesh-system |
| Hyprland control | ✅ shesh-shell |
| File organizer | ✅ shesh-files |
| Voice/wake word | ✅ shesh-voice (Newelle) |
| Display/GPU runtime validation | ❌ P1 | Hardware smoke test suite (can't run in this sandbox). |
| Backup (real restic) | 🟡 script referenced; implement + verify. |
| Scheduling/reminders | ✅ basic |
| Media/screenshots/recording | ❌ P2 |  |
| Accessibility (a11y) | ❌ P2 |  |

## 6. Platform/infrastructure

| Need | Status | Gap / action |
|---|---|---|
| Component repos | ✅ 4 live |
| Ecosystem manifest + locks + gates | ✅ |
| Cross-distro CI | 🟡 canary workflow defined; add ACP/multi-agent tests |
| **Canary integration tests** | ❌ P1 | Spin up MCP+ACP+orchestrator in a container; assert end-to-end. |
| Reproducible dev envs | 🟡 documented | Provide a `distrobox assemble`/Containerfile for onboarding. |
| Secret management | ❌ P1 | KeePassXC/gopass integration; never put keys in config/MCP. |
| Telemetry/observability | ❌ P1 | OpenTelemetry traces + journal; local only. |
| Supply-chain security | 🟡 lockfiles; add sigstore/provenance |  |
| Installer/updater | 🟡 setup exists | Need channel-based update (stable/canary/devel) with rollback snapshots. |
| Documentation | ✅ extensive | Keep ADRs for each protocol decision. |

## 7. Immediate P0 backlog (next builds)

1. **`shesh-acp`** — minimal ACP server: session init, prompt turn streaming, permission
   requests, file/terminal bridge. Lets Shesh work in Zed/JetBrains.
2. **`shesh-orchestrator`** — multi-agent runtime: RLM subagent spawning, role routing,
   agent-to-agent messaging, persistent sessions, heartbeats/goals (Prime Agent patterns).
3. **`shesh-harness`** — the Continual Harness: durable CRUD state + `/refine` + rollback +
   automatic skill creation, gated by `llm-eval-harness`.
4. **`shesh-audit`** — append-only hash-chained event log + policy engine (bridge to SheshAOS).
5. **Canary end-to-end test** — container that boots all servers and runs a real task.

P1 follows: memory, browser/GitHub MCP packaging, email/calendar, phone, containers,
observability, secret manager, hardware tests.

The rest of this document set adds the architecture and specs for items 1–4.
