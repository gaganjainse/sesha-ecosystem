# 📅 shesh-calendar

Local-first calendar/agenda over an iCalendar **vdir** (as used by
vdirsyncer/khal). Reads upcoming events, searches, lists calendars — no
network, sync delegated to vdirsyncer.

- License: GPL-3.0
- Layer: Mind
- Part of: [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)

## MCP tools
`upcoming_events`, `search_calendar`, `list_calendars`, `calendar_status`

## Develop
```bash
uv run pytest -q
uv run ruff check .
uv run shesh-calendar-mcp
```
