#!/usr/bin/env bash
# install-shesh-stack.sh — install the Shesh MCP stack (Brain / Mind / Soma servers).
#
#   bash tools/install-shesh-stack.sh [--no-sysupgrade] [--skip-ai] [--channel CH]
#
# Part of shesh-ecosystem. Invoked by shesh-desktop/tools/bootstrap.sh.
#
# What it does (idempotent; per-step failures warn and continue):
#   1. (optional) system update            — skipped with --no-sysupgrade
#   2. Clone the Shesh-owned component repos (or reuse --src-dir)
#   3. Build one shared uv venv and `uv pip install -e .` each Python component:
#        - shesh-core       -> audit secrets brain mind shell system media
#                              messaging calendar backup containers ebpf mcp-bundle
#                              acp desktop-ctl
#        - shesh-memory     -> memory
#        - shesh-orchestrator -> orchestrator
#        - shesh-harness    -> harness
#        - shesh-skills     -> skills
#        - shesh-voice      -> voice frontend (skipped with --skip-ai)
#   4. Expose every `<name>-mcp` console script on PATH (~/.local/bin)
#   5. Generate MCP client configs (~/.config/shesh/mcp) via generate_mcp_config.py
#   6. Install + enable systemd user units (shesh-mcp.target + per-server)
#
# Flags:
#   --no-sysupgrade   skip `pacman -Syu`
#   --skip-ai         skip the voice frontend (shesh-voice) + model pulls
#   --channel CH      manifest channel for config generation (default: all)
#   --src-dir DIR     use existing clones here instead of cloning
#   --dry-run         print every step, run nothing
#   --help
#
# Headless / no-DE sudo (same convention as bootstrap.sh):
#   SUDO_ASKPASS / BOOTSTRAP_SUDO_PASSWORD — used if set.

set -uo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log_info(){ echo -e "${BLUE}[STACK]${NC} $*"; }
log_ok()  { echo -e "${GREEN}[OK]${NC}   $*"; }
log_warn(){ echo -e "${YELLOW}[WARN]${NC} $*"; }
log_err() { echo -e "${RED}[FATAL]${NC} $*" >&2; }

NO_SYSUPGRADE=0; SKIP_AI=0; DRY=0; CHANNEL=""; SRC_DIR=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-sysupgrade) NO_SYSUPGRADE=1; shift;;
    --skip-ai) SKIP_AI=1; shift;;
    --channel) CHANNEL="$2"; shift 2;;
    --src-dir) SRC_DIR="$2"; shift 2;;
    --dry-run) DRY=1; shift;;
    -h|--help) sed -n '2,40p' "$0"; exit 0;;
    *) log_warn "unknown arg $1 — ignoring"; shift;;
  esac
done

# Optional non-interactive sudo (mirrors bootstrap.sh).
if [[ -n "${SUDO_ASKPASS:-}" ]]; then
  sudo() { command sudo -A "$@"; }
  export SUDO_ASKPASS
elif [[ -n "${BOOTSTRAP_SUDO_PASSWORD:-}" ]]; then
  _ap_dir="$(mktemp -d "${XDG_RUNTIME_DIR:-/tmp}/shesh-sudo.XXXXXX")"
  _ap="$_ap_dir/askpass.sh"
  printf '#!/usr/bin/env bash\necho "%s"\n' "$BOOTSTRAP_SUDO_PASSWORD" > "$_ap"
  chmod 700 "$_ap"
  SUDO_ASKPASS="$_ap"; export SUDO_ASKPASS
  sudo() { command sudo -A "$@"; }
fi

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SRC_DIR:-$HOME/Workspace}"
VENV="${XDG_STATE_HOME:-$HOME/.local/state}/shesh/venv"
BIN_DIR="$HOME/.local/bin"
CFG_DIR="$HOME/.config/shesh/mcp"
UNIT_DIR="$HOME/.config/systemd/user"

# Shesh-owned Python component repos.
CORE_REPOS=(shesh-core)
EXTRA_REPOS=(shesh-memory shesh-orchestrator shesh-harness shesh-skills)
AI_REPOS=(shesh-voice)
ALL_REPOS=("${CORE_REPOS[@]}" "${EXTRA_REPOS[@]}")
[[ $SKIP_AI -eq 0 ]] && ALL_REPOS+=("${AI_REPOS[@]}")

# Server console-script stems that get a systemd unit (matches shesh-mcp.target Wants).
SERVERS=(audit secrets brain mind shell system media messaging calendar backup containers ebpf mcp-bundle memory orchestrator harness skills)

run_cmd() { if [[ $DRY -eq 1 ]]; then log_info "[dry-run] $*"; else "$@"; fi; }

preflight() {
  log_info "=== Shesh stack installer ==="
  command -v git >/dev/null 2>&1 || { log_err "git required"; exit 1; }
  command -v uv  >/dev/null 2>&1 || { log_err "uv required (install via shesh-desktop bootstrap step 2)"; exit 1; }
  mkdir -p "$BIN_DIR" "$CFG_DIR" "$UNIT_DIR" "$VENV"
  log_ok "preflight ok (venv=$VENV)"
}

clone_repos() {
  log_info "=== Clone component repos into $REPO_ROOT ==="
  for r in "${ALL_REPOS[@]}"; do
    if [[ -d "$REPO_ROOT/$r/.git" ]]; then
      log_info "using existing clone: $r"
    else
      log_info "cloning $r"
      run_cmd git clone --depth 1 "https://github.com/gaganjainse/$r.git" "$REPO_ROOT/$r" \
        || log_warn "clone failed for $r"
    fi
  done
}

install_venv() {
  log_info "=== Build venv + install components ($VENV) ==="
  run_cmd uv venv "$VENV"
  for r in "${ALL_REPOS[@]}"; do
    local d="$REPO_ROOT/$r"
    [[ -d "$d" ]] || { log_warn "skip $r (not found)"; continue; }
    log_info "installing $r"
    if run_cmd uv pip install --python "$VENV/bin/python" -e "$d" 2>/tmp/kilo/stack_err; then
      log_ok "$r installed"
    else
      log_warn "$r install failed: $(tail -1 /tmp/kilo/stack_err 2>/dev/null)"
    fi
  done
  log_info "linking *-mcp console scripts to $BIN_DIR"
  for f in "$VENV"/bin/shesh-*-mcp "$VENV"/bin/shesh-acp "$VENV"/bin/shesh-desktop-ctl*; do
    [[ -e "$f" ]] || continue
    run_cmd ln -sf "$f" "$BIN_DIR/$(basename "$f")"
  done
}

gen_config() {
  log_info "=== Generate MCP client configs ==="
  local gen="$SCRIPT_DIR/../scripts/generate_mcp_config.py"
  if [[ ! -f "$gen" ]]; then
    log_warn "generate_mcp_config.py not found at $gen — skipping config"
    return 0
  fi
  local chan_args=()
  [[ -n "$CHANNEL" ]] && chan_args=(--channel "$CHANNEL")
  run_cmd python3 "$gen" "${chan_args[@]}" --out "$CFG_DIR"
  log_ok "config written to $CFG_DIR"
}

install_units() {
  log_info "=== Install systemd user units ==="
  local target="$UNIT_DIR/shesh-mcp.target"
  if [[ $DRY -eq 1 ]]; then
    log_info "[dry-run] write $target + per-server units"
  else
    cat > "$target" <<TARGET
[Unit]
Description=Shesh MCP servers (Brain/Mind/Soma)
Documentation=https://github.com/gaganjainse/shesh-ecosystem
After=graphical-session.target
$(for s in "${SERVERS[@]}"; do echo "Wants=shesh-$s-mcp.service"; done)
[Install]
WantedBy=graphical-session.target
TARGET
  fi
  for s in "${SERVERS[@]}"; do
    local bin="$BIN_DIR/shesh-$s-mcp"
    [[ -e "$bin" ]] || { log_warn "no console script shesh-$s-mcp — skipping its unit"; continue; }
    local svc="$UNIT_DIR/shesh-$s-mcp.service"
    if [[ $DRY -eq 0 ]]; then
      cat > "$svc" <<UNIT
[Unit]
Description=Shesh MCP: $s
After=network-online.target
PartOf=shesh-mcp.target

[Service]
Type=simple
ExecStart=$bin
Restart=on-failure
RestartSec=5

[Install]
WantedBy=shesh-mcp.target
UNIT
      systemctl --user enable "shesh-$s-mcp.service" 2>/dev/null || log_warn "enable failed: shesh-$s-mcp.service"
    fi
    log_ok "unit shesh-$s-mcp.service"
  done
  if [[ $DRY -eq 0 ]]; then
    systemctl --user daemon-reload 2>/dev/null || log_warn "systemd daemon-reload failed (no user session?)"
    systemctl --user enable shesh-mcp.target 2>/dev/null || log_warn "enable failed: shesh-mcp.target"
  fi
  log_ok "units installed + enabled (start after login / graphical session)"
}

verify() {
  log_info "=== Verify ==="
  local missing=0
  for s in "${SERVERS[@]}"; do
    command -v "shesh-$s-mcp" >/dev/null 2>&1 || { log_warn "shesh-$s-mcp not on PATH"; missing=$((missing+1)); }
  done
  if [[ $missing -eq 0 ]]; then
    log_ok "all server scripts present"
  else
    log_warn "$missing server script(s) missing"
  fi
}

main() {
  preflight
  if [[ $NO_SYSUPGRADE -eq 0 ]]; then
    log_info "system update"; run_cmd sudo pacman -Syu --noconfirm || log_warn "pacman -Syu failed"
  else
    log_info "skipping system update (--no-sysupgrade)"
  fi
  clone_repos
  install_venv
  gen_config
  install_units
  verify
  echo
  log_ok "=== Shesh stack install complete ==="
  log_info "Start with: systemctl --user start shesh-mcp.target   (needs a graphical session)"
}

main "$@"
