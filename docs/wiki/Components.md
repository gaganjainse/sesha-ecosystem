# Components

Every Shesha component is a standalone Python package (or Rust crate) exposing
an MCP server. Tests count as of the latest autopilot run: **226 passing**.

| Component | Layer | Tests | What it does |
|-----------|-------|------:|--------------|
| [shesha-audit](https://github.com/gaganjainse/shesha-audit) | Brain | 20 | Hash-chained event log, policy Guard, Nexus bridge, MCP gate |
| [shesha-secrets](https://github.com/gaganjainse/shesha-secrets) | Brain | 8 | env/gopass/keepassxc/file secret resolution |
| [shesha-orchestrator](https://github.com/gaganjainse/shesha-orchestrator) | Mind | 28 | RLM multi-agent runtime, sessions, A2A, traces |
| [shesha-memory](https://github.com/gaganjainse/shesha-memory) | Mind | 26 | Episodes, FTS, vector embeddings, habits, intentions |
| [shesha-mind](https://github.com/gaganjainse/shesha-mind) | Mind | 13 | Role→model router (6 GB VRAM budget) |
| [shesha-harness](https://github.com/gaganjainse/shesha-harness) | Mind | 14 | Self-improvement, held-out `/refine` evaluator |
| [shesha-skills](https://github.com/gaganjainse/shesha-skills) | Mind | 10 | Everyday tools + Markdown skills |
| [shesha-calendar](https://github.com/gaganjainse/shesha-calendar) | Mind | 6 | iCalendar vdir agenda |
| [shesha-voice](https://github.com/gaganjainse/shesha-voice) | Soma | — | Newelle fork + MCP overlay |
| [shesha-desktop](https://github.com/gaganjainse/shesha-desktop) | Soma | 26 | Hyprland dotfiles, ambient offers |
| [shesha-files](https://github.com/gaganjainse/shesha-files) | Soma | 5 | Rust watcher + classifier |
| [shesha-shell](https://github.com/gaganjainse/shesha-shell) | Soma | 3 | Hyprland/Quickshell MCP |
| [shesha-system](https://github.com/gaganjainse/shesha-system) | Soma | 13 | Power/GPU/MUX, updates, health, maintenance |
| [shesha-backup](https://github.com/gaganjainse/shesha-backup) | Soma | 8 | Restic wrapper, AC-gated |
| [shesha-phone](https://github.com/gaganjainse/shesha-phone) | Soma | 7 | ADB control for Realme Narzo |
| [shesha-containers](https://github.com/gaganjainse/shesha-containers) | Soma | 5 | Podman/distrobox sandboxed exec |
| [shesha-mcp-bundle](https://github.com/gaganjainse/shesha-mcp-bundle) | Soma | 4 | filesystem/fetch/git proxied through Guard |
| [shesha-acp](https://github.com/gaganjainse/shesha-acp) | Soma | 12 | Agent Client Protocol server |
| [SheshaAOS](https://github.com/gaganjainse/SheshaAOS) | Brain | 981 | Rust governance kernel |
| [shesha-ecosystem](https://github.com/gaganjainse/shesha-ecosystem) | — | 18 | Manifest, gates, docs, this wiki |

## Adding a component

1. Create a repo with `pyproject.toml`, `src/<pkg>/server.py` (GuardedMCP),
   tests under `tests/`, and `.github/workflows/ci.yml` (copy any existing one).
2. Add an entry to `manifests/components.toml` in shesha-ecosystem.
3. Add its command to `scripts/generate_mcp_config.py`.
4. Add a step to `scripts/e2e-canary.sh`.
5. Run the canary locally; open a PR.

See [[Contributing]] for details.
