# Threat Model — Shesh ecosystem

Audience: anyone changing security-relevant behavior (Guard policy, MCP
servers, CI workflows, secrets handling, the desktop). Read before touching
those surfaces.

## Assets (what we protect)

1. **GitHub PAT + org** — fine-grained PAT at `~/.config/shesh/github.pat`;
   compromise = org-wide code control.
2. **The hash-chained audit ledger** (`~/.local/state/shesh/audit/*.jsonl`) —
   the forensic record; tamper-evident, not tamper-proof.
3. **Local secrets** in external stores (gopass/keepassxc) resolved by
   shesh-secrets; tokens (Telegram bot, Signal account) at runtime.
4. **The desktop machine itself** — files, camera/mic paths (media, voice),
   displays, GPU.
5. **CI integrity** — 26 repos auto-merging outputs users run locally.

## Actors

- Malicious/compromised **third-party dependency or Action** (supply chain).
- **Prompt injection** through content an agent ingests (docs, web pages,
  tool outputs, MCP tool descriptions).
- **Rug-pull / poisoned MCP tool** (description mutated post-approval —
  Invariant Labs 2025-04 class).
- Compromised **upstream fork** we track (dots, terminal, models list).
- Rogue **swarm worker / PR author** (the auto-merge path).
- Physical/OS-level compromise — **out of scope**: we assume the OS keeps
  its guarantees; we do not defend against a root-level attacker.

## Surfaces & controls (each: state + evidence)

| Surface | Threat | Control | Evidence |
|---|---|---|---|
| PAT file | leak via git/transcripts | push protection + secret scanning (53/53 repos); gitleaks gate; askpass refuses world-readable PAT; rotation reminder open | SECURITY.md; component-ci.yml gitleaks step |
| Audit ledger | silent tampering | sha256 hash chain, `verify()`; verify-runbook in RECOVERY.md | shesh-audit log.py |
| MCP tool defs | rug pull, poisoning | tool-pin verify at both seams (decorator + middleware middleware middleware), poisoning markers scan | shesh-audit tool_pins.py + tests |
| MCP tool calls | destructive action | Guard allow/confirm/deny; two-phase confirmations in shesh-brain | gate.py, brain 81777f5 |
| **Lethal trifecta** | agent with private-data + untrusted-content + external-comms simultaneously | architectural rule below | below |
| GH Actions | tag rewrite (tj-actions) | all actions SHA-pinned; Dependabot moves pins weekly | 2026-08-13 sweep, 26 repos |
| GH Actions | fork PR RCE (pull_request_target) | trigger removed fleet-wide; same-repo guard; read-all default tokens; zizmor gate | swarm-auto-merge.yml |
| GH Actions | injection via PR metadata | fields pass through env, never inline (actionlint-gated) | PR body handling comments |
| Dependencies | known CVEs | Dependabot alerts + auto-security-fixes + weekly bump PRs (pip+actions); cargo-deny | org API state |
| Backups | silent loss | shesh-backup + recovery drill | docs/RECOVERY.md |
| Vendor forks | upstream rug-pull (dots etc.) | thin overrides; rebase reviewed; archived forks excluded from audits | manifest policy |

## The lethal-trifecta rule (hard rule for component design)

A component must not combine all three of: **(a) reads private data**,
**(b) ingests untrusted content**, **(c) can exfiltrate** (network send).
Examples of compliant splits living today: shesh-messaging sends but reads no
private stores; shesh-secrets reads stores but has no network surface;
shesh-knowledge ingests content but cannot send. New components get checked
against this in review (it is in the component README template).

## Residual risks (accepted, documented)

1. Prompt injection has **no complete mitigation** (Willison's curse) — we
   reduce blast radius via the trifecta split + confirmations, we do not
   claim prevention.
2. TOFU pins: a poisoned FIRST version would be learned as good. Accepted for
   our own-authored servers; third-party MCP servers are not auto-mounted —
   a deliberate decision, revisit before adopting any.
3. The PAT itself is a standing credential on disk. Mitigations are
   push protection, least scope, and the pending rotation reminder. OIDC/
   app-token replacement is the follow-up when multi-agent workers run in
   Actions only.
4. Voice/audio paths (shesh-voice) implicitly trust local audio daemons.

## Verification discipline

Security claims in this repo follow the house tell-triple: what is STATED
here, what is VERIFIED by which gate/test, what EVIDENCE to check. A claim
without a gate rots silently — every row above names its enforcement point.
