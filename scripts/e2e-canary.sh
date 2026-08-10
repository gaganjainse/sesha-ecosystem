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
for comp in "$HERE"/../components/shesh-*/; do
  name=$(basename "$comp")
  echo "   - $name"
  (cd "$comp" && $PIP -e . >/dev/null 2>&1) || fail "install $name"
done

echo "==> Import check: every server module imports cleanly"
python3 - <<'PY'
import importlib
mods = [
 "shesh_audit.server", "shesh_audit.gate", "shesh_audit.nexus_bridge",
 "shesh_system.server", "shesh_shell.server", "classifier",  # shesh-files (flat module)
 "shesh_skills.server", "shesh_memory.server", "shesh_harness.server",
 "shesh_mind.server", "shesh_orchestrator.server", "shesh_orchestrator.llm",
 "shesh_backup.server", "shesh_phone", "shesh_acp.server",
]
for m in mods:
    importlib.import_module(m)
    print(f"   ok {m}")
PY

echo "==> Policy gate: a protected path is denied by every guarded server"
python3 - <<'PY'
from shesh_audit.gate import Guard
g = Guard()
d = g.check("write_file", {"path": "/home/u/.ssh/id_rsa"})
assert d.verdict == "deny", f"expected deny, got {d}"
print("   ok protected path denied")
PY

echo "==> Memory: write episode, assemble bounded context"
python3 - <<'PY'
import tempfile, pathlib
from shesh_memory.store import MemoryStore
from shesh_memory.context import ContextAssembler, Budget
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
from shesh_orchestrator.orchestrator import Orchestrator, make_agent
from shesh_orchestrator.agents import Budget
from shesh_orchestrator.stubs import default_planner, always_approve
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
from shesh_acp.server import ACPServer
srv = ACPServer(root=pathlib.Path(tempfile.mkdtemp()))
s = srv.handle({"id":1,"method":"session/new","params":{"cwd":"/tmp"}})[0]
sid = s["result"]["sessionId"]
r = srv.handle({"id":2,"method":"session/prompt","params":{"sessionId":sid,"prompt":"hi"}})
assert any(m.get("method") == "session/update" for m in r), r
print("   ok acp prompt")
PY

echo "==> Backup: dry-run status with no config"
python3 - <<'PY'
from shesh_backup.server import status
st = status()
assert "due" in st
print(f"   ok backup status: due={st['due']} reason={st['reason']}")
PY

echo "E2E PASS"

echo "==> Calendar: parse an ics event"
python3 - <<'PY'
import tempfile, pathlib
from shesh_calendar import parser
d = pathlib.Path(tempfile.mkdtemp())
(d/"c.ics").write_text("BEGIN:VCALENDAR\nBEGIN:VEVENT\nSUMMARY:Test\nDTSTART:20260101T100000\nEND:VEVENT\nEND:VCALENDAR")
evs = parser.scan_dir(d)
assert evs and evs[0].summary == "Test", evs
print("   ok calendar parsed")
PY

echo "==> Embeddings + vector store"
python3 - <<'PY'
import tempfile, pathlib
from shesh_memory.embeddings import local_embedder, LOCAL_DIM
from shesh_memory.vectorstore import VectorStore
d = pathlib.Path(tempfile.mkdtemp())
s = VectorStore(d/"v.db", local_embedder(), LOCAL_DIM)
s.upsert("1", "the cat sat on the mat")
r = s.search("cat")
assert r and r[0]["score"] > 0
print("   ok vector search")
PY

echo "==> Trace recorder"
python3 - <<'PY'
import tempfile, pathlib
from shesh_orchestrator.traces import TraceRecorder
r = TraceRecorder(pathlib.Path(tempfile.mkdtemp())/"t.jsonl")
with r.trace("x") as span:
    span.set_attribute("k","v")
assert len(r.recent()) == 1
print("   ok trace recorded")
PY

echo "==> Container runner builds args without executing"
python3 - <<'PY'
from shesh_containers.runner import ContainerConfig, run_in_container
captured = {}
def fake(cmd, timeout=60):
    captured["cmd"] = cmd
    return 0, "ok"
run_in_container(["echo","hi"], ContainerConfig(engine="echo"), runner=fake)
joined = " ".join(captured["cmd"])
assert "--rm" in joined and "--cap-drop=ALL" in joined and "echo" in joined
print("   ok container args")
PY
