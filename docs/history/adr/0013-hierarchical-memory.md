# ADR-0013: Hierarchical Memory + Token-Bounded Context Assembly

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** memory, rag, context-window, token-budget

## Context
Agent needs:
- Episodic memory (what happened today + yesterday).
- Semantic memory (facts that persist).
- Working memory (current goal steps).
- Intentions (long-term goals), mannerisms (tone), habits (frequently done).

LLM context window is finite (phi4-mini ~8k tokens). Naive "dump all history" overflows; naive truncation loses important mannerisms.

Also retention: old episodes should summarize, not live forever.

## Decision
Implement `shesh-memory` with hierarchy:

```
working/         # current task trace (hot)
episodic/YYYY-MM-DD.md  # daily notes, appended
semantic.md      # persistent facts
intentions.md    # user's stated goals
mannerisms.md    # tone/communication style
habits.md        # frequentist learned habits
skills/*.md      # Markdown skills
```

- **ContextAssembler**: token-bounded assembly with priority:
  1. mannerisms
  2. intentions
  3. facts
  4. habits
  5. skills
  6. working
  7. relevant (FTS/vector results)
  8. recent episodes

  Trims lowest priority first; never exceeds model budget.

- **Retrieval**: FTS over episodes + SQLite vector store (cosine) with pluggable Embedder:
  - Offline: deterministic hash embedder (no model needed, tests green).
  - Online: Ollama `nomic-embed-text`.

- **Compaction**: `compact_memory()` MCP tool — summarizes old episodes in batches into `semantic.md` via injectable summarizer (LLM in prod, deterministic stub offline), retention window, very old deleted.

MCP tools: `recall`, `remember`, `semantic_search`, `index_memory`, `compact_memory`.

## Consequences
- ✅ Context never overflows — token budget enforced.
- ✅ Important stuff (mannerisms/intentions) always present.
- ✅ Searchable past — semantic_search returns relevant memories.
- ✅ Compaction prevents infinite growth.
- ❌ Summarizer quality matters — LLM summarizer needs eval.

## Links
- `docs/LEARNING.md`, `docs/components/shesh-memory.md`
- `shesh-memory` (26 tests)
- D6, D14
