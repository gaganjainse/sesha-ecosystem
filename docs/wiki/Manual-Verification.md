# Manual Verification

Some things cannot be tested in the build sandbox and must be checked on
the physical MSI. The full checklist lives in
[MANUAL_VERIFICATION.md](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/MANUAL_VERIFICATION.md)
and is summarized here.

## Must check on real hardware

- Boot CachyOS/Hyprland at 1920×1200 @ 144 Hz; audio + mic work
- Ollama running with the 6 GB model set (`phi4-mini`, `qwen2.5-coder:3b`,
  `moondream2`, `nomic-embed-text`)
- Restic repo initialized, backup run + a restore tested
- NVIDIA driver loaded, MUX switching works, VRAM stays in budget
- ADB sees the Realme phone; safe-area taps enforced
- Wake word "hey shesh" + STT/TTS
- MCP mesh connected in Newelle; canary e2e passes
- Destructive ACP terminal commands ask for confirmation
- All 9 generated MCP servers appear in `~/.config/shesh/mcp/`

## Deliberate non-autopilot items

- **Kernel merge** (careful Rust work per `KERNEL_MERGE_PLAN.md`)
- **Editor ACP testing** against real Zed/JetBrains
- **Email/CalDAV sync** with vdirsyncer if desired

Run the one-command health check at the bottom of the manual doc.
