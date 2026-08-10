# Glossary

The Shesh ecosystem uses these terms consistently.

## Name

**Shesh** (शेष) — from Shesh Naag, the many-headed serpent on which Vishnu
rests; the many-headed agent whose "heads" are its specialist subagents. The
desktop agent and all components are spelled **shesh-** (lowercase for repos
and packages), **Shesh** in prose.

## Acronyms

| Term | Meaning |
|---|---|
| **AOS** | Agentic Operating System — the governance/runtime layer (SheshAOS) |
| **AB** | Agentic Body — the full Brain+Mind+Soma system |
| **AM** | Agentic Mind — deliberative models, planning, memory, learning |
| **AI** | Agentic Intelligence — the reasoning/model capability (distinct from the generic "AI") |
| **AS** | Agentic Soma — sensors and actuators (desktop, phone, tools) |
| **AP** | Agentic Physique — the hardware/device profile (MSI Sword, etc.) |
| **OS** | Operating System (CachyOS/Linux underneath it all) |

## The three layers (the Body)

- **Brain** — governance kernel (`shesh-audit`, `SheshAOS`): event store,
  policy, scheduling. Models propose; the kernel disposes.
- **Mind** — deliberation (`shesh-mind`, `shesh-memory`, `shesh-harness`,
  `shesh-orchestrator`, `shesh-skills`): model routing, memory, self-improvement.
- **Soma** — the body (`shesh-voice`, `shesh-files`, `shesh-shell`,
  `shesh-system`, `shesh-acp`, `shesh-phone`): sensors/actuators over MCP.

## Protocols

- **MCP** (Model Context Protocol): agent ↔ tools.
- **ACP** (Agent Client Protocol): editor ↔ agent (Zed/JetBrains).
- **A2A** (Agent2Agent): agent ↔ agent (local bus now, remote later).
- **JSON-RPC**: wire format for all three over stdio/sockets.

## Components vs products

Each `shesh-*` repository is a component. They integrate into the
**shesh-ecosystem** manifest and run on **shesh-desktop** (the CachyOS/Hyprland
dotfiles fork).
