# ADR-0009: Newelle Fork as shesh-voice with Overlay, Core Untouched

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** voice, stt, tts, upstream-rebase

## Context
We need wake word, STT, TTS, chat UI, and MCP client. Newelle (qwersyk/Newelle) is GPL-3.0, has all of these: openwakeword, faster-whisper, Piper/Kokoro/Edge TTS, subagents, skills, STDIO MCP since 1.4.5, Telegram interface, OpenAI-compatible local API.

Building voice from scratch would take months; forking with heavy edits would make rebase painful.

## Decision
- Fork Newelle as `shesh-voice` (GPL-3.0), keep **core untouched**.
- Add overlay dir `shesh-overlay/` (now `shesh-overlay/`) containing:
  - `shesh-mcp-servers.json` — wires all `shesh-*` MCP servers.
  - Default model = local Ollama `phi4-mini` (not cloud).
  - Wake word model: "hey shesh" via openwakeword.
  - About-screen rebrand: "Shesh (Newelle core)" + link to ecosystem.
- Native build (Meson), not Flatpak — host audio (PipeWire) and MCP stdio.
- Track upstream `main` — weekly rebase job in `upstream_tracker.py`.

## Consequences
- ✅ 14k★ voice stack in days, not months.
- ✅ Upstream features (subagents, skills 1.3.5, chat folders 1.4.0) merge cleanly.
- ✅ Local-first: Piper + faster-whisper offline.
- ❌ GNOME assumptions remain — need Quickshell overlay for Hyprland.
- ❌ TTS/STT model downloads ~2 GB — documented in MANUAL_VERIFICATION.

## Links
- `shesh-voice` repo, `shesh-voice/shesh-overlay/`
- `docs/components/shesh-voice.md`
- `docs/SOURCES.md` §A
