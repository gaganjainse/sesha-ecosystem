# Welcome to SheshAOS

**Shesh** is a local-first, privacy-respecting AI agent operating system
for Linux (target: CachyOS on an MSI Sword 16 HX). It is a federation of
small, single-purpose MCP components orchestrated by a Rust governance
kernel, with a Newelle-based voice frontend.

This wiki is auto-generated from `docs/wiki/` in the
[shesh-ecosystem](https://github.com/gaganjainse/shesh-ecosystem) repo via
a GitHub Actions sync. **Edit the source, not the wiki directly.**

## Start here

- [[Architecture]] — how the Brain, Mind, and Soma fit together
- [[Components]] — the 16 MCP servers and what they do
- [[Roadmap]] — what's done and what's next
- [[Manual-Verification]] — what you must check on real hardware
- [[Contributing]] — how to add a component
- [[Security]] — audit log, policy Guard, and secrets

## Repositories

| Repo | Layer | Purpose |
|------|-------|---------|
| [SheshAOS](https://github.com/gaganjainse/SheshAOS) | Brain | Rust governance kernel (12 crates) |
| [shesh-ecosystem](https://github.com/gaganjainse/shesh-ecosystem) | — | Manifest, gates, docs, wiki source |
| [shesh-audit](https://github.com/gaganjainse/shesh-audit) | Brain | Hash-chained event log + policy Guard |
| [shesh-orchestrator](https://github.com/gaganjainse/shesh-orchestrator) | Mind | Multi-agent RLM runtime |
| [shesh-memory](https://github.com/gaganjainse/shesh-memory) | Mind | Episodic/semantic/habit memory |
| [shesh-mind](https://github.com/gaganjainse/shesh-mind) | Mind | Role-to-model router |
| [shesh-harness](https://github.com/gaganjainse/shesh-harness) | Mind | Self-improvement / refine |
| [shesh-skills](https://github.com/gaganjainse/shesh-skills) | Mind | Everyday MCP tools + skills |
| [shesh-voice](https://github.com/gaganjainse/shesh-voice) | Soma | Newelle fork (voice/chat UI) |
| [shesh-desktop](https://github.com/gaganjainse/shesh-desktop) | Soma | CachyOS/Hyprland dotfiles |

## Status

**226 tests passing across 16 components.** All unblocked P0/P1 work is
complete; remaining items are the kernel merge and physical-hardware
validation (see [[Roadmap]]).


> **One-time setup:** after creating the first wiki page in the web UI,
> the sync workflow keeps these pages up to date automatically.
