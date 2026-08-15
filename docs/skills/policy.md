# Skills policy — tool risk classes

Status: living · last verified 2026-08-13
Implementation: `shesh-audit/src/shesh_audit/policy.py` + `mcp_guard.py`
· Decision record: [ADR-0015](https://github.com/gaganjainse/shesh-docs/blob/main/src/governance/adr/0015-guard-policy.md)

Every tool call from every agent passes the audit guard before execution.
The policy is an ordered rule list; first match wins; the default for an
unknown action is **confirm** — Shesh never silently does something it was
not explicitly allowed to do.

## The three verdicts

| Verdict | Meaning | Built-in examples |
|---|---|---|
| `allow` | proceed silently | read-only tools: `get_*`, `list_*`, `search*`, `recall`, `assemble_context` |
| `confirm` | ask the human first | `run_backup`, `set_power_profile`, and **everything unmatched** |
| `deny` | refuse, always | any path under `.ssh/`, `.gnupg/`, `Vaults/`, or job folders |

## Properties that matter

- **Fail-closed default.** An unrecognized tool name matches no rule, so it
  lands on `confirm` — unknown capability can never self-authorize. This is
  deliberate and matches the MCP authorization guidance.
- **Protected paths deny even reads.** Secrets and job data are off-limits to
  every tool regardless of name.
- **Description integrity.** Since 2026-08-13 the guard also pins MCP tool
  descriptions (learn-on-first-boot, refuse-on-drift) so a poisoned or
  rug-pulled server cannot change what a tool claims to do — see
  [THREAT_MODEL](https://github.com/gaganjainse/shesh-docs/blob/main/src/governance/threat-model.md) §MCP and shesh-audit's `tool_pins.py`.
- **Receipts.** Allowed and denied calls are hash-chained into
  `~/.local/share/shesh/audit/events.jsonl` (verification:
  [MANUAL_VERIFICATION](https://github.com/gaganjainse/shesh-docs/blob/main/src/reference/verification-checklist.md) §10).
