# Shesh Ecosystem — developer quality gates
# Run `make` from the repo root. Nothing here touches the host system.

PY ?= python3
RUFF ?= $(PY) -m ruff
PYTEST ?= $(PY) -m pytest

.PHONY: help lint test silent-failures resolve check all clean linkcheck verify-all depgraph upstream journal-check steer-check sync-check fleet-health assimilate sync handoff

help:
	@echo "Shesh Ecosystem gates:"
	@echo "  make lint      ruff on scripts/ and tests/"
	@echo "  make test      pytest (offline, no hardware)"
	@echo "  make resolve   build shesh.lock from the manifest"
	@echo "  make check     license + manifest + tests"
	@echo "  make depgraph  regenerate + check docs/architecture/dependency-graph.md"
	@echo "  make silent-failures  audit cwd for silent-failure patterns (SF1-SF6)"
	@echo "  make upstream  query upstream repos for new releases (network)"
	@echo "  make linkcheck broken relative links under docs/"
	@echo "  make verify-all  orchestrator sweep: remotes+fetch, worktree-vs-origin"
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
	$(PY) tools/depgraph.py > docs/architecture/dependency-graph.md
	$(PY) tools/depgraph.py --check docs/architecture/dependency-graph.md

check: lint test sync-check journal-check steer-check
	$(PY) scripts/check_licenses.py manifests/components.toml
	$(PY) scripts/resolve_manifest.py --channel stable --out channels/stable.lock
	$(PY) scripts/resolve_manifest.py --channel canary --out channels/canary.lock
	$(PY) scripts/resolve_manifest.py --channel devel --out channels/devel.lock
	@echo "GATE OK"

upstream:
	$(PY) scripts/upstream_tracker.py

linkcheck:
	$(PY) tools/linkcheck.py docs
	$(PY) tools/docs_index.py --check

verify-all:
	$(PY) tools/verify_worktrees.py
	SHESH_VENV_PY=$${SHESH_VENV_PY:-/tmp/fm3/bin/python} bash tools/verify_all_strict.sh
	$(PY) tools/silent_failures.py .

clean:
	rm -rf .pytest_cache __pycache__ scripts/__pycache__ tests/__pycache__
	rm -f shesh.lock channels/*.lock channels/upstream-status.json

handoff:
	python3 tools/handoff.py

sync:
	python3 tools/sync_fleet.py

journal-check:
	python3 ../shesh-workspace/tools/journal.py check

fleet-health:
	python3 tools/fleet_health.py --check

assimilate:
	python3 tools/assimilate.py --report

steer-check:
	python3 ../shesh-workspace/tools/steer.py check

sync-check:
	python3 tools/sync_fleet.py --check
	python3 tools/handoff.py --check
