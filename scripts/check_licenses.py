#!/usr/bin/env python3
"""Verify every pinned component's license is GPL-3-body-compatible.

Used both as a CLI gate and imported by the test suite. Reads the manifest
(not the lockfile) so an incompatible component is caught before resolution.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from resolve_manifest import COMPATIBLE_LICENSES, SERVICE_ONLY_LICENSES, VALID_LAYERS  # noqa


def check_manifest(path: Path) -> list[str]:
    with path.open("rb") as f:
        data = tomllib.load(f)
    problems: list[str] = []
    for name, c in data.get("component", {}).items():
        lic = c.get("license", "")
        if lic in COMPATIBLE_LICENSES:
            continue
        if lic in SERVICE_ONLY_LICENSES and c.get("separate_service"):
            continue
        problems.append(
            f"{name}: license {lic!r} is not compatible with the GPL-3 body"
        )
        if c.get("layer") not in VALID_LAYERS:
            problems.append(f"{name}: invalid layer {c.get('layer')!r}")
    return problems


def main() -> int:
    manifest = Path(sys.argv[1] if len(sys.argv) > 1 else "manifests/components.toml")
    problems = check_manifest(manifest)
    if problems:
        for p in problems:
            print(f"FAIL: {p}", file=sys.stderr)
        return 1
    print(f"OK: all licenses in {manifest} are GPL-3-compatible")
    return 0


if __name__ == "__main__":
    sys.exit(main())
