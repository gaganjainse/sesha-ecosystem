---
name: web-research
description: Research a topic using web search and fetch. Cite sources, prefer primary docs, stay local-first.
---

# Web research skill

1. `web_search(query)` → skim titles/URLs. Prefer official docs, release notes, arch wiki, GitHub.
2. For 2–3 authoritative results, `fetch_url(url)` and extract the relevant section.
3. **Cite every claim** with its URL. Prefer primary sources over blogs.
4. Note the date of the source; flag outdated info.
5. Save useful findings with `append_note("research/<topic>", ...)`.
6. If cloud is off (default), never use an external API; DuckDuckGo HTML + fetch are allowed.
7. Distinguish fact vs recommendation; end with a concrete next step.

Avoid SEO spam and content farms. For code libraries, use Context7-style up-to-date docs
when available (separate MCP), not the model's training cutoff.
