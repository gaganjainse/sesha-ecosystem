# ADR-0005: Local-First, Cloud Opt-In

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** privacy, security, offline

## Context
AI OS that phones home with file names, voice transcripts, or calendar events violates user trust and GDPR expectations. The target user runs on a laptop that sleeps, goes offline, and processes job docs that must never leave disk.

Yet we need embeddings/RAG, model routing, and occasional frontier models.

## Decision
- **Default: offline only.**
  - Ollama local stack: `phi4-mini`, `qwen2.5-coder:3b`, `moondream2`, `nomic-embed-text` (6 GB VRAM budget).
  - Local hash embedder fallback when Ollama unavailable — deterministic stubs keep system working.
  - No keys in config. Secrets via `shesh-secrets` (env/gopass/keepassxc/file with 0600 check, refuses world-readable).
- **Cloud opt-in behind policy:**
  - `[cloud] enabled = true` in config + per-session voice confirmation.
  - Guard denies cloud for protected paths (`.ssh`, `Vaults/`, `~/Documents/Job`, etc.) regardless of setting.
  - Audit log records every tool decision + route.

## Consequences
- ✅ Works on airplane — calendar, notes, RAG (local hash), organizer.
- ✅ `shesh-secrets` → `get_secret("gopass:shesh/backup")` never logs value.
- ✅ No accidental exfil — network disabled in sandboxed container by default.
- ❌ Local models weaker than frontier; `shesh-mind` router must budget VRAM carefully.
- ❌ First-time Ollama pull is ~10 GB — documented in GETTING_STARTED.

## Links
- `policies/SKILLS_POLICY.md`, `docs/architecture/AGENTIC_BODY.md`
- `shesh-secrets`, `shesh-mind`, `shesh-memory`
- D15 (Guard)
