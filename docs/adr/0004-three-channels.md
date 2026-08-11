# ADR-0004: Three Release Channels

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** releases, promotion, safety

## Context
Developer machine is CachyOS daily driver on MSI Sword 16 HX. Breaking the desktop shell blocks work. We need staging like a Linux distro: raw work → integration soak → stable release.

Naive single-branch releases caused workspace-over-budget and broken Hyprland keybinds landing directly on main.

## Decision
Three channels with strict promotion:

- **devel**: every component's `main` head; `devel.lock` = all 19 components (stable+canary+devel). Daily dev, may break.
- **canary**: daily canary CI (`.github/workflows/canary.yml`) on Arch/Fedora/Ubuntu matrix + `e2e-canary.sh` covering all 16 MCPs; `canary.lock` = 16 components. Soak 24h.
- **stable**: only `auto-desktopenv` (desktop) after btrfs snapshot verified. Promoted manually after MANUAL_VERIFICATION.

Rules:
- `resolve()` filters: stable=0, canary≤1, devel≤2 rank.
- Promotion only via PR that includes green CI + lock regeneration (`make check`).
- Installer supports `--channel stable|canary|devel` with pre-install `btrfs subvolume snapshot` + rollback boot entry.

## Consequences
- ✅ Nothing reaches stable without canary e2e green.
- ✅ `channels/*.lock` SHA256 auditable.
- ✅ Developer can test `canary` in VM/DistoBox before laptop.
- ❌ Three lockfiles to keep in sync — `make check` does it.
- ❌ Rollback needs btrfs (documented, not ext4).

## Links
- `channels/`, `scripts/e2e-canary.sh`, `Makefile`
- D3, SESSION_HANDOFF §7
