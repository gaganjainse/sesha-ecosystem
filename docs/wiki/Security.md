# Security

Shesh is local-first and enforces governance at every tool boundary.
The canonical posture, reporting policy, and full control list:

**[SECURITY.md](https://github.com/gaganjainse/shesh-ecosystem/blob/main/SECURITY.md)**
(plus [THREAT_MODEL.md](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/THREAT_MODEL.md)
and [RECOVERY.md](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/RECOVERY.md))

Summary of what is enforced today:

- **Audit log** — append-only, SHA-256 hash-chained events under
  `~/.local/state/shesh/audit/`; `verify_integrity()` detects tampering.
- **GuardedMCP** — policy check before every tool runs, outcome recorded
  after; default for unknown tools is *confirm*, never auto-allow.
- **Tool pins** — tool descriptions are hash-pinned at first boot; any later
  mutation (rug pull) refuses registration until explicitly re-pinned.
- **Supply chain** — every CI action pinned to an immutable SHA; Dependabot
  moves pins weekly; secret scanning + push protection on all repos; gitleaks
  and zizmor are CI gates.
- **Silent-failure audit** — no `|| true`, no swallowed exceptions, no
  fabricated success anywhere in the estate (0-error gate).
