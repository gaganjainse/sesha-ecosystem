# Multi-Agent & Orchestration Architecture

> How Shesh runs **multiple agents** without becoming an unobservable swarm. We adopt the useful
> parts of the Prime Agent RLM model, CrewAI-style role crews, and Google A2A for inter-agent
> communication — but keep governance in the Brain (SheshAOS) and local-first execution.

---

## 1. Three protocols, three directions

```
        ACP (editor ↔ agent)                 MCP (agent ↔ tools)
Zed/JetBrains ───────────► shesh-acp ──┐
                                        ├──► shesh-orchestrator ──► MCP servers
Newelle (voice/chat) ──────────────────┘           │
                                                   ├──► child agents (RLM)
A2A (agent ↔ agent) ◄──────────────────────────────┘
```

- **ACP:** editor launches an agent; agent streams edits/permissions back. (P0)
- **MCP:** every agent calls tools through the same servers. (✅ done)
- **A2A:** agents message other agents across a local bus (and optionally remote). (P1)

## 2. Agent roles (the Shesh "crew")

| Role | Model (6 GB safe) | Responsibility |
|---|---|---|
| **coordinator** | phi4-mini | Routes tasks, spawns subagents, enforces policy/audit |
| **planner** | phi4-mini | Decomposes goals into steps |
| **coder** | qwen2.5-coder:3b | Edits code, runs tests, produces diffs (ACP) |
| **researcher** | phi4-mini | web search/fetch, summarizes with citations |
| **vision** | moondream2 | screenshots/OCR/GUI understanding |
| **critic** | phi4-mini | Reviews outputs, gates promotion (eval harness) |

Roles are *configurations*, not separate programs: one binary with a role + model + tool allow-list.

## 3. RLM pattern (from Prime Agent)

The coordinator treats context as variables and subagents as function calls:

```python
# pseudocode — the Recursive Language Model style
plan = rlm("break this goal into steps", role="planner")
for step in plan:
    result = rlm(step, role=role_for(step), tools=tools_for(step))
    audit.log(step, result)
    if needs_review(step):
        critic.review(result)   # human or automated gate
```

Properties we adopt:
- **Persistent control environment** (Python REPL/daemon) so state survives a turn.
- **Subagents are real child processes** with their own context; results return as messages.
- **Background/detached sessions** for long tasks; reattach later.
- **Bounded autonomy:** token/time/turn budgets + quality gates; never unbounded `while True`.

## 4. Continual Harness (self-evolution)

The harness stores mutable **supplemental state** (not the immutable base prompt):

```
~/.local/share/shesh/harness/
├── supplemental.md       # extra system-prompt notes (refined, never base)
├── skills/               # auto-created skills (markdown + optional code)
├── memories/             # durable facts/lessons
├── subagents/            # reusable subagent specifications
└── refinements.jsonl     # append-only history: {id, trigger, edit, outcome, reverted}
```

`/refine` (port of Prime Agent):
1. **Plan** (background LLM call): read recent trajectory + failures, propose the *smallest*
   CRUD edit to harness state that would improve outcomes.
2. **Apply** at a turn boundary: write file, rebuild prompt, record outcome.
3. **Grade** with `llm-eval-harness` on a held-out check. Only promote to canary if it passes.
4. **Rollback** by refinement ID if it regresses.

The base system prompt is **immutable**. Safety/governance skills are **read-only** to refine.

## 5. Automatic skill lifecycle

Inspired by Memento-Skills (Read→Execute→Reflect→Write) and EvoSkill (frontier scoring):

1. **Capture** recurring successful patterns into a draft skill.
2. **Execute** the skill in similar contexts.
3. **Reflect** on success/failure; update.
4. **Score** against held-out tasks; maintain a top-N frontier; deprecate/archive unused or
   low-success skills ("discard the dross").
5. Skills are plain Markdown (+ optional code in `skills/<name>/`), reviewed in the settings UI.

## 6. Safety boundaries (non-negotiable)

- Every subagent inherits the Brain's policy; destructive calls still require confirmation.
- Refine **cannot** edit `policies/`, `skills/safety-governance.md`, or the audit config.
- Autonomous mode is bounded (turns/tokens/time) and writes to a disposable working tree.
- The Prime "Factorio cheating" lesson: an agent optimizing a metric may game it — so gates verify
  real outcomes, and refinements are human-reviewable before reaching `stable`.

## 7. Build order

1. `shesh-orchestrator`: process supervisor + role configs + RLM spawning over MCP (no A2A yet).
2. `shesh-harness`: CRUD state + `/refine` + rollback; skills are Markdown.
3. `shesh-acp`: expose the coordinator/coder to editors.
4. A2A local bus for subagent messaging; then optional remote.
5. Auto-skill scoring with `llm-eval-harness`, promoted through the canary gate.
