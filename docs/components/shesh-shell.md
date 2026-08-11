# shesha-shell

**Hyprland/Quickshell control over MCP** — Window, workspace, opacity, and visual-state tools.

- Layer: Soma (Soma)
- License: GPL-3.0
- Part of: [Shesha ecosystem](https://github.com/gaganjainse/shesha-ecosystem)

---
**Shesha Soma — Hyprland/Quickshell control over MCP (stdio).**
Exposes workspaces, windows, focus, opacity, and power-saver visuals to the agent.

- License: GPL-3.0
- Layer: Soma
- Provides: `mcp:hyprland`, `window-control`, `workspaces`
- Part of: [Shesha ecosystem](https://github.com/gaganjainse/shesha-ecosystem)

## Develop

```bash
uv sync --extra dev
uv run pytest -q
uv run ruff check .
uv run shesha-shell-mcp     # runs the stdio MCP server
```

All Hyprland interactions go through `hyprctl`; tests mock subprocess so they need no display.