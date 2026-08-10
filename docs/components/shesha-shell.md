# 🖥️ sesha-shell

**Sesha Soma — Hyprland/Quickshell control over MCP (stdio).**
Exposes workspaces, windows, focus, opacity, and power-saver visuals to the agent.

- License: GPL-3.0
- Layer: Soma
- Provides: `mcp:hyprland`, `window-control`, `workspaces`
- Part of: [Sesha ecosystem](https://github.com/gaganjainse/sesha-ecosystem)

## Develop

```bash
uv sync --extra dev
uv run pytest -q
uv run ruff check .
uv run sesha-shell-mcp     # runs the stdio MCP server
```

All Hyprland interactions go through `hyprctl`; tests mock subprocess so they need no display.
