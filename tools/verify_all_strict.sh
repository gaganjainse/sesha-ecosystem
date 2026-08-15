#!/usr/bin/env bash
# tools/verify_all_strict.sh — run every Python component's strict gates locally.
#
# Adopted from the orchestrator home directory (2026-08-12).
#
# Per component: pytest -W error (warnings are errors — no suppression is
# the org rule) + ruff check. Reports one line per repo, always exits 0; a
# repo failing its gate shows up as FAIL in the line, not as a hidden skip.
#
# Env:
#   SHESH_SRC       clones dir (default ~/src)
#   SHESH_VENV_PY   python with pytest+fastmcp+pytest-asyncio provisioned
#                   (default: /tmp/fm3/bin/python — bootstrap_workspace.sh
#                   recreates that venv)
#   SHESH_SKIP      space-separated repos to skip (default: forks/external
#                   codebases that do not carry the component test harness)
set -u
SRC="${SHESH_SRC:-$HOME/src}"
VENV="${SHESH_VENV_PY:-/tmp/fm3/bin/python}"
SKIP="${SHESH_SKIP:-shesh-voice shesh-desktop waveterm shesh-kernel SeshaOS shesh-docs}"
export PYTHONDONTWRITEBYTECODE=1

for d in "$SRC"/shesh-*/ "$SRC"/SheshAOS/; do
    r=$(basename "$d")
    case " $SKIP " in *" $r "*) continue ;; esac
    [ -d "$d/tests" ] || {
        echo "$r|n/a (no tests/)"
        continue
    }
    out=$(cd "$d" && PYTHONPATH="src:$SRC/shesh-audit/src" "$VENV" -m pytest tests/ -q -W error 2>&1 | tail -1)
    ruff=$("$VENV" -m ruff check "$d/src" "$d/tests" 2>&1 | tail -1)
    echo "$r|pytest=$out|ruff=$ruff"
done
