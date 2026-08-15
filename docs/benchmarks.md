# Benchmarks — account-wide status (2026-08-13)

Benchmarks exist where there is a **measurable hot path**. No fake/stub
benches anywhere — repos without benches are documented below with the
reason. Every bench runs in CI (`bench.yml`, SHA-pinned, read-only
permissions; Python benches are stdlib-only median-of-N, Rust uses
criterion with `-- --test` smoke mode so CI never fails on timing noise).

## Repos WITH real benchmarks

| Repo | What is benchmarked | Measured (2026-08-13) | CI |
|---|---|---|---|
| **SheshAOS** | (pre-existing) criterion benches in `crates/*/benches/` | green | bench.yml |
| **shesha-kernel** | (pre-existing) criterion benches (event store, kernel) | green | bench.yml |
| **Vyakrti** | lexer + lex&parse throughput (per-keystroke IDE hot path), `benches/compiler_pipeline.rs` | added `68ff2c8a9d119df25c983885c4902908d118cea5` | bench.yml |
| **shesh-memory** | vector search (1000 docs), context assembly (100 eps+20 facts), embedding | search ~73 ms, assembly ~186 µs, embed ~29 µs | bench.yml |
| **shesh-audit** | guard check allow/deny, hash-chained audit append | ~51 µs / ~47 µs / ~34 µs | bench.yml |
| **shesh-phone** | vision→tap cycle, template match (400×800) | **template match 1.65 s → 95.7 ms after coarse-to-fine optimization (`77ec779f53a0dcdc766a5823015200611617212b`)** — 17× | bench.yml |
| **FWRS** | LP allocation pipeline scaling (10/20 → 40/100 instances) | 75 ms → 860 ms | bench.yml |
| **rag-service** | chunk_text, hybrid search, embedding over corpus | ~14 µs / ~2.3 ms / ~38 µs | bench.yml |

## Repos WITHOUT benchmarks — honest reasons

| Repo | Reason |
|---|---|
| **shesh-ecosystem / shesh-workspace** | build-time tooling (manifest resolve, book build). No interactive hot path; CI gates already cover correctness. A resolve-time bench is marginal — revisit if manifest grows past ~50 components |
| **shesh-docs** | static mdBook projection — nothing runtime to measure |
| **shesh-desktop** | dotfiles/config — the "hot path" is shell startup, which is machine-specific and covered by manual verification |
| **Hyprland-Dots / hyprdots / gaganjainse / ePustakalay** | config/profile repos — no code hot path |
| **ClinicLedger / ClinicLedger-Template / VillageClinicLedger** | mobile apps; the voice parser is µs-scale and covered by unit tests. JMH/Gradle benchmark infra is disproportionate for this |
| **GameVault** | no measurable server hot path |
| **AIM** | Flask app; endpoint latency is dominated by MySQL, not app code |
| **llm-eval-harness** | runs evals on demand (minutes-scale); scorer µs-scale, covered by tests |
| **shesh-voice / shesh-* components not listed** | MCP servers; per-call work is I/O-bound (IPC), not compute-bound |
| **Forks (pipecat, waveterm, ollama, OmniRoute, prime-agent, leon, khoj, browser-use, openWakeWord, servers, register, Hermes, Memento-Skills, phone-harness)** | upstream owns bench infra; our forks track upstream. Duplicating benches in forks would be dead weight |
| **Archived repos** | frozen — no active development, benches pointless |

## Bench workflow policy

- Runs **weekly** (Mon 03:00 UTC) + on `workflow_dispatch` + on PRs touching
  source/benchmark paths.
- Python: `python benchmarks/bench_*.py` — prints medians, exits 0 (report
  mode; human reads the trend; gross regressions are caught by tests).
- Rust: `cargo bench -- --test` — compiles + smoke-runs benches, no flaky
  timing gates in CI.
- Full timing runs happen locally / on the MSI machine.
