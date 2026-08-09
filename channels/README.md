# Channels

Channels are release filters, exactly like a distro's `core` / `testing` / `devel` repos.

| Channel | Contains | Promoted when | Runs on |
|---|---|---|---|
| `stable` | only components tagged `stable` in the manifest | canary soaks N days, no regressions, manual sign-off | **your MSI Sword (production)** |
| `canary` | `stable` + `canary` components | each component passes its own tests and the integration suite | a VM / secondary account |
| `devel` | everything (`stable` + `canary` + `devel`) | component works on a developer branch | development only |

The lockfile is channel-specific:

```bash
python scripts/resolve_manifest.py --channel stable  --out channels/stable.lock
python scripts/resolve_manifest.py --channel canary  --out channels/canary.lock
python scripts/resolve_manifest.py --channel devel   --out channels/devel.lock
```

Promotion is gated by `scripts/gates/` (future): lint → unit tests → integration tests on an
Arch/CachyOS container → hardware smoke (display/GPU/audio) → soak timer. No component reaches
`stable` without passing every gate, and every promotion creates a btrfs snapshot before applying.
