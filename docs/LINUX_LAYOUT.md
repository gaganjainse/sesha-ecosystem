# Linux Filesystem Layout & Shesh Integration

> Linux has a well-defined hierarchy (FHS) plus XDG user dirs. We respect it instead of dumping
> everything in `$HOME`. This keeps the system clean, makes backup policies precise, and ensures
> the package manager, systemd, and containers all find what they expect.

---

## 1. System directories (owned by the distro / pacman)

We **never** hand-edit these except via the package manager or our installer:

| Path | Purpose | Shesh interaction |
|---|---|---|
| `/usr/bin`, `/usr/lib` | distro packages | installs via `pacman`/AUR only |
| `/usr/local/bin`, `/usr/local/lib` | sysadmin-local binaries | our `nvidia-run`, `msi-mux-switcher` symlinks |
| `/etc` | system config | udev rules, `sysctl.d`, `zram-generator.conf`, mkinitcpio |
| `/boot` | kernels/bootloader | only via `mkinitcpio`/bootloader config tooling |
| `/var` | system state/logs | journal, pacman cache |
| `/run`, `/tmp` | runtime/ephemeral | never persist anything here |

Rule: anything in `/etc` or `/usr/local` we add carries a comment `# managed-by=shesh-desktop`
so `2.undo-setups.sh` can revert it precisely.

---

## 2. User directories (XDG Base Directory spec)

| Variable | Path | What lives there |
|---|---|---|
| `XDG_CONFIG_HOME` | `~/.config` | dotfiles (Hyprland, Quickshell, Newelle, Shesh config) |
| `XDG_DATA_HOME` | `~/.local/share` | app data: Shesh audit log, Chroma memory, icons, fonts |
| `XDG_STATE_HOME` | `~/.local/state` | venvs, logs, history, systemd user state |
| `XDG_CACHE_HOME` | `~/.cache` | regenerable caches (**never backed up**) |
| `XDG_BIN_HOME` | `~/.local/bin` | user binaries (sm-watcher, shesh-*-mcp) |

Every Shesh component obeys these via the shared `tools/lib/common.sh` and Python `platformdirs`/
`pathlib` conventions — no hardcoded `~/.sesha` sprawl.

---

## 3. Where each Shesh component stores data

| Component | Config | State/data | Cache |
|---|---|---|---|
| Shesh MCP servers | `~/.config/shesh/` | `~/.local/state/shesh/.venv` | `~/.cache/sesha` |
| Audit log | — | `~/.local/share/shesh/audit/` | — |
| Smart-organizer | `~/.config/smart-organizer/` | `~/.local/share/smart-organizer/{history.db,undo}` | `~/.cache/smart-organizer` |
| Ollama models | `~/.config/ollama` | **`~/AI/Models/ollama`** (symlinked, large) | — |
| HuggingFace | — | **`~/AI/Weights-Cache`** | — |
| Newelle | `~/.config/newelle` | `~/.local/share/Newelle` | `~/.cache/Newelle` |
| Quickshell | `~/.config/quickshell` | `~/.local/share/quickshell` | — |
| Hyprland | `~/.config/hypr` | `~/.local/state/hyprland` | — |
| Restic backups | `~/.config/shesh/backup.conf` | `~/Backups` repo | — |

The large AI assets stay under `~/AI/` (excluded from snapshots/backups — regenerable) while config
and the audit log stay in their proper XDG homes.

---

## 4. systemd unit search paths (user vs system)

| Kind | Path | Used for |
|---|---|---|
| system units | `/etc/systemd/system/`, `/usr/lib/systemd/system/` | `nvidia-suspend`, zram, display manager |
| user units | `~/.config/systemd/user/` | Shesh MCP servers, organizer watcher, timers |
| system drop-ins | `/etc/systemd/system/<unit>.d/` | overrides we add |

Our installer `install -Dm644` units into the user dir; it never writes to `/usr/lib`.

---

## 5. Containers (Podman/Distrobox)

| Path | Purpose |
|---|---|
| `~/.local/share/containers` | rootless podman storage (images/volumes) |
| `~/.config/containers` | podman registries/policy |
| Distrobox homes | inside the container; host `$HOME` is shared |

This is why we use **rootless Podman** — all container state stays under the user's XDG data dir,
no daemon, no root-owned `/var/lib/docker`.

---

## 6. Reorganization summary (what changed from a flat `$HOME`)

- `~/Pictures`, `~/Music`, `~/Videos` consolidated into **`~/Media/{Images,Music,Videos,...}`**.
- `~/Downloads` is transient (auto-sorted, 30-day cleanup).
- `~/Desktop` renamed **`~/Desk`** and kept empty.
- Code split into **`~/Projects/{job,personal,labs,forks,_archive}`**.
- AI assets isolated in **`~/AI/{Models,Datasets,Vectors,Weights-Cache,Sessions}`**.
- Secrets in **`~/Vaults`** (700 perms), notes in **`~/Notes`**.

The one-time layout creator is `tools/setup-dirs.sh` (idempotent, dry-run capable).
