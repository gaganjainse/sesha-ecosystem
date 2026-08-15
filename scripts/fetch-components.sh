#!/usr/bin/env bash
# scripts/fetch-components.sh
# Clone every component repo declared in the manifest, shallow, into the
# sibling `components/` directory (the layout e2e-canary.sh expects:
# $HERE/../components/shesh-*). Used by the canary gate; also useful for a
# local container with the repo mounted at /src.
#
# Federation consolidation (2026-08-13): many components now share the
# shesh-core repo. Each repo is cloned ONCE; component dirs that share a repo
# are symlinked to the single clone (so `components/shesh-shell` -> shesh-core).
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

pairs = []  # (component_name, repo)
for name, comp in data.get("component", {}).items():
    repo = comp.get("repo", "")
    if not repo or not name.startswith("shesh-"):
        continue  # only our components; upstreams are not part of the e2e
    pairs.append((name, repo))
pairs.sort()

# clone each unique repo once
repo_dir = {}  # repo -> dir it was cloned to
for name, repo in pairs:
    if repo in repo_dir:
        # symlink the shared-repo component dir to the single clone
        link = dest / name
        if link.exists() or link.is_symlink():
            continue
        target = repo_dir[repo].name  # relative symlink
        link.symlink_to(target, target_is_directory=True)
        print(f"  link {name} -> {target}")
        continue
    target = dest / name
    if target.exists():
        print(f"  exists {name}")
        repo_dir[repo] = target
        continue
    print(f"  clone {repo}")
    subprocess.run(
        ["git", "clone", "--quiet", "--depth", "1",
         f"https://github.com/{repo}.git", str(target)],
        check=True,
    )
    repo_dir[repo] = target
print(f"fetched {len(pairs)} components -> {dest} ({len(repo_dir)} unique repos)")
PY
