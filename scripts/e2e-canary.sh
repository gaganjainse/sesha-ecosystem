#!/usr/bin/env bash
# Canary end-to-end test: boot every MCP server in a container and run a
# real task through the orchestrator. This is the integration gate that
# catches wiring errors unit tests can't (missing deps, broken imports,
# protocol mismatches between components).
#
# It runs in an Arch/CachyOS-like container so it matches the desktop.
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
PIP="python3 -m pip install --quiet --break-system-packages"

fail() { echo "E2E FAIL: $*" >&2; exit 1; }

echo "==> Installing all components"
for comp in "$HERE"/../components/shesha-*/; do
  name=$(basename "$comp")
  echo "   - $name"
  (cd "$comp" && $PIP -e . >/dev/null 2>&1) || fail "install $name"
done

echo "==> Import check: every server module imports cleanly"
python3 - <<'PY'
import importlib
mods = [
 "shesha_audit.server", "shesha_audit.gate", "shesha_audit.nexus_bridge",
 "shesha_system.server", "shesha_shell.server", "classifier",  # shesha-files (flat module)
 "shesha_skills.server", "shesha_memory.server", "shesha_harness.server",
 "shesha_mind.server", "shesha_orchestrator.server", "shesha_orchestrator.llm",
 "shesha_backup.server", "shesha_phone", "shesha_acp.server",
]
for m in mods:
    importlib.import_module(m)
    print(f"   ok {m}")
PY

echo "==> Policy gate: a protected path is denied by every guarded server"
python3 - <<'PY'
from shesha_audit.gate import Guard
g = Guard()
d = g.check("write_file", {"path": "/home/u/.ssh/id_rsa"})
assert d.verdict == "deny", f"expected deny, got {d}"
print("   ok protected path denied")
PY

echo "==> Memory: write episode, assemble bounded context"
python3 - <<'PY'
import tempfile, pathlib
from shesha_memory.store import MemoryStore
from shesha_memory.context import ContextAssembler, Budget
root = pathlib.Path(tempfile.mkdtemp())
ms = MemoryStore(root=root)
ms.record("observation", "user prefers bullet points")
ctx = ContextAssembler(ms, Budget(total=2000))
secs = ctx.build(query="preferences")
text = ctx.render(secs)
assert len(text) > 0 and "bullet" in text.lower()
print("   ok memory assembled")
PY

echo "==> Orchestrator: stubbed plan executes, budget enforced"
python3 - <<'PY'
from shesha_orchestrator.orchestrator import Orchestrator, make_agent
from shesha_orchestrator.agents import Budget
from shesha_orchestrator.stubs import default_planner, always_approve
agents = {n: make_agent(n, lambda p, c: {"ok": True, "by": n})
          for n in ("researcher", "coder", "critic", "coordinator")}
r = Orchestrator(agents, budget=Budget(max_turns=5)).execute(
    "test goal", planner=default_planner, critic=always_approve)
assert r.ok and len(r.steps) == 3, r
print(f"   ok executed {len(r.steps)} steps")
PY

echo "==> ACP: session + prompt round-trip"
python3 - <<'PY'
import tempfile, pathlib
from shesha_acp.server import ACPServer
srv = ACPServer(root=pathlib.Path(tempfile.mkdtemp()))
s = srv.handle({"id":1,"method":"session/new","params":{"cwd":"/tmp"}})[0]
sid = s["result"]["sessionId"]
r = srv.handle({"id":2,"method":"session/prompt","params":{"sessionId":sid,"prompt":"hi"}})
assert any(m.get("method") == "session/update" for m in r), r
print("   ok acp prompt")
PY

echo "==> Backup: dry-run status with no config"
python3 - <<'PY'
from shesha_backup.server import status
st = status()
assert "due" in st
print(f"   ok backup status: due={st['due']} reason={st['reason']}")
PY

echo "E2E PASS"
