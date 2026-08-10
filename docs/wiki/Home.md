# Welcome to SheshaAOS

**Shesha** is a local-first, privacy-respecting AI agent operating system
for Linux (target: CachyOS on an MSI Sword 16 HX). It is a federation of
small, single-purpose MCP components orchestrated by a Rust governance
kernel, with a Newelle-based voice frontend.

This wiki is auto-generated from `docs/wiki/` in the
[shesha-ecosystem](https://github.com/gaganjainse/shesha-ecosystem) repo via
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
| [SheshaAOS](https://github.com/gaganjainse/SheshaAOS) | Brain | Rust governance kernel (12 crates) |
| [shesha-ecosystem](https://github.com/gaganjainse/shesha-ecosystem) | — | Manifest, gates, docs, wiki source |
| [shesha-audit](https://github.com/gaganjainse/shesha-audit) | Brain | Hash-chained event log + policy Guard |
| [shesha-orchestrator](https://github.com/gaganjainse/shesha-orchestrator) | Mind | Multi-agent RLM runtime |
| [shesha-memory](https://github.com/gaganjainse/shesha-memory) | Mind | Episodic/semantic/habit memory |
| [shesha-mind](https://github.com/gaganjainse/shesha-mind) | Mind | Role-to-model router |
| [shesha-harness](https://github.com/gaganjainse/shesha-harness) | Mind | Self-improvement / refine |
| [shesha-skills](https://github.com/gaganjainse/shesha-skills) | Mind | Everyday MCP tools + skills |
| [shesha-voice](https://github.com/gaganjainse/shesha-voice) | Soma | Newelle fork (voice/chat UI) |
| [shesha-desktop](https://github.com/gaganjainse/shesha-desktop) | Soma | CachyOS/Hyprland dotfiles |

## Status

**226 tests passing across 16 components.** All unblocked P0/P1 work is
complete; remaining items are the kernel merge and physical-hardware
validation (see [[Roadmap]]).
