# Next Session Prompt — COPY THIS WHOLE FILE into new Arena.ai Agent Mode chat

You are continuing **Shesh** — federated local-first AI OS for CachyOS/Hyprland on MSI Sword 16 HX B14VEKG (i7-14700HX, RTX 4050 6GB, 1920x1200@144).

**Owner:** Gagan Jain (@gaganjainse) — 27 repos. GitHub: https://github.com/gaganjainse
**Main repo:** shesh-ecosystem (this repo). **Target OS:** CachyOS 260628 + Hyprland ≥0.55 + Quickshell
**Language policy:** Rust, Python 3.11+, Lua, QML/JS, Bash only — cross-lang via MCP/JSON (ADR-0001)

**Federation:**
- 19 components declared in `manifests/components.toml` (brain/mind/soma), 3 channels stable/canary/devel
- Locks: `channels/stable.lock 1, canary.lock 16, devel.lock 19` — SHA256 audited
- Components in `/home/user/src` (22 repos cloned): shesh-audit/mind/memory/orchestrator/skills/acp/harness/backup/calendar/mcp-bundle/containers/phone/secrets/shell/system/files/voice/desktop + SheshaAOS/SeshaOS/shesha-kernel/NexusAOS
- MCP servers: `shesh-*-mcp` console scripts, 9 in `servers.json` (audit, backup, files, harness, memory, mind, orchestrator, shell, skills + containers/secrets/calendar)
- Tests: 30 ecosystem (make check), 182 component (pytest), 26 desktop ambient = 238 green

**Your stack (must respect):**
- `docs/SESSION_HANDOFF.md` — READ FIRST, live anchor, repo list, done/remains
- `docs/AUDIT_AND_ROADMAP.md` — 15 decisions D1-D15, audit, penny-picked tasks
- `TODO.md` — single roadmap ⬜todo ✅done 🟡in-progress 🔴blocked — 16 todos left
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
- Workspace 88.0 MB, file count 3400, age 0.0 min, uncommitted 97
- Last lock SHA: 16 components canary
- Pending todos: 16

**Swarm (parallel sessions):**
- See `docs/SWARM.md` — GitHub as command center via `swarm/` queue/claims/heartbeats
- To be orchestrator: `python tools/swarm/orchestrator.py --seed TODO.md`
- To be worker: `python tools/swarm/worker.py --component shesh-memory`
- Orchestrator monitors `swarm/` and assigns; workers claim via atomic git push (PAT needed), work, push result

**Message to give you as user:** "Continue Shesh — read SESSION_HANDOFF first, then TODO top-to-bottom, pick next ⬜. PAT is in env GITHUB_PAT or ~/.config/shesh/github.pat. Run session_guard --status and make check. Continue autopilot."

---
Generated: 2026-08-11T09:32:30.981744+00:00 — handoff /home/user/dist/handoff.json
