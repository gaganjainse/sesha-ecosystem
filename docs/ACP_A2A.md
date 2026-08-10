# ACP & A2A Integration

Two protocols Shesh adopts alongside MCP so it can live in editors and coordinate agents.

## ACP — Agent Client Protocol (Zed/JetBrains)

- **Direction:** editor (client) ↔ coding agent (server). JSON-RPC 2.0 over stdio.
- **Why:** implement once, run in Zed, JetBrains, Neovim, Emacs without per-editor plugins.
- **vs MCP:** ACP is the outer layer (human-in-editor driving the agent); MCP is the inner
  layer (agent calling tools). We run both.
- **Component:** `shesh-acp` (P0).

Minimum ACP surface we implement:
- `initialize` / capability negotiation.
- `session/new`, `session/prompt` with **streaming** token updates.
- `fs/read_text_file`, `fs/write_text_file`, `fs/list`, terminal create/exec (permission-gated).
- `session/request_permission` before edits/commands (human-in-the-loop).
- Progress + diff updates so the editor shows changes.

The ACP server spawns `shesh-orchestrator` (coder role) as its agent, handing it the MCP
endpoint list. All actions still flow through the Brain policy/audit.

Reference: https://agentclientprotocol.com (Zed Industries).

## A2A — Agent2Agent (Google/Linux Foundation)

- **Direction:** agent ↔ agent across processes/trust boundaries.
- **Why:** lets Shesh's specialist subagents talk directly (coordinator→researcher→critic) and,
  later, lets remote agents participate without us inventing a protocol.
- **Component:** `shesh-orchestrator` speaks A2A on a local Unix socket (P1).

We use A2A for **local agent messaging first**; remote/cross-org A2A is off by default and requires
explicit opt-in + the cloud tier.

## Protocol layering (the complete nervous system)

```
Editor (Zed/JetBrains)
   │ ACP (stdio JSON-RPC, streaming, permissions)
   ▼
shesh-acp ──► shesh-orchestrator (coordinator)
                   │  A2A (local socket)   ┌─ planner ─┐
                   ├──────────────────────►┤ coder      │
                   │                       │ researcher │  each over
                   │                       │ vision      │  MCP to tools
                   │                       └─ critic ────┘
                   ▼
              Brain (SheshAOS policy + audit event log)
                   │ MCP (stdio JSON-RPC)
                   ▼
   shesh-files / shesh-shell / shesh-system / shesh-skills / ...
```

## Security

- ACP permission requests map 1:1 to Brain policy classes (auto/confirm/deny).
- A2A agents authenticate over the Unix socket (peer credentials) + a per-session token.
- No agent ever gets broader filesystem/tool access than its role's allow-list.
