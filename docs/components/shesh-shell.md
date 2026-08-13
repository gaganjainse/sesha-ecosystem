# shesh-shell

**Hyprland/Quickshell control over MCP** — Window, workspace, opacity, and visual-state tools.

- Layer: Soma (Soma)
- License: GPL-3.0
- Part of: [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)

---
**Shesh Soma — Hyprland/Quickshell control over MCP (stdio).**
Exposes workspaces, windows, focus, opacity, and power-saver visuals to the agent.

- License: GPL-3.0
- Layer: Soma
- Provides: `mcp:hyprland`, `window-control`, `workspaces`
- Part of: [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)

## Develop

```bash
uv sync --extra dev
uv run pytest -q
uv run ruff check .
uv run shesh-shell-mcp     # runs the stdio MCP server
```

All Hyprland interactions go through `hyprctl`; tests mock subprocess so they need no display.

## Security

Security posture and vulnerability reporting: [canonical ecosystem security
policy](https://github.com/gaganjainse/shesh-ecosystem/blob/main/SECURITY.md).
