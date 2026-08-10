# Contributing

## Add a component

1. **Create the repo** from any existing component (e.g. `shesh-shell`):
   - `pyproject.toml` with a `*-mcp` console script
   - `src/<package>/server.py` using `GuardedMCP` from shesh-audit
   - `tests/` with offline tests (no network)
   - `.github/workflows/ci.yml` matrix on Python 3.11–3.13
   - `.gitignore` for Python build artifacts
2. **Register it** in `manifests/components.toml`:
   ```toml
   [component.shesh-thing]
   layer = "soma"
   repo = "gaganjainse/shesh-thing"
   version = "0.1.0"
   license = "GPL-3.0"
   channel = "canary"
   provides = ["thing"]
   notes = "What it does."
   ```
3. **Wire configs** — add its console-script name to
   `scripts/generate_mcp_config.py` and a step to `scripts/e2e-canary.sh`.
4. **Test locally**: `pytest -q && ruff check . && bash scripts/e2e-canary.sh`.
5. **Open a PR** against shesh-ecosystem.

## Conventions

- **Offline-first**: every tool must work without internet; LLM/network calls
  are injectable and degrade to deterministic stubs.
- **Guarded**: every MCP tool is wrapped by `GuardedMCP` so policy applies.
- **Tests before code**: each component ships with tests; the canary gates
  integration.
- **No secrets in config**: use `shesh-secrets` references.
- **Small commits**, one logical change per PR.
- **License**: GPL-3.0-or-later for all components.

## Channels

- `devel` → daily work
- `canary` → nightly e2e, integration
- `stable` → btrfs-snapshotted releases

## The autopilot contract

When working in autonomous mode:
1. Anchor to `TODO.md`; pick the highest-priority unblocked item.
2. Branch per item, test before push, never push red.
3. After every user message append to `docs/queries/QUERYLOG.md` and update
   TODO statuses.
4. Archive, never delete; no force-push to main.
5. Mark hardware-only items 🟡 rather than faking success.
