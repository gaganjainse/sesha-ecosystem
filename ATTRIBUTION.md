# Attribution — What we took from whom

> The Shesha ecosystem is GPL-3.0 as a whole, but it stands on the shoulders of open source. This file
> credits every upstream we fork, wrap, or learn from, and states exactly what we use. We do not claim
> others' work as our own; we rename *our wrappers and integrations*, never the upstream project.
>
> The machine-readable version is `manifests/components.toml`. See `docs/SOURCES.md` for the full
> steal-map and rationale.

## Core agent body

| Upstream | License | What Shesha uses | Our wrapper |
|---|---|---|---|
| [qwersyk/Newelle](https://github.com/qwersyk/Newelle) | GPL-3.0 | Voice/wake word/STT/TTS, MCP client, subagents, skills, chat UI | `shesha-voice` (native, config + our MCP servers prewired) |
| [end-4/dots-hyprland](https://github.com/end-4/dots-hyprland) | GPL-3.0 | Hyprland Lua config, Quickshell `ii`, Material You/matugen, AI sidebar | `shesha-desktop` (thin `custom/` overrides, system + AI layers added) |
| [ollama/ollama](https://github.com/ollama/ollama) | MIT | Local model runtime (phi4-mini, qwen2.5-coder:3b, moondream2, nomic-embed) | (runtime dependency, not forked) |

## Brain / governance (Gagan's existing lineage)

| Upstream | License | What Shesha uses | Our wrapper |
|---|---|---|---|
| [gaganjainse/SheshaAOS](https://github.com/gaganjainse/SheshaAOS) | MIT | Event store, policy engine, scheduler, router, tool broker, RPC | `shesha-audit` / `shesha-brain` |
| [gaganjainse/shesha-kernel](https://github.com/gaganjainse/shesha-kernel) | MIT | Architecture ADRs, microkernel research track | (research, integrated selectively) |
| [gaganjainse/SheshaOS](https://github.com/gaganjainse/SheshaOS) | MIT | Specialist model routing (planner/coder/vision) | `shesha-mind` |
| [gaganjainse/rag-service](https://github.com/gaganjainse/rag-service) | MIT | Hybrid dense+BM25+RRF retrieval over ChromaDB | `shesha-memory` |
| [gaganjainse/llm-eval-harness](https://github.com/gaganjainse/llm-eval-harness) | MIT | LLM-as-judge eval for mind quality gates | mind quality gate |

## Ideas and patterns adopted (read, not vendored)

| Upstream | License | Idea borrowed |
|---|---|---|
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | MIT | Skill format, scheduled automations, multi-platform gateway, self-improvement loop |
| [avifenesh/computer-use-linux](https://github.com/avifenesh/computer-use-linux) | Apache-2.0 | AT-SPI + Wayland input/screenshots for desktop control (future `shesha-control`) |
| [block/goose](https://github.com/block/goose) | Apache-2.0 | MCP extension registry, desktop+CLI shape |
| [earendil-works/pi](https://github.com/earendil-works/pi) | MIT | Agent-loop design, supply-chain hardening (lockfile ground truth) |
| [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) | MIT | "Continual Harness" — append-only skill/prompt refinements that never mutate base |
| [ShawnPana/phone-harness](https://github.com/ShawnPana/phone-harness) | MIT | OCR/vision → coordinate → act loop, reimplemented over ADB for Android (`shesha-phone`) |
| [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | MIT | Test-driven learning track for the kernel research |
| [pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat) | BSD-2 | Real-time voice pipeline (barge-in/interruption) if we outgrow Newelle voice |
| [dscripka/openWakeWord](https://github.com/dscripka/openWakeWord) | Apache-2.0 | Fallback/custom "Hey Shesha" wake word model |
| [ML4W](https://github.com/mylinuxforwork) / [JaKooLit](https://github.com/JaKooLit) / [HyDE](https://github.com/prasanthrangan/hyprdots) / [CachyOS Noctalia](https://github.com/CachyOS) | various | statusbar.json pattern, distro guards, Wallbash/theming, animation curves |

## Deliberately NOT vendored (license/architecture reasons)

- **Open Interpreter (AGPL-3.0)** and **Khoj (AGPL-3.0)** — studied for patterns only; if ever used, run as
  isolated separate services, never linked into the GPL-3 body.
- **Suna / Elastic-2.0 / SSPL projects** — source-available, not open source; excluded by the license gate.
- **supergfxctl** — ASUS-oriented, deprecated for non-ASUS; we use our own `msi-mux-switcher` + envycontrol.

## How to keep this accurate

`scripts/check_licenses.py` fails the build if a component's license isn't GPL-3-compatible. When you
add a dependency to `manifests/components.toml`, add a row here in the same commit. The upstream
tracker (`scripts/upstream_tracker.py`) records star/issue/release data in
`channels/upstream-status.json` so we know when to re-sync.
