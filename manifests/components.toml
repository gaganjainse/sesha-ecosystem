# Shesh Ecosystem — component manifest
#
# Every organ of the Agentic Body is declared here. The resolve-manifest script
# validates this file, checks license compatibility, resolves versions, and writes
# shesh.lock. This is the "package repository" metadata in one auditable file.
#
# Channels: stable | canary | devel  (see channels/)
# Layers:   brain | mind | soma

[ecosystem]
name = "shesh"
schema_version = 1
stable_channel = "stable"
body_doc = "docs/architecture/AGENTIC_BODY.md"

# ─────────────────────────────────────────────────────────────────────────────
# BRAIN — governance kernel (your own lineage)
# ─────────────────────────────────────────────────────────────────────────────

[component.shesh-secrets]
upstream = "original"
layer = "brain"
repo = "gaganjainse/shesh-secrets"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["secrets", "credentials"]
notes = "Multi-backend secret resolution (env/gopass/keepassxc/file); no keys in config."

[component.shesh-audit]
layer = "brain"
repo = "gaganjainse/shesh-audit"
version = "0.1.0"
license = "MIT"
channel = "canary"
provides = ["audit-log", "policy-engine", "event-store"]
upstream = { name = "SheshAOS", repo = "gaganjainse/SheshAOS", ref = "main" }
notes = "Bridge to SheshAOS append-only event store and policy engine."

[component.shesh-brain]
layer = "brain"
repo = "gaganjainse/shesh-brain"
version = "0.1.0"
license = "MIT"
channel = "devel"
provides = ["task-router", "scheduler", "tool-broker"]
upstream = { name = "shesh-kernel", repo = "gaganjainse/shesha-kernel", ref = "main" }
notes = "Packaged shesh-kernel for desktop; routes tool calls through policy."

# ─────────────────────────────────────────────────────────────────────────────
# MIND — deliberative models (SheshOS specialist routing, small models on 6GB)
# ─────────────────────────────────────────────────────────────────────────────
[component.shesh-mind]
layer = "mind"
repo = "gaganjainse/shesh-mind"
version = "0.1.0"
license = "MIT"
channel = "canary"
provides = ["intent", "planner", "coder", "vision"]
upstream = { name = "SheshOS", repo = "gaganjainse/SheshOS", ref = "main" }
models = ["phi4-mini", "qwen2.5-coder:3b", "moondream2", "nomic-embed-text"]
notes = "Model routing interface; large SheshOS models map to 6GB-safe equivalents on the laptop."

[component.shesh-memory]
layer = "mind"
repo = "gaganjainse/shesh-memory"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["rag", "episodic-memory", "semantic-memory", "habit-learning", "context-assembly"]
upstream = { name = "rag-service", repo = "gaganjainse/rag-service", ref = "main" }
notes = "Hierarchical memory, habit/intention learning, token-bounded context assembly."

# ─────────────────────────────────────────────────────────────────────────────
# SOMA — the body (desktop, voice, files, devices)
# ─────────────────────────────────────────────────────────────────────────────
[component.shesh-voice]
layer = "soma"
repo = "gaganjainse/shesh-voice"
version = "1.4.5-sesha1"
license = "GPL-3.0"
channel = "canary"
provides = ["wakeword", "stt", "tts", "chat-ui", "mcp-client"]
upstream = { name = "Newelle", repo = "qwersyk/Newelle", ref = "1.4.5" }
notes = "Native (not Flatpak). STDIO MCP, wake word, faster-whisper + Piper."

[component.shesh-files]
layer = "soma"
repo = "gaganjainse/shesh-files"
version = "0.2.0"
license = "GPL-3.0"
channel = "canary"
provides = ["file-organizer", "inotify-watcher", "undo-log"]
upstream = { name = "shesh-desktop smart-organizer", repo = "gaganjainse/shesh-desktop", ref = "main" }
notes = "Rust notify watcher + Python classifier; promoted from shesh-desktop."

[component.shesh-shell]
layer = "soma"
repo = "gaganjainse/shesh-shell"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["mcp:hyprland", "window-control", "workspaces"]
notes = "Hyprland/Quickshell control MCP server."

[component.shesh-system]
layer = "soma"
repo = "gaganjainse/shesh-system"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["mcp:system", "power", "gpu-mux"]
notes = "Power/GPU/MUX MCP + automations."

[component.shesh-skills]
layer = "mind"
repo = "gaganjainse/shesh-skills"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["mcp:skills", "notes", "web-search", "git-tools", "docs", "reminders", "skill-library"]
upstream = { name = "MCP skills pattern", repo = "modelcontextprotocol/servers", ref = "main" }
notes = "Everyday MCP tools + Markdown skills (coding, web research, docs, safety, briefing)."

# ─────────────────────────────────────────────────────────────────────────────
# PROTOCOLS & ORCHESTRATION (P0 gap fill)
# ─────────────────────────────────────────────────────────────────────────────
[component.shesh-acp]
layer = "soma"
repo = "gaganjainse/shesh-acp"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["acp", "editor-integration", "zed", "jetbrains"]
upstream = { name = "Agent Client Protocol", repo = "zed-industries/agent-client-protocol", ref = "main" }
notes = "ACP server so Shesh runs inside Zed/JetBrains with streaming + permissions."

[component.shesh-orchestrator]
layer = "mind"
repo = "gaganjainse/shesh-orchestrator"
version = "0.0.0"
license = "GPL-3.0"
channel = "devel"
provides = ["multi-agent", "rlm", "subagents", "a2a", "role-routing"]
upstream = { name = "Prime Agent RLM", repo = "PrimeIntellect-ai/prime-agent", ref = "main" }
notes = "PLANNED: RLM multi-agent runtime (coordinator/planner/coder/researcher/vision/critic)."

[component.shesh-harness]
layer = "mind"
repo = "gaganjainse/shesh-harness"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["continual-harness", "refine", "auto-skills", "self-evolution"]
upstream = { name = "Memento-Skills / Prime Harness", repo = "Memento-Teams/Memento-Skills", ref = "main" }
notes = "PLANNED: CRUD supplemental state, evidence-backed /refine, auto skill creation + rollback."


[component.shesh-backup]
layer = "soma"
repo = "gaganjainse/shesh-backup"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["backup", "restic", "snapshots"]
notes = "Verified local restic backups; AC-gated and daily-scheduled."



[component.shesh-calendar]
upstream = "original"
layer = "mind"
repo = "gaganjainse/shesh-calendar"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["calendar", "agenda", "ical"]
notes = "Local-first iCalendar vdir reader (vdirsyncer/khal compatible)."

[component.shesh-mcp-bundle]
layer = "soma"
repo = "gaganjainse/shesh-mcp-bundle"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["mcp-bundle", "filesystem", "fetch", "git"]
notes = "Third-party MCP servers (filesystem/fetch/git) proxied behind Guard."


[component.shesh-containers]
layer = "soma"
repo = "gaganjainse/shesh-containers"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["containers", "sandbox", "podman"]
notes = "Unprivileged podman/distrobox sandboxed command execution."

[component.shesh-phone]
layer = "soma"
repo = "gaganjainse/shesh-phone"
version = "0.1.0"
license = "GPL-3.0"
channel = "devel"
provides = ["android-adb", "phone-sensors", "phone-actuators"]
upstream = { name = "phone-harness", repo = "ShawnPana/phone-harness", ref = "main" }
notes = "ADB port of the macOS phone-harness OCR/vision→tap loop for Realme Narzo 90x."

[component.shesh-media]
layer = "soma"
repo = "gaganjainse/shesh-media"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["screenshots", "recording", "wallpaper", "audio-routing"]
notes = "Media tools — grim+slurp screenshots, wf-recorder screen recording, swaybg/hyprpaper wallpaper, wpctl/pactl audio routing — all behind Guard"

[component.shesh-ebpf]
layer = "soma"
repo = "gaganjainse/shesh-ebpf"
version = "0.1.0"
license = "GPL-3.0-or-later"
channel = "canary"
provides = ["ebpf-telemetry", "system-metrics", "performance-sensing"]
notes = "eBPF telemetry with Aya (Rust, read-only) — /proc metrics now, Aya probes later — all behind Guard"

[component.shesh-messaging]
layer = "soma"
repo = "gaganjainse/shesh-messaging"
version = "0.1.0"
license = "GPL-3.0"
channel = "canary"
provides = ["telegram-bridge", "signal-bridge", "messaging"]
notes = "Messaging bridges Telegram/Signal as isolated opt-in services, flag file ~/.config/shesh/messaging/{telegram,signal}.enabled, token via shesh-secrets"

# ─────────────────────────────────────────────────────────────────────────────
# CLOUD GATEWAY — optional free big models via OmniRoute (forked)
# ─────────────────────────────────────────────────────────────────────────────
[component.shesh-omniroute]
layer = "mind"
repo = "gaganjainse/shesh-omniroute"
version = "0.1.0"
license = "MIT"
channel = "devel"
provides = ["omniroute", "free-gateway", "big-models", "cloud-fallback"]
upstream = { name = "OmniRoute", repo = "diegosouzapw/OmniRoute", ref = "main" }
notes = "Forked OmniRoute 291 providers 90+ free 500+ models 1.53B free tokens/mo RTK+Caveman 15-95% compression, optional to local Ollama primary in final product, where enable is user choice (settings GUI). For making ecosystem (dev), use free big models via OmniRoute gateway http://localhost:20128/v1 — industry-used Claude/GPT/Gemini/DeepSeek/Llama/Mistral/Qwen/Kimi/GLM etc free."

[component.shesh-desktop]
layer = "soma"
repo = "gaganjainse/shesh-desktop"
version = "rolling"
license = "GPL-3.0"
channel = "stable"
provides = ["dotfiles", "hyprland-config", "quickshell", "installer"]
upstream = { name = "dots-hyprland", repo = "end-4/dots-hyprland", ref = "main" }
notes = "The desktop body. Thin custom/ overrides; rebase upstream often."
