#!/usr/bin/env python3
"""Resolve the Sesha component manifest into a lockfile.

Validates schema, enforces GPL-3 body license compatibility, and writes
``sesha.lock`` (deterministic, sorted). This is the first quality gate: a
component with an incompatible license or a missing field fails the build.

Run:  python scripts/resolve-manifest.py [--manifest manifests/components.toml]
                                       [--out sesha.lock] [--channel stable]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

# Licenses that may be vendored/linked into a GPL-3 body.
# AGPL and SSPL/Elastic are NOT compatible for linking (allowed only as separate services,
# which must be declared in a component's `separate_service = true`).
COMPATIBLE_LICENSES = {
    "MIT", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "Apache-2",
    "ISC", "Zlib", "GPL-3.0", "GPL-3", "LGPL-3.0", "LGPL-2.1", "MPL-2.0",
}
SERVICE_ONLY_LICENSES = {"AGPL-3.0", "AGPL-3", "SSPL-1.0", "Elastic-2.0"}
VALID_LAYERS = {"brain", "mind", "soma"}
VALID_CHANNELS = {"stable", "canary", "devel"}
REQUIRED_FIELDS = {"layer", "repo", "version", "license", "channel", "provides"}


def load_manifest(path: Path) -> dict:
    with path.open("rb") as f:
        data = tomllib.load(f)
    if "ecosystem" not in data or "component" not in data:
        raise ValueError("manifest must contain [ecosystem] and [component.*] tables")
    return data


def validate(components: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    seen_provides: dict[str, str] = {}
    for name, c in components.items():
        missing = REQUIRED_FIELDS - c.keys()
        if missing:
            errors.append(f"{name}: missing fields {sorted(missing)}")
            continue
        if c["layer"] not in VALID_LAYERS:
            errors.append(f"{name}: invalid layer {c['layer']!r}")
        if c["channel"] not in VALID_CHANNELS:
            errors.append(f"{name}: invalid channel {c['channel']!r}")
        lic = c["license"]
        if lic not in COMPATIBLE_LICENSES:
            if lic in SERVICE_ONLY_LICENSES and c.get("separate_service"):
                pass
            else:
                errors.append(
                    f"{name}: license {lic!r} is not GPL-3-compatible "
                    f"(set separate_service=true for {sorted(SERVICE_ONLY_LICENSES)})"
                )
        if not isinstance(c.get("provides"), list) or not c["provides"]:
            errors.append(f"{name}: provides must be a non-empty list")
        for cap in c.get("provides", []):
            if cap in seen_provides:
                other = seen_provides[cap]
                errors.append(
                    f"{name}: capability {cap!r} already provided by {other}"
                )
            else:
                seen_provides[cap] = name
        if "version" in c and not isinstance(c["version"], str):
            errors.append(f"{name}: version must be a string")
    return errors


def resolve(components: dict, channel: str) -> dict:
    # Channel filter: stable includes only stable; canary includes stable+canary;
    # devel includes everything.
    rank = {"stable": 0, "canary": 1, "devel": 2}
    cutoff = rank[channel]
    selected = {}
    for name, c in sorted(components.items()):
        if rank[c["channel"]] <= cutoff:
            selected[name] = {
                "layer": c["layer"],
                "repo": c["repo"],
                "version": c["version"],
                "license": c["license"],
                "channel": c["channel"],
                "provides": sorted(c["provides"]),
                "upstream": c.get("upstream"),
                "models": c.get("models", []),
            }
    body = {
        "components": selected,
        "count": len(selected),
    }
    payload = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    body["sha256"] = hashlib.sha256(payload).hexdigest()
    return body


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", default="manifests/components.toml", type=Path)
    ap.add_argument("--out", default="sesha.lock", type=Path)
    ap.add_argument("--channel", default="canary", choices=sorted(VALID_CHANNELS))
    args = ap.parse_args()

    data = load_manifest(args.manifest)
    components = data.get("component", {})
    errors = validate(components)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    lock = resolve(components, args.channel)
    args.out.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n")
    print(f"Resolved {lock['count']} components for channel "
          f"{args.channel!r} -> {args.out} (sha256 {lock['sha256'][:12]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
