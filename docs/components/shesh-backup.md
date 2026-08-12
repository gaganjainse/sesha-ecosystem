# 💾 shesh-backup

**Verified local restic backups.** Wraps `restic` with safe defaults: only
runs on AC, respects a daily schedule, verifies snapshots, and never forgets/
prunes unless explicitly asked.

- License: GPL-3.0
- Layer: Soma
- Part of: [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)

## MCP tools

- `configure(repo, paths, exclude)` — set restic repo and backup paths
- `status()` — due? last result? snapshot count?
- `run_backup()` — run if due and on AC
- `run_prune()` — apply retention policy (explicit, destructive)

State lives in `~/.local/state/shesh/backup/`. The restic password is read
from the environment (never stored in config).

## Develop

```bash
uv sync --extra dev
uv run pytest -q        # 8 offline tests (restic is faked)
uv run ruff check .
```
