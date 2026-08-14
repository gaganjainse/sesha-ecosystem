# ADR-0007: Six Agent Roles, 6 GB VRAM Budget

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** multi-agent, routing, vram

## Context
One generalist LLM doing planner/coder/vision/critic burns VRAM and conflates skills. Specialist small models on 6 GB RTX 4050 Mobile need routing. We have 16 GB RAM, 6 GB VRAM, 1920x1200@144 Hz target.

Need crew-like specialization without crew AI complexity.

## Decision
Six roles (inspired by Prime Agent + CrewAI):

| Role | Model (6 GB-safe) | Job |
|------|-----------------|-----|
| coordinator | phi4-mini | Triages user goal, delegates |
| planner | phi4-mini | Produces JSON steps |
| coder | qwen2.5-coder:3b | Writes patches/tools |
| researcher | phi4-mini | Web/notes/FTS search |
| vision | moondream2 | Screenshot/OCR/vision→tap |
| critic | phi4-mini | Approves/rejects plan |
| embedding | nomic-embed-text | RAG embeddings |

- `shesh-mind` router: `select_model(role)`, `plan_session()` budgets distinct loaded models — prefers already-loaded to avoid evict/load thrash, honors 5.5 GB budget, fallback chain.
- `shesh-orchestrator`: orchestrates RLM runtime — planner → role agents → critic → trace.
- One GPU model resident at a time; router evicts before loading another (policy in `shesh-system`).

## Consequences
- ✅ 6 GB laptop runs all roles via routing, not OOM.
- ✅ `shesh-mind-mcp` → `list_roles`, `plan_session` auditable.
- ✅ Critic gates `/refine`.
- ❌ Small models weaker than 70B — need careful prompting, JSON extraction (balanced brace scan).
- ❌ Embedding separate from chat models — needs provider abstraction.

## Links
- `docs/architecture/MULTI_AGENT.md`, `docs/components/shesh-mind.md`
- `shesh-mind`, `shesh-orchestrator`
