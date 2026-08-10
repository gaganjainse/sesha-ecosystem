# Tooling & Skills Catalog

> What turns Shesh from a demo into a full ecosystem. We **build** the Shesh-specific organs
> (system, shell, files, skills) and **package** the best mature open-source MCP servers for the
> rest — pinning versions, wrapping them in our policy/audit layer. This catalog is the intake list.

---

## 1. Organs we build (already in the ecosystem)

| Component | Repo | Provides |
|---|---|---|
| shesh-system | gaganjainse/shesh-system | power/GPU/MUX/backup, system status |
| shesh-shell | gaganjainse/shesh-shell | Hyprland/Quickshell control |
| shesh-files | gaganjainse/shesh-files | real-time organizer (Rust+Python) |
| shesh-skills | gaganjainse/shesh-skills | notes, web, git, docs, reminders + skill library |
| shesh-voice | (fork of Newelle) | STT/TTS/wake word, chat UI |
| shesh-audit/brain/mind/memory/phone | planned | governance, routing, RAG, ADB |

## 2. Mature MCP servers we package (do NOT rebuild)

Pin each in a component repo; run as a stdio MCP server behind the Shesh policy.

| Need | Recommended server | License | Why |
|---|---|---|---|
| Local filesystem | **@modelcontextprotocol/server-filesystem** (Anthropic) | MIT | Scoped, read/write controls; we point it only at allowed dirs |
| Git operations | **server-git** (Anthropic) | MIT | status/diff/log without shelling out |
| Web fetch | **mcp-server-fetch** (Anthropic) | MIT | Safe URL→markdown fetch (use alongside our fetch_url) |
| Sequential reasoning | **server-sequential-thinking** | MIT | Complex multi-step problem solving |
| Memory | **server-memory** (knowledge graph) | MIT | Persistent entity/relation memory |
| Browser automation | **Playwright MCP** (Microsoft) | Apache-2.0 | Real browser for JS sites/testing; runs sandboxed |
| GitHub | **github-mcp-server** | MIT | Issues/PRs/CI using your PAT (read-only by default) |
| SQLite | **server-sqlite** | MIT | Local analytics/history DBs |
| Time/calendar | **server-time** | MIT | Timezone-aware scheduling |
| Docs (PDF/Office) | **markitdown-mcp** (Microsoft) | MIT | Convert PDF/DOCX/XLSX→markdown |
| Browser devtools | **chrome-devtools-mcp** | Apache-2.0 | Web dev/debugging |
| Search (optional) | **Tavily MCP** / Brave | varies | API-key search; DuckDuckGo in shesh-skills needs no key |

All are stdio and lockfile-pinned via `uvx`/`npx`. We never run an MCP server with broader
filesystem/shell access than its task needs (principle of least privilege + our policy engine).

## 3. Skills library (Markdown, in shesh-skills/skills)

Shipped: `coding`, `web-research`, `docs-writer`, `safety-governance`, `daily-briefing`.

To add next (each is a small Markdown file + optional tool wiring):

- **email-messaging** — read/send via local client/CLI (e.g., `neomutt`/`thunderbird` API), never store passwords.
- **calendar** — CalDAV (`vdirsyncer` + `khal`) for local-first scheduling.
- **terminal-ops** — safe shell patterns over SSH (wraps sheshaos-terminal patterns).
- **container-ops** — podman/distrobox control (build/run/list) for sandboxed tasks.
- **kernel-tuning** — eBPF/telemetry queries (research track), read-only by default.
- **media** — screenshots, screen recording, wallpaper, audio routing.
- **job-mode** — isolated profile: work git identity, no personal cloud, different theme.
- **writing** — long-form editing with markdown/pdf export.
- **finance** — parse bills/invoices into `~/Documents/Personal/Finance`.
- **language** — Vyākṛti integration; translation/sanskrit tooling.

## 4. What we deliberately avoid (for now)

- **Hosted SaaS MCPs** (Notion, Slack, Linear, Stripe) until the cloud tier is explicitly opted in
  and audited; local-first is the default.
- **Arbitrary shell-execution MCPs** ("run any command") — we use scoped servers + policy instead.
- **AGPL servers linked into the body** — if needed, run as isolated separate services.
- **Multiple agent runtimes** — Newelle is the host; Goose/Hermes/pi are references, not daemons.

## 5. Promotion

Each third-party server is wrapped in a component repo that:
1. pins the version (`uv.lock`/`package-lock.json`),
2. sets its allowed directories/env in a config under `~/.config/shesh/mcp/`,
3. is registered in `manifests/components.toml`,
4. passes the same lint/test/license gate,
5. runs through `shesh-audit` so every tool call is logged.
