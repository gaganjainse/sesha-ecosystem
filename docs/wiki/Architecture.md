# Architecture

Shesha follows a **federated, local-first** design: small components
communicate over Model Context Protocol (MCP), governed by an audit log
and a policy engine. Nothing in the core requires the cloud.

## Layers

```
┌─────────────────────────────────────────────┐
│  Soma (body)   voice · desktop · files ·    │
│                shell · system · backup ·    │
│                phone · containers · mcp     │
├─────────────────────────────────────────────┤
│  Mind (agents) orchestrator · memory ·      │
│                mind · harness · skills ·    │
│                calendar · embeddings        │
├─────────────────────────────────────────────┤
│  Brain (governance)                         │
│   SheshaAOS (Rust)  ←→  shesha-audit       │
│   event-sourced kernel · policy Guard       │
└─────────────────────────────────────────────┘
```

### Brain (governance)

- **SheshaAOS** — Rust workspace of 12 crates; event-sourced task/tool/model
  state. This is the long-term system of record.
- **shesha-audit** — append-only, SHA-256 chained event log; a `GuardedMCP`
  wrapper that policy-checks every tool call and emits SheshaAOS-compatible
  events. Also resolves secrets via `shesha-secrets`.

### Mind (agents)

- **shesha-orchestrator** — RLM-style multi-agent runtime: a coordinator
  plans, delegates by role (researcher/coder/vision/critic), runs in
  background sessions with A2A messaging.
- **shesha-mind** — role-to-model routing for the 6 GB VRAM budget, with
  fallback and session planning.
- **shesha-memory** — episodic JSONL + SQLite FTS, semantic vector store,
  habits, intentions, compaction/retention.
- **shesha-harness** — conservative self-improvement: immutable base prompt,
  evidence-backed refinements scored by held-out checks, revertible.
- **shesha-skills** — everyday tools (notes, web, code, docs, reminders) and
  Markdown skills.
- **shesha-calendar** — local iCalendar vdir reader (vdirsyncer/khal).

### Soma (body)

- **shesha-voice** — fork of [Newelle](https://github.com/qwersyk/Newelle) with
  an overlay wiring all MCP servers, wake word, STT/TTS.
- **shesha-desktop** — Hyprland dotfiles, Quickshell UI, ambient offers.
- **shesha-files / shell / system / backup / phone / containers / mcp-bundle**
  — the MCP servers that touch the machine.

## Protocols

- **MCP** (stdio) between every component and clients.
- **ACP** for editor integration (Zed/JetBrains): `initialize`,
  `session/new`, `session/prompt`, `terminal/exec`, `fs/diff`.
- **A2A** over a Unix socket for cross-process agent messaging.
- Events flow into the audit log / SheshaAOS as JSON.

## Why federated?

Each component is independently versioned, tested, and replaceable. The
ecosystem repo's manifest resolves a coherent set, the canary gate tests
them together nightly, and stable/canary/devel channels promote changes
safely. A bug in one server cannot compromise the whole system because the
Guard enforces policy at every boundary.
