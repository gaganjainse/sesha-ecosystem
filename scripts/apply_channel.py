#!/usr/bin/env python3
"""Apply a release channel with a btrfs snapshot for rollback.

Usage:
  python scripts/apply_channel.py --channel stable
  python scripts/apply_channel.py --channel canary --no-snapshot

On btrfs, a read-only snapshot of the install root is created before any
package/config change. If anything fails, the previous snapshot can be
booted from the grub/btrfs-grub menu. On non-btrfs systems, --no-snapshot
is required (the caller accepts the risk).

This is deliberately conservative: it resolves the lock, installs the
component versions pinned there, and records the applied channel.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = Path.home() / ".local" / "state" / "shesh"


def _run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def on_btrfs(path: Path) -> bool:
    """True if path lives on a btrfs filesystem."""
    if shutil.which("btrfs") is None:
        return False
    r = _run(["findmnt", "-no", "FSTYPE", str(path)], check=False)
    return r.returncode == 0 and r.stdout.strip() == "btrfs"


def btrfs_subvolume(path: Path) -> str | None:
    r = _run(["btrfs", "subvolume", "show", str(path)], check=False)
    if r.returncode != 0:
        return None
    # Output line: "Subvolume <id> level <n> path <subvol>"
    for line in r.stdout.splitlines():
        if line.strip().startswith("path "):
            return line.split("path", 1)[1].strip()
    return None


def snapshot(root: Path, channel: str) -> Path | None:
    """Create a timestamped read-only snapshot of root. Returns its path."""
    sub = btrfs_subvolume(root)
    if not sub:
        return None
    # Default snapshot location next to the subvolume.
    base = root.parent
    stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    snap_name = f"@shesh-{channel}-{stamp}"
    snap_path = base / snap_name
    _run(["sudo", "btrfs", "subvolume", "snapshot", "-r", str(root), str(snap_path)])
    return snap_path


def resolve_lock(channel: str) -> Path:
    lock = ROOT / "channels" / f"{channel}.lock"
    if not lock.exists():
        # Build it on demand.
        _run([sys.executable, str(ROOT / "scripts" / "resolve_manifest.py"),
              "--channel", channel, "--out", str(lock)])
    return lock


def apply(channel: str, take_snapshot: bool) -> int:
    lock = resolve_lock(channel)
    data = json.loads(lock.read_text())

    root = Path("/")
    if take_snapshot:
        if not on_btrfs(root):
            print("ERROR: not on btrfs; pass --no-snapshot to apply without one.",
                  file=sys.stderr)
            return 2
        snap = snapshot(root, channel)
        if snap is None:
            print("ERROR: could not create btrfs snapshot.", file=sys.stderr)
            return 2
        print(f"Snapshot created: {snap}")

    # Install components from the lock into the user environment.
    # Components are Python packages; pip install the pinned versions.
    for name, spec in sorted(data.get("components", {}).items()):
        repo = spec.get("repo", "")
        if not repo.startswith("gaganjainse/"):
            continue
        pkg = "git+https://github.com/" + repo
        version = spec.get("version")
        target = f"{pkg}@{version}" if version else pkg
        print(f"installing {name} {version or ''}".strip())
        r = _run([sys.executable, "-m", "pip", "install", "--user",
                  "--break-system-packages", "-q", target], check=False)
        if r.returncode != 0:
            print(f"WARN: failed to install {name}: {r.stderr.strip()[:300]}",
                  file=sys.stderr)

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    (STATE_DIR / "channel").write_text(channel + "\n")
    (STATE_DIR / "applied.json").write_text(json.dumps({
        "channel": channel,
        "applied_at": datetime.now(UTC).isoformat(),
        "components": list(data.get("components", {})),
    }, indent=2))
    print(f"Applied channel '{channel}'.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Apply a release channel safely")
    ap.add_argument("--channel", choices=["stable", "canary", "devel"],
                    default="stable")
    ap.add_argument("--no-snapshot", action="store_true",
                    help="skip btrfs snapshot (required on non-btrfs)")
    args = ap.parse_args(argv)
    return apply(args.channel, take_snapshot=not args.no_snapshot)


if __name__ == "__main__":
    raise SystemExit(main())
