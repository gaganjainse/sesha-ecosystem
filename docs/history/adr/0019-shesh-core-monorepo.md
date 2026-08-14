# ADR-0019: Fold sub-service shesh-* modules into shesh-core monorepo

**Date:** 2026-08-13
**Status:** Accepted
**Tags:** architecture, federation, packaging, drift

## Context

The fleet had 22 `shesh-*` Python repos. Fifteen of them were under ~460 LOC of
source, and each re-carried its own `pyproject.toml`, CI workflow, `SECURITY.md`,
and `dependabot.yml` — with subtle drift between them:

- ruff configs differed (some `extend-select=["BLE","TRY"]`, some not; some
  added `select`/`ignore` on top).
- `shesh-files` had no console script, yet the MCP config generator emitted a
  nonexistent `shesh-files-mcp` command.
- Cross-repo deps (`shesh-audit>=0.1`, `shesh-mind>=0.1`) cannot resolve from
  PyPI — the manifest/lock system must build them from git, fragile for anyone
  other than the owner.

Federation (ADR-0003) is the right call for **independently versioned services**.
A 150-line module is not a service — it's a file.

## Decision

Consolidate the 16 sub-service modules + wave config into one repo, **`shesh-core`**:

- One `pyproject.toml` shipping all 16 packages (`shesh_audit`, `shesh_secrets`,
  `shesh_brain`, `shesh_mind`, `shesh_shell`, `shesh_system`, `shesh_files`,
  `shesh_media`, `shesh_messaging`, `shesh_calendar`, `shesh_backup`,
  `shesh_containers`, `shesh_ebpf`, `shesh_skills`, `shesh_mcp_bundle`,
  `shesh_acp`) plus the 15 MCP console scripts — **command names unchanged**, so
  every existing MCP client config keeps working.
- One ruff config, one CI, one license (GPL-3.0-or-later), one SECURITY.md.
- The folded repos are archived with a "superseded by shesh-core" banner.

Keep as separate repos (genuinely independent services):
`shesh-memory`, `shesh-orchestrator`, `shesh-harness`, `shesh-phone`,
`shesh-omniroute` (MIT), plus the domain repos `shesh-desktop`,
`shesh-voice`, `shesh-docs`, `shesh-ecosystem`.

The kept services now depend on `shesh-core>=0.1` (one dep instead of
`shesh-audit` + `shesh-mind`). Import paths are unchanged because core ships the
same top-level packages.

## Consequences

- 22 repos → 6 component repos (+ domain). One repo to patch for the small
  organs instead of sixteen.
- Cross-repo Python deps reduced to a single `shesh-core` (still git-resolved
  via the manifest/lock, but now one edge instead of many).
- The manifest keeps the 23 component *organs* (brain/mind/soma declarations,
  `provides`, channels) — only their `repo` field now points at
  `gaganjainse/shesh-core`. `fetch-components.sh` clones each repo once and
  symlinks shared components; `install.sh` installs unique repos only.
- The folded repos' history is preserved (archived, not deleted).
