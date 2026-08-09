#!/usr/bin/env bash
# scripts/gate-in-container.sh
# Runs the offline quality gates inside an Arch (or other distro) container.
# Used by the canary gate. Assumes the repo is mounted at /src (ro).
set -euo pipefail

cd /src

echo "==> distro: $(. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME" || uname -a)"

# Install only what we need (best-effort across pacman/dnf/apt).
if command -v pacman >/dev/null; then
  pacman -Sy --noconfirm --needed python python-pip ruff >/dev/null 2>&1 || true
elif command -v dnf >/dev/null; then
  dnf install -y python3 python3-pip >/dev/null 2>&1 || true
elif command -v apt-get >/dev/null; then
  apt-get update -y >/dev/null 2>&1 && apt-get install -y python3 python3-pip >/dev/null 2>&1 || true
fi

python3 -m pip install --quiet --break-system-packages --user ruff pytest 2>/dev/null || true

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

echo "==> GATE PASSED ($(. /etc/os-release 2>/dev/null && echo "$ID"))"
