# Fork Gardening Policy (Decision D2 — executed 2026-08-13)

**Rule:** a fork earns its place only if living documentation (excluding
immutable history: QUERYLOG, ADRs, changelogs, audit snapshots) or a
manifest cites it as active plumbing or a load-bearing study source.
Uncited or strictly-superseded forks are **archived, never deleted** —
archiving is reversible with one API call and preserves every byte.

## Verdicts — 2026-08-13 sweep

| Fork | Verdict | Reason |
|---|---|---|
| hyprdots | **archived** | Stale (upstream last push 2025-03); strictly superseded by Hyprland-Dots (2026-02) as the dots study base. Live docs cite the *upstream* project (STYLE_PERFORMANCE, desktop 01_AUDIT), never the fork. |
| Hyprland-Dots | keep | Cited in 6 living docs incl. manifests; current dots study/reference base for shesh-desktop lineage. |
| register | **archived** | Zero true citations — every "register" hit is the English word, not the repo. |
| Hermes-Function-Calling | **archived** | Zero citations anywhere living. |
| leon | **archived** | Only parked as a 🔜-study entry (SOURCES.md, skills architecture). The fork itself is unconsumed; the upstream pointer stays in SOURCES.md for when mining starts. |
| khoj | **archived** | Only appears in an audit tally; nothing living cites it. |
| servers | keep | 39 living refs — MCP protocol reference, load-bearing. |
| ollama | keep | 14 living refs, manifest-cited — local-model plumbing. |
| OmniRoute | keep | 13 living refs, 2 manifest entries — free-model gateway for the ecosystem. |
| openWakeWord | keep | 3 living refs — wake-word path for shesh-voice. |
| phone-harness | keep | 6 living refs, manifest-cited — shesh-phone lineage. |
| Memento-Skills | keep | 3 living refs, manifest-cited — skills architecture source. |
| prime-agent | keep | 4 living refs, manifest-cited — orchestrator study source (D6 lineage). |
| pipecat | keep | 2 living refs — voice-pipeline study source. |
| browser-use | keep | 3 living refs — shesh-browser automation study. |
| waveterm | keep | Active local clone, shell/terminal substrate direction for SheshAOS. |

Re-audit trigger: any fork whose living-doc citation count drops to zero
at a quarterly review gets archived at the next orchestrator session.
