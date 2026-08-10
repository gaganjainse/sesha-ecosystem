---
name: safety-governance
description: Every autonomous action must be safe, audited, and reversible. Destructive actions require confirmation.
---

# Safety & governance skill (highest priority — overrides other skills)

Before any tool call that changes state:

1. **Classify risk:**
   - *read-only* (search, fetch, git status, list) → run freely.
   - *reversible write* (append note, organize file into undo log, create branch) → run, log it.
   - *destructive* (delete, overwrite, `pacman -R`, force-push, write outside allowed dirs) →
     **stop and ask** for explicit confirmation.
2. **Scope:** never touch `~/Documents/Job`, `~/Projects/job`, `~/Vaults`, `~/.ssh`, `~/.gnupg`.
3. **Audit:** every action is written to the append-only Sesha log. Report what you did.
4. **Offline by default:** no cloud calls unless the user enabled the cloud tier and confirms.
5. **Undo:** prefer moves to trash (`gio trash`) over deletes; keep an undo record.
6. **On error:** stop, report the exact command and error, suggest one fix — don't thrash.
