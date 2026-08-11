# ADR-0002: Rootless Containers for Exotic Runtimes

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** containers, reproducibility, security

## Context
Some useful tools require runtimes outside the five core languages: Node.js for filesystem/fetch MCP servers, Playwright, Go linters, etc. Installing them on the host pollutes the dev environment, creates version conflicts (e.g., system Node vs project's), and is not reproducible across CachyOS/Fedora/Ubuntu canary CI.

We need isolation without Docker daemon/root.

## Decision
- **Rootless Podman** is the default runtime. No Docker daemon.
- **Distrobox** for interactive development of exotic stacks (`distrobox-assemble`).
- `uv` for Python venvs with lockfiles.
- Container images are **ephemeral** (`--rm`), `--network=none` and `--cap-drop=ALL` by default for sandboxed tasks (`shesh-containers`).
- Third-party MCP bundle (`shesh-mcp-bundle`) launches `npx`/`uvx` only if present; fails open with skip-if-missing.

## Consequences
- ✅ Host stays clean (CachyOS 260628 + Hyprland only).
- ✅ `shesh-containers-mcp` → `run_sandboxed(["echo","hi"])` works offline.
- ✅ Canary CI runs same container on Arch/Fedora/Ubuntu.
- ❌ First run needs podman pull — documented in MANUAL_VERIFICATION.
- ❌ GUI apps that need host Wayland socket need explicit passthrough (documented).

## Links
- `docs/CONTAINERS_AND_VENV.md`
- `shesh-containers`, `shesh-mcp-bundle`
- D1
