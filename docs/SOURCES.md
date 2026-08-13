# Sources & Steal-Map

> Deep research (2026-08-09) into what the Shesh body should absorb, from where, under what license,
> and which part of the Agentic Body it feeds. **"Steal" = adopt/adapt/wrap with attribution; we do not
> violate licenses. Every upstream is forked (①), wrapped as a `shesh-*` component (②), pinned in
> the manifest, AND upgraded/customized/specialized for our CachyOS/Hyprland/6GB VRAM system and improved (③). We are integrating various different systems, but there should be no conflict between them. We have to be cautious but enterprising — namespace via MCP stdio process boundaries, Guard policy allow/confirm/deny, separate systemd services, no in-process FFI, so integrations don't clash.**
> 
> We only want **open-source things** — MIT/Apache-2.0/GPL-3.0, truly free, no API key, no subscription, self-hostable, offline-first. No online-led subscription search like Tavily (paid per query). Use self-hosted open-source alternatives like SearXNG, agent-search (bundles SearXNG, MIT, zero keys), DuckDuckGo MCP truly free no key.

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
- **Steal (from yourself):** `shesh-kernel`, `shesh-rpc`, `shesh-ai` provider abstraction,
  `shesh-terminal`, resource budgets, append-only audit, manifest lifecycle.
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

## J. First-wave intake (done 2026-08-09)

1. **Fork & track:** Newelle, end-4/dots-hyprland — ✅ done, now shesh-voice 41M, shesh-desktop 22M
2. **Promote from shesh-desktop:** `shesh-files`, `shesh-shell`, `shesh-system`, `shesh-voice` (Newelle wrapper config) — ✅ done
3. **Bridge:** `shesh-audit` to SheshAOS event store — ✅ done via KernelBridge
4. **Reference-only (read, don't vendor yet):** Goose, Hermes, pi, Prime, computer-use-linux, pipecat, Leon — ✅ read, cataloged in TOOLING_CATALOG
5. Set up the weekly upstream-tracker bot (see `scripts/upstream-tracker.py`) — ✅ done

## K. Second-wave intake — 2026-08-11 deep research (open-source only, truly free, no API key, no subscription)

> User said: Tavily not completely free but subscription based, don't want things that are online led, only open-source things. Also: our job is not just to fork and wrap, but to upgrade wrapper for our needs and customize and specialize for our system and improve it. We are integrating various different systems, but there should be no conflict — cautious but enterprising.

From web search 2026-08-11 (awesome-hyprland, best MCP servers 2026, CachyOS June 2026, Rust eBPF, file watcher):

### K.1 Desktop shells — Quickshell ecosystem (steal, upgrade, specialize for 1920x1200@144 RTX 4050 6GB)

- **⭐ DankMaterialShell** (AvengeMedia/DankMaterialShell) — MIT, Quickshell+Go, complete desktop shell for Wayland, optimized for Hyprland/Niri/Sway/MangoWC, replaces waybar, swaylock, swayidle, mako, fuzzel, polkit. Provides dankcalendar (local/Google/Microsoft/CalDAV), dgop system monitoring TUI, dank-qml-common shared QML, dankgo common Go modules. **Steal:** calendar integration, system monitoring TUI library, shared QML widgets — upgrade wrapper for our MSI: add power profile + GPU MUX + backup status widgets, specialize for 6GB VRAM budget
- **⭐ ekremx25/quickshell** — MIT, modern feature-rich Wayland shell, modular bar, dock, Material You theming, event-driven, 10-band EQ, multi-monitor, HDR/VRR/10-bit, night light hyprsunset/gammastep, OSD volume/brightness, app drawer fuzzy search, wallpaper picker with matugen, lock screen, mouse/keyboard sensitivity, network/bluetooth/VPN managers, API keys for SmartComplete AI (OpenAI/Claude/Groq/Ollama). **Steal:** bar_config.json declarative pattern, dock drag-and-drop pinning, monitor management single hyprctl --batch (no flicker), night light 1000-6500K slider + fixed-time schedule midnight-wrap, EQ filter-chain, not rebuild
- **⭐ qs-hyprview** (dom0/qs-hyprview) — MIT? Quickshell, native highly customizable Window Switcher/Exposé for Hyprland, 9 mathematical layout algorithms, Qt/QML Wayland Layershell zero latency smooth animations, standalone drop-in replacement, no heavy Python. **Steal:** 9 layout algorithms for overview, upgrade wrapper for our 144 Hz smoothness, specialize for Hyprland workspace overview
- **awesome-hyprland** list: `hyprpaper` (wallpaper daemon IPC), `hyprpicker` colorpicker, `rofi`/`tofi`/`bemenu`/`wofi`/`fuzzel`/`yofi` launchers, `swww` wallpaper daemon live switching animations GIF support, `ironbar` Rust customizable bar, `HyprPanel` TS bar/panel extensive customizability + context menus, `ashell` Rust ready-to-go bar, `ignis` Python GTK4 widget framework
  - **Steal:** `swww` live switching + GIF for wallpaper (better than hyprpaper), `HyprPanel` context menus pattern, `ashell` ready-to-go bar for reference — upgrade wrapper: add Shesh ambient offer overlay, not just bar

### K.2 MCP servers — truly free, open-source, no API key, no subscription (discard Tavily)

From Best Free MCP Servers 2026 (designrevision.com, 2026-07-30): **Truly free, no key, no account, open-source reference servers from @modelcontextprotocol**:

- **Filesystem** — sandboxed local file read/write — truly free, no key — MIT — we already package in shesh-mcp-bundle, but upgrade wrapper: scoped allowed dirs `~/Projects/personal`, `~/Documents/Inbox`, Guard deny `~/Documents/Job`, `~/.ssh`, etc.
- **Git** — repository operations on local repo — truly free — MIT — already packaged, upgrade: add `git_view` read-only + `github_view` via `shesh-secrets` PAT scoped
- **Fetch** — fetch URL and return clean markdown — truly free — MIT — already packaged, upgrade: add user-agent `Shesh/1.0` + timeout + content size limit
- **Sequential Thinking** — structured step-by-step reasoning — truly free — MIT — package next, not built
- **Memory** — persistent knowledge graph — truly free — MIT — we have `shesh-memory` hierarchical but can steal knowledge graph pattern
- **Playwright** — drive real local browser — truly free — MIT — package next: `npx @playwright/mcp@latest` — runs sandboxed, no key
- **DuckDuckGo** — privacy-first web search — truly free, no key — from `shesh-skills` keyless DDG HTML, but now formal MCP server `duckduckgo-mcp` — upgrade wrapper: add rate limit + result deduplication
- **GitHub** — repos, issues, PRs — free with account, needs PAT token — we have `shesh-secrets` multi-backend, okay, open-source reference
- **Obsidian** — read/write Obsidian vaults — fully free, no key — MIT — package for Notes vault `~/Notes/` (Obsidian/logseq)
- **Chrome DevTools MCP** — browser devtools — fully free — open-source

**Discarded per user request (online-led, subscription, not open-source):**
- **Tavily MCP** — closed-source, $0.005/query, needs API key, online-led, subscription — **DISCARDED** — replaced with self-hosted open alternatives below
- **Brave Search MCP** — needs API key, $5/1k queries, not fully free — **DISCARDED** unless user explicitly opts in with key via shesh-secrets
- **Perplexity MCP** — needs API key, subscription — **DISCARDED**

**Open-source self-hosted search alternatives to Tavily (free, no keys, self-hostable, offline-first):**
- **SearXNG** — AGPL-3.0, self-hosted metasearch 70+ engines, no key, fully private, no monthly fees, no vendor lock-in — `docker compose up` — aggregates 70+ sources, we can self-host on `localhost:3939`
- **agent-search** (brcrusoe72/agent-search) — MIT, self-hosted search API + MCP server for AI agents, bundles SearXNG, zero API keys, one-command deploy, 17 endpoints, layered content extraction with optional browser rendering, deduplication cross-engine, prompt injection scrubbing, adaptive failure analysis (evolver), optional Tor-anonymized stack — **open-source alternative to Tavily, Exa, Serper** — `git clone && ./scripts/prepare-searxng.sh && docker compose up`
- **fastCRW** — AGPL-3.0, Rust + bundled SearXNG, Tavily-style endpoints, adapter shim, MCP server: `crw_search, crw_scrape, crw_crawl, crw_map`, Rust runtime ~8 MB image low idle RAM
- **OrioSearch** — MIT, Python FastAPI + SearXNG + Redis, explicit Tavily drop-in
- **TrailSearch / tavily-open** (jianjungki/tavily-open) — MIT, powered by SearXNG and Crawl4AI, self-hosted web search, crawl, content extraction API, low-cost search router local SQLite FTS first, then SearXNG, only call Brave when explicitly enabled

**Steal and upgrade:** Package `agent-search` as `shesh-search` component — MIT, zero keys, one-command, MCP server for Claude Desktop/Cursor, Tor option, better than Tavily because free forever, private, no API key. Upgrade wrapper: add Guard policy (allow search, deny exfil of protected paths), add cache `~/.cache/shesh/search/`, add result ranking via RRF.

### K.3 Rust eBPF / Observability — Aya and friends

From search: **aya-rs/aya** 4.7k★ pure Rust eBPF library, focus developer experience and operability, no libbpf dep, fast builds, BTF portable, supports tokio/async-std

- **Top Rust eBPF projects:** `aya` 4.7k, `oryx` 2.5k TUI sniffing network eBPF, `rbpf` 1.1k Rust VM JIT for eBPF, `kunai` 1k threat-hunting, `pulsar` 1k modular runtime security IoT, `libbpf-rs` 998 minimal opinionated eBPF tooling, `tracexec` 436 tracer for execve/at, `aya-template` cargo-generate template
- **Observability:** `vector` 22.2k, `greptimedb` 6.5k Observability 2.0 DB metrics/logs/traces, `autometrics-rs` 834 easily add metrics, `weaver` 450 OTel Weaver semantic conventions

**Steal:** Use `aya` + `aya-template` `cargo generate --name demo -d program_type=xdp https://github.com/aya-rs/aya-template` for execve/openat/tcp-retransmit tracers — we did stub in `shesh-ebpf` with `/proc` fallback, should upgrade to real Aya programs for execve, openat, tcp_retransmit_skb via `BPF_MAP_TYPE_PERF_EVENT_ARRAY`, read-only, behind Guard allow/confirm/deny — P2 done minimal, future real Rust.

### K.4 File watcher — notify-rs

- **notify-rs/notify** 🔭 3.3k★ cross-platform filesystem notification library Rust, used by Alacritty, cargo watch, mdBook, Zed, etc. Platforms: Linux inotify, macOS FSEvents, Windows ReadDirectoryChangesW, FreeBSD kqueue, iOS etc. — **steal**: replace our custom watcher-rs with `notify` RecommendedWatcher (selects best backend automatically), we already did in `shesh-files` but should ensure we use `notify` crate, not custom polling loop — audit found smart-organizer `--watch` is polling loop, not inotify, wastes I/O

- **Other Rust file managers:** `yazi` blazing fast terminal file manager Rust async I/O, client-server architecture Lua pub-sub, package manager for plugins/themes, integration ripgrep/fd/fzf/zoxide — steal: async task scheduling, real-time progress, package manager pattern for `shesh-files`

### K.5 CachyOS June/August 2026 — performance

From search: CachyOS June 2026 ships Python PGO, GCC patch, OpenBLAS fix, **CachyOS Hyprland Noctalia desktop option**, GNOME Resources app, Welcome app improvements; August 2026 ships Linux 6.18 LTS + 7.1, KDE Plasma 6.7.4, improved installer, Noctalia greeter login screen instead of SDDM. BORE scheduler, LTO, PGO, BOLT, x86-64-v3/v4, Zen4, gaming meta.

**Steal:** Noctalia animation curves + NVIDIA compositing hints, compare BORE vs EEVDF scheduler, use `cachyos-rate-mirrors` + `cachyos-gaming-meta` — already in CachyOS, we should not rebuild.

### K.6 Computer-use agents

- **Best open source AI computer-use agents 2026:** `Fazm` MIT Claude/GPT-4o/Ollama + Accessibility API + vision macOS, `Browser Use` MIT 52k Any LangChain model DOM+vision cross-platform, `Open Interpreter` AGPL-3.0 versatile, `UI-TARS` Apache-2.0 custom fine-tuned screenshot native, `OS-Copilot` Apache-2.0 shell+screenshot Linux/macOS, `OpenAdapt` MIT screenshot+recording, `Skyvern` AGPL-3.0, etc.
- **Our gap:** `computer-use-linux` Apache-2.0 AT-SPI tree + Wayland input injection + screenshots + compositor window targeting — missing eyes/hands for Shesh beyond `hyprctl` — need `shesh-control` MCP behind policy

### L. How we avoid conflicts while being enterprising (cautious but enterprising)

User said: integrating various different systems, but there should be no conflict between them. We have to be cautious but enterprising.

**Design we already have (LANGUAGE_POLICY.md):**

- Five languages only: Rust, Python, Lua, QML/JS, Bash — no Zig/C/Mojo/Go — minimize FFI, cross-language talk is MCP/JSON over processes, not in-process links
- Exotic runtimes go in rootless Podman/Distrobox, not host — reproducible envs, no host pollution
- Federated component repos + manifest/locks, not monorepo — each independently versioned/tested
- MCP over stdio process boundaries — one job per component, one process per MCP server, one policy gate — no in-process FFI, so integrations don't clash
- Guard policy allow/confirm/deny + hash-chained audit + protected paths deny

**New from second-wave research:**

- **Quickshell + Go (DankMaterialShell, ekremx25) shows how to avoid conflict:** Shell framework (outfoxxed/quickshell) + Go daemon for system monitoring, shared QML widgets via `dank-qml-common` — separate processes, QML widgets communicate via IPC, not shared memory — we should adopt same: Go daemon for system, QML for UI, MCP for tools, all separate
- **HyprPanel / ashell / qs-hyprview:** Each is standalone drop-in replacement, no heavy Python background processes, logic entirely in QML/JS — we should keep our shell as standalone drop-in, not modifying Hyprland core, so no conflict with Noctalia (CachyOS option) — user can switch shell via `hyprland.conf` `exec-once`
- **Aya eBPF:** Pure Rust, no C toolchain, BTF portable — eBPF programs run inside kernel, not userspace, so no conflict with userspace MCP servers — separate domain

**Cautious but enterprising checklist:**

- [ ] One job per component — `shesh-files` only watches Downloads/Desktop/Documents/Pictures, never touches `Projects/`, `Vaults/`, `Documents/Job`, `.ssh`
- [ ] One process per MCP server — `shesh-audit-mcp`, `shesh-system-mcp`, etc each stdio, not shared
- [ ] One policy gate — every tool call passes Guard `check(actor, tool, args)` → allow/confirm/deny + logged + kernel event
- [ ] Separate config dirs — `~/.config/shesh/mcp/` per server, `~/.config/shesh/messaging/` flags, `~/.local/share/shesh/` state, `~/.cache/shesh/` cache
- [ ] Separate btrfs subvolumes — `AI/Models` nocow, `Downloads` transient, `Documents/Personal` snapshot hourly, `Documents/Job` no snapshot per employer policy
- [ ] Namespace via MCP — tool names prefixed `fs_*, fetch_*, git_*` via `shesh-mcp-bundle` proxy, so no collision
- [ ] Version pin + license gate — `manifests/components.toml` + `scripts/check_licenses.py` refuses incompatible licenses (AGPL/SSPL only as separate service)
- [ ] Test before push — `make check` ruff + pytest + license + locks, autopilot refuses red commits

## M. Discard what we made if something better exists (no pointless brooding)

User: we can discard what we made if there is something better we can steal. We should never engage in pointless brooding.

- **Discard custom power/GPU logic** — steal Night Light backend `hyprsunset`/`gammastep` + EQ filter-chain + monitor management `hyprctl --batch` from `ekremx25/quickshell` instead of rebuilding
- **Discard custom bar/panel** — steal `HyprPanel` context menus pattern + `ashell` ready-to-go bar + `qs-hyprview` 9 layout algorithms for overview
- **Discard custom file watcher polling loop** — audit found smart-organizer `--watch` is polling loop not inotify, wastes I/O — replace with `notify-rs/notify` RecommendedWatcher (selects best backend automatically)
- **Discard custom web-search/fetch DDG HTML scraper** — package `agent-search` MIT self-hosted SearXNG zero keys + DuckDuckGo MCP truly free no key + `SearXNG` self-hosted metasearch 70+ engines, no API key, fully private
- **Keep only Shesh-specific organs** — `shesh-audit` hash-chained, `shesh-brain` packaged kernel, `shesh-mind` 6GB VRAM router, `shesh-memory` hierarchical + habit learning, `shesh-harness` continual harness + /refine, `shesh-orchestrator` RLM + A2A UDS + sessions, `shesh-ambient` catch-up scheduler + warm proactivity
- **Package, don't rebuild** — mature MCP servers: Filesystem, Git, Fetch, Sequential Thinking, Memory, Playwright, Context7, DuckDuckGo, Obsidian, Chrome DevTools — all truly free no key, MIT/Apache-2.0, open-source reference servers from Model Context Protocol project

## N. First-wave intake (done 2026-08-09) — kept for history

1. **Fork & track:** Newelle, end-4/dots-hyprland — ✅ done
2. **Promote from shesh-desktop:** `shesh-files`, `shesh-shell`, `shesh-system`, `shesh-voice` — ✅ done
3. **Bridge:** `shesh-audit` to SheshAOS event store — ✅ done
4. **Reference-only:** Goose, Hermes, pi, Prime, computer-use-linux, pipecat, Leon — ✅ read
5. Upstream-tracker bot — ✅ done

