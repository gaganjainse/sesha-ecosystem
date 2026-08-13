# Next Session Prompt — COPY THIS WHOLE FILE into new Arena.ai Agent Mode

You are continuing **Shesh** — federated local-first AI OS for CachyOS/Hyprland
MSI Sword 16 HX B14VEKG (i7-14700HX, RTX 4050 6GB, 1920x1200@144).

**Owner:** Gagan Jain (@gaganjainse) — 53-repo fleet https://github.com/gaganjainse
**Main repo:** shesh-ecosystem **Target OS:** CachyOS 260628 + Hyprland 0.55 + Quickshell
**Lang policy:** Rust, Python 3.11+, Lua, QML/JS, Bash only — MCP/JSON (ADR-0001)

**Federation:**
- 19 components in manifests/components.toml (brain/mind/soma), 3 channels
- Locks: stable 1, canary 18, devel 19 — SHA256 audited
- Components cloned in /home/user/src (22 repos): shesh-* + SheshAOS/SheshAOS/shesha-kernel/SheshAOS
- MCP servers: shesh-*-mcp, 9 in servers.json + containers/secrets/calendar
- Tests: 61 eco (make check), 235+ comp, 26 desktop, 872 SheshAOS (cargo) — all green 2026-08-13

**Stack must respect:**
- docs/SESSION_HANDOFF.md READ FIRST, live anchor
- docs/AUDIT_AND_ROADMAP.md 15 decisions D1-D15
- TODO.md ⬜todo ✅done 🟡in-progress 🔴blocked — 11 left
- docs/MANUAL_VERIFICATION.md 16-section checklist (hardware + rolling-deps + security + recovery drill)
- SECURITY.md + docs/THREAT_MODEL.md + docs/RECOVERY.md — canonical security posture/runbooks
- docs/policies/DEPENDENCY_POLICY.md — rolling-release ownership: agent bumps, downgrade-one break-glass
- docs/policies/DOCUMENTATION_POLICY.md + docs/STYLE_GUIDE.md + docs/INDEX.md — docs SSOT + nav root
- tools/book_build.py — shesh-docs pure projection (mirror map/fissions/orphan sweep); sync-docs.sh wraps it
- docs/queries/QUERYLOG.md full trail newest first — append after each user msg
- docs/SESSION_PROTOCOL.md 60-sec hop protocol (docs/SESSION_HOP_ALERT.md is transient, untracked)
- docs/adr/ 15 ADRs
- docs/GETTING_STARTED.md full install + Ollama 6GB stack
- Containerfile, distrobox.ini, tools/install.sh --channel

**GitHub PAT — SECURED WITH PASSWORD (auto prompt):**
- Encrypted file: ~/.config/shesh/github.pat.enc (600) — uses PBKDF2HMAC 200k + Fernet
- Plain file: ~/.config/shesh/github.pat (600) — auto-deleted on handoff for security
- Current: enc_exists=True plain_exists=False need_password=True
- Flow new session:
  1. Guard detects enc exists but plain missing → NEED_PASSWORD
  2. Agent automatically asks you for password via ask_user UI
  3. You give password (`YOUR_ENCRYPTION_PASSWORD`) → tools/secure_pat.py decrypts enc → plain 600
  4. tools/github_auth.py loads it, never logs value
- Manual: python tools/secure_pat.py --prompt (prompts GetPass) or --password `PW`
- Handoff: python tools/secure_pat.py --handoff deletes plain, keeps enc
- Alt providers if enc missing: env GITHUB_PAT/GH_TOKEN or gh auth login
- Do NOT echo PAT. Tool redacts.

**Commands FIRST in new session:**
```bash
cd /home/user
git pull origin main
python tools/session_guard.py --status
# If NEED_PASSWORD → agent will ask for password automatically
python tools/github_auth.py --check
make check   # GATE OK
ls src/ | wc -l  # 22
cat docs/SESSION_HANDOFF.md
cat TODO.md | grep -E "⬜|🔴|🟡" | head -n 40
```

**Autopilot rules:**
1. Pick highest ⬜ not blocked from TODO.md
2. Branch feat/`THING` — small change one component
3. Tests — never push red — pytest -q -p no:cacheprovider
4. GuardedMCP from shesh-audit
5. No secrets in config — via shesh-secrets env:, gopass:, file:0600
6. After each user msg: append QUERYLOG.md, update TODO.md
7. Before push: session_guard --tick — if hop needed, handoff not new task
8. Archive not delete, no force-push main

**Handoff metrics (regenerated at hop):**
- Last state-refresh 2026-08-13 — run `python tools/session_guard.py --status` for live numbers

**CI closure status (2026-08-13, new session):**
- ✅ shesh-desktop lock-refresh GREEN — `9f46a15` (libgirepository-2.0-dev on
  noble) → bot committed fresh lock `668e07fc`; stale desktop lock cleared.
- ✅ portfolio Auto-Update GREEN — `cd30013` (prettier-normalize after
  regeneration) + `c7673c2` (generator updated for the AI-OS repo rename; 8 curated,
  22/22 tests).
- Fleet: 173 GREEN / 0 PENDING / 16 RED — 13 are dependabot-PR/stale-SHA
  runs, shesh-workspace janitor red = removed workflow (stale run), genuine
  main reds only on out-of-scope repos (AIM tests, ClinicLedger Gradle) —
  see QUERYLOG 2026-08-13 entry.
- Fresh-session gotchas: `.git/config` (origin) + `~/.git-credentials` are
  excluded from Arena snapshots → re-add remote + credential helper +
  identity; reinstall cryptography/ruff/node24. Repo layout: this repo at
  /home/user root, components in /home/user/src.

**Swarm parallel:**
- docs/SWARM.md — GitHub as bus via swarm/ queue/claims/heartbeats
- Orchestrator: python tools/swarm/orchestrator.py --seed TODO.md --monitor (also supports --seed-issues for GitHub Issues)
- Workers: python tools/swarm/worker.py --component shesh-memory (file queue) OR python tools/swarm/worker_github.py --component shesh-memory --github (Issues + atomic branch + PR + auto-merge Action swarm-auto-merge.yml)
- PAT needed for push/PR — decrypted via password flow above

**Message to give you:** "Continue Shesh — read SESSION_HANDOFF first, TODO top-to-bottom, next ⬜. PAT encrypted at ~/.config/shesh/github.pat.enc — agent will ask password and decrypt. Run session_guard --status and make check."

---
Generated: 2026-08-11T16:49:08 by tools/session_guard.py --handoff · hand-refreshed 2026-08-13 (numbers/canon); regenerates on next hop
PAT status at gen: {'enc_exists': True, 'plain_exists': False, 'need_password': True}
