# Shesh Ecosystem — reproducible dev/canary container (Arch-based, matches CachyOS)
# Build: podman build -f Containerfile -t shesh-ecosystem:canary .
# Run:   podman run --rm -it shesh-ecosystem:canary bash
# Distrobox: distrobox create -i shesh-ecosystem:canary -n shesh

FROM archlinux:latest

LABEL org.opencontainers.image.title="shesh-ecosystem"
LABEL org.opencontainers.image.description="Federated AI body: brain/mind/soma MCP components — offline gates"
LABEL org.opencontainers.image.source="https://github.com/gaganjainse/shesh-ecosystem"

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm \
      python python-pip python-pipx base-devel git curl jq \
      podman buildah distrobox fuse-overlayfs slirp4netns \
      nodejs npm \
      restic \
      android-tools \
      ruff \
    && pacman -Sc --noconfirm

ENV PIP_BREAK_SYSTEM_PACKAGES=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/root/.local/bin:${PATH}"

# uv (for the mcp-bundle / fetch/git servers)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /src

# Copy ecosystem manifests/scripts first for better layer caching.
COPY pyproject.toml README.md Makefile ./
COPY manifests/ manifests/
COPY scripts/ scripts/
COPY tools/ tools/
COPY tests/ tests/
COPY policies/ policies/
COPY channels/ channels/
COPY components/ components/

# Install the ecosystem + every shesh-* component in editable mode.
RUN pip install -q ruff pytest mcp fastmcp tomli && \
    pip install -e . && \
    for d in components/shesh-*/; do \
      [ -f "$d/pyproject.toml" ] && pip install -e "$d"; \
    done

# Resolve the canary lock and verify licenses at build time.
RUN python scripts/resolve_manifest.py --channel canary --out /tmp/canary.lock && \
    python scripts/check_licenses.py manifests/components.toml

# Default: run all gates.
ENTRYPOINT ["make", "check"]
CMD ["check"]
