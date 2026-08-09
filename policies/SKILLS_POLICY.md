# Sesha Skills & Tools Policy

> How the Brain decides what the Mind is allowed to ask Soma to do. This is the desktop analogue of
> NexusAOS's policy engine: **models propose; the kernel disposes.**

## 1. Tool risk classes

| Class | Meaning | Default | Examples |
|---|---|---|---|
| `auto` | safe, reversible, no side effects outside local state | allow | `get_system_status`, `list_workspaces`, `last_moves`, read-only queries |
| `confirm` | changes local state but is reversible | ask once / remember choice | `organize`, `set_power_profile`, `move_window`, `switch_workspace` |
| `privileged` | affects system/hardware or many files | ask every time | `set_gpu_mode`, `run_backup`, MUX switch, package operations |
| `forbidden` | never run by the agent unprompted | deny | `rm -rf` outside trash, writes to `~/Documents/Job`, `~/Vaults`, `~/.ssh`, network exfil |

## 2. Confirmation surface
- Voice sessions: Sesha speaks a one-line confirmation and waits for "yes/do it".
- Newelle chat: an approval button with a "always allow for this tool" toggle.
- Every decision (allow/deny + reason) is written to the append-only audit log.

## 3. Resource budgets (from nexus-kernel ADR-005)
On the MSI Sword (16 GB RAM / 6 GB VRAM), the brain enforces:
- One GPU model resident at a time; the router evicts before loading another.
- Agent CPU quota 15% avg over 60s (background jobs are `IOSchedulingClass=idle`).
- Memory cap per tool (configurable, 512 MB default for MCP servers).
- Refuse new tasks when over budget and emit `ResourceBudgetExceeded`.

## 4. Learning is append-only
The Mind may propose new "always allow" rules or skill refinements, but they land in a *supplemental*
store (the Prime-Agent "Continual Harness" pattern), never by mutating the base system prompt or this
policy. You review and promote them.

## 5. Network
- Default: **offline**. Local Ollama only.
- Opt-in cloud tier (OmniRoute/etc.) requires `[cloud] enabled = true` and per-session voice confirmation.
- Job folders and secrets are never sent anywhere, regardless of cloud setting.
