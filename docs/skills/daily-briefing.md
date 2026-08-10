---
name: daily-briefing
description: Produce a concise morning briefing: calendar/tasks, weather, system health, updates, unread notes.
---

# Daily briefing skill (08:00)

Gather and summarize:
1. **System health:** `get_system_status` (battery, RAM, GPU temp), failed units, last backup.
2. **Updates:** number of pending repo/AUR packages (notify, never auto-update).
3. **Agenda:** today's note `~/Notes/Daily/YYYY-MM-DD.md`, reminders due.
4. **Weather:** optional, only if configured and online.
5. **Inbox:** files in `~/Documents/Inbox` and unprocessed notes.

Output: a short spoken summary (≤5 lines) + a markdown section appended to today's daily note.
Flag anything red (low disk, high temp, backup failure) prominently.
