# ADR-0003: Federated Repos + Manifest, Not Monorepo

**Date:** 2026-08-09
**Status:** Accepted
**Tags:** repo-topology, versioning, gates

## Context
We have ~20 components (audit, mind, memory, voice, desktop, etc.). A monorepo would couple Rust and Python releases, make independent versioning hard, and blow up CI (144 Hz display tests can't run in sandbox).

We need:
- Independent semver + CI per component.
- One auditable integration point.
- Offline quality gates before promotion.

## Decision
- **Federated**: each `shesh-*` is its own repo under `gaganjainse/`, with `pyproject.toml`, `src/`, `tests/`, `ci.yml`.
- **Ecosystem repo** (`shesh-ecosystem`) holds `manifests/components.toml` — every organ declared with layer, repo, version, license, channel, provides, upstream.
- `scripts/resolve_manifest.py` validates schema + licenses, resolves versions deterministically, writes `channels/{stable,canary,devel}.lock` with SHA256.
- `scripts/check_licenses.py` refuses GPL-incompatible licenses (AGPL/SSPL only as separate service).
- `scripts/generate_mcp_config.py` emits canonical `servers.json` + Zed/Newelle configs from manifest.

## Consequences
- ✅ `shesh-audit` can release v0.1.0 without bumping `shesh-desktop`.
- ✅ `canary.lock` = tested combination; `stable.lock` = daily driver.
- ✅ 30 ecosystem tests offline; component tests isolated (`--confcutdir`).
- ❌ Need to sync READMEs to `docs/components/` — we automate via doc-sync job.
- ❌ Renames require GitHub redirects (handled — shesha→shesh).

## Links
- `docs/architecture/REPO_TOPOLOGY.md`
- `manifests/components.toml`, `scripts/resolve_manifest.py`
- D4 (channels)
