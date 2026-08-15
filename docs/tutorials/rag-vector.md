# Tutorial — memory and recall (RAG today, vector search planned)

Status: living · last verified 2026-08-13
Component: [shesh-memory](https://github.com/gaganjainse/shesh-memory)

Honest scope note: `shesh-memory` today stores episodes under
`~/.local/share/shesh/memory/` — **human-readable, portable, no vector DB**.
Embedding retrieval is an explicitly optional future provider, not shipped
code. This tutorial covers what exists, not the roadmap.

## What you get today

- **Memory layers** — short/long-term split per ADR-0013, token-bounded
  context assembly.
- **Habit learning** — frequentist with decay (ADR-0014): routines surface
  without an LLM call.
- **MCP tools (stdio)** — including `recall(query)` to search past episodes
  and context assembly for prompt building.

## Walkthrough

1. Let the agent run for a day; episodes accumulate in the store.
2. Ask "what did we decide about X last week?" — the agent calls `recall`.
3. Inspect the store directly: it is plain files, so `grep` works and
   backups via [shesh-backup](https://github.com/gaganjainse/shesh-backup)
   cover it with the rest of `~/.local/share/shesh/`.

## When vector search lands

The provider seam is designed for it; the migration path is additive (embed
alongside the plain store, keep files canonical). It will be announced in
QUERYLOG and this tutorial updated in the same commit (docs change with
code — [documentation policy](https://github.com/gaganjainse/shesh-docs/blob/main/src/governance/documentation-policy.md) rule 7).
