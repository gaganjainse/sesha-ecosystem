# Containers, Virtual Environments & Reproducible Dev

> We keep the host clean. Every non-core language/runtime lives in a **rootless Podman** container or
> a per-component **uv** venv. This matches the language policy in `LANGUAGE_POLICY.md` and protects
> the daily driver — the "don't break anything" rule enforced technically, not just by discipline.

---

## 1. Python — Astral `uv` (not pip/venv/poetry)

Each Python component (`sesha` MCP servers, classifier, rag-service) is a proper uv project:

```bash
cd tools/shesh
uv init --bare --lib            # if creating fresh
uv add mcp[cli] fastmcp httpx
uv add --dev pytest ruff
uv sync                        # creates .venv, installs exactly per uv.lock
uv run python -m pytest         # run inside the venv
uv run ruff check .
```

Rules:
- Commit `pyproject.toml` **and** `uv.lock`. CI runs `uv sync --frozen` (no implicit resolution).
- One venv per component under `~/.local/state/<component>/.venv` at install time (the installer
  uses `uv venv` + `uv pip install -r ...` only for the dotfiles bootstrap; components use `uv sync`).
- Never `sudo pip`, never global `pip install`. Use `uvx <tool>` for one-off CLIs.
- Pin Python ≥ 3.11 (we use 3.13 in dev/CI; CachyOS ships 3.13).

## 2. Rust — rustup + cargo

```bash
rustup default stable
cargo fmt --check && cargo clippy -D warnings && cargo test
```
Release binaries are LTO/stripped (already set in `watcher-rs/Cargo.toml`). Install to `~/.local/bin`.

## 3. Containers — rootless Podman + Distrobox

**Podman** is the engine (daemonless, rootless, user namespaces). **Distrobox** is the wrapper for
long-lived dev environments that need host `$HOME`, Wayland, and audio.

### 3.1 Quick isolated test box (Arch, throwaway)
```bash
podman run --rm -it archlinux:latest bash
# inside: pacman -Syu git bash shellcheck python ...
```

### 3.2 Persistent dev container with host integration
```bash
distrobox create --name shesh-dev --image archlinux:latest \
  --additional-packages "git base-devel shellcheck python uv rustup"
distrobox enter shesh-dev
```
This shares `$HOME`, the Wayland socket, and PipeWire — so you can even run GUI/ML tooling without
polluting CachyOS. Export binaries/apps to the host with `distrobox-export`.

### 3.3 Canary / other-distro testing
The canary gate runs components against multiple bases in CI:
```bash
for img in archlinux:latest fedora:40 ubuntu:24.04; do
  podman run --rm -v "$PWD":/src:ro -w /src "$img" ./scripts/gate-in-container.sh
done
```
Use this to validate the installer on Fedora/Ubuntu (guarded paths) without a VM.

### 3.4 Isolating non-core / cloud tools
Any agent/service in a non-approved language (Go, Mojo, a Node-heavy tool) or any cloud-tier agent
runs in a rootless container with a read-only mount of only the paths it needs, exposing MCP over a
Unix socket. It never links into the host.

## 4. Security notes

- Prefer rootless Podman over Docker (ArchWiki): rootful Docker containers have unrestricted host FS
  access by default.
- Distrobox is **not a security sandbox** — it shares your home. Use it for convenience, not for
  isolating untrusted code (use plain podman with limited mounts for that).
- Pin image digests in CI for reproducibility; use `:latest` only on dev boxes.
- Keep secrets out of containers; pass via `systemd-ask-password`/secret service, never env in a
  committed compose file.

## 5. Why this stack over alternatives

- **uv** replaces pip-tools/poetry/virtualenv: 10–100× faster, lockfile + project metadata in one,
  `uvx` for ephemeral tools. Best practice in 2026.
- **Podman** over Docker: daemonless, rootless, systemd integration, OCI-compatible.
- **Distrobox** over raw podman for interactive dev: POSIX shell, any OCI image, app/binary export.
- No Conda/mamba (heavy, conflicts with system Python); no Nix on the host (we keep `dist-nix/` for
  upstream parity but don't run it daily).
