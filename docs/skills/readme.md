# Skills — the behavior library

Status: living · last verified 2026-08-13
Runtime component: [shesh-skills](https://github.com/gaganjainse/shesh-skills)
· Policy: [POLICY](POLICY.md)

Skills are Markdown documents with YAML frontmatter (`name`, `description`)
that steer agent behavior for a recurring task class. This directory is the
canonical text; `shesh-skills` serves them to agents over MCP.

## The set

| Skill | Job |
|---|---|
| [coding](coding.md) | read-before-edit discipline, tests always, never push unreviewed |
| [web-research](web-research.md) | source-cited research protocol |
| [docs-writer](docs-writer.md) | documentation in the house [style](../STYLE_GUIDE.md) |
| [safety-governance](safety-governance.md) | the immutable safety layer (never refined away) |
| [daily-briefing](daily-briefing.md) | morning/evening digest format |
| [autopilot](autopilot.md) | safe unattended progress rules |

## Rules

- Safety skills are **immutable** — the continual harness (shesh-harness)
  can refine supplemental state but never the base safety layer.
- New skills arrive as Markdown with frontmatter; no code shipment, so a bad
  skill can degrade style but never execute anything by itself.
