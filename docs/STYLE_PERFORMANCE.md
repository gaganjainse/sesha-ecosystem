# Style + Performance — Non-Negotiable (illogical-impulse + CachyOS)

> User: "My need is style + performance. I am using illogical impulse because i love its look, and using CachyOS because i love its performance. We can't compromise on this, and last point don't break these systems or anything else per se. I am already using end-4's dots-hyprland so i don't need looks, i need a good backend and other systems that integrate into that look, do you understand. I am not using native Hyprland and need to customize it, i am already using the best customized dotfiles riced look."

## What you are using

- **Look:** `illogical-impulse` — end-4's `dots-hyprland` — the best customized dotfiles riced look, Material You, Quickshell `ii` widgets, anti-flashbang, screen translate, clipboard IPC, keybinds, Lua config Hyprland ≥0.55, Quickshell framework
- **Performance:** CachyOS 260628 (Arch-based, Linux 6.18 live / 7.1 installed, BORE scheduler, LTO, PGO, BOLT, x86-64-v3/v4, Zen4, gaming meta) — you love its performance

You are **NOT** using native Hyprland and need to customize it — you already have best customized look, you need **good backend and other systems that integrate into that look** without breaking it.

## What we must NOT do

- **Do NOT replace look** with DankMaterialShell, ekremx25/quickshell, HyprPanel, ashell, etc — those are different looks that would break illogical-impulse
- **Do NOT switch shells** — CachyOS Noctalia shell is now a Hyprland option on 260628 ISO, but you already have illogical-impulse, don't switch
- **Do NOT break CachyOS performance** — don't install heavy dependencies, don't use Flatpak for Newelle (use native AUR), keep host clean via rootless Podman/Distrobox, keep `custom/` overrides thin, rebase upstream often
- **Do NOT break systems** — don't break Hyprland, Quickshell, CachyOS, or anything else per se

## What we must do — backend that integrates into look

**Backend systems that integrate into illogical-impulse look, without breaking it:**

### Already built, correctly integrated (thin custom overrides)

- **shesh-files** — Rust watcher + Python classifier — watches Downloads/Desktop/Documents/Pictures, debounces 30s, emits JSON, deterministic extension/name rules first (no LLM, instant, private), optional Ollama phi4-mini for ambiguous, vision moondream2 for screenshots, rules.toml, SQLite history + undo log at `~/.local/share/smart-organizer/`, trash via `gio trash` not rm, always --dry-run capable, low-confidence → notify-send action buttons, wire into MCP so Shesh can say "organize downloads" / "undo last move", Quickshell indicator widget (last N moves, pause/resume, open undo) — integrates into illogical-impulse look via Quickshell widget, not replacing bar
- **shesh-shell** — Hyprland/Quickshell MCP — `hyprctl` wrapper + Quickshell IPC, does NOT replace Hyprland config, only controls via existing Hyprland IPC, behind Guard
- **shesh-system** — power/GPU/MUX/backup/status MCP — powerprofilesctl, MUX switch `msi-mux-switcher`, restic backup, update check read-only, health, maintenance cache clean — integrates via systemd user services, not via bar replacement, uses `powerprofilesctl` which CachyOS already has
- **shesh-audit** — hash-chained append-only event log + policy Guard + Nexus bridge — logs every tool call, behind all MCP servers, no UI, no conflict with look
- **shesh-voice** — Newelle fork overlay — wake word "hey shesh", STT faster-whisper, TTS Piper, MCP client stdio, 6GB-safe model defaults, about-screen "Shesh (Newelle core)" — integrates into illogical-impulse AI sidebar (Ollama/Gemini) as host for overlay, not replacing sidebar
- **shesh-ambient** (in desktop) — polite catch-up scheduler + warm proactivity — OnStartupSec + jitter, not fixed wall-clock, heavy jobs need AC+idle, budget bounds, courtesy policy defers during fullscreen/calls/high-CPU/low battery, proactivity one optional offer at natural pause 45s–15m idle throttled ≤3/day snoozeable — integrates via Quickshell overlay, not interrupting look

### Need to build, backend that integrates into look (not look itself)

From `GAP_ANALYSIS.md` + `SOURCES.md` second-wave research, but filtered to **backend only, not look**:

- **shesh-control MCP** — AT-SPI accessibility tree + Wayland input injection + screenshots + compositor window targeting — **needs backend eyes and hands beyond `hyprctl`** — steal from `computer-use-linux` Apache-2.0, wrap as MCP server behind brain policy (destructive actions require approval) — integrates into illogical-impulse look via existing Hyprland windows, doesn't replace look
- **shesh-browser MCP** — drive real browser for web tasks, sandboxed profile — steal from `browser-use` MIT — backend, no UI, integrates via existing browser window
- **shesh-files improvements** — use `notify-rs/notify` RecommendedWatcher cross-platform filesystem notification library Rust (used by Alacritty, cargo watch, mdBook, Zed) — replaces custom polling loop that wastes I/O, <100ms reaction, not replacing look
- **shesh-system improvements** — steal **backend logic only** from `ekremx25/quickshell`: monitor management single `hyprctl --batch` (no flicker) for resolution/refresh/HDR/VRR, night light backend `hyprsunset`/`gammastep` with 1000-6500K slider + fixed-time schedule, not the bar itself; steal `DankMaterialShell` system monitoring TUI library `dgop` + shared QML widgets via `dank-qml-common` — backend, not look
- **shesh-media** — screenshots `grim+slurp` pipeline (already in illogical-impulse? check `configs/quickshell/rishot` — pure Wayland Quickshell app, keybind Print), screen recording, wallpaper, audio routing — backend, integrates into existing keybinds
- **shesh-messaging** — Telegram/Signal isolated opt-in services — backend, separate systemd services, no UI conflict
- **shesh-containers** — podman/distrobox sandboxed `run_sandboxed(["echo","hi"])` with `--cap-drop=ALL --network=none` — backend, no UI
- **shesh-ebpf** — eBPF telemetry with Aya Rust read-only — backend, no UI, behind Guard
- **shesh-omniroute** — free big models gateway 291 providers 90+ free, optional to local Ollama primary — backend, where enable is user choice in settings GUI `SeshaConfig.qml` (in same widget style as General/Bar/Services, not breaking style)

### What we must NOT steal for looks

- **ML4W 2.14.1** `statusbar.json` pattern — single-file Quickshell bar config, declarative bar pattern — **do NOT take GUI configurator**, only steal declarative pattern if needed for backend, but keep illogical-impulse look
- **JaKooLit/Hyprland-Dots** per-monitor refresh scripts, SDDM sugar-candy, Bluetooth menu — borrow logic only, keep end-4 visuals
- **prasanthrangan/hyprdots (HyDE)** Wallbash one wallpaper → all apps theming, themepatcher, `hyde-cli` modularity — we already use matugen, consider Wallbash for apps matugen doesn't cover, but don't replace look
- **CachyOS Noctalia shell** — animation/perf ideas, now Hyprland option on 260628 ISO — compare animation curves and NVIDIA compositing hints, do NOT switch shells
- **Caelestia-shell** Qt6/Quickshell — copy easing/blur parameters QML, no dep change, for 144 Hz smoothness — backend perf, not look

## How we integrate without conflict (cautious but enterprising)

From `REPO_TOPOLOGY.md` + `LANGUAGE_POLICY.md` already, plus second-wave research:

- **One job per component** — `shesh-files` only watches Downloads/Desktop/Documents/Pictures, never touches `Projects/`, `Vaults/`, `Documents/Job`, `.ssh` — protected via `safety.sh`
- **One process per MCP server** — `shesh-audit-mcp`, `shesh-system-mcp`, etc each stdio, separate systemd user services, not shared
- **One policy gate** — every tool call passes Guard `check(actor, tool, args)` → allow/confirm/deny + logged + Nexus event — behind all MCP servers
- **Separate config dirs** — `~/.config/shesh/mcp/` per server, `~/.config/shesh/messaging/` flags, `~/.local/share/shesh/` state, `~/.cache/shesh/` cache
- **Separate btrfs subvolumes** — `AI/Models` nocow, `Downloads` transient, `Documents/Personal` snapshot hourly, `Documents/Job` no snapshot per employer policy
- **Namespace via MCP** — tool names prefixed `fs_*, fetch_*, git_*` via `shesh-mcp-bundle` proxy, so no collision
- **Version pin + license gate** — `manifests/components.toml` + `scripts/check_licenses.py` refuses incompatible licenses
- **Test before push** — `make check` ruff + pytest + license + locks, autopilot refuses red commits
- **Thin custom/ overrides** — keep `custom/` overrides thin in `shesh-desktop` (end-4 base), rebase often, add MCP/automations without diverging `dots/`
- **Quickshell + Go pattern** — from DankMaterialShell, ekremx25: shell framework + Go daemon for system monitoring, shared QML widgets via `dank-qml-common` — separate processes, QML widgets communicate via IPC, not shared memory — adopt same: Go daemon for system, QML for UI, MCP for tools, all separate

## Open-source only, no online-led subscription

User: "Tavily not completely free but subscription based, don't want things that are online-led, only want open-source things"

- **Discarded:** Tavily ($0.005/query, needs API key, closed-source, online-led, subscription), Brave Search ($5/1k queries, needs API key)
- **Keep truly free, no key, open-source:** Filesystem `@modelcontextprotocol/server-filesystem` MIT, Git `server-git` MIT, Fetch `mcp-server-fetch` MIT, Sequential Thinking MIT, Memory knowledge graph MIT, Playwright MCP Microsoft MIT (Apache-2.0), Context7 free optional key, DuckDuckGo privacy-first web search truly free no key, Obsidian fully free, Chrome DevTools fully free, SearXNG AGPL-3.0 self-hosted metasearch 70+ engines no key fully private, agent-search MIT bundles SearXNG zero keys one-command deploy MCP server for AI agents, Tor option

## Upgrade wrapper, not just fork and wrap

Our job is not just to fork and wrap, but to **upgrade the wrapper for our needs and customize and specialize it for our system and improve it** — e.g., Newelle fork stripped GNOME-only assumptions, added Hyprland Quickshell overlay, prewired our MCP servers, set 6GB-safe model defaults, renamed in about-screen to "Shesh (Newelle core)" — that's upgrade and specialization, not just wrap.

Examples:

- **Newelle → shesh-voice:** strip GNOME, add Quickshell overlay, prewire MCP servers, 6GB-safe models, wake "hey shesh", faster-whisper, Piper — upgrade
- **dots-hyprland → shesh-desktop:** keep `custom/` thin, add `shesh` config object to Quickshell settings system + Sesha settings page `SeshaConfig.qml` in same widget style as General/Bar/Services, service `Sesha.qml` applies toggles to systemd units and hyprctl — upgrade, not just fork
- **modelcontextprotocol/servers filesystem → shesh-mcp-bundle:** proxy via Guard with tool prefixing `fs_*`, handshake, skip-if-missing, policy check every call, log + Nexus event — upgrade with governance
- **phone-harness concept → shesh-phone:** macOS-only OCR→coordinate→act loop ported to ADB on Realme Narzo 90x, safe-area bounds, moondream2 vision instead of OCR — upgrade and specialize

This point added to `SOURCES.md` and `REPO_TOPOLOGY.md`.

## How far till CachyOS install and first release with style+performance intact

See `docs/desktop/02_ROADMAP.md` Phases 0–7, but filtered to **backend only, not look**:

- **Phase 0 Pre-install fixes (1–2 sessions):** Fix N-01..N-10 new bugs introduced by prior AI + BUG-05 MSI DMI content check + HIGH-05 zram config + etc — 10 things in `01_AUDIT.md` §E — **must do BEFORE installing CachyOS**, else `./setup install` crashes. Does NOT break look, only backend installer.
- **Phase 1 CI gates (½ session):** Expand ShellCheck to all `.sh`, Arch container CI — so bugs never reach main — backend only
- **Phase 2 Refactor (1–2 sessions):** One source per unit, straight-line read, uninstall actually cleans up — backend maintainability, not look
- **Phase 3 Device tuning (1 session + on-device 🧪):** Monitor `eDP-1,1920x1200@144`, VRR, tearing, NVIDIA hybrid `GBM_BACKEND=nvidia-drm`, iGPU primary for compositing, `prime-run`/`nvidia-run` for offload, MUX via `msi-mux-switcher`, ZRAM 8GB zstd, BORE scheduler, PipeWire low-latency 256 @48k, AX211 Wi-Fi power-save off — **performance tuning, not look**, steals animation curves/easing/blur QML from Caelestia-shell (no dep change) for 144 Hz smoothness — backend perf
- **Till CachyOS install:** **1–2 sessions fixing Phase 0 top 10**

- **Phase 4 Smart-Organizer v2 (2–3 sessions):** watcher-rs Rust `notify` (3 MB) + classifier deterministic rules first (no LLM) + optional Ollama phi4-mini + vision moondream2, rules.toml, SQLite history + undo log, `gio trash` not rm, notify-send action buttons — backend that integrates into illogical-impulse look via Quickshell indicator widget (last N moves, pause/resume, open undo) — **backend, not look**
- **Phase 5 Automations (1–2 sessions):** AC/battery → power profile + GPU hint via udev, nightly deep scan + backup verification + maintenance, weekly `pacman -Syu` notification-only (never auto), disk 80% alert, SMART/battery monthly, font cache via pacman hooks — backend, not look
- **Phase 6 Shesh agent (3–5 sessions):** Newelle 1.4.5 native AUR (not Flatpak) + Ollama ≥0.32 6GB-safe models, 3 MCP servers stdio, Quickshell overlay listening/thinking/speaking states driven by Newelle's OpenAI-compatible endpoint, audit log, daily 08:00 briefing skill, optional ADB phone harness — **backend voice + overlay, not replacing illogical-impulse bar**

- **Till first release (Phases 0–3 first week, 4–5 week two, 6 weeks 3–4):** **~3-4 weeks** with you + AI pair-programmer, if we **steal backend patterns** (monitor management single `hyprctl --batch` no flicker from ekremx25, Night Light backend hyprsunset/gammastep, EQ filter-chain, SearXNG self-hosted free, agent-search MIT, notify-rs RecommendedWatcher) and **do NOT steal/replace look** (keep illogical-impulse).

**We are on right track for Mind/Brain** (memory, harness, orchestrator, skills, audit, mind router, model-agnostic free-first) — 100+ tests, 15 ADRs, swarm via GitHub Issues atomic lock + PR auto-merge + scheduled janitor true hours, secure PAT password flow.
**We were off track for Soma/Desktop** — rebuilt what we should have stolen as backend, introduced 10 new bugs, looked further along than we are because stub files added. Now fixed: keep illogical-impulse look intact, steal backend logic only, expand CI to lint all scripts so N-01..N-09 never slip again.
