# Language & FFI Policy

> Decision: **use five core languages, each for one job.** Resist adding a sixth unless it passes the
> bar in §4. The fastest way to sink this ecosystem is a tower of FFI bindings no one can debug.
> Cross-language communication happens over **process boundaries with typed JSON/MCP**, not in-process
> FFI. This is the single most important rule for overhead, security, and debugging.

---

## 1. The five core languages

| Language | Owns (and only these) | Why it wins there |
|---|---|---|
| **Rust** | Brain/kernel, event store, policy engine, file watcher, low-level daemons, eBPF (Aya), security-critical tools | Memory safety without GC, single static binary, `cargo`/`clippy`, your existing SheshAOS/shesh-kernel code |
| **Python 3.11+** | Mind/AI glue: MCP servers, LLM routing, classifiers, RAG, eval, orchestration scripts, tests | The AI ecosystem (Ollama, mcp, chromadb, faster-whisper) lives here; `uv` + `ruff` + `pytest` make it production-grade |
| **Lua** | Hyprland configuration only (Hyprland ≥0.55 is Lua-native) | It's the host's config language — no runtime added, no FFI |
| **QML + modern JavaScript/TypeScript** | Quickshell UI (bar, overlay, widgets) | It's the shell's language (Qt6/QML); use JS inside QML, **no separate Node runtime** |
| **POSIX Bash 5+** | Installer (`sdata/`), bootstrapping, glue, distrobox/podman helpers | It's the universal automation surface on CachyOS; kept small, `shellcheck`-clean |

That's the whole list for the daily-driver system.

---

## 2. Explicitly NOT chosen (and why)

| Language | Verdict | Reason |
|---|---|---|
| **Zig** | ❌ Don't add | Excellent language, but it would duplicate Rust in the "systems" slot and add a second toolchain + FFI (you already replaced a Zig VT100 FFI with Rust `vte` in shesh-kernel ADR-002). Only use if *forced* by a dependency (none currently). |
| **C** | ❌ Don't write new C | Use only when binding to a kernel/library that requires it; prefer Rust `bindgen` wrapping. C is the largest source of memory bugs and we already have Rust. |
| **C++/Qt C++** | ⚠️ Last resort | Quickshell is QML; never write Qt C++ unless a QML extension is provably impossible (it isn't, for our UI). |
| **Mojo** | ❌ Not production-ready | Modular/ML promise, but immature, no distro packaging, adds FFI to CPython with no stable ABI. Re-evaluate late 2027. |
| **Go** | ❌ Don't add | Would overlap Rust; its runtime/GC and FFI story buys us nothing here. |
| **Emacs Lisp** | ❌ Not part of system | We use Hyprland/Quickshell/fish, not Emacs. Personal elisp dotfiles are fine but out of scope. |
| **Java/Kotlin/JVM** | ❌ No JVM on the desktop path | Heavy startup/memory for a 16 GB laptop that also runs local LLMs. |
| **Node.js as a service** | ❌ No separate JS daemon | JS only exists *inside* QML. Newelle/Goose-style Node agents run as isolated containers if ever needed, never as host daemons. |
| **Ruby/Perl/PHP** | ❌ | No role. |

---

## 3. Why this minimizes FFI overhead and risk

1. **Process boundaries, not linkage.** Every component is a separate process speaking **MCP (stdio) or
   JSON-RPC (Unix socket)** — exactly how SheshAOS (`sheshaos-rpc`) and Newelle already work. There is
   no `ctypes`/`cdylib`/CGo/JNI in our architecture. Each language stays inside its own memory space;
   a crash in one organ doesn't take down the brain.
2. **Serialization stays simple:** JSON for MCP/control (low volume), SQLite for local state. Use
   MessagePack/CBOR *only* if profiling a hot path proves it necessary (don't pre-optimize).
3. **One runtime per slot:** Rust binaries are static; Python runs from a single `uv` venv per
   component; no competing runtimes on the host.
4. **Type boundaries are checked:** MCP tool schemas (JSON Schema) are the contract; tests assert them
   on both sides. This catches integration errors where FFI type mismatches would segfault.
5. **Containers for the exotic.** If we ever want a tool written in, say, Go or Mojo, it runs in a
   **rootless Podman/Distrobox** container and exposes MCP over a socket. It never links into the
   host. This is the escape hatch that protects the core from language sprawl.

---

## 4. Bar to add a new language

A new language enters the ecosystem only if **all** are true:
1. It solves a problem no core language can (cited, not vibes).
2. It ships in CachyOS/Arch repos (or builds reproducibly in a container).
3. It has a stable FFI-free story — i.e., it can speak MCP/JSON over stdio/socket.
4. Lint, format, test, and debug tooling exist and are wired into CI.
5. A maintainer (you) accepts ongoing ownership.
Otherwise: wrap it in a container, or don't use it.

---

## 5. Toolchain & quality standards (per language)

| Lang | Build/pm | Lint | Format | Test | Debug |
|---|---|---|---|---|---|
| Rust | cargo | `cargo clippy -D warnings` | `cargo fmt` | `cama test` | rust-gdb, tokio-console |
| Python | **uv** (`pyproject.toml` + committed `uv.lock`, `uv sync --frozen`) | `ruff` | `ruff format` | `pytest` (+pytest-asyncio) | `pdb`/`debugpy` |
| Lua | (host) | `luacheck` | `stylua` | `busted` where logic exists | print/log |
| QML/JS | qmllive | `qmllint` | `qmlformat` (repo ships `.qmlformat.ini`) | QML test harness | qmllint, GammaRay |
| Bash | distro | **shellcheck -S warning** | `shfmt -i 2 -ci` | `bats` | `bash -x` |

Every repo has `make lint && make test`; CI runs the matrix; nothing promotes without green.

---

## 6. Environments (no host pollution)

- **Python:** per-component venvs under `~/.local/state/<component>/.venv`, managed by `uv`. Never
  `sudo pip`. Commit `uv.lock`; `uv sync --frozen` in CI and containers.
- **Rust:** installed via `rustup`, builds into `~/.cargo/bin`; distro packages for runtime only.
- **Containers:** **Podman (rootless)** is the standard. Distrobox wraps it for long-lived dev
  environments sharing `$HOME`/Wayland/PipeWire. Use this for:
  - running agents/services in non-core languages,
  - testing the installer on other distros (Fedora/Ubuntu) without a VM,
  - isolating untrusted MCP servers or cloud-tier tools.
  Docker is allowed only if a workflow demands it; rootless Podman is preferred for security.
- **Node:** never a host service; only tooling invoked inside QML or a container.

---

## 7. eBPF / kernel-adjacent work

For the research track (AI-assisted tuning/telemetry), write **eBPF in Rust with
[Aya](https://aya-rs.dev)** (no libbpf-c dependency, no C BPF code to maintain). The userspace
collector is also Rust. If a probe is impossible in Aya, write the *minimum* C BPF and wrap it from
Rust — and document why. This keeps the "no new C" rule even at the kernel edge.

---

## 8. Summary one-liner

> **Rust for the body's reflexes, Python for its mind, Lua/QML/Bash for the world it lives in;
> everything else runs in a rootless container and talks MCP.**
