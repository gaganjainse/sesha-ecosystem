# Learning Architecture

How Shesh learns intentions, habits, and mannerisms without destabilizing itself
or overflowing the model's context window.

## Layers

1. **Working** — current task/session, always in context and small.
2. **Episodic** — append-only JSONL events (`remember`) with SQLite FTS.
3. **Semantic** — durable facts about the user (`note_fact`), editable Markdown.
4. **Intentions** — active goals with priority and lifecycle.
5. **Mannerisms** — communication style preferences, editable Markdown.
6. **Habits** — corroborated recurring patterns with confidence/decay.
7. **Procedural/Harness** — learned skills and supplemental prompt refinements.

## Context assembly

`shesh-memory assemble_context(query, working, max_tokens)` builds a bounded prompt
in priority order: mannerisms, intentions, semantic facts, active habits, skills,
working task, relevant episodes, recent tail. Lowest-priority sections are trimmed
first so the prompt always fits.

## Habit learning

`shesh-memory learn_habit(signature, description, success)` counts observations
with reliability-weighted confidence. After enough corroboration it becomes a
candidate habit; confidence decays over time and stale habits archive. This is
frequentist, not hidden model state, so the user can inspect/edit/disable it.

## Continual Harness

`shesh-harness refine(trigger, trajectory)` proposes the smallest supported
change to supplemental state, evaluates it, applies only if the score passes,
records before/after, and supports revert. Immutable base prompt and safety
skills cannot be changed. This prevents overfitting/cheating loops and makes
self-improvement reviewable.

## Ambient feedback loop

`shesh-ambient` observes coarse signals (workspace switches, idle, completed
commands) and records episodes/habits without keystroke-level surveillance.
Proactive offers are informed by active intentions and habits but always optional.

## Retention policy

- Episodes retained indefinitely but summarized/archived by a future compaction job.
- Habits decay with a two-week half-life and archive below threshold.
- Harness refinements are append-only; bad ones are reverted, not deleted.
