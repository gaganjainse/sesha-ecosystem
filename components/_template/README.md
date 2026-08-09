# Component template — `sesha-<organ>`

Copy this directory when creating a new Sesha component repository (② in the topology). Each
component is independently versioned and tested; the ecosystem pins it in
`manifests/components.toml`.

## Required files

- `README.md` — what it does, which Body layer (brain/mind/soma), how to run.
- `LICENSE` — must be GPL-3-compatible (MIT/Apache-2.0/BSD/GPL-3).
- `manifest.toml`:

```toml
[component]
name = "sesha-<organ>"
layer = "soma"            # brain | mind | soma
version = "0.1.0"
license = "GPL-3.0"
provides = ["capability"]
upstream = { name = "<project>", repo = "<owner>/<repo>", ref = "<tag>" }
```

- `tests/` — unit tests, runnable offline.
- `CHANGELOG.md` — Keep a Changelog format; semver tags.

## Quality gates

A component is promoted from `devel` → `canary` only when:

1. Lint passes (ruff for Python, cargo/clippy for Rust, shellcheck for Bash, stylua for Lua).
2. Offline tests pass on all supported Pythons/toolchains.
3. No incompatible-license dependency (run the ecosystem license gate).
4. The lockfile resolves with the component included.
5. For `soma` components: dry-run works on an Arch/CachyOS container.

## Naming

- Binaries/units: `sesha-<organ>` and `sesha-<organ>.service`.
- MCP servers: `sesha-<organ>-mcp` (stdio transport by default).
- Never use "Jarvis"; the agent is **Sesha**.
- Keep the upstream project's name in attribution; our wrapper is ours.

## Promoting

Bump `version` in `manifest.toml`, tag `vX.Y.Z`, then open a PR against `sesha-ecosystem`
bumping the pin in `manifests/components.toml`. CI runs integration tests; on green it lands in
`canary`. After soak + hardware smoke, a maintainer promotes the component's `channel` to `stable`.
