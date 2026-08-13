#!/usr/bin/env bash
# install-shesh-stack.sh — Shesh Brain/Mind/Soma MCP stack (desktop-agnostic).
#
# Installs the shesh-core monorepo + the kept service repos into a shared venv,
# wires MCP client configs, systemd user units, and (optionally) Ollama models.
# Idempotent; safe to re-run. Runs after `setup install` (which already created
# the venv and installed Ollama/models on the desktop) OR standalone.
#
# Usage:
#   bash install-shesh-stack.sh [--skip-ai] [--no-sysupgrade] [--channel canary] [--dry-run]
#   --skip-ai       skip Ollama + model pulls (MCP servers still install)
#   --no-sysupgrade skip `pacman -Syu` (bootstrap already upgraded)
#   --channel       stable|canary|devel (default canary — matches the desktop)
set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()  { echo -e "${GREEN}[OK]${NC}   $*"; }
info(){ echo -e "${BLUE}[..]${NC}   $*"; }
warn(){ echo -e "${YELLOW}[!!]${NC}   $*"; }
die() { echo -e "${RED}[FATAL]${NC} $*" >&2; exit 1; }

SKIP_AI=0; NOSYS=0; DRY=0; CHANNEL="canary"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-ai) SKIP_AI=1; shift;;
    --no-sysupgrade) NOSYS=1; shift;;
    --channel) CHANNEL="$2"; shift 2;;
    --dry-run) DRY=1; shift;;
    -h|--help) cat <<'EOF'
install-shesh-stack.sh — install the Shesh MCP stack (desktop-agnostic)
  --skip-ai        skip Ollama + model pulls
  --no-sysupgrade  skip `pacman -Syu`
  --channel        stable|canary|devel (default canary)
  --dry-run        print actions only
EOF
      exit 0;;
    *) warn "unknown arg $1"; shift;;
  esac
done

SRC="${HOME}/src"
ECO="${SRC}/shesh-ecosystem"
COMP="${SRC}/components"
VENV="${XDG_STATE_HOME:-$HOME/.local/state}/shesh/.venv"
BIN_LINK="${HOME}/.local/bin"

run() { if [[ $DRY -eq 1 ]]; then info "[dry-run] $*"; else "$@"; fi; }

info "== Preflight =="
[[ $EUID -eq 0 ]] && die "run as your normal user"
command -v sudo >/dev/null || die "sudo required"
grep -qiE 'arch|cachyos' /etc/os-release || warn "not Arch/CachyOS — steps may differ"

info "== 1. Base tooling =="
[[ $NOSYS -eq 0 ]] && run sudo pacman -Syu --noconfirm
run sudo pacman -S --noconfirm --needed git curl base-devel
if ! command -v uv >/dev/null 2>&1; then
  run bash -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
  export PATH="$HOME/.local/bin:$PATH"
fi
ok "uv: $(uv --version 2>/dev/null || echo 'restart shell to load uv')"

info "== 2. Clone ecosystem + component repos =="
run mkdir -p "$SRC"
if [[ -d "$ECO/.git" ]]; then
  run git -C "$ECO" pull --ff-only || warn "ecosystem pull failed — continuing with existing checkout"
else
  run git clone https://github.com/gaganjainse/shesh-ecosystem.git "$ECO"
fi
run bash "$ECO/scripts/fetch-components.sh" "$COMP" "$ECO/manifests/components.toml"

info "== 3. Shared venv (reuses setup's ~/.local/state/shesh/.venv if present) =="
if [[ ! -x "$VENV/bin/python" ]]; then
  run uv venv "$VENV"
fi
ok "venv: $VENV"

info "== 4. Install components (editable) =="
if [[ -d "$COMP" ]]; then
  for d in "$COMP"/shesh-*; do
    [[ -d "$d" && ! -L "$d" ]] || continue   # skip symlinks (shared-repo aliases)
    [[ -f "$d/pyproject.toml" ]] || continue
    info "installing $(basename "$d")"
    run uv pip install --python "$VENV/bin/python" -e "$d"
  done
else
  warn "components dir missing — fetch-components.sh may need network"
fi

info "== 5. Symlink console scripts into ~/.local/bin (MCP clients resolve them) =="
run mkdir -p "$BIN_LINK"
if [[ -d "$VENV/bin" ]]; then
  for s in "$VENV"/bin/shesh-*; do
    [[ -f "$s" ]] || continue
    run ln -sf "$s" "$BIN_LINK/$(basename "$s")"
  done
fi

info "== 6. MCP client configs (channel: $CHANNEL) =="
run python3 "$ECO/scripts/generate_mcp_config.py" --channel "$CHANNEL"

info "== 7. systemd user units (absolute venv paths) =="
UNIT_DIR="$HOME/.config/systemd/user"
run mkdir -p "$UNIT_DIR"
write_unit() { # name, exec, desc
  local name="$1" exec_cmd="$2" desc="$3"
  local f="$UNIT_DIR/$name"
  if [[ $DRY -eq 1 ]]; then info "[dry-run] write unit $name"; return; fi
  cat > "$f" <<UNIT
[Unit]
Description=$desc
After=network-online.target

[Service]
ExecStart=$exec_cmd
Restart=on-failure
RestartSec=3

[Install]
WantedBy=default.target
UNIT
}
if [[ -d "$VENV/bin" ]]; then
  for s in "$VENV"/bin/shesh-*-mcp; do
    [[ -f "$s" ]] || continue
    bn="$(basename "$s")"
    write_unit "$bn.service" "$s" "Shesh MCP server: $bn"
  done
fi
run systemctl --user daemon-reload
if [[ -d "$UNIT_DIR" ]]; then
  for u in "$UNIT_DIR"/shesh-*-mcp.service; do
    [[ -f "$u" ]] || continue
    run systemctl --user enable "$(basename "$u")"
  done
fi

info "== 8. Ollama model stack (6GB VRAM) =="
if [[ $SKIP_AI -eq 0 ]]; then
  if ! command -v ollama >/dev/null 2>&1; then
    run sudo pacman -S --noconfirm --needed ollama
    run systemctl enable --now ollama 2>/dev/null || run sudo systemctl enable --now ollama
  fi
  MODELS=(phi4-mini qwen2.5-coder:3b moondream2 nomic-embed-text)
  for m in "${MODELS[@]}"; do
    run ollama pull "$m"
  done
  ok "models pulled: ${MODELS[*]}"
fi

info "== 9. Verification =="
[[ $DRY -eq 1 ]] && { info "[dry-run] verification skipped"; exit 0; }
fails=0
check() { if "$@" >/dev/null 2>&1; then ok "$*"; else warn "FAILED: $*"; fails=$((fails+1)); fi; }
check "$VENV/bin/python" -c "import tomllib"
check uv --version
for c in "$BIN_LINK"/shesh-*-mcp; do
  [[ -e "$c" ]] && check test -x "$c"
done
[[ $SKIP_AI -eq 0 ]] && check ollama list
if [[ $fails -gt 0 ]]; then die "$fails verification step(s) failed — see above"; fi
ok "Shesh stack installed. MCP config: ~/.config/shesh/mcp/servers.json"
