# 📜 History — Timeline & Decision Archive

> **Every decision, audit, incident, and retired document lives here.** This folder
> is the single link from the living docs to the historical record — the main docs
> (README → docs/INDEX.md) deliberately do **not** enumerate these; they point here.

## What lives here

| Sub-folder | What it holds |
|---|---|
| [`adr/`](adr/) | Architecture Decision Records — 19 accepted decisions (0001–0019) |
| [`audits/`](audits/) | Dated audit snapshots (exhaustive audit, ecosystem audit JSON) |
| [`incidents/`](incidents/) | Post-mortems for real incidents |
| [`queries/`](queries/) | QUERYLOG — the full prompt/answer decision trail (append-only) |
| [`attic/`](attic/) | Cold storage — superseded documents (archive-not-delete) |
| Root files | Dated, one-off records: `AUDIT_AND_ROADMAP.md`, `GAP_ANALYSIS.md`, `TOOLING_CATALOG.md`, `SITUATION_REPORT.md` |

## Timeline (chronological)

| Date | Event | Record |
|---|---|---|
| 2026-08-09 | 15 founding decisions (languages, containers, federation, channels, local-first, guard policy…) | [adr/](adr/) 0001–0015 |
| 2026-08-10 | shesh-kernel archived; Wave adopted | [ADR-0016](adr/0016-kernel-consolidation.md) |
| 2026-08-11 | Exhaustive audit of all 54 repos | [audits/AUDIT_EXHAUSTIVE.md](audits/AUDIT_EXHAUSTIVE.md) |
| 2026-08-11 | Five-tab swarm collision incident | [incidents/2026-08-11-multi-tab-swarm.md](incidents/2026-08-11-multi-tab-swarm.md) |
| 2026-08-12 | Ecosystem audit JSON + silent-failure sweep | [audits/AUDIT_ECOSYSTEM_2026-08-12.json](audits/AUDIT_ECOSYSTEM_2026-08-12.json) |
| 2026-08-12 | Canonical naming purge (Nexus→Shesh) | [ADR-0017](adr/0017-naming-purge-completed.md) |
| 2026-08-12 | Adopt-vs-build excision | [ADR-0018](adr/0018-adopt-vs-build.md) |
| 2026-08-13 | Fleet "brutal review" audit (60 repos) | [AUDIT_AND_ROADMAP.md](AUDIT_AND_ROADMAP.md) |
| 2026-08-13 | Desktop mirror retired to attic (canonical = shesh-desktop repo) | [attic/desktop-mirror-2026-08-13/](attic/desktop-mirror-2026-08-13/) |
| 2026-08-14 | shesh-core monorepo consolidation (16 folded packages) | [ADR-0019](adr/0019-shesh-core-monorepo.md) |
| 2026-08-14 | Fleet-wide GPL-3.0 license sweep + CI fixes + install dry-run | [queries/QUERYLOG.md](queries/QUERYLOG.md) (newest entry) |

## Rules for this folder

- **Immutable records** (`adr/`, `queries/QUERYLOG.md`, `audits/`) are never rewritten —
  only link/name repairs are allowed (see [`policies/DOCUMENTATION_POLICY.md`](../policies/DOCUMENTATION_POLICY.md)).
- **Archive-not-delete:** obsolete documents move to [`attic/`](attic/), never get deleted.
- The full decision trail is [`queries/QUERYLOG.md`](queries/QUERYLOG.md) — newest first.

---

*This folder is linked from the main workflow (README → docs/INDEX.md) as a single
"History" entry. Regenerate the index with `python tools/docs_index.py` after adding
files here.*
