# Sources & Steal-Map

> Deep research (2026-08-09) into what the Shesh body should absorb, from where, under what license,
> and which part of the Agentic Body it feeds. "Steal" = adopt/adapt/wrap with attribution; we do not
> violate licenses. Every upstream is forked (①), wrapped as a `shesh-*` component (②), and pinned in
> the manifest. This document is the intake log.

Legend: **MIND** / **BRAIN** / **SOMA**; license; ⭐ = first-wave (do now), 🔜 = later.

---

## A. The user-facing agent / mind

### ⭐ Newelle (qwersyk) — GPL-3.0  → `shesh-voice`
Frontend + voice + wake word + MCP client. Already our primary mind shell.
- **Steal:** wake word (1.3.0+), STT faster-whisper, TTS (Kokoro/Piper/Edge), MCP client (stdio+http,
  1.4.5 supports STDIO on native), subagents (1.3.5), skills, scheduled tasks, file permissions,
  chat folders/branching, OpenAI-compatible local API (1.4.0), Telegram interface.
- **Watch issues/features for:** better MCP tool lazy-loading, per-profile models.
- **Our fork (`shesh/` branch):** strip GNOME-only assumptions, add Hyprland Quickshell overlay,
  prewire our MCP servers, set 6 GB-safe model defaults, rename in about-screen to "Shesh (Newelle core)".
- **Do NOT take:** Flatpak manifest (use native AUR), cloud provider defaults.

### 🔜 Goose (block/goose) — Apache-2.0  → reference for `shesh-mind`
Model-agnostic agent, 70+ MCP extensions, CLI+desktop. Steal: MCP extension registry patterns, the
desktop+CLI shape, provider abstraction. Don't replace Newelle; mine it for extension ideas.

### 🔜 Hermes Agent (NousResearch) — MIT  → reference for skills/cron/gateway
Self-improving agent with skills creation, cron automations, multi-platform gateway (Telegram/Discord),
6 execution backends. Steal: skill format, scheduled automations, gateway (talk to Shesh from phone).
Its companion `computer-use-linux` (Apache-2.0) is the blueprint for deeper Soma control.

### 🔜 Open Interpreter — AGPL-3.0 (careful)  → patterns only
AGPL is **incompatible with linking** into our GPL-3 desktop unless we keep it as a separate
process/service. Use its approval-prompt and code-execution sandboxing patterns; do not vendor code.

### 🔜 pi (earendil-works) — MIT  → reference
The agent-loop harness under Prime Agent. Steal: supply-chain hardening (lockfile as ground truth,
lifecycle allowlist), clean agent-loop/state design. Read-only inspiration.

### 🔜 Prime Agent / RLM Harness (PrimeIntellect) — MIT  → reference
"Continual Harness": a supplemental prompt/skill store refined with evidence without mutating the base
system prompt. **This is exactly how Shesh should learn safely.** Implement in `shesh-mind`.

---

## B. Brain / governance (your own lineage)

### ⭐ SheshAOS (you) — MIT  → `shesh-brain`
The kernel: event store, policy engine, scheduler, router, tool broker, RPC. Already 981 tests.
- **Steal (from yourself):** `sheshaos-kernel`, `sheshaos-rpc`, `sheshaos-ai` provider abstraction,
  `sheshaos-terminal`, resource budgets, append-only audit, manifest lifecycle.
- **Adapt:** target CachyOS/Hyprland instead of Ubuntu/GNOME; make policy gate MCP tool calls; expose
  the event log as `shesh-audit`.
- **Branches to study:** `bolt-optimize-raf-loop` (UI perf), `palette-ux-theme-switcher-a11y`
  (accessibility/theme), `recovery/phase-1` (resilience). Fold the good bits in.

### ⭐ shesh-kernel (you) — MIT  → research track
Alpha microkernel. Steal the architecture ADRs (vte over Zig FFI, JSON-RPC id fix, resource budgets,
policy-decision events, wgpu terminal). Many of these are *desktop-app* lessons directly applicable to
a Quickshell/terminal Shesh UI. Keep as research, not daily driver.

### 🔜 SheshOS (you) — MIT  → `shesh-mind` spec
Specialist model routing (planner/coder/vision). Steal the router logic and manifest spec. On 6 GB
VRAM, map its three large models to small equivalents (phi4-mini / qwen2.5-coder:3b / moondream2) and
keep the same interface so bigger models drop in later.

### 🔜 llm-eval-harness (you) — MIT  → `shesh-mind` reflection
LLM-as-judge golden-set eval. Use it to grade specialists and gate mind changes.

---

## C. Soma — desktop shell and looks

### ⭐ end-4/dots-hyprland — GPL-3.0  → base of `shesh-desktop`
Our shell base. Steal: Lua config (Hyprland ≥0.55), Quickshell `ii` widgets, Material You/matugen,
AI sidebar (Ollama/Gemini), anti-flashbang, screen translate, clipboard IPC, keybinds.
- **Upstream strategy:** keep `custom/` overrides thin; rebase often. Add our MCP/automations without
  diverging `dots/`.
- **Watch:** their Quickshell/Lua migrations; their AI sidebar is a host for our overlay.

### 🔜 ML4W 2.14.1 — GPL-3.0  → `statusbar.json` pattern
Single-file Quickshell bar config; steal the declarative bar pattern and (optionally) the welcome app
concept. Don't take the GUI configurator.

### 🔜 JaKooLit/Hyprland-Dots — (check license, GPL-ish)  → robustness patterns
Distro guards, per-monitor refresh scripts, SDDM sugar-candy, reliable Bluetooth menu. Borrow logic
only; keep end-4 visuals.

### 🔜 prasanthrangan/hyprdots (HyDE) — GPL-ish  → theming
Wallbash (one wallpaper → all apps theming), themepatcher, `hyde-cli` modularity. We already use
matugen; consider Wallbash for apps matugen doesn't cover.

### 🔜 CachyOS Noctalia shell — (CachyOS)  → animation/perf ideas
Now a Hyprland option on the 260628 ISO. Compare animation curves and NVIDIA compositing hints; do
not switch shells.

### 🔜 Caelestia-shell — Qt6/Quickshell  → animation curves
Copy easing/blur parameters (QML, no dep change) for 144 Hz smoothness.

---

## D. Soma — file/automation organs

### ⭐ Our own smart-organizer (in shesh-desktop)  → `shesh-files`
Rust `notify` watcher + Python classifier + MCP. Promote to its own repo; add:
- **Steal from `waku-agent`** (MIT): single-afternoon agent harness shape (loop/memory/eval) — use as
  the structural model for `shesh-files`'s agent mode, not a dependency.
- **Steal from OpenAdapt** (MIT): record-and-replay demonstration for automations.
- Trash via `gio trash`; undo log; SQLite history (already specced).

### 🔜 system-aidai/**openclaw** family (MIT if used) → gateway ideas
Personal agent servers (moltis/clawdbot) — single Rust binary, sandboxed, multi-LLM, voice, Telegram.
Reference for packaging Shesh as one binary later.

### 🔜 Leon (leon-ai/leon) — MIT  → skills architecture
17.4k★ open personal assistant, Python+Node, skills/memory layers. Older but clean; mine its skill
packaging and i18n.

### 🔜 pipecat-ai/pipecat — BSD-2  → real-time voice pipeline
13.9k★ framework for voice/multimodal conversational pipelines. Use if we outgrow Newelle's voice
pipeline (interruption, barge-in, low latency).

### 🔜 openWakeWord (dscripka) — Apache-2.0
Fallback if Newelle's wake word is insufficient; train a custom "Hey Shesh" model.

---

## E. Soma — computer/device control

### 🔜 computer-use-linux (avifenesh) — Apache-2.0
AT-SPI accessibility tree + Wayland input injection + screenshots + compositor window targeting. This
is the missing "eyes and hands" for Shesh on Hyprland beyond `hyprctl`. Evaluate maturity; wrap as
`shesh-control` MCP server, behind brain policy (destructive actions require approval).

### 🔜 OS-Copilot / OS-Copilot (Ubuntu) — Apache-2.0
Linux-oriented shell+screenshot agent; good reference for Linux-first control.

### 🔜 browser-use — MIT
Drive a real browser for web tasks. Wrap as `shesh-browser` MCP; run in a separate sandboxed profile.

### ⭐ phone-harness concept (ShawnPana) — MIT  → `shesh-phone`
macOS-only; we port the OCR→coordinate→act loop to **ADB on the Realme Narzo 90x**. Use `moondream2`
vision instead of OCR. Direct coordinates via `adb shell input`.

---

## F. Mind — memory and knowledge

### 🔜 Khoj — AGPL-3.0  → patterns only (or separate service)
Self-hosted second brain over docs/ Obsidian/Emacs. AGPL means run as a **separate service** the brain
talks to, don't link. Great reference for personal RAG. We have our own `rag-service` (MIT) which is
preferred and license-clean.

### 🔜 AnythingLLM / Jan / GPT4All — MIT/Apache
Reference UIs and local model management; not direct deps.

---

## G. Build-your-own / learning track (build-your-own-x, MIT)

Use the test-driven, increment-by-increment tutorials for the `shesh-kernel` research track:
build-a-shell, build-a-database, build-an-interpreter, build-a-docker. Not production code; a learning
scaffold so the AI-first kernel vision is grounded, not fantasy.

---

## H. Dotfile/rice leaderboard signals (star-history / trendshift)

Fastest-moving in 2026: Newelle (voice/MCP), Hermes/pi/Prime (agents), end-4/Noctalia/Caelestia
(Quickshell shells). The signal: **Quickshell + MCP + local voice** is the winning combo — exactly our
stack. We're surfing the wave, not fighting it.

---

## I. License compatibility summary for our GPL-3 body

| License | Vendored into GPL-3 code? | Notes |
|---|---|---|
| MIT / BSD-2 / Apache-2.0 | ✅ yes, with attribution/NOTICE | bulk of the ecosystem |
| LGPL | ✅ dynamic linking only | Quickshell |
| GPL-3 | ✅ same license | Newelle, end-4, HyDE |
| AGPL-3.0 | ⚠️ separate service only | Open Interpreter, Khoj — never link |
| Elastic/SSPL/source-available | ❌ no | Suna and similar — skip |

We maintain `NOTICES.md` and a per-component `LICENSE` in each `shesh-*` repo. The manifest gate
(`scripts/check-licenses.py`) refuses incompatible licenses.

---

## J. First-wave intake (do now)

1. **Fork & track:** Newelle, end-4/dots-hyprland.
2. **Promote from shesh-desktop:** `shesh-files`, `shesh-shell`, `shesh-system`, `shesh-voice`
   (Newelle wrapper config).
3. **Bridge:** `shesh-audit` to SheshAOS event store.
4. **Reference-only (read, don't vendor yet):** Goose, Hermes, pi, Prime, computer-use-linux,
   pipecat, Leon.
5. Set up the weekly upstream-tracker bot (see `scripts/upstream-tracker.py`).
