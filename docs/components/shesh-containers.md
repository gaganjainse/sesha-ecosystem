# 📦 shesh-containers

Run commands inside **unprivileged, network-isolated podman/distrobox
containers** instead of on the host, exposed as MCP tools. Containers are
disposable (`--rm`) with `--cap-drop=ALL` and PID limits.

- License: GPL-3.0
- Layer: Soma
- Part of: [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)

## MCP tools
- `run_sandboxed(command, image, network)` — ephemeral container execution
- `list_container_images()`, `pull_image(image)`, `set_engine(engine)`

## Develop
```bash
uv run pytest -q
uv run ruff check .
uv run shesh-containers-mcp
```
