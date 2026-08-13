#!/usr/bin/env bash
# scripts/fetch-components.sh
# Clone every component repo declared in the manifest, shallow, into the
# sibling `components/` directory (the layout e2e-canary.sh expects:
# $HERE/../components/shesh-*). Used by the canary gate; also useful for a
# local container with the repo mounted at /src.
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:-$HERE/../components}"
MANIFEST="${2:-$HERE/manifests/components.toml}"
mkdir -p "$DEST"

python3 - "$DEST" "$MANIFEST" <<'PY'
import pathlib, subprocess, sys, tomllib

dest = pathlib.Path(sys.argv[1]).resolve()
manifest = pathlib.Path(sys.argv[2]).resolve()
data = tomllib.loads(manifest.read_text())

repos = []
components = data.get("component", {})
for name, comp in components.items():
    repo = comp.get("repo", "")
    if not repo:
        continue
    if not name.startswith("shesh-"):
        continue  # only our components; upstreams are not part of the e2e
    repos.append((name, repo))

repos.sort()
for name, repo in repos:
    target = dest / name
    if target.exists():
        print(f"  exists {name}")
        continue
    print(f"  clone {repo}")
    subprocess.run(
        ["git", "clone", "--quiet", "--depth", "1",
         f"https://github.com/{repo}.git", str(target)],
        check=True,
    )
print(f"fetched {len(repos)} components -> {dest}")
PY
