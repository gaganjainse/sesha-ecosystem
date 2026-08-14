# README & Docs Style Guide — Shesh fleet

Status: living · last verified 2026-08-14
Applies to: every own repo (non-fork). Forks keep their upstream README.

This is the canonical template every Shesh README follows, grounded in current
(2026) open-source conventions: value-first tagline, 3–5 badges, a copy-paste
quick start inside the first ~200 words, scannable feature tables, and one
focused mermaid diagram per concern.

## The template (in order)

1. **Title + one-line tagline** — what it is, for whom, in one sentence.
   First paragraph must contain the search keywords (e.g. "AI operating
   system", "RAG", "compiler") because it's the first thing a reader/recruiter
   crawls.
2. **Badges** — 3–5 maximum, one line, below the title: language, license,
   version, CI status, test count. No decorative badges ("made with ❤️").
3. **Quick start** — install + first run in ≤5 commands, copy-paste ready.
4. **What it is / Features** — a short pitch paragraph + scannable bullets or
   a feature table. Keep it factual; never claim a capability the code lacks.
5. **Architecture** (mermaid, where it helps) — see below.
6. **Usage / API / CLI** — real examples with expected output.
7. **Project structure** — `tree`-style, current (update when files move).
8. **Development** — build/lint/test commands that actually run today.
9. **Docs / Contributing / Security / License** — link out, don't duplicate.

## Numbers must be real
- Test counts, crate counts, component counts, versions: source them from the
  code (`cargo test`, `pytest --collect-only`, `Cargo.toml`, `pyproject.toml`).
  The fleet's canon gate (`tools/proofread.py --fleet`) forbids retired names,
  and the portfolio facts gate checks the resume numbers — the READMEs must be
  equally honest. No "981", no "Ubuntu", no "v2.0.0" unless the code says so.

## Naming canon
- `SheshAOS` (never NexusAOS / SeshaOS / sesha / seshaos).
- `Kernel bridge` (never "Nexus bridge").
- Org is `github.com/gaganjainse`; contact is `gagan.jain.se@gmail.com`.
  There is no `shesh.dev`, no `shesh` GitHub org, no `@shesh.dev` email.

## Architecture diagrams (mermaid)
Keep them — they're some of the best content in the repo. Rules:

- **One concern per diagram.** Don't paste the same layer diagram twice.
- **Label edges with verbs** (`records to`, `validates`, `routes to`) — not bare
  `-->` where the meaning is unclear.
- **Stay under ~20 nodes**; group by layer with `subgraph`.
- **Use stable names** (crate/component names that match `Cargo.toml` members,
  manifest component names) so the diagram survives refactors.
- **Title each diagram** with `--- title: ... ---` so it renders in all viewers.
- When the architecture changes, update the diagram in the same PR.

## The no-stale checklist (run before shipping any README)
1. No `Ubuntu` unless the project genuinely targets it (bootstrap/ is apt-based,
   and even there it's marked historical).
2. No `.kilo`/`.kilocode`/agent-scratch links; those dirs are gitignored.
3. No wrong-org links (`github.com/shesh/`), no `shesh.dev`, no `@shesh.dev`.
4. Version badge == manifest version. Test badge == actual test run.
5. Every link resolves (the ecosystem's `tools/linkcheck.py` + each repo's CI).

## Regeneration of derived docs
`docs/INDEX.md`, the mdBook (`shesh-docs`), the dependency graph, and
`docs/components/*.md` are **generated** — never hand-edit them. Run:

```bash
python tools/docs_index.py            # INDEX.md
python tools/sync_component_docs.py   # docs/components/*.md
python tools/depgraph.py              # DEPENDENCY_GRAPH.md
DOCS_REPO=/path/to/shesh-docs python tools/book_build.py   # mdBook
```
