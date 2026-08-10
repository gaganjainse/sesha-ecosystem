# Components

Every Shesh component is a standalone Python package (or Rust crate) exposing
an MCP server. Tests count as of the latest autopilot run: **226 passing**.

| Component | Layer | Tests | What it does |
|-----------|-------|------:|--------------|
| [shesh-audit](https://github.com/gaganjainse/shesh-audit) | Brain | 20 | Hash-chained event log, policy Guard, Nexus bridge, MCP gate |
| [shesh-secrets](https://github.com/gaganjainse/shesh-secrets) | Brain | 8 | env/gopass/keepassxc/file secret resolution |
| [shesh-orchestrator](https://github.com/gaganjainse/shesh-orchestrator) | Mind | 28 | RLM multi-agent runtime, sessions, A2A, traces |
| [shesh-memory](https://github.com/gaganjainse/shesh-memory) | Mind | 26 | Episodes, FTS, vector embeddings, habits, intentions |
| [shesh-mind](https://github.com/gaganjainse/shesh-mind) | Mind | 13 | Role→model router (6 GB VRAM budget) |
| [shesh-harness](https://github.com/gaganjainse/shesh-harness) | Mind | 14 | Self-improvement, held-out `/refine` evaluator |
| [shesh-skills](https://github.com/gaganjainse/shesh-skills) | Mind | 10 | Everyday tools + Markdown skills |
| [shesh-calendar](https://github.com/gaganjainse/shesh-calendar) | Mind | 6 | iCalendar vdir agenda |
| [shesh-voice](https://github.com/gaganjainse/shesh-voice) | Soma | — | Newelle fork + MCP overlay |
| [shesh-desktop](https://github.com/gaganjainse/shesh-desktop) | Soma | 26 | Hyprland dotfiles, ambient offers |
| [shesh-files](https://github.com/gaganjainse/shesh-files) | Soma | 5 | Rust watcher + classifier |
| [shesh-shell](https://github.com/gaganjainse/shesh-shell) | Soma | 3 | Hyprland/Quickshell MCP |
| [shesh-system](https://github.com/gaganjainse/shesh-system) | Soma | 13 | Power/GPU/MUX, updates, health, maintenance |
| [shesh-backup](https://github.com/gaganjainse/shesh-backup) | Soma | 8 | Restic wrapper, AC-gated |
| [shesh-phone](https://github.com/gaganjainse/shesh-phone) | Soma | 7 | ADB control for Realme Narzo |
| [shesh-containers](https://github.com/gaganjainse/shesh-containers) | Soma | 5 | Podman/distrobox sandboxed exec |
| [shesh-mcp-bundle](https://github.com/gaganjainse/shesh-mcp-bundle) | Soma | 4 | filesystem/fetch/git proxied through Guard |
| [shesh-acp](https://github.com/gaganjainse/shesh-acp) | Soma | 12 | Agent Client Protocol server |
| [SheshAOS](https://github.com/gaganjainse/SheshAOS) | Brain | 981 | Rust governance kernel |
| [shesh-ecosystem](https://github.com/gaganjainse/shesh-ecosystem) | — | 18 | Manifest, gates, docs, this wiki |

## Adding a component

1. Create a repo with `pyproject.toml`, `src/<pkg>/server.py` (GuardedMCP),
   tests under `tests/`, and `.github/workflows/ci.yml` (copy any existing one).
2. Add an entry to `manifests/components.toml` in shesh-ecosystem.
3. Add its command to `scripts/generate_mcp_config.py`.
4. Add a step to `scripts/e2e-canary.sh`.
5. Run the canary locally; open a PR.

See [[Contributing]] for details.
