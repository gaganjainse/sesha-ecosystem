# 🐍 Shesh Ecosystem

> The federated, local-first AI body for CachyOS/Hyprland. **An agent is a body** — a *Mind*
> (models/planning), a *Brain* (SheshAOS governance/event-sourced kernel), and a *Soma* (sensors and
> actuators on the desktop). This repository is the **orchestrator**: it pins forks, resolves
> components through quality gates, and promotes them from `devel` → `canary` → `stable`, like a
> miniature Linux distribution.

- **License:** GPL-3.0 (the body as a whole; components keep their own upstream-compatible licenses)
- **Owner:** Gagan Jain ([@gaganjainse](https://github.com/gaganjainse))
- **Target hardware:** MSI Sword 16 HX B14VEKG (i7-14700HX, RTX 4050 6 GB, 1920×1200@144, 16 GB DDR5)
- **Target OS:** CachyOS 260628 + Hyprland ≥0.55 (Lua) + Quickshell

---

## Why this repo exists

We fork every upstream we depend on and keep those forks rolling. We steal the best ideas and code from
the open-source agent/desktop world, rename and integrate them as **Shesh components**, and only let
tested combinations reach the daily driver. This gives us:

- **Latest upstream** without waiting for releases (forks track `main`).
- **Safety** — breakage is caught in canary, not on your machine.
- **Coherence** — one manifest, one lockfile, one audit log, one policy engine.
- **Ownership** — the integrated whole is *Shesh*, not a pile of someone else's brands.

Read the conceptual foundation: [`docs/architecture/AGENTIC_BODY.md`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/architecture/AGENTIC_BODY.md).
Read the federation model: [`docs/architecture/REPO_TOPOLOGY.md`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/architecture/REPO_TOPOLOGY.md).
Language choices: [`docs/architecture/LANGUAGE_POLICY.md`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/architecture/LANGUAGE_POLICY.md).
Environments (Podman/uv): [`docs/CONTAINERS_AND_VENV.md`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/CONTAINERS_AND_VENV.md).
Linux layout: [`docs/LINUX_LAYOUT.md`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/LINUX_LAYOUT.md).
Tooling/skills catalog: [`docs/TOOLING_CATALOG.md`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/TOOLING_CATALOG.md).
See the [glossary](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/GLOSSARY.md).

See everything we absorb: [`docs/SOURCES.md`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/docs/SOURCES.md) and [`ATTRIBUTION.md`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/ATTRIBUTION.md).

---

## Repository layout

```
shesh-ecosystem/
├── manifests/components.toml   # every Shesh organ (brain/mind/soma), versions & upstreams
├── channels/                   # stable.lock / canary.lock / devel.lock (resolved)
├── scripts/
│   ├── resolve_manifest.py     # TOML -> lockfile, validates schema + licenses
│   ├── check_licenses.py       # GPL-3 compatibility gate
│   └── upstream_tracker.py     # checks forks vs upstream releases/issues
├── tests/                      # offline tests for all gates (pytest)
├── policies/                   # tool/skill policy (what the agent may do)
├── components/                 # component integration specs (one subdir per organ)
├── docs/architecture/          # AGENTIC_BODY, REPO_TOPOLOGY
└── Makefile                    # make lint / test / check / upstream
```

---

## Quick start (developer)

```bash
# 1. Run all quality gates (offline — no hardware needed)
make check

# 2. Resolve a specific channel
python scripts/resolve_manifest.py --channel canary

# 3. See which upstreams moved (network)
make upstream
```

`make check` runs lint (ruff), 13 offline tests, the license gate, and writes all three channel
locks. It must pass before anything is promoted.

---

## The three layers

| Layer | Components | Source lineage |
|---|---|---|
| **Brain** | `shesh-audit`, `shesh-brain` | SheshAOS / shesh-kernel (your Rust governance kernel) |
| **Mind** | `shesh-mind`, `shesh-memory` | SheshOS model routing + rag-service + llm-eval-harness |
| **Soma** | `shesh-voice`, `shesh-files`, `shesh-shell`, `shesh-system`, `shesh-phone` | Newelle, shesh-desktop, your MCP servers, ADB harness |

See `manifests/components.toml` for the full list and `components/` for integration docs.

---

## Promotion flow

```
upstream forks ──▶ component repos ──▶ shesh-ecosystem integration ──▶ canary ──▶ stable
     ①                  ②                        ③                       ④          ⑤
 (track main)     (tests+semver)          (integration tests)        (soak/VM)   (your laptop)
```

Every arrow is a gate in `scripts/` (CI runs them). Nothing reaches ⑤ without a green gate and a
btrfs snapshot before apply. The policy engine governs all tool actions the agent takes — see
[`policies/SKILLS_POLICY.md`](https://github.com/gaganjainse/shesh-ecosystem/blob/main/policies/SKILLS_POLICY.md).

---

## Testing

All tests are offline and hardware-independent; they validate manifests, the resolver, the license
gate, channel filtering, determinism, and upstream parsing.

```bash
python -m pytest tests/ -q
```

Component repos carry their own unit/integration tests; hardware tests (GPU/display/audio) run only in
the canary gate on real or VM hardware.

---

## Status

Ecosystem-wide CI is green: one reusable component pipeline (D1) covers all
21 components with `-W error`; silent-failure audit 0 errors; every third-party
Action is SHA-pinned with Dependabot moving the pins weekly. See
[SECURITY.md](SECURITY.md) for the posture and
[docs/THREAT_MODEL.md](docs/THREAT_MODEL.md) for the threat model.

## Documentation index

The full map: **[docs/INDEX.md](docs/INDEX.md)** (generated, CI-checked).

- **Start here:** [TODO.md](TODO.md) — master roadmap · [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) · [docs/GLOSSARY.md](docs/GLOSSARY.md)
- **Security:** [SECURITY.md](SECURITY.md) · [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md) · [docs/RECOVERY.md](docs/RECOVERY.md)
- **Policies:** [docs/policies/](docs/policies) — dependency, documentation, janitor-TODO, fork-gardening
- **Architecture:** [Agentic Body](docs/architecture/AGENTIC_BODY.md) · [Repo topology](docs/architecture/REPO_TOPOLOGY.md) · [Languages](docs/architecture/LANGUAGE_POLICY.md) · [Multi-agent](docs/architecture/MULTI_AGENT.md) · [Dependency graph](docs/architecture/DEPENDENCY_GRAPH.md) (generated)
- **Platform:** [Containers/uv](docs/CONTAINERS_AND_VENV.md) · [Linux layout](docs/LINUX_LAYOUT.md) · [ACP & A2A](docs/ACP_A2A.md)
- **Mind:** [Learning/memory](docs/LEARNING.md) · [Tooling catalog](docs/TOOLING_CATALOG.md) · [Style & performance](docs/STYLE_PERFORMANCE.md)
- **Process:** [Gap analysis](docs/GAP_ANALYSIS.md) · [Swarm](docs/SWARM.md) · [Query log](docs/queries/QUERYLOG.md)
- **Components:** [docs/components/](docs/components) — one page per component, generated cross-links
- **Desktop:** [shesh-desktop/docs/SHESH/](https://github.com/gaganjainse/shesh-desktop/tree/main/docs/SHESH) — the canonical SHESH desktop set (mirrored by the book; old in-repo mirror retired to docs/attic/desktop-mirror-2026-08-13)
