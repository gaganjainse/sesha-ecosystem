# Manual Verification Checklist

Everything Shesh automates is unit-tested, but some things **cannot be verified
in this build sandbox** — they need you, on the actual MSI laptop, with real
hardware, accounts, and GUI apps. Work through this top-to-bottom after
installing. Tick items as you confirm them.

> Last updated: 2026-08-13 (16 sections — added rolling-dependency, security-posture and recovery-drill sections). This file is updated on every autopilot run (now automatic via live_update.py); the companion `docs/history/queries/QUERYLOG.md` records what changed and why.

---

## 0. First boot

- [ ] **Boots into CachyOS / Hyprland** without errors
- [ ] `hyprctl version` works; keybinds from the desktop fork are active
- [ ] Resolution is **1920×1200 @ 144 Hz** (check `hyprctl monitors`)
- [ ] The Quickshell status bar / settings render with no pink placeholders
- [ ] Audio works (speakers + headphone jack): `wpctl status`, play a sound
- [ ] Microphone works (for wake word / STT)
- [ ] Network (Wi-Fi + Ethernet) connects
- [ ] `~/.local/share/shesh/` directory tree exists after first run

---

## 1. Accounts, keys, and secrets

- [ ] **Ollama installed and running**: `systemctl --user status ollama`
- [ ] Models pulled for the 6 GB stack:
  - [ ] `phi4-mini` (primary/planner/researcher/critic)
  - [ ] `qwen2.5-coder:3b` (coder)
  - [ ] `moondream2` (vision)
  - [ ] `nomic-embed-text` (embeddings/RAG)
  - [ ] Pull only what you need: `ollama pull <model>`
- [ ] **`restic` installed** and a repo initialized: `restic -r <repo> snapshots`
- [ ] `restic` repository password stored in **gopass/KeePassXC**, referenced as
  `env:RESTIC_PASSWORD` or `gopass:shesh/backup` — **never** in plain config
- [ ] MCP servers resolve secrets via `shesh-secrets`:
  `shesh-secrets-mcp` → `get_secret("env:MY_TOKEN")`
- [ ] No API keys/tokens committed to any repo (run a secret scan)
- [ ] Git identity configured: `git config --global user.email/name`

---

## 2. MCP mesh (the core integration)

After `pipx install`-ing all `shesh-*` packages, run the canary:

```bash
bash scripts/e2e-canary.sh   # from shesh-ecosystem
```

- [ ] **E2E canary passes** (all 16 components import, policy denies protected
      paths, memory/orchestrator/ACP/backup/calendar/vectors/traces all respond)
- [ ] **Generate the MCP config**: `python scripts/generate_mcp_config.py --channel canary`
- [ ] `~/.config/shesh/mcp/servers.json` lists **9 MCP servers**
      (audit, backup, files, harness, memory, mind, orchestrator, shell, skills;
      + containers/secrets/calendar if installed)
- [ ] **Newelle (shesh-voice)** starts and its MCP panel shows the servers
      connected (green)
- [ ] Restart Newelle and ask it to **list its tools** — it should see
      `check_system_updates`, `semantic_search`, `start_session`, etc.
- [ ] Zed / another MCP client (if you use one) can connect via the generated
      `zed.json`
- [ ] Each MCP server starts standalone without import errors, e.g.
      `shesh-system-mcp` (Ctrl-C to exit)

---

## 3. Voice (shesh-voice / Newelle fork)

- [ ] Fork `gaganjainse/shesh-voice` is tracking upstream `qwersyk/Newelle`
      (rebase occasionally)
- [ ] The overlay config copied:
  - [ ] `cp shesh-overlay/shesh-mcp-servers.json ~/.config/Newelle/mcp-servers.json`
  - [ ] Default model set to local Ollama `phi4-mini`
- [ ] **Wake word "hey shesh"** triggers listening (openwakeword)
- [ ] Speech-to-text transcribes your voice accurately (try faster-whisper)
- [ ] Text-to-speech reads responses aloud
- [ ] Mic permission / PipeWire access not blocked

---

## 4. GPU, power, and MUX (MSI-specific)

- [ ] **NVIDIA driver loaded**: `nvidia-smi` shows the GPU and temp/power
- [ ] `powerprofilesctl list`; switching performance↔balanced↔power-saver works
  - [ ] `shesh-system-mcp` → `set_power_profile("gaming")` changes it
  - [ ] Hyprland blur/shadow auto-reduce on battery (verify visually)
- [ ] **MUX switch** (if you use it): `sudo msi-mux-switcher status` shows the
      current mode; switching requires a reboot as documented
- [ ] GPU VRAM doesn't exceed the 5.5 GB budget when two models load
      (`watch nvidia-smi`)
- [ ] Hybrid graphics routes apps correctly (offload with `__NV_PRIME_RENDER_OFFLOAD=1`)

---

## 5. Display and desktop

- [ ] Refresh rate stays at 144 Hz (no drop to 60)
- [ ] Fractional/HiDPI scaling looks correct
- [ ] Screen recording / screenshots work (the `grim`+`slurp` pipeline)
- [ ] Notifications appear and are not duplicated
- [ ] Idle inhibitor works during video/media
- [ ] The **ambient offer overlay** appears at natural pauses (not while typing
      or gaming) and doesn't nag (max 3/day, 30-min cooldown)

---

## 6. Backup

- [ ] `shesh-backup-mcp` → `run_backup` completes (after a manual first
      `restic init`)
- [ ] First backup verified: `restic -r <repo> snapshots` lists it
- [ ] `check_system_updates` reports pending pacman/AUR packages (read-only)
- [ ] **System update is never automatic** — it only notifies; you run `pacman -Syu`
- [ ] `clean_system_caches("user")` frees space without error
- [ ] A scheduled backup timer is enabled if you want daily unattended runs
- [ ] **Test a restore** to a temp dir before trusting backups

---

## 7. Phone (shesh-phone, Realme Narzo)

- [ ] ADB debugging enabled on the phone; `adb devices` lists it
- [ ] `shesh-phone-mcp` connects (safe-area taps land on screen)
- [ ] Taps **outside the status/nav bars are refused** (try a coordinate at y=10)
- [ ] Screenshots pull successfully
- [ ] Vision model can describe a screenshot if you wire it
- [ ] The phone does **not** accept destructive commands without confirmation

---

## 8. Containers / sandboxing

- [ ] `podman` installed and rootless works: `podman run --rm alpine echo ok`
- [ ] `shesh-containers-mcp` → `run_sandboxed(["echo","hi"])` returns output
- [ ] Sandboxed commands have **no network** by default (`--network=none`)
- [ ] `--cap-drop=ALL` is in effect (verify with a privileged syscall)
- [ ] Containers are removed after each run (`--rm`)
- [ ] The third-party MCP bundle (filesystem/fetch/git) launches only if
      `npx`/`uvx` are present

---

## 9. Agent behavior

- [ ] Start a goal via `shesh-orchestrator-mcp` → `execute("...")`; it plans,
      delegates by role, and the critic approves
- [ ] **Background sessions** work: `start_session`, disconnect, `get_session`
      later shows progress/result
- [ ] `cancel_session` actually stops a long-running goal
- [ ] `/refine` only promotes a skill/memory change if the held-out evaluator
      scores ≥ 0.7 (check `recent_refinements`)
- [ ] The LLM is used when Ollama responds; offline, the deterministic stubs
      keep the system working
- [ ] **Memory compaction** runs without data loss:
      `shesh-memory-mcp` → `compact_memory()`; old episodes move to
      `semantic.md`, very old ones are deleted
- [ ] Semantic search (`semantic_search`) returns relevant memories
- [ ] Habits/intentions/mannerisms reflect your actual preferences over time

---

## 10. Security & audit

- [ ] Every tool call is logged: `~/.local/share/shesh/audit/events.jsonl`
- [ ] The hash chain verifies: no "tampered" results
- [x] kernel-format events appear in `kernel-events.jsonl` and are ingested by the Rust kernel (`kernel_ingest`) — wiring done 2026-08-13; on-machine run remains a hardware check
- [ ] Writing to `.ssh`, `.gnupg`, `Vaults/`, or job folders is **denied**
      (try via any MCP tool)
- [ ] Destructive terminal commands in ACP ask for confirmation
- [ ] No MCP server runs as root
- [ ] The audit Guard wraps every MCP server (check each server's logs for a
      "policy" line)

---

## 11. Canary / releases

- [ ] The daily canary GitHub Actions run is green
      (https://github.com/gaganjainse/shesh-ecosystem/actions)
- [ ] If you switch to **stable**, `btrfs snapshot` is taken before install
- [ ] Rollback works: boot the snapshot from grub/btrfs-grub
- [ ] Component versions in `manifests/components.toml` match what's installed

---

## 12. Rolling dependency hygiene (monthly, ~5 minutes)

CachyOS rolls; so do we. Full protocol: `docs/policies/DEPENDENCY_POLICY.md`.

- [ ] **Dependabot PRs are landing green**: each repo → Pull requests →
      filter `author:app/dependabot` — weekly grouped bumps for GitHub
      Actions and pip should be merged, not piling up.
- [ ] **SheshAOS supply-chain job is green** (cargo-deny + cargo-machete +
      typos): https://github.com/gaganjainse/SheshAOS/actions
- [ ] **Python tool floors are current** — spot-check the big three:
      `pip index versions pytest ruff fastmcp` (or pypi.org) against the
      `>=` floors in any component `pyproject.toml`. If PyPI shows newer
      majors, that is a legitimate task to hand the agent (policy §Bumps).
- [ ] **Rust tree refreshes monthly** — agent runs `cargo update` in
      SheshAOS, then `cargo test --workspace` + `cargo clippy --all-targets
      -- -D warnings` must stay green before the lockfile lands.
- [ ] **No deprecated actions/content**: if GitHub emails "Node X
      deprecation" or a workflow annotation warns, hand it to the agent —
      never pin-and-forget.
- [ ] **Break-glass works** (only if a bump breaks CI): downgrade the
      offender by exactly one minor, repeat once; if still broken, drop and
      replace per policy — and the incident gets a QUERYLOG entry.

## 13. Security posture (GitHub-side browser checks, quarterly)

Canonical posture: `SECURITY.md`; threat model: `docs/THREAT_MODEL.md`.

- [ ] **Push protection + secret scanning ON**, every repo: Settings →
      Code security → both toggles enabled (enabled fleet-wide 2026-08-13;
      verify a random sample).
- [ ] **Private vulnerability reporting enabled** on shesh-ecosystem:
      Settings → Code security → "Private vulnerability reporting".
- [ ] **Dependabot alerts are empty or triaged**: Security tab →
      Dependabot — zero unreviewed criticals.
- [ ] **SHA pins intact**: open any recent CI run → "Set up job” step
      shows actions by 40-char SHA, and Dependabot keeps moving them weekly.
- [ ] **PAT hygiene**: `~/.config/shesh/github.pat` is mode 600
      (`stat -c %a`), never pasted into chats. **Outstanding owner action:
      rotate the PAT** — it appeared twice in tool transcripts on
      2026-08-11/12 (GitHub → Settings → Developer settings → revoke +
      regenerate, then re-seed the file).
- [ ] **Tool-pin defense live** (shesh-audit ≥ 53a60b6): first MCP server
      boot prints `learned pin` lines to stderr; a tampered tool
      description must refuse with `ToolPinDrift` (demo:
      `python -m shesh_audit.tool_pins --help`).
- [ ] **swarm-auto-merge canary**: the workflow refuses non-`swarm/*`
      branches and `pull_request_target` is gone from the trigger list
      (Settings → Actions → run history shows only `pull_request`).

## 14. Recovery drill (quarterly, ~15 minutes)

Runbook: `docs/RECOVERY.md`. Automated checker: `tools/dr_check.sh`.

- [ ] `bash tools/dr_check.sh` reports all-green locally.
- [ ] **Backup restore actually restores**: `restic restore latest --target
      /tmp/restore-test --include ~/.config` (dry-run of your real data),
      spot-read a file, delete the target.
- [ ] **Workspace-restore drill known by heart**: re-seed PAT perms
      (`chmod 600`), re-add dropped `origin` remotes, `git fetch`, mixed
      `git reset origin/<branch>`, exec bits from `git ls-files -s` — the
      exact commands are in RECOVERY.md class C.
- [ ] **Stale-base repair drill**: know the graft pattern
      (`git commit-tree HEAD^{tree} -p origin/main`) for when a sandbox
      snapshot rewinds HEAD — RECOVERY.md class C §2.
- [ ] **Incident comms path works**: you can open a `SECURITY: …` issue
      without proof-of-concept details, per SECURITY.md.

## 15. Known things that need deliberate (non-autopilot) work

These are 🔴 in TODO.md and intentionally **not** auto-forced:

- [ ] **shesh-kernel → SheshAOS merge**: the Rust trees diverged at the type
      level. Follow `KERNEL_MERGE_PLAN.md` in SheshAOS; port leaf crates first,
      reconcile `KernelError`/TUI, bring in `shesh-protocols`, fix the
      upstream `russh`/`zig` build breaks, gate on `cargo test --workspace`.
- [ ] **Hardware validation on the physical MSI** (this whole document)
- [ ] Rebase shesh-voice on upstream Newelle periodically
- [ ] Set up real CalDAV/IMAP sync with vdirsyncer if you want email/calendar
      beyond the local .ics reader
- [ ] Optionally connect Telegram/Signal bridges (isolated accounts)
- [ ] Test ACP against actual Zed/JetBrains (the protocol is implemented but
      untested against real editors)

---


## 16. Wiki (one-time setup)

- [ ] Open https://github.com/gaganjainse/SheshAOS/wikis and click **"Create the first page"**
      (GitHub has no API to initialize a wiki; this single click creates the
      `.wiki.git` repo).
- [ ] After that, the **wiki-sync** GitHub Action automatically mirrors
      `docs/wiki/*.md` to the wiki on every push. No manual editing needed.

---

## Quick health command

Run this anytime; it should report all-green:

```bash
echo "=== Shesh health ===" && \
systemctl --user is-active ollama && \
bash ~/src/shesh-ecosystem/scripts/e2e-canary.sh && \
for s in shesh-{audit,system,shell,files,skills,memory,mind,harness,orchestrator,backup,phone,containers,secrets,calendar,acp}-mcp; do
  command -v "$s" >/dev/null && echo "ok  $s" || echo "MISSING  $s"
done && \
echo "=== done ==="
```
