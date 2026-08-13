#!/usr/bin/env bash
# install-shesh-stack.sh — Shesh AI stack on CachyOS/Arch (desktop-agnostic)
#
# Installs the Brain/Mind/Soma MCP servers + Ollama model stack so the agent
# layer runs regardless of which desktop dots you use (end-4/dots-hyprland,
# shesh-desktop, or plain Hyprland). Idempotent; safe to re-run.
#
# Usage:
#   bash install-shesh-stack.sh [--skip-ai] [--dry-run] [--channel stable]
#   --skip-ai   skip Ollama + model pulls
#   --channel   stable|canary|devel (default stable)
#
# What it does:
#   1. Preflight (Arch/CachyOS, user not root, network, ~/src)
#   2. Install uv + ollama
#   3. Clone shesh-ecosystem + fetch component repos (manifest)
#   4. uv install each component (console scripts: shesh-*-mcp)
#   5. Generate MCP client configs (~/.config/shesh/mcp/*.json)
#   6. Install systemd user units for the core MCP servers
#   7. Pull the 6GB-VRAM Ollama model set
#   8. Verification gate
set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()  { echo -e "${GREEN}[OK]${NC}   $*"; }
info(){ echo -e "${BLUE}[..]${NC}   $*"; }
warn(){ echo -e "${YELLOW}[!!]${NC}   $*"; }
die() { echo -e "${RED}[FATAL]${NC} $*" >&2; exit 1; }

SKIP_AI=0; DRY=0; CHANNEL="stable"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-ai) SKIP_AI=1; shift;;
    --channel) CHANNEL="$2"; shift 2;;
    --dry-run) DRY=1; shift;;
    -h|--help) sed -n '2,20p' "$0"; exit 0;;
    *) warn "unknown arg $1"; shift;;
  esac
done

SRC="${HOME}/src"
ECO="${SRC}/shesh-ecosystem"
COMP="${SRC}/components"

info "== Preflight =="
[[ $EUID -eq 0 ]] && die "run as your normal user (sudo will be used where needed)"
command -v sudo >/dev/null || die "sudo required"
grep -qiE 'arch|cachyos' /etc/os-release || warn "not Arch/CachyOS — some steps may differ"
[[ $DRY -eq 1 ]] && info "[dry-run] mode: printing actions only"

run() { if [[ $DRY -eq 1 ]]; then info "[dry-run] $*"; else "$@"; fi; }

info "== 1. Base tooling (uv, git, ollama) =="
run sudo pacman -Syu --noconfirm
run sudo pacman -S --noconfirm --needed git curl base-devel
if ! command -v uv >/dev/null 2>&1; then
  run bash -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
  export PATH="$HOME/.local/bin:$PATH"
fi
ok "uv: $(uv --version 2>/dev/null || echo 'pending PATH reload')"
if [[ $SKIP_AI -eq 0 ]] && ! command -v ollama >/dev/null 2>&1; then
  run sudo pacman -S --noconfirm --needed ollama
  run systemctl --user enable --now ollama 2>/dev/null || run systemctl enable --now ollama
fi

info "== 2. Clone ecosystem + components =="
run mkdir -p "$SRC"
if [[ -d "$ECO/.git" ]]; then
  info "shesh-ecosystem present; pulling"
  run git -C "$ECO" pull --ff-only || warn "ecosystem pull failed (continuing with existing checkout)"
else
  run git clone https://github.com/gaganjainse/shesh-ecosystem.git "$ECO"
fi
run "$ECO/scripts/fetch-components.sh" "$COMP" "$ECO/manifests/components.toml"

info "== 3. Install components (uv, editable) =="
if [[ -d "$COMP" ]]; then
  for d in "$COMP"/shesh-*; do
    [[ -d "$d" ]] || continue
    [[ -f "$d/pyproject.toml" ]] || continue
    info "installing $(basename "$d")"
    run bash -c "cd '$d' && uv pip install --system -e . 2>/dev/null || uv pip install -e ."
  done
else
  warn "components dir missing — fetch-components.sh may need network"
fi
# ensure console scripts resolve
hash -r 2>/dev/null || true

info "== 4. MCP client configs =="
run python3 "$ECO/scripts/generate_mcp_config.py" --channel "$CHANNEL"

info "== 5. systemd user units (core MCP servers) =="
UNIT_DIR="$HOME/.config/systemd/user"
run mkdir -p "$UNIT_DIR"

write_unit() { # name, exec, desc
  local name="$1" exec_cmd="$2" desc="$3" f="$UNIT_DIR/$name"
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

# Commands match the console_scripts each pyproject declares.
write_unit shesh-audit-mcp.service    "shesh-audit-mcp"    "Shesh governance audit MCP"
write_unit shesh-secrets-mcp.service  "shesh-secrets-mcp"  "Shesh secret resolution MCP"
write_unit shesh-memory-mcp.service   "shesh-memory-mcp"   "Shesh hierarchical memory MCP"
write_unit shesh-brain-mcp.service    "shesh-brain-mcp"    "Shesh brain (kernel) MCP"

# shesh-system/files/shell are optional soma services — enable only if installed
for svc in shesh-system-control-mcp shesh-files-mcp shesh-shell-mcp; do
  if command -v "$svc" >/dev/null 2>&1; then
    write_unit "$svc.service" "$svc" "Shesh soma MCP ($svc)"
  else
    warn "$svc not installed — skipping unit (install its repo to enable)"
  fi
done

run systemctl --user daemon-reload
for u in "$UNIT_DIR"/shesh-*.service; do
  [[ -f "$u" ]] || continue
  run systemctl --user enable "$(basename "$u")"
done

info "== 6. Ollama model stack (6GB VRAM) =="
if [[ $SKIP_AI -eq 0 ]]; then
  MODELS=(phi4-mini qwen2.5-coder:3b moondream2 nomic-embed-text)
  for m in "${MODELS[@]}"; do
    run ollama pull "$m"
  done
  ok "models pulled: ${MODELS[*]}"
fi

info "== 7. Verification =="
if [[ $DRY -eq 1 ]]; then
  info "[dry-run] verification skipped"
  exit 0
fi
fails=0
check() { if "$@" >/dev/null 2>&1; then ok "$*"; else warn "FAILED: $*"; fails=$((fails+1)); fi; }
check python3 -c "import tomllib"
check uv --version
for c in shesh-audit-mcp shesh-secrets-mcp shesh-memory-mcp shesh-brain-mcp; do
  check command -v "$c"
done
[[ $SKIP_AI -eq 0 ]] && check ollama list
if [[ $fails -gt 0 ]]; then
  die "$fails verification step(s) failed — see warnings above"
fi
ok "Shesh stack installed and verified. MCP config: ~/.config/shesh/mcp/servers.json"
