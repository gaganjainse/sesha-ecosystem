# 📁 sesha-files

**Sesha Soma — file organizer.** A tiny Rust inotify watcher pipes file-create events
(JSON) to a Python classifier (deterministic rules first, local LLM only for unknowns)
and a safe apply layer that never deletes user data.

- License: GPL-3.0
- Layer: Soma
- Provides: `file-organizer`, `inotify-watcher`, `undo-log`
- Part of: [Sesha ecosystem](https://github.com/gaganjainse/sesha-ecosystem)

## Layout

```
watcher-rs/   # Rust binary `sm-watcher` (notify, debounced JSON output)
src/          # classifier.py (stdin JSON -> decision JSON)
tests/        # offline pytest (no model/network)
```

## Develop

```bash
uv sync --extra dev
uv run pytest -q
uv run ruff check .
(cd watcher-rs && cargo fmt --check && cargo clippy -D warnings && cargo test)
```

## Runtime

```bash
sm-watcher | python -m classifier | sesha-files-apply   # apply layer lives in Auto-desktopenv
```

Designed to run on an RTX 4050 / 6 GB laptop; the LLM is optional (`SESHA_NO_LLM=1`).
