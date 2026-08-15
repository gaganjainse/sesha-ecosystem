# Shesh Ecosystem — developer quality gates
# Run `make` from the repo root. Nothing here touches the host system.

PY ?= python3
RUFF ?= $(PY) -m ruff
PYTEST ?= $(PY) -m pytest

.PHONY: help lint test silent-failures resolve check all clean linkcheck verify-all

help:
	@echo "Shesh Ecosystem gates:"
	@echo "  make lint      ruff on scripts/ and tests/"
	@echo "  make test      pytest (offline, no hardware)"
	@echo "  make resolve   build shesh.lock from the manifest"
	@echo "  make check     license + manifest + tests (CI gate)"
	@echo "  make depgraph  regenerate + check docs/architecture/DEPENDENCY_GRAPH.md"
	@echo "  make silent-failures  audit cwd for silent-failure patterns (SF1-SF6)"
	@echo "  make upstream  query upstream repos for new releases (network)"
	@echo "  make linkcheck broken relative links under docs/"
	@echo "  make verify-all  orchestrator sweep: remotes+fetch, worktree-vs-origin"
	@echo "                   content verify, per-component strict gates, SF self-audit"
	@echo "  make clean     remove caches and generated locks"

lint:
	$(RUFF) check scripts/ tests/ tools/

test:
	$(PYTEST) tests/ -q

silent-failures:
	$(PY) tools/silent_failures.py .

resolve:
	$(PY) scripts/resolve_manifest.py --channel canary

depgraph:
	$(PY) tools/depgraph.py > docs/architecture/DEPENDENCY_GRAPH.md
	$(PY) tools/depgraph.py --check docs/architecture/DEPENDENCY_GRAPH.md

check: lint test sync-check
	$(PY) scripts/check_licenses.py manifests/components.toml
	$(PY) scripts/resolve_manifest.py --channel stable  --out channels/stable.lock
	$(PY) scripts/resolve_manifest.py --channel canary  --out channels/canary.lock
	$(PY) scripts/resolve_manifest.py --channel devel   --out channels/devel.lock
	@echo "GATE OK"

upstream:
	$(PY) scripts/upstream_tracker.py

linkcheck:
	$(PY) tools/linkcheck.py docs
	$(PY) tools/docs_index.py --check

# Orchestrator-scale verification (network + a provisioned venv required):
#   1. every sibling clone gets its origin remote back and is fetched
#   2. every worktree is byte-compared against origin/<default> (catches
#      snapshot-restore damage that git status cannot see)
#   3. every component runs pytest -W error + ruff (no suppression policy)
#   4. the SF1-SF6 audit runs on this repo itself
	$(PY) tools/verify_worktrees.py
	SHESH_VENV_PY=$${SHESH_VENV_PY:-/tmp/fm3/bin/python} bash tools/verify_all_strict.sh
	$(PY) tools/silent_failures.py .

clean:
	rm -rf .pytest_cache __pycache__ scripts/__pycache__ tests/__pycache__
	rm -f shesh.lock channels/*.lock channels/upstream-status.json

handoff:  ## regenerate STATE.md from the working trees
	python3 tools/handoff.py

sync:  ## push shared boilerplate to every repository
	python3 tools/sync_fleet.py

sync-check:  ## fail if any repository drifted from the canonical boilerplate
	python3 tools/sync_fleet.py --check
	python3 tools/handoff.py --check
