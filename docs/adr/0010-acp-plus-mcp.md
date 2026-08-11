# ADR-0010: ACP Adopted Alongside MCP

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** protocols, editor, mcp, acp

## Context
MCP = agent ↔ tools (shell, files, memory). But editors (Zed, JetBrains) need agent ↔ editor protocol: sessions, file view, diffs, terminal, permission prompts. Inventing our own would be NIH; Agent Client Protocol (ACP) from Zed is precisely that.

We need both:
- Tools (filesystem, power, backup) → MCP
- Editor integration (code edits, terminal) → ACP
- Agent-to-agent → A2A

## Decision
- **Stack them**: MCP for tools, ACP for editor, A2A for agent→agent. All JSON-RPC over stdio/UDS.
- Implement `shesh-acp`:
  - Session init, prompt streaming, cancellation.
  - Permission responses (allow/deny/destructive confirmation).
  - Terminal bridge (`terminal/exec`).
  - Fs + diff messages (`fs/read`, `diff/apply`).
- ACP server is NOT an MCP server — excluded from `servers.json` (checked in `generate_mcp_config.py`).
- Wire ACP traces into same JSONL recorder as MCP traces (`recent_traces` MCP tool).

## Consequences
- ✅ Zed/JetBrains can host Shesh with streaming + permission UX.
- ✅ MCP mesh remains clean — 9 servers in `servers.json`, ACP separate.
- ✅ e2e canary tests ACP session/prompt round-trip.
- ❌ ACP spec evolving — need to track `agent-client-protocol` repo via upstream tracker.
- ❌ Real editor testing needs manual verification (MMSI hardware).

## Links
- `docs/ACP_A2A.md`, `docs/architecture/MULTI_AGENT.md`
- `shesh-acp`, `scripts/generate_mcp_config.py`
