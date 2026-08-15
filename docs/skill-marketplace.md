# Skill Marketplace — Sharing Evolved Skills (Opt-in, P2)

> Future: skill marketplace / sharing evolved skills (open-space.cloud style, opt-in) — P2

## Concept (from open-space.cloud)

- Skills are Markdown files in `skills/` + MCP tools in `src/shesh_skills/`
- When agent learns via `/refine` (Read→Execute→Reflect→Write) and a skill scores >=0.7 on held-out evaluator, it becomes candidate for marketplace
- Marketplace is local-first JSON file `~/.local/share/shesh/marketplace/index.json` with skill metadata, not cloud
- Opt-in sharing: if user enables `marketplace.share=true`, anonymized skill (no personal data, no secrets) can be published to `shesh-marketplace` repo (future) via PR
- Other users can browse and install: `shesh-skills-mcp -> install_skill("autopilot")`

## Current Implementation (Minimal, P2 done)

- `shesh-skills` already has 5 markdown skills: coding, web-research, docs-writer, safety-governance, daily-briefing + autopilot
- Skill capture framework exists: Read→Execute→Reflect→Write via shesh-harness
- Deprecation: low-success skills (<0.3 score over 10 uses) auto-archived to `skills/archived/`

## Marketplace Index (local)

```json
{
  "skills": [
    {
      "name": "autopilot",
      "version": "0.1.0",
      "author": "gaganjainse",
      "description": "Autonomous safe progress — pick next todo, branch, implement, test, commit",
      "path": "skills/autopilot.md",
      "mcp_tools": ["start_session", "get_session"],
      "score": 0.85,
      "uses": 42,
      "success_rate": 0.9,
      "shareable": true
    }
  ]
}
```

## Opt-in sharing (future, when marketplace repo exists)

```bash
# Enable sharing
mkdir -p ~/.config/shesh
echo "share=true" > ~/.config/shesh/marketplace.conf

# Publish skill (anonymized, no secrets)
shesh-skills-mcp -> publish_skill("autopilot")
# Creates PR to https://github.com/gaganjainse/shesh-marketplace with skill file + metadata
```

## Security

- No secrets in skills — Guard denies writes to .ssh, Vaults/, Job folders
- Skills are Markdown + MCP tool definitions, not arbitrary code
- Marketplace index is local-first, cloud opt-in behind policy

## Status: P2 done minimal

- Docs: this file
- Implementation: skill capture + deprecation in shesh-skills, marketplace index local JSON
- Future: actual shesh-marketplace repo with PR-based sharing (open-space.cloud style)
