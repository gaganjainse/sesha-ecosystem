# 🔍 shesh-ebpf

eBPF telemetry with Aya (Rust) for system/performance sensing — read-only.

- Part of [Shesh ecosystem](https://github.com/gaganjainse/shesh-ecosystem)
- Layer: Soma (body) — future: eBPF/Aya for system/performance sensing
- Provides: ebpf-telemetry, system-metrics, performance-sensing
- Upstream: Aya Rust eBPF library (https://github.com/aya-rs/aya) — read-only, no kprobes that modify

## Tools
- `get_system_metrics` — CPU, memory, load, disk, network via /proc (Aya placeholder)
- `get_network_stats` — TCP retransmits, packet loss via /proc/net
- `get_process_io` — per-process I/O via /proc/[pid]/io

Future Rust: Aya programs for execve, openat, TCP events — read-only, behind policy Guard.

All behind Guard — protected paths denied, read-only.

## Dev
```bash
uv sync && uv run pytest
```

## Rust (future)
```bash
cd ebpf-rs
cargo build --release
# Aya program: ebpf/src/main.rs — trace execve with BPF_MAP_TYPE_PERF_EVENT_ARRAY
```
