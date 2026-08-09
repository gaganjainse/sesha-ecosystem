# Repository Topology — the federated "sinkhole"

> The model: **fork everything upstream, keep forks rolling-release, steal the best parts into
> component repos, integrate components into an ecosystem repo, promote it through canary → stable.**
> Exactly how a Linux distribution works: upstream projects → distro packages → [testing] → [core].
> This keeps you current with upstream *and* in control, with filters at every layer so breakage
> never reaches your daily driver.

---

## 1. The layers (bottom → top)

```
① UPSTREAM FORKS          (mirrors of external projects, track main/default)
        │  cherry-pick / rebase our patches
        ▼
② COMPONENT REPOS        (one per Sesha organ; our code + vendored fork pins)
        │  tagged releases, semver, individually tested
        ▼
③ ECOSYSTEM INTEGRATION  (sesha-ecosystem: manifests pin component versions)
        │  built together, full integration tests → "canary"
        ▼
④ CANARY REPO            (sesha-ecosystem:canary branch — daily build, bleeding edge)
        │  soak on a spare machine/VM for N days; gates pass
        ▼
⑤ STABLE / DOTFILES      (Auto-desktopenv:main — your actual machine, production)
```

### ① Upstream forks (`gaganjainse/fork-<project>`)
- A bare fork of each external project we use, with a tiny `sesha/` branch carrying our patches
  (MCP additions, branding, config, bug fixes).
- A bot opens a PR weekly when upstream advances; CI rebases our branch and runs the upstream tests.
- We never diverge more than necessary — every patch has a reason and an upstreaming attempt.
- These are the "raw material" intake. Nothing here runs on your machine directly.

### ② Component repos (`sesha-<organ>`)
- One repository per body organ, e.g.:
  - `sesha-brain` — packaging/patches around NexusAOS kernel for desktop.
  - `sesha-mind` — model routing + specialist prompts (from SeshaOS).
  - `sesha-voice` — Newelle fork/config + STT/TTS + wake word.
  - `sesha-files` — smart-organizer v2 (Rust watcher + Python classifier).
  - `sesha-shell` — Hyprland/MCP control (hyprland-control MCP).
  - `sesha-system` — power/GPU/MUX/backup/maintenance MCP.
  - `sesha-memory` — rag-service wrapper (sensory/long-term memory).
  - `sesha-phone` — ADB Android harness.
  - `sesha-audit` — the append-only event log/policy (NexusAOS bridge).
- Each has its own tests, its own semver tag, and a `manifest.toml` declaring dependencies.
- Components are independently usable (you can run `sesha-files` without the voice).

### ③ Ecosystem integration (this repo, `sesha-ecosystem`)
- The **workspace manifest** pins every component to a specific tag + the upstream fork SHA.
- Integration tests prove the organs work together (e.g., voice → brain policy → file move).
- Produces a lockfile (`sesha.lock`) like a distro repo snapshot.
- This is where we decide the *combination* — "the best of everything."

### ④ Canary (`canary` branch)
- Built daily from the latest component tags that pass their own tests.
- Runs full integration suite; if green, publishes a canary release.
- Intended for a VM / spare laptop / secondary user account — NOT your main work.

### ⑤ Stable → your machine (`Auto-desktopenv:main`)
- Only canary releases that soaked N days with no regressions are merged here.
- This is what runs on the MSI Sword daily. Boring is good.

---

## 2. Filters / quality gates at each layer

| Layer | Gate that blocks promotion |
|---|---|
| ① Fork | upstream tests pass; our `sesha/` branch rebases cleanly; license check |
| ② Component | unit tests, lint, `shellcheck`/`ruff`/`cargo test`, no known CVEs in deps, signature/attestation |
| ③ Ecosystem | integration tests on an Arch/CachyOS container; manifest resolves; MCP smoke tests |
| ④ Canary | soak period, hardware smoke test (display/GPU/audio), no failed systemd units |
| ⑤ Stable | manual sign-off + rollback snapshot (btrfs) before apply |

Every gate is a script in `scripts/gates/`, runnable locally and in CI. Nothing is promoted by hand
without a green gate.

---

## 3. Manifests (the single source of truth)

`manifests/components.toml` lists every organ with its repo, version, license, and source:

```toml
[component.sesha-voice]
repo    = "gaganjainse/sesha-voice"
version = "1.4.5-sesha1"
license = "GPL-3.0"
upstream = { name = "Newelle", repo = "qwersyk/Newelle", ref = "1.4.5" }
provides = ["mcp:voice", "wakeword", "stt", "tts"]
```

`scripts/resolve-manifest.py` resolves the full set, checks licenses are GPL-3-compatible, verifies
tag SHAs, and writes `sesha.lock`. This is the "package repo" metadata, in one auditable file.

---

## 4. Why this isn't a sinkhole of endless work

- **Upstream does most of the work.** We track, we don't rewrite. Forks + thin patches.
- **Components are independent.** You can pause any organ without stopping the body.
- **Gates are automated.** The weekly bot does the rebasing/testing; you only review failures.
- **Stable is protected.** Canary absorbs the breakage; your machine only gets tested combinations.
- **We start narrow.** Phase 1 builds 3 components (files, shell, system) that already exist in
  Auto-desktopenv; the rest are added as the gates and time allow.

---

## 5. Repository creation order

1. `sesha-ecosystem` (this repo — the orchestrator/manifests).
2. Forks of the first-wave upstreams (Newelle, end-4/dots-hyprland, plus the Rust/Python deps).
3. Component repos split out from the working Auto-desktopenv code:
   `sesha-files`, `sesha-shell`, `sesha-system`, `sesha-voice`.
4. `sesha-audit` (brain bridge) once MCP is stable.
5. Everything else (memory, phone, mind) after the integration harness proves itself.

The exact first-wave list and steal-map is in `SOURCES.md`.
