#!/usr/bin/env bash
# Sync all docs to shesh-docs repo for reading only — properly organised, no navigation issues
# Called by tools/live_update.py --docs ALL and by GitHub Actions

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_REPO="${DOCS_REPO:-/tmp/shesh-docs}"
ECOSYSTEM_DOCS="$ROOT/docs"
DESKTOP_DOCS="$ROOT/src/shesh-desktop/docs"
WORKSPACE_DOCS="$ROOT/../shesh-workspace/docs" # if exists

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

# Copy ecosystem docs (product + factory + gateway)
echo "Copying ecosystem docs..."
cp -r "$ECOSYSTEM_DOCS"/* "$DOCS_REPO/src/" 2>/dev/null || true
cp "$ROOT/README.md" "$DOCS_REPO/src/product/overview.md" 2>/dev/null || true
cp "$ROOT/docs/GETTING_STARTED.md" "$DOCS_REPO/src/product/getting-started.md" 2>/dev/null || true
cp "$ROOT/manifests/components.toml" "$DOCS_REPO/src/product/reference/manifest.md" 2>/dev/null || true
cp "$ROOT/manifests/models.toml" "$DOCS_REPO/src/product/reference/models.md" 2>/dev/null || true

# Copy desktop docs
if [ -d "$ROOT/src/shesh-desktop/docs" ]; then
  echo "Copying desktop docs..."
  cp -r "$ROOT/src/shesh-desktop/docs"/* "$DOCS_REPO/src/desktop/" 2>/dev/null || true
fi

# Copy workspace docs if exists
if [ -d "$ROOT/../shesh-workspace/docs" ]; then
  cp -r "$ROOT/../shesh-workspace/docs"/* "$DOCS_REPO/src/factory/" 2>/dev/null || true
fi

# Ensure SUMMARY.md exists (already in docs repo)
if [ ! -f "$DOCS_REPO/src/SUMMARY.md" ]; then
  echo "SUMMARY.md missing in docs repo, creating minimal"
  cat > "$DOCS_REPO/src/SUMMARY.md" <<'SUMMARY'
# Summary
- [Introduction](./introduction.md)
- [Product Overview](./product/overview.md)
SUMMARY
fi

echo "Docs sync complete — $(find "$DOCS_REPO/src" -type f | wc -l) files in $DOCS_REPO/src"
echo "Build with: cd $DOCS_REPO && mdbook build && mdbook serve"
