# 📅 shesh-calendar

Local-first calendar/agenda over an iCalendar **vdir** (as used by
vdirsyncer/khal). Reads upcoming events, searches, lists calendars — no
network, sync delegated to vdirsyncer.

Email (roadmap P1): `tools/setup-email.sh` configures local-first IMAP sync
into `~/.maildir` + a neomutt config — same discipline (network only during
sync, all mail local, secrets via shesh-secrets env, never written to disk).

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

## Security

Security posture and vulnerability reporting: [canonical ecosystem security
policy](https://github.com/gaganjainse/shesh-ecosystem/blob/main/SECURITY.md).
