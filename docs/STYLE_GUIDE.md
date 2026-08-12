# Documentation Style Guide — uniform and pure by construction

One page, applied everywhere. When this guide and an old doc disagree, fix
the doc. Exceptions get a comment at the exception site, not a fork of the
standard.

## Structure

- Exactly **one `#` H1** per document: its title, first line.
- Sections: `##`, subsections `###`; never skip levels (`#` → `###`).
- Tables for comparisons/config matrices; prose for reasoning; code fences
  with a language tag (```bash, ```python) — never bare fences.
- Status line at the top of governed docs: `Status: living · last verified YYYY-MM-DD`.
- The tell-triple where claims live: **STATED** (claim) → **VERIFIED** (gate)
  → **EVIDENCE** (file/test/runbook).

## Language

- Short sentences. Imperative mood for instructions.
- Canonical names only: **SHESH** (assistant/OS), `shesh-*` components,
  `SHESH_*` env vars, SheshAOS for the AOS project. Legacy names appear
  solely in immutable-history files.
- No emojis in body text of policies/security docs (docs may use them in
  dashboards/summaries only).
- Dates ISO `YYYY-MM-DD`; `ACC` era-tags only where the user table uses them.

## Formatting

- Markdown lint-clean: no trailing whitespace, single blank line between
  blocks, lists use `-`, code spans for paths/flags (`--dry-run`, file.md).
- Links: descriptive text, never bare URLs; cross-repo → absolute
  `https://github.com/gaganjainse/<repo>/blob/main/...`.
- Shell examples are `set -euo pipefail`-safe: no `|| true`, no unquoted
  expansions, 4-space continuation indent (shfmt -i 4 -ci compatible).

## Review bar

A doc is done when: a newcomer can follow it without asking; every claim
names its proof; every link resolves; the orphan gate knows its parent.
