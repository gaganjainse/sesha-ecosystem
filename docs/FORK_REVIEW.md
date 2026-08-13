# Fork & Upstream Review — 2026-08-13

Account-wide review of every forked/copied repo against its upstream:
delta, notable upstream changes, adoptions made, and what remains honest.

Legend: behind/ahead = commits vs upstream default branch.

| Fork | Upstream | behind/ahead | Status |
|---|---|---|---|
| **ollama** | ollama/ollama@main | 17/1 | ✅ **ADOPTED** — merged upstream (incl. security fix `server/images: prevent skipVerify map collision with duplicate digests #15504`); dependabot config re-added on top |
| **OmniRoute** | diegosouzapw/OmniRoute@release/v3.8.50 | 139/0 | ✅ **ADOPTED** — fast-forwarded to upstream HEAD (139 commits: SSE/provider/MCP/dashboard/translator fixes, deps bump); meta preserved via API |
| **prime-agent** | PrimeIntellect-ai/prime-agent@main | 11/0 | ✅ **ADOPTED** — fast-forwarded (coding-agent lifecycle fixes, TUI URL handling, Gemini test model fix, release v0.7.2) |
| **pipecat** | pipecat-ai/pipecat@main | 89/6 | ⏸️ **Deliberate divergence** — our 6 ahead commits are the security fixes (transformers 5.15.0, mcp 1.28.1, speechmatics-extra fix). Upstream 89 commits are TTS feature work (Flux TTS controls, Rime fixes, sample-rate fixes) — no security items. Merge would conflict on pyproject.toml; queue for a careful rebase session |
| **shesh-voice** | qwersyk/Newelle@master | 19/7 | ⏸️ **Parked per user order** (libghostty) — upstream added modes/skills-catalog/Mistral TTS/vision-2nd-LLM; our 7 ahead commits are the Shesh overlay work. Review after libghostty decision |
| **leon** | leon-ai/leon@develop | 8/2 | ⏸️ Study fork — upstream is mid web-app-2.0 refactor; no security items; keep until refactor stabilizes |
| **browser-use** | browser-use/browser-use@main | 2/1 | ✅ current enough (2 fixes behind; no security items) |
| **khoj** | khoj-ai/khoj@master | 0/2 | ✅ current; upstream Pages-deploy workflow disabled in fork (cannot run — no Pages on fork; would stay red otherwise) |
| **openWakeWord** | dscripka/openWakeWord@main | 0/1 | ✅ current |
| **servers** | modelcontextprotocol/servers@main | 0/0 | ✅ current |
| **waveterm** | wavetermdev/waveterm@main | 0/6 | ✅ current (6 ahead = our dep-security fixes: dompurify override, undici chain bump) |
| **Hyprland-Dots** | JaKooLit/Hyprland-Dots@main | 0/3 | ✅ current (3 ahead = emoji-data split + CI + dependabot) |
| **Hermes-Function-Calling** | (upstream private/404) | — | archived; CI + dependabot added (account sweep) |
| **hyprdots** | (upstream 404) | — | archived; CI + dependabot added |
| **Memento-Skills / phone-harness / register** | (upstream 404/private) | — | CI + dependabot added |

## Findings worth adopting (upstream, security-relevant)
- **ollama `#15504`** — skipVerify map collision with duplicate digests (server/images): **adopted**.
- pipecat/shesh-voice upstream commits contain **no security fixes** in the scanned window — feature work only, so no urgent adoption needed.

## What was done this sweep (account-wide)
- CI workflows added to all repos lacking one (10 gap repos + 7 archived; fixed 4 real bugs found by the new CIs: Hyprland-Dots emoji-data-as-.sh, grievance-portal dead vite scripts + Laravel bootstrap/cache, VillageClinicLedger invalid setup-java SHA).
- Dependabot configs added everywhere missing (14 earlier + 7 archived + 7 fork gaps).
- Benchmarks: SheshAOS + shesha-kernel bench workflows exist and are green; other repos have no bench infra (honest — no stubs created).
- Fork adoptions above; all rulesets re-enabled after pushes.
