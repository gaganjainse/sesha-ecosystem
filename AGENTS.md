# AGENTS.md

Operational context for AI coding agents working in the Shesh fleet. Human
documentation is in [shesh-docs](https://github.com/gaganjainse/shesh-docs).

## Overview

Shesh is a local-first agent system for Arch-based Linux desktops. It separates
into three layers: a deterministic governance kernel (Brain), model-driven
reasoning (Mind), and tool servers that sense and act (Soma). Models propose
actions; the kernel validates, executes, and records them in an append-only
hash-chained log.

This repository, `shesh-ecosystem`, owns the component manifest and the gates
that resolve it. It does not own component code.

## Which repository to change

| Change | Repository |
|---|---|
| A tool server or governance primitive | `shesh-core` |
| Memory, orchestration, harness, phone, routing | The matching `shesh-*` service repository |
| Component versions, channels, licence gate | `shesh-ecosystem` (here) |
| Architecture, procedures, reference, policy | `shesh-docs` |
| Skills served to agents | `shesh-skills` |
| Contributor tooling | `shesh-workspace` |
| Superseded records | `shesh-docs-archive` |

Do not span repositories in one change. Sequence them and state the order.

## Setup commands

```bash
make help          # list targets
make lint          # ruff
make test          # pytest
make check         # lint + test; the gate that must pass before promotion
make resolve       # resolve the manifest to a channel lockfile
make depgraph      # dependency graph
make upstream      # report upstream movement (network)
make linkcheck     # documentation links
make verify-all    # full verification
make clean
```

`make check` must pass before anything is committed. A failing gate ends the
task; do not weaken a test to make it pass.

## Code style

- Languages are limited to Rust, Python, Lua, QML/JavaScript, and Bash
  ([ADR-0001](https://github.com/gaganjainse/shesh-docs/blob/main/src/governance/adr/0001-five-languages.md)).
  Adding a sixth needs an ADR.
- Python targets 3.11, formatted and linted with `ruff`, line length 120.
  `BLE` and `TRY` are errors, not style: a blind `except Exception` is where
  silent failures live.
- Rust uses `cargo fmt` and `clippy`.
- Conventional Commit messages: `feat:`, `fix:`, `docs:`, `refactor:`,
  `chore(ci):`.
- One logical change per commit.
- Prefer the standard library. Justify every new dependency and verify its
  licence is compatible with GPL-3.0-or-later.

## Architecture constraints

- **Every tool call passes the policy engine.** Never call a subsystem directly
  to bypass the guard
  ([ADR-0015](https://github.com/gaganjainse/shesh-docs/blob/main/src/governance/adr/0015-guard-policy.md)).
- **Process boundaries, not in-process linking.** Components communicate over
  the Model Context Protocol on stdio. No foreign-function interfaces between
  languages.
- **Local by default.** No network model route is enabled without explicit
  user opt-in
  ([ADR-0005](https://github.com/gaganjainse/shesh-docs/blob/main/src/governance/adr/0005-local-first.md)).
- **The manifest is the single source of truth** for component composition.
  Pages that list components are generated from it, never hand-edited.

## Judgment boundaries

**NEVER**

- Commit a credential, token, or `.env` file. If one appears in a diff, stop and
  report it.
- Force-push, rewrite published history, or push to `main`.
- Weaken a test, a gate, or a policy rule to make a task pass.
- Write to `~/.ssh`, `~/.gnupg`, vaults, or employer directories. The policy
  engine denies these and logs the attempt.
- Report a test as passing without running it.
- Add a volatile count to documentation. Test counts and component counts go
  stale silently.
- State that a component does something without verifying it in the code.

**ASK FIRST**

- Adding a dependency.
- Changing a policy rule or a licence gate.
- Any irreversible action: pruning backups, deleting data, publishing a release.
- Changing the manifest schema.

**ALWAYS**

- Read the relevant files before editing them.
- State the plan before a non-trivial change.
- Run `make check` before committing.
- Add a test with a fix.
- Record a load-bearing decision as an ADR before implementing it.

## Documentation rules

Documentation lives in `shesh-docs` and follows the
[style guide](https://github.com/gaganjainse/shesh-docs/blob/main/STYLEGUIDE.md).

- Each page is exactly one Diátaxis type: tutorial, how-to, reference, or
  explanation.
- Second person, present tense, active voice. Sentence-case headings.
- No first person, no self-assessment ("clean", "robust"), no filler
  ("simply", "just").
- One fact lives in one place. Link, never copy.
- `python3 tools/check_docs.py` enforces this and runs in CI.

## Skills

Agent skills follow the [Agent Skills specification](https://agentskills.io) and
live in `shesh-skills`. `allowed-tools` is a pre-approval that widens
permissions, not a sandbox. Scope it (`Bash(git status:*)`), never grant a bare
shell, and never add it to a skill that governs safety.

## Testing

- Tests are offline. Network, git, and hardware are mocked.
- Hardware-dependent checks are marked, not faked. An unverifiable claim is
  reported as unverified.
- `pytest -q` per component; `make check` for the gate.
