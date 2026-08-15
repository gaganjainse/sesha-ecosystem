# CLAUDE.md

@AGENTS.md

The operational context for this repository is in AGENTS.md, imported above.
This file adds only what is specific to Claude Code.

## Skills

Agent skills live in [shesh-skills](https://github.com/gaganjainse/shesh-skills).
Install them for this project:

```bash
ln -s ../../shesh-skills/skills .claude/skills
```

Skills follow the Agent Skills open standard, so they also load in Codex,
Cursor, and other compliant agents without modification.

## Frontmatter portability

Claude Code accepts frontmatter fields that the Agent Skills specification does
not. Skills in this fleet stay within the six portable fields — `name`,
`description`, `license`, `compatibility`, `metadata`, `allowed-tools` — so they
package and upload without a hard error.

Do not add `argument-hint`, `disable-model-invocation`, or other Claude
Code-only fields to a skill in `shesh-skills`.

## Permission model

`allowed-tools` pre-approves tools for the turn that invokes a skill. It grants;
it does not restrict. Use `disallowed-tools` to remove a tool, and the
`shesh-audit` policy engine for enforcement that survives outside Claude Code.
