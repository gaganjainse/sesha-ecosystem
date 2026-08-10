---
name: docs-writer
description: Write and convert documentation and notes in Markdown. Keep them organized, linked, and dated.
---

# Docs & notes skill

- **Capture first:** `append_note("inbox", ...)` for quick thoughts.
- **Structure:** notes live under `~/Notes/{Daily,Tech,Ideas,Meetings,Sesha}`.
  Daily notes are named `YYYY-MM-DD.md`.
- **Markdown everywhere:** use headings, tables for comparisons, code fences with language.
- **Convert docs:** `convert_to_markdown(path)` for PDF/DOCX/XLSX (pandoc).
- **Link notes:** use relative `[[wikilinks]]`; tag with `#tag` at the bottom.
- **Keep an index:** maintain `~/Notes/README.md` with links to active notes.
- When answering from notes, `search_notes` first and cite the file.
- Never put secrets in notes. Use `~/Vaults` (KeePassXC) instead.
