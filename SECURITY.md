# Security Policy

**Canonical home:** this file (ecosystem root). Every `shesh-*` component
links here instead of carrying its own copy — one posture to maintain.

## Reporting a vulnerability

Email/Über private channel is not set up for a solo project yet, so:

- Use GitHub **private vulnerability reporting** on the affected repo, or
- open an issue titled `SECURITY: …` **without proof-of-concept details**, and
  expect contact there for the private thread.

Response target: acknowledged within 7 days, triaged within 30.

## Supported versions

This is a rolling-release ecosystem on `main`. Only the latest `main` is
supported. We do not maintain release branches today; the security model is
"roll forward fast" (see docs/policies/DEPENDENCY_POLICY.md).

## Posture summary (current, verified 2026-08-13)

**Secrets**
- Push protection + secret scanning enabled on all 53 active repos.
- gitleaks gate in every component CI (via the reusable pipeline).
- Secrets are never read into repo files: `tools/git_askpass.py` reads the PAT
  from `~/.config/shesh/github.pat` (mode 600, world-readable refused).
- `shesh-secrets` resolves external stores (gopass/keepassxc/file) at runtime.

**Supply chain**
- All GitHub Actions pinned to immutable SHAs (latest releases), with
  Dependabot opening weekly moves — pins cannot silently rot or be rewritten
  (tj-actions-class attacks).
- cargo-deny + cargo-machete + typos in SheshAOS supply-chain job; two
  documented RUSTSEC ignores only (no-patch-exists / unreachable-path).
- `pip install` in CI installs nothing leniently — no `|| true` anywhere
  (SF4-gated, including inside workflow YAML since 2026-08-13).

**Workflow / CI-CD**
- No `pull_request_target` anywhere. The one instance (swarm auto-merge) ran
  checked-out PR code with a write token — removed 2026-08-13; same-repo
  guard added instead.
- `permissions: read-all` at every workflow top level; writes per-job.
- zizmor static analysis gates every workflow change.
- Checkouts drop the credential after clone (`persist-credentials: false`)
  except the three workflows that legitimately push.

**Attack resistance on the machine**
- Every MCP tool call passes the Guard policy engine (`shesh-audit`),
  default-unknown → **confirm** (never auto-allow).
- Two-phase confirmation flow completed in shesh-brain: every decision and
  every resolution lands in the hash-chained audit ledger.
- Tool-description integrity pins (rug-pull/tool-poisoning defense):
  any mutation after first boot refuses registration until explicitly
  re-pinned (`python -m shesh_audit.tool_pins --repin <server>`).
- No fabricated success anywhere: failure reporting is SF-audited ecosystem-
  wide (0 errors).

**Recovery**
- docs/RECOVERY.md is a tested runbook (executed 4× against real sandbox
  incident patterns in one week).
- `tools/dr_check.sh` verifies the recovery prerequisites are in place.
- Archive-not-delete policy: anything dropped lands in ~/archive/ with a
  manifest, never `/dev/null`.

## Out of scope today (honest)

- Release signing/attestation for SheshAOS images (cosign/Rekor evaluation is
  a deliberate parked item; see TODO).
- Sandbox profile for running third-party MCP servers (we only run our own).
- GUI process isolation on the desktop — nothing here runs setuid; the threat
  model documents what we intentionally do not defend.

See: docs/THREAT_MODEL.md · docs/RECOVERY.md · docs/policies/ (all policies)
