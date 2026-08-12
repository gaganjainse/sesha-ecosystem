# Contributing

This is Gagan Jain's personal ecosystem, orchestrated by AI agents under
written policy. Contributions (human or agent) follow the same rails:

1. **Read TODO.md first** — the anchored list. New work aligns with it or
   amends it (pointer in the same commit).
2. **Gates are the review:** ruff, pytest `-W error`, shellcheck/shfmt,
   actionlint + zizmor on workflows, gitleaks, silent_failures, linkcheck,
   rename_sweep2 — all must be green before a push; nobody knowingly pushes red.
3. **No silent failures, ever:** no suppression, no `|| true`, no bare
   except-pass without an adjacent reason comment. Fix the issue, not the
   symptom (enforced: tools/silent_failures.py).
4. **Docs change with code** in the same commit (DOCUMENTATION_POLICY.md);
   the tell-triple (STATED/VERIFIED/EVIDENCE) for behavior claims.
5. **Security-sensitive changes** (Guard policy, secrets, workflow triggers,
   new MCP tools): read docs/THREAT_MODEL.md first; new tools get pin-learned
   on first boot and refusal-to-drift after.
6. **Immutable classes:** QUERYLOG/ADRs/audit snapshots are records — links
   and name pointers may be repaired, content never rewritten; archive-not-
   delete for everything else.

Questions land in docs/queries/QUERYLOG.md (append-only).
