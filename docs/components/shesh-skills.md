# shesh-skills

**everyday tools + Markdown skills** — Notes, web search/fetch, git, docs, reminders.

- Layer: Mind (Mind)
- License: GPL-3.0
- Part of: [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)

---
**Everyday tools and skills for the Shesh agent.** A stdio MCP server plus a library of
Markdown skills covering notes, web research, coding, docs, scheduling, and safety/governance.

- License: GPL-3.0
- Spans: Soma (actuators) + Mind (workflows)
- Part of: [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)

## Tools (MCP)

| Tool | Does |
|---|---|
| `append_note` / `find_notes` / `search_notes` | markdown notes vault (`~/Notes`) |
| `web_search` / `fetch_url` | DuckDuckGo HTML search + URL→text (no API key) |
| `git_status` / `git_log` / `github_view` | repo inspection |
| `convert_to_markdown` | pandoc wrapper for docs |
| `remind` | desktop notification scheduler |

## Skills (`skills/*.md`)

`coding`, `web-research`, `docs-writer`, `safety-governance`, `daily-briefing`.
Skills are prompt-level workflows the agent loads per task; the safety skill always applies.

## Develop

```bash
uv sync --extra dev
uv run pytest -q          # offline; network/git are mocked
uv run ruff check .
uv run shesh-skills-mcp
```

## Design

- **Local-first:** web uses the keyless DuckDuckGo HTML endpoint; no cloud keys.
- **Testable:** all side effects go through `runner.run`, monkeypatched in tests.
- **Safe:** destructive actions require confirmation (see the safety-governance skill).