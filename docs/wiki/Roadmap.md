# Roadmap

Tracked in detail in
[TODO.md](https://github.com/gaganjainse/shesh-ecosystem/blob/main/TODO.md).
This page summarizes status.

## ✅ Done (autopilot, this cycle)

- **Governance** — audit log, policy Guard, MCP gate, Nexus event bridge
- **Agents** — multi-agent orchestrator, role-based model routing, persistent
  background sessions with cancel, A2A Unix-socket transport, local traces
- **Memory** — episodes + FTS + vector embeddings, habits/intentions/mannerisms,
  episodic compaction/retention, semantic search
- **Self-improvement** — harness with held-out evaluator and LLM responder
- **Skills** — notes/web/code/docs/reminders + 5 Markdown skills
- **Calendar** — local iCal vdir reader
- **Voice/desktop** — Newelle fork overlay, Hyprland dotfiles, data-aware
  ambient offers, settings GUI
- **System body** — power/GPU/MUX, restic backup, phone ADB, podman sandbox,
  filesystem/fetch/git MCP bundle, ACP terminal/diff
- **Platform** — manifest resolver, license gate, 3-channel releases, canary
  e2e covering all 15 components, MCP config generator, secrets resolver,
  .gitignore across all repos

**Tests: 226 passing · 16 components · all pushed to GitHub.**

## 🔴 Blocked (need deliberate / physical work)

- **shesh-kernel → SheshAOS merge.** The archived Rust kernel diverged at the
  type level (`NexusError`/TUI API). Port leaf crates first (protocols,
  waveobj, wps, blockctl, wconfig), reconcile APIs, bring in
  `sheshaos-protocols`, fix upstream `russh`/`zig` build breaks, gate on
  `cargo test --workspace`. See `KERNEL_MERGE_PLAN.md` in SheshAOS.
- **Hardware validation on the physical MSI Sword 16 HX** — display @144 Hz,
  NVIDIA/MUX, wake word, PipeWire, Quickshell. See [[Manual-Verification]].
- **Zed/JetBrains ACP testing** — protocol implemented, untested against real
  editors.

## 🟡 Next P1 (unblocked, in priority order)

- LLM-backed auto skill capture (Read→Execute→Reflect→Write) with deprecation
- Distrobox/Containerfile for one-command onboarding
- Installer channels with btrfs snapshot + rollback
- Local-first email (IMAP via vdirsyncer/neomutt)
- Messaging bridges (Telegram/Signal, isolated)
- Media tools (screenshots, recording, wallpaper)
- OTLP export of local traces

## Release channels

- **devel** — daily work, all components
- **canary** — integration-tested nightly, e2e green
- **stable** — btrfs-snapshot releases
