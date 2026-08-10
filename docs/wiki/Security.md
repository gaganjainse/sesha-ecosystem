# Security

Shesh is local-first and enforces governance at every tool boundary.

## Audit log

Every action is recorded in `~/.local/share/shesh/audit/events.jsonl`:

- Events are **append-only** and **hash-chained** (SHA-256 of each event
  includes the previous hash). `verify_integrity()` detects tampering.
- The `GuardedMCP` wrapper (in shesh-audit) checks policy **before** a tool
  runs and records the outcome **after**.
- A parallel `nexus-events.jsonl` is written in SheshAOS's Rust event format
  so the governance kernel can consume the same stream.

## Policy

The default policy:

- **Allow silently**: read-only tools (`get_*`, `list_*`, `search*`, `recall`)
- **Deny**: protected paths (job folders, `.ssh`, `.gnupg`, vaults)
- **Confirm**: everything else (the editor/voice UI surfaces the prompt)

Rules are evaluated in order; the first match wins. Runtime rules can be
prepended via `add_rule`.

## Secrets

- API keys and passwords are **never stored in MCP config files**.
- `shesh-secrets` resolves references like `env:VAR`, `gopass:path`,
  `keepassxc:attr=value`, or `file:/0600-file`.
- File-based secrets are refused if the file is group/world-readable.

## Sandboxing

- `shesh-containers` runs untrusted commands in ephemeral podman containers
  with `--rm`, `--network=none`, `--cap-drop=ALL`, and PID limits.
- The `shesh-mcp-bundle` proxies upstream filesystem/fetch/git servers
  through the same Guard; protected paths are denied before they reach the
  upstream server.

## ACP hardening

- `terminal/exec` requires `confirm=true` for destructive commands
  (`rm`, `sudo`, `mkfs`, `dd`, redirection, etc.).
- Path escapes outside a session's cwd are refused.
- Editors connect over stdio only; no network listeners.

## Verifying

```bash
# Check the hash chain
shesh-audit-mcp  # then call verify_integrity

# Confirm protected paths are denied
# (any MCP tool writing to ~/.ssh should return denied)
```

See the `Security` section of [[Manual-Verification]] for hands-on checks.
