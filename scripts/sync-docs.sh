#!/usr/bin/env bash
# Sync all docs to the shesh-docs repo (mdbook) — properly organised.
# Called by tools/live_update.py --docs ALL and by GitHub Actions.
#
# Failure policy: REQUIRED sources abort the sync loudly (set -e); OPTIONAL
# sources print a SKIPPED line (missing source is a deploy-layout fact, not
# an error). No copy may fail invisibly — that is how stale docs happen.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_REPO="${DOCS_REPO:-/tmp/shesh-docs}"
ECOSYSTEM_DOCS="$ROOT/docs"
# Component checkouts live as siblings of the ecosystem checkout.
SRC_ROOT="${SRC_ROOT:-$(cd "$ROOT/.." && pwd)/src}"
DESKTOP_DOCS="$SRC_ROOT/shesh-desktop/docs"
WORKSPACE_DOCS="${WORKSPACE_DOCS:-$SRC_ROOT/shesh-workspace/docs}"

echo "Syncing docs to $DOCS_REPO ..."

# Clone docs repo if not exists
if [ ! -d "$DOCS_REPO" ]; then
    echo "Cloning shesh-docs to $DOCS_REPO"
    git clone --depth 1 https://github.com/gaganjainse/shesh-docs.git "$DOCS_REPO"
fi

# Ensure structure exists (from src/SUMMARY.md)
mkdir -p "$DOCS_REPO/src/product/architecture" "$DOCS_REPO/src/product/concepts" "$DOCS_REPO/src/product/tasks" "$DOCS_REPO/src/product/reference/components" "$DOCS_REPO/src/product/tutorials"
mkdir -p "$DOCS_REPO/src/factory/swarm" "$DOCS_REPO/src/factory/steal"
mkdir -p "$DOCS_REPO/src/gateway" "$DOCS_REPO/src/desktop" "$DOCS_REPO/src/adr" "$DOCS_REPO/src/audits" "$DOCS_REPO/src/verification" "$DOCS_REPO/src/skills" "$DOCS_REPO/src/policies" "$DOCS_REPO/src/queries" "$DOCS_REPO/src/portfolio"

# copy_req SRC... DST — required copy: a missing source aborts the sync.
copy_req() {
    local dst="${!#}"
    local srcs=("${@:1:$#-1}")
    local s
    for s in "${srcs[@]}"; do
        if [ ! -e "$s" ]; then
            echo "ERROR: required doc source missing: $s" >&2
            return 1
        fi
    done
    cp -r "${srcs[@]}" "$dst"
}

# copy_opt SRC DST — optional copy: absent source is announced, never silent.
copy_opt() {
    local src="$1" dst="$2"
    if [ -e "$src" ]; then
        cp -r "$src" "$dst"
    else
        echo "SKIPPED (absent): $src"
    fi
}

# Copy ecosystem docs (product + factory + gateway) — required.
# NB: docs/desktop/ is deliberately NOT copied flat into src/desktop/ — it
# mirrors the shesh-desktop repo's docs/SHESH tree, which is copied below.
# Copying both under different paths is how SESHA/SHESH name drift entered
# the book (fixed 2026-08-13); the mirror lands in the canonical SHESH/ name
# so the source repo always overwrites it if the two diverge.
echo "Copying ecosystem docs..."
for item in "$ECOSYSTEM_DOCS"/*; do
    [ "$(basename "$item")" = "desktop" ] && continue
    [ -e "$item" ] || {
        echo "ERROR: required doc source missing: $item" >&2
        exit 1
    }
    cp -r "$item" "$DOCS_REPO/src/"
done
mkdir -p "$DOCS_REPO/src/desktop/SHESH"
copy_req "$ECOSYSTEM_DOCS"/desktop/* "$DOCS_REPO/src/desktop/SHESH/"
copy_req "$ROOT/README.md" "$DOCS_REPO/src/product/overview.md"
copy_req "$ROOT/docs/GETTING_STARTED.md" "$DOCS_REPO/src/product/getting-started.md"
copy_req "$ROOT/manifests/components.toml" "$DOCS_REPO/src/product/reference/manifest.md"
copy_req "$ROOT/manifests/models.toml" "$DOCS_REPO/src/product/reference/models.md"

# Copy desktop docs — optional (sibling checkout layout).
echo "Copying desktop docs..."
if [ -d "$DESKTOP_DOCS" ]; then
    copy_req "$DESKTOP_DOCS"/* "$DOCS_REPO/src/desktop/"
else
    echo "SKIPPED (absent): $DESKTOP_DOCS"
fi

# Name-drift guard (canonical name is SHESH, per 2026-08-13 decision): the
# pre-rename mirror shipped 06_SESHA_AGENT.md / SHESHA_README.md and flat
# uppercase dupes; if an old checkout ever resurrects them, the sync removes
# them instead of republishing drift. Removing fixed names is explicit, not
# magic cleanup.
for stale in \
    "$DOCS_REPO/src/desktop/06_SESHA_AGENT.md" \
    "$DOCS_REPO/src/desktop/SHESHA_README.md" \
    "$DOCS_REPO/src/desktop/00_INDEX.md" \
    "$DOCS_REPO/src/desktop/01_AUDIT.md" \
    "$DOCS_REPO/src/desktop/02_ROADMAP.md" \
    "$DOCS_REPO/src/desktop/03_DISK_STRUCTURE.md" \
    "$DOCS_REPO/src/desktop/04_DEVICE_PROFILE.md" \
    "$DOCS_REPO/src/desktop/05_SMART_ORGANIZER_V2.md" \
    "$DOCS_REPO/src/desktop/07_AUTOMATIONS.md" \
    "$DOCS_REPO/src/desktop/08_ECOSYSTEM_TOOLS.md" \
    "$DOCS_REPO/src/desktop/09_AI_PROMPTS.md" \
    "$DOCS_REPO/src/desktop/10_LICENSES_AND_SOURCES.md" \
    "$DOCS_REPO/src/desktop/AMBIENT_DESIGN.md"; do
    rm -f "$stale"
done

# Copy workspace docs — optional.
if [ -d "$WORKSPACE_DOCS" ]; then
    copy_req "$WORKSPACE_DOCS"/* "$DOCS_REPO/src/factory/"
else
    echo "SKIPPED (absent): $WORKSPACE_DOCS"
fi

# Ensure SUMMARY.md exists (already in docs repo)
if [ ! -f "$DOCS_REPO/src/SUMMARY.md" ]; then
    echo "SUMMARY.md missing in docs repo, creating minimal"
    cat >"$DOCS_REPO/src/SUMMARY.md" <<'SUMMARY'
# Summary
- [Introduction](./introduction.md)
- [Product Overview](./product/overview.md)
SUMMARY
fi

echo "Docs sync complete — $(find "$DOCS_REPO/src" -type f | wc -l) files in $DOCS_REPO/src"
echo "Build with: cd $DOCS_REPO && mdbook build && mdbook serve"
