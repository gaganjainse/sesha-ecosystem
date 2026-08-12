# The Agentic Body: Brain + Mind + Soma

> The unifying thesis behind the Shesh ecosystem, derived from your SheshAOS/SheshOS/shesh-kernel
> work. **An agent is not a chatbot — it is a body.** A body has a *mind* (reasoning/planning),
> a *brain* (reflexes, coordination, governance), and a *soma* (sensors and actuators in the real
> world). We build each layer as a replaceable component, then compose them.

This is the conceptual map every other document in the ecosystem references.

---

## 1. The three layers

```
┌─────────────────────────────────────────────────────────────┐
│  MIND — deliberative cognition                              │
│  Planner · reasoner · critic · long-term memory · theory    │
│  of self · model routing · goals. Slow, model-driven.       │
│  (SheshOS specialist models: planner / coder / vision)      │
├─────────────────────────────────────────────────────────────┤
│  BRAIN — coordination kernel (SheshAOS)                     │
│  Event store · policy/permission engine · task scheduler ·  │
│  router · audit/replay · resource budgets · tool broker.    │
│  Fast, deterministic, local. Models propose; brain disposes.│
├─────────────────────────────────────────────────────────────┤
│  SOMA — the living body (shesh-desktop + MCP + devices)   │
│  Sensors: screen, mic, files, input, phone, telemetry.      │
│  Actuators: hyprctl, shell, apps, GPU, voice, ADB phone.    │
│  The "nervous system": MCP servers, watchers, automations.  │
└─────────────────────────────────────────────────────────────┘
```

### Why split it this way
- **MIND** is allowed to be nondeterministic, slow, model-bound, and swappable (Gemma/Qwen/phi4).
- **BRAIN** must be deterministic, auditable, crash-proof, and local. This is exactly SheshAOS:
  *"models propose actions; the kernel validates and records."* It is the immune system — it stops
  the mind from doing damage.
- **SOMA** is where cognition meets the machine. It is the biggest surface and where most of the
  best open-source projects (Newelle, MCP servers, computer-use agents) already live. We don't
  rebuild it; we integrate it, behind the brain's policy gate.

---

## 2. Mapping to your existing repositories

| Layer | Your repo | Role in the Body | Status |
|---|---|---|---|
| **BRAIN** | `SheshAOS` (12-crate Rust workspace, 981 tests) | Governance kernel: event store, policy, scheduler, router, tool broker, RPC/terminal | production-ready core, Ubuntu-targeted |
| **MIND** | `SheshOS` (SheshAOS v2) | Specialist-model routing: planner (Gemma 4 12B), coder (Qwen3-Coder 30B), vision (Qwen3.5 9B) | architecture brief + bootstrap |
| **BRAIN (low-level)** | `shesh-kernel` | Alpha microkernel track; same crate family + protocols crate; deeper kernel design | alpha |
| **SOMA (desktop)** | `shesh-desktop` | CachyOS/Hyprland body: dotfiles, MCP servers, smart-organizer, GPU, automations | this ecosystem's main integration target |
| **SOMA (memory)** | `rag-service` | Sensory memory: hybrid RAG (dense+BM25+RRF) over ChromaDB | production API |
| **MIND (quality)** | `llm-eval-harness` | Reflection/self-check loop for the mind (LLM-as-judge) | CI-ready |
| **SOMA (language)** | `Vyākṛti` | (separate creative project) Sanskrit programming language/IDE — not part of the body but dogfoods the agent | 123 tests |

> Note: `SheshOS` README targets Ubuntu/GNOME and 16 GB RAM with three large models (12B/30B/9B).
> Your actual machine (RTX 4050 6 GB) cannot resident those simultaneously. The ecosystem resolves
> this by making the **Mind layer model-routed**: on the laptop, use small models
> (phi4-mini / qwen2.5-coder:3b / moondream2); the same protocols target the larger SheshOS models on
> a future bigger box or when offloaded. The Brain doesn't care which model answers.

---

## 3. The nervous system: how layers talk

Two protocols only (everything else is an adapter):

1. **Nexus Kernel Protocol** (from `shesh-rpc`, JSON-RPC over Unix socket) — Brain-internal and
   Brain↔Mind. Strongly typed, append-only event semantics, policy-checked.
2. **Model Context Protocol (MCP 2026-07-28)** — Brain↔Soma. Every actuator/sensor is an MCP
   server (stdio locally; HTTP only when explicitly bridged). This lets us reuse the entire MCP
   ecosystem (Newelle, Goose, Hermes, pi, etc.) as interchangeable Soma organs.

Data flow for "Hey Shesh, organize my downloads and switch to performance mode":
```
mic (Soma) → STT (Soma/Newelle) → text
  → MIND: parse intent, propose tool calls {organize_downloads, set_power(performance)}
  → BRAIN: policy check (both auto-allowed), append events, assign task IDs
  → SOMA: MCP calls smart-organizer.organize() + system_control.set_power()
  → Soma sensors observe result (file list, powerprofilesctl)
  → MIND: formulates confirmation → TTS (Soma) → audit event committed
```
Every arrow is an event in the append-only log. Nothing the mind proposes is executed until the brain
validates it. This is the governance guarantee inherited from SheshAOS.

---

## 4. Build order (body grows bottom-up, but is safe top-down)

Per `shesh-kernel`'s own phased plan (event store → kernel runtime → resource budgets → model
providers → tool broker → IPC/MCP/ACP):

1. **Soma first (this ecosystem):** make the body reliable — dotfiles, MCP servers, organizer,
   automations, voice. A body you can trust.
2. **Brain wiring:** connect Shesh's audit log to SheshAOS's event store; route MCP tool calls
   through `shesh-kernel` policy instead of Newelle executing directly.
3. **Mind specialists:** plug SheshOS model routing into `shesh-ai`'s provider abstraction; use
   `llm-eval-harness` to grade each specialist.
4. **Reflection loop:** the mind uses the audit log + eval harness to propose improvements to skills
   (the "Continual Harness" idea — small, evidence-backed updates, never mutating the base prompt).
5. **Kernel track (research):** eBPF sensing for Soma, then `shesh-kernel` experiments on the side.

We never block step 1 on step 4. The body ships and is useful immediately; the brain plugs in
behind it without changing how Soma works.

---

## 5. Naming conventions (everything is ours)

- **No "Jarvis".** The agent is **Shesh** (शेष) across all layers.
- **Nexus** = the brain/kernel family (SheshAOS, shesh-kernel, shesh-* crates).
- **Shesh** = the whole body / the user-facing agent (SheshOS = the mind spec, shesh-* MCP organs).
- **Soma** = the bodily/device layer codename (soma-* sensors/actuators).
- Components we integrate keep their **upstream names** in `sources/upstream/` (attribution), but our
  forks and wrappers are renamed: `shesh-voice` (wraps Newelle voice), `shesh-files` (organizer),
  `shesh-shell`, `shesh-memory`, `shesh-phone`, etc.
- Every MCP server is `shesh-<organ>-mcp`. Every systemd unit is `shesh-<organ>.service`.
