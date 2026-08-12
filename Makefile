# Shesh Ecosystem — developer quality gates
# Run `make` from the repo root. Nothing here touches the host system.

PY ?= python3
RUFF ?= $(PY) -m ruff
PYTEST ?= $(PY) -m pytest

.PHONY: help lint test resolve check all clean

help:
	@echo "Shesh Ecosystem gates:"
	@echo "  make lint      ruff on scripts/ and tests/"
	@echo "  make test      pytest (offline, no hardware)"
	@echo "  make resolve   build shesh.lock from the manifest"
	@echo "  make check     license + manifest + tests (CI gate)"
	@echo "  make depgraph  regenerate + check docs/architecture/DEPENDENCY_GRAPH.md"
	@echo "  make upstream  query upstream repos for new releases (network)"
	@echo "  make clean     remove caches and generated locks"

lint:
	$(RUFF) check scripts/ tests/

test:
	$(PYTEST) tests/ -q

resolve:
	$(PY) scripts/resolve_manifest.py --channel canary

depgraph:
	$(PY) tools/depgraph.py > docs/architecture/DEPENDENCY_GRAPH.md
	$(PY) tools/depgraph.py --check docs/architecture/DEPENDENCY_GRAPH.md

check: lint test
	$(PY) scripts/check_licenses.py manifests/components.toml
	$(PY) scripts/resolve_manifest.py --channel stable  --out channels/stable.lock
	$(PY) scripts/resolve_manifest.py --channel canary  --out channels/canary.lock
	$(PY) scripts/resolve_manifest.py --channel devel   --out channels/devel.lock
	@echo "GATE OK"

upstream:
	$(PY) scripts/upstream_tracker.py

clean:
	rm -rf .pytest_cache __pycache__ scripts/__pycache__ tests/__pycache__
	rm -f shesh.lock channels/*.lock channels/upstream-status.json
