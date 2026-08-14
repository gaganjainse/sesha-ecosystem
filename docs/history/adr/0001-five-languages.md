# ADR-0001: Five Languages Only

**Date:** 2026-08-09
**Status:** Accepted
**Decision makers:** Gagan Jain, Shesh Autopilot
**Tags:** language, ffi, complexity

## Context
The ecosystem spans a governance kernel, AI glue, desktop compositor config, UI shell, and installer scripts. Earlier prototypes mixed Rust, Python, Go, Zig, C, Lua, QML, TypeScript — leading to FFI nightmares, cross-toolchain build failures (e.g., `russh::Error::msg` API break, Zig required by terminal crate), and hard-to-audit unsafe boundaries.

We need to cover:
- Systems/performance + safety → Rust
- AI orchestration, MCP, RAG, embeddings → Python
- Hyprland config → Lua (required by Hyprland ≥0.55)
- Quickshell UI → QML/JS (Qt6 declarative)
- Installer/glue → Bash 5+

## Decision
We allow **only five core languages** in-tree:
- **Rust** (brain, kernel, watchers)
- **Python 3.11+** (mind, MCP servers)
- **Lua** (Hyprland config only)
- **QML/JS** (Quickshell)
- **Bash** (installer)

No Zig, C, Mojo, Go in the main build. Cross-language communication is **MCP/JSON over process boundaries**, never in-process FFI.

Exotic runtimes (Node for some MCP servers, Go tools) run in **rootless Podman/Distrobox**, not on host.

## Consequences
- ✅ Build matrix is 2 toolchains (Rust + Python) on host; reproducible.
- ✅ Auditable unsafe boundary: only MCP stdio/JSONL.
- ✅ New contributors learn 2 languages to be productive.
- ❌ Some upstream MCP servers need Node (`npx`) — we proxy them via `shesh-mcp-bundle` behind the Guard, not link.
- ❌ Zig/C experiments must live in containers; can't be first-class.

## Links
- `docs/architecture/LANGUAGE_POLICY.md`
- `docs/CONTAINERS_AND_VENV.md`
- D2 (containers)
