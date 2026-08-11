#!/usr/bin/env python3
"""Session Guard — detect slowdown and remind to hop sessions.

Tracks:
- workspace size (du), file count, age, tool latency, uncommitted files
- logs to ~/.local/share/shesh/session_guard.jsonl (persists via git push of dist? no, local)
- creates docs/SESSION_HOP_ALERT.md when hop needed
- --handoff generates docs/NEXT_SESSION_PROMPT.md + dist/handoff.json

Integration: called by supervise.sh and autopilot runner before each task.

Thresholds can be tuned — defaults are Arena.ai safe.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARD_LOG = pathlib.Path.home() / ".local/share/shesh/session_guard.jsonl"
ALERT_FILE = ROOT / "docs/SESSION_HOP_ALERT.md"
NEXT_PROMPT = ROOT / "docs/NEXT_SESSION_PROMPT.md"
HANDOFF_JSON = ROOT / "dist/handoff.json"

# Tunables — Arena limits: 128 MB snapshot, 10k files, context blowup after ~60-90 min
DEFAULTS = {
    "max_workspace_mb": 100,
    "max_file_count": 8000,
    "max_age_min": 60,
    "max_avg_latency_ms": 5000,
    "max_uncommitted": 20,
}


def sh(cmd: str) -> str:
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def get_workspace_mb() -> float:
    try:
        out = sh("du -sm /home/user 2>/dev/null | cut -f1")
        return float(out) if out else 0
    except Exception:
        return 0


def get_file_count() -> int:
    try:
        out = sh("find /home/user -type f 2>/dev/null | wc -l")
        return int(out) if out else 0
    except Exception:
        return 0


def get_uncommitted() -> int:
    try:
        out = sh("cd /home/user && git status --porcelain 2>/dev/null | wc -l")
        return int(out) if out else 0
    except Exception:
        return 0


def get_session_age_min() -> float:
    try:
        if not GUARD_LOG.exists():
            return 0
        first = None
        for line in GUARD_LOG.read_text().splitlines():
            try:
                j = json.loads(line)
                first = j.get("ts")
                break
            except Exception:
                continue
        if not first:
            return 0
        dt = datetime.fromisoformat(first.replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - dt).total_seconds() / 60
        return age
    except Exception:
        return 0


def get_avg_latency() -> float:
    try:
        if not GUARD_LOG.exists():
            return 0
        vals = []
        for line in GUARD_LOG.read_text().splitlines()[-20:]:
            try:
                j = json.loads(line)
                if "latency_ms" in j:
                    vals.append(float(j["latency_ms"]))
            except Exception:
                continue
        return sum(vals) / len(vals) if vals else 0
    except Exception:
        return 0


def log_tick(latency_ms: float | None = None) -> dict:
    GUARD_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "workspace_mb": get_workspace_mb(),
        "file_count": get_file_count(),
        "uncommitted": get_uncommitted(),
        "age_min": round(get_session_age_min(), 1),
        "latency_ms": latency_ms,
        "avg_latency_ms": round(get_avg_latency(), 1) if latency_ms is None else latency_ms,
    }
    with GUARD_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def check_hop_needed(metrics: dict) -> tuple[bool, list[str]]:
    reasons = []
    if metrics["workspace_mb"] > DEFAULTS["max_workspace_mb"]:
        reasons.append(f"workspace {metrics['workspace_mb']} MB >{DEFAULTS['max_workspace_mb']} MB")
    if metrics["file_count"] > DEFAULTS["max_file_count"]:
        reasons.append(f"file count {metrics['file_count']} >{DEFAULTS['max_file_count']}")
    if metrics["age_min"] > DEFAULTS["max_age_min"]:
        reasons.append(f"age {metrics['age_min']:.1f} min >{DEFAULTS['max_age_min']} min")
    if metrics.get("avg_latency_ms", 0) > DEFAULTS["max_avg_latency_ms"]:
        reasons.append(f"avg latency {metrics['avg_latency_ms']} ms >{DEFAULTS['max_avg_latency_ms']} ms")
    if metrics["uncommitted"] > DEFAULTS["max_uncommitted"]:
        reasons.append(f"uncommitted {metrics['uncommitted']} files >{DEFAULTS['max_uncommitted']}")
    return (len(reasons) > 0, reasons)


def write_alert(metrics: dict, reasons: list[str]) -> None:
    ALERT_FILE.write_text(
        f"""# 🚨 SESSION HOP RECOMMENDED

**Generated:** {datetime.now(timezone.utc).isoformat()}
**Reason:** {', '.join(reasons)}

## Metrics
```json
{json.dumps(metrics, indent=2)}
```

## What to do (60 sec)

```bash
python tools/session_guard.py --status
python tools/session_guard.py --handoff
make check
git add -A
git commit -m "chore: handoff $(datetime.now(timezone.utc).isoformat())"
git push origin main
```

Then close this chat and open new Agent Mode, paste `docs/NEXT_SESSION_PROMPT.md`.

## Why
Arena.ai snapshots workspace at ~128 MB / 10k files. Tool latency spikes indicate context overflow.
Hopping now is cheaper than fighting slowdown.

---
*This file is auto-generated by `tools/session_guard.py`. Delete after hop.*
"""
    )


def generate_next_prompt() -> str:
    # Gather live info
    try:
        lock_count = json.loads((ROOT / "channels/canary.lock").read_text()).get("count", "?")
    except Exception:
        lock_count = "?"

    try:
        todo_pending = open(ROOT / "TODO.md").read().count("⬜")
    except Exception:
        todo_pending = "?"

    prompt = f"""# Next Session Prompt — COPY THIS WHOLE FILE into new Arena.ai Agent Mode chat

You are continuing **Shesh** — federated local-first AI OS for CachyOS/Hyprland on MSI Sword 16 HX B14VEKG (i7-14700HX, RTX 4050 6GB, 1920x1200@144).

**Owner:** Gagan Jain (@gaganjainse) — 27 repos. GitHub: https://github.com/gaganjainse
**Main repo:** shesh-ecosystem (this repo). **Target OS:** CachyOS 260628 + Hyprland ≥0.55 + Quickshell
**Language policy:** Rust, Python 3.11+, Lua, QML/JS, Bash only — cross-lang via MCP/JSON (ADR-0001)

**Federation:**
- 19 components declared in `manifests/components.toml` (brain/mind/soma), 3 channels stable/canary/devel
- Locks: `channels/stable.lock 1, canary.lock {lock_count}, devel.lock 19` — SHA256 audited
- Components in `/home/user/src` (22 repos cloned): shesh-audit/mind/memory/orchestrator/skills/acp/harness/backup/calendar/mcp-bundle/containers/phone/secrets/shell/system/files/voice/desktop + SheshaAOS/SeshaOS/shesha-kernel/NexusAOS
- MCP servers: `shesh-*-mcp` console scripts, 9 in `servers.json` (audit, backup, files, harness, memory, mind, orchestrator, shell, skills + containers/secrets/calendar)
- Tests: 30 ecosystem (make check), 182 component (pytest), 26 desktop ambient = 238 green

**Your stack (must respect):**
- `docs/SESSION_HANDOFF.md` — READ FIRST, live anchor, repo list, done/remains
- `docs/AUDIT_AND_ROADMAP.md` — 15 decisions D1-D15, audit, penny-picked tasks
- `TODO.md` — single roadmap ⬜todo ✅done 🟡in-progress 🔴blocked — {todo_pending} todos left
- `docs/MANUAL_VERIFICATION.md` — 13-section hardware checklist for MSI (GPU@144, NVIDIA MUX, wake word, PipeWire, Quickshell, backup, phone ADB, podman)
- `docs/queries/QUERYLOG.md` — full decision trail, newest first — append after each user message
- `docs/SESSION_PROTOCOL.md` — how to hop sessions in 60 sec without loss
- `docs/adr/` — 15 ADRs for D1-D15
- `docs/GETTING_STARTED.md` — full install with bootstrap, Ollama 6GB stack phi4-mini/qwen2.5-coder:3b/moondream2/nomic-embed-text, pipx, voice, secrets, backup
- `Containerfile`, `distrobox.ini`, `tools/install.sh --channel stable|canary|devel` (btrfs snapshot+rollback)

**GitHub PAT (important):**
- You need push rights. PAT is NOT in repo for security.
- Provide it via ONE of (in order, tool `tools/github_auth.py` checks):
  1. Env `GITHUB_PAT` or `GH_TOKEN` or `GITHUB_TOKEN`
  2. File `~/.config/shesh/github.pat` with 0600 (refuses world-readable) — create: `mkdir -p ~/.config/shesh && echo "$PAT" > ~/.config/shesh/github.pat && chmod 600 $_`
  3. `gh` CLI logged in: `gh auth login` — reads `~/.config/gh/hosts.yml`
- Do NOT echo PAT in chat. Tool `tools/github_auth.py` loads securely and never logs value.
- If PAT missing, work offline (tests, docs) but cannot push swarm claims.

**Commands to run FIRST in new session:**

```bash
cd /home/user
git pull origin main
python tools/session_guard.py --status
make check   # must be GATE OK (ruff 30 tests + license + locks)
ls src/ | wc -l   # should be 22 components
python tools/github_auth.py --check   # verifies PAT loading

# Then read anchors
cat docs/SESSION_HANDOFF.md
cat docs/SESSION_PROTOCOL.md | head -n 80
cat TODO.md | grep -E "⬜|🔴|🟡" | head -n 40
```

**How to work (autopilot rules):**
1. Pick highest-priority ⬜ not blocked from TODO.md top-to-bottom
2. Branch `feat/<thing>` — small focused change in one component
3. Implement with tests — never push red — `python -m pytest tests/ -q -p no:cacheprovider`
4. Use `GuardedMCP` from shesh-audit for any new MCP server (auto policy+audit+Nexus)
5. No secrets in config — via `shesh-secrets` refs `env:`, `gopass:`, `file:0600`
6. After each user message: append to `docs/queries/QUERYLOG.md`, update TODO.md status, refresh relevant docs
7. Before push: `python tools/session_guard.py --tick` — if hop needed, do 60-sec handoff instead of new task
8. Archive, don't delete. No force-push main. No root. Mark hardware items 🟡 not fake ✅

**Current session handoff metrics:**
- Workspace {get_workspace_mb()} MB, file count {get_file_count()}, age {get_session_age_min():.1f} min, uncommitted {get_uncommitted()}
- Last lock SHA: {lock_count} components canary
- Pending todos: {todo_pending}

**Swarm (parallel sessions):**
- See `docs/SWARM.md` — GitHub as command center via `swarm/` queue/claims/heartbeats
- To be orchestrator: `python tools/swarm/orchestrator.py --seed TODO.md`
- To be worker: `python tools/swarm/worker.py --component shesh-memory`
- Orchestrator monitors `swarm/` and assigns; workers claim via atomic git push (PAT needed), work, push result

**Message to give you as user:** "Continue Shesh — read SESSION_HANDOFF first, then TODO top-to-bottom, pick next ⬜. PAT is in env GITHUB_PAT or ~/.config/shesh/github.pat. Run session_guard --status and make check. Continue autopilot."

---
Generated: {datetime.now(timezone.utc).isoformat()} — handoff {HANDOFF_JSON}
"""
    NEXT_PROMPT.write_text(prompt)
    return prompt


def main() -> int:
    ap = argparse.ArgumentParser(description="Session guard — hop detection")
    ap.add_argument("--status", action="store_true", help="print status")
    ap.add_argument("--tick", action="store_true", help="log tick with optional latency")
    ap.add_argument("--latency-ms", type=float, help="last tool latency ms")
    ap.add_argument("--handoff", action="store_true", help="generate handoff files")
    ap.add_argument("--clean", action="store_true", help="clean caches to reduce size")
    args = ap.parse_args()

    if args.clean:
        print("Cleaning caches...")
        for pat in [
            "find /home/user -type d -name __pycache__ -prune -exec rm -rf {{}} + 2>/dev/null || true",
            "rm -rf /home/user/.cache /home/user/.pytest_cache /home/user/.ruff_cache 2>/dev/null; true",
            "find /home/user -type d -name .venv -prune -exec rm -rf {{}} + 2>/dev/null || true",
            "rm -rf /home/user/src/*/target /home/user/src/*/dist /home/user/src/*/__pycache__ 2>/dev/null; true",
        ]:
            os.system(pat)
        print("Cleaned")

    tick = log_tick(latency_ms=args.latency_ms)
    metrics = {
        "workspace_mb": get_workspace_mb(),
        "file_count": get_file_count(),
        "uncommitted": get_uncommitted(),
        "age_min": round(get_session_age_min(), 1),
        "avg_latency_ms": round(get_avg_latency(), 1),
    }
    hop, reasons = check_hop_needed(metrics)

    if args.status or args.tick or args.handoff:
        print(json.dumps(metrics, indent=2))
        if hop:
            print(f"\n🚨 HOP RECOMMENDED: {', '.join(reasons)}")
            write_alert(metrics, reasons)
        else:
            print("\n✅ Session healthy — continue")

    if args.handoff or hop:
        prompt = generate_next_prompt()
        HANDOFF_JSON.parent.mkdir(parents=True, exist_ok=True)
        HANDOFF_JSON.write_text(
            json.dumps(
                {
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "metrics": metrics,
                    "reasons": reasons if hop else [],
                    "pending_todos": open(ROOT / "TODO.md").read().count("⬜")
                    if (ROOT / "TODO.md").exists()
                    else 0,
                },
                indent=2,
            )
            + "\n"
        )
        print(f"\nGenerated {NEXT_PROMPT} and {HANDOFF_JSON}")
        print("Copy NEXT_SESSION_PROMPT.md into new chat to continue without explaining.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
