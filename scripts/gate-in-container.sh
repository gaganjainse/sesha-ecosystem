#!/usr/bin/env bash
# scripts/gate-in-container.sh
# Runs the offline quality gates inside an Arch (or other distro) container.
# Used by the canary gate. Assumes the repo is mounted at /src (ro).
set -euo pipefail

cd /src

if [ -r /etc/os-release ]; then
  # shellcheck source=/dev/null
  . /etc/os-release
  echo "==> distro: ${PRETTY_NAME}"
else
  echo "==> distro: $(uname -a)"
fi

# Install only what we need (best-effort across pacman/dnf/apt), then VERIFY.
if command -v pacman >/dev/null; then
  pacman -Sy --noconfirm --needed python python-pip ruff >/dev/null
elif command -v dnf >/dev/null; then
  dnf install -y python3 python3-pip >/dev/null
elif command -v apt-get >/dev/null; then
  apt-get update -y >/dev/null && apt-get install -y python3 python3-pip >/dev/null
fi

if ! python3 -m ruff --version >/dev/null 2>&1; then
  python3 -m pip install --quiet --break-system-packages --user ruff pytest
fi
python3 -m ruff --version   # hard-fail here with a clear message, not at the gate

echo "==> lint"
python3 -m ruff check scripts/ tests/

echo "==> tests"
python3 -m pytest tests/ -q

echo "==> license gate"
python3 scripts/check_licenses.py manifests/components.toml

echo "==> resolve all channels"
for ch in stable canary devel; do
  python3 scripts/resolve_manifest.py --channel "$ch" --out "/tmp/${ch}.lock"
done

echo "==> GATE PASSED (${ID:-unknown-distro})"
