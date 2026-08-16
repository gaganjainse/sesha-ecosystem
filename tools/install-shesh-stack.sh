#!/usr/bin/env bash
# install-shesh-stack.sh — install the Shesh MCP stack (Brain / Mind / Soma servers).
#
#   bash tools/install-shesh-stack.sh [--no-sysupgrade] [--skip-ai] [--channel CH]
#
# Part of shesh-ecosystem. Invoked by shesh-desktop/tools/bootstrap.sh.
#
# The installer is fail-visible: individual steps are attempted independently,
# but any failed required step makes the final process exit non-zero. This keeps
# the bootstrap from reporting a complete installation when the stack is partial.

set -uo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
log_info(){ echo -e "${BLUE}[STACK]${NC} $*"; }
log_ok()  { echo -e "${GREEN}[OK]${NC}   $*"; }
log_warn(){ echo -e "${YELLOW}[WARN]${NC} $*"; }
log_err() { echo -e "${RED}[FATAL]${NC} $*" >&2; }

NO_SYSUPGRADE=0; SKIP_AI=0; DRY=0; CHANNEL=""; SRC_DIR=""
FAILURES=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-sysupgrade) NO_SYSUPGRADE=1; shift;;
    --skip-ai) SKIP_AI=1; shift;;
    --channel) [[ $# -ge 2 ]] || { log_err "--channel requires a value"; exit 2; }; CHANNEL="$2"; shift 2;;
    --src-dir) [[ $# -ge 2 ]] || { log_err "--src-dir requires a value"; exit 2; }; SRC_DIR="$2"; shift 2;;
    --dry-run) DRY=1; shift;;
    -h|--help) sed -n '2,28p' "$0"; exit 0;;
    *) log_warn "unknown arg $1 — ignoring"; shift;;
  esac
done

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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SRC_DIR:-$HOME/Workspace}"
VENV="${XDG_STATE_HOME:-$HOME/.local/state}/shesh/venv"
BIN_DIR="$HOME/.local/bin"
CFG_DIR="$HOME/.config/shesh/mcp"
UNIT_DIR="$HOME/.config/systemd/user"
ERR_FILE="${XDG_RUNTIME_DIR:-/tmp}/shesh-stack-errors.log"

CORE_REPOS=(shesh-core)
EXTRA_REPOS=(shesh-memory shesh-orchestrator shesh-harness shesh-skills)
AI_REPOS=(shesh-voice)
ALL_REPOS=("${CORE_REPOS[@]}" "${EXTRA_REPOS[@]}")
[[ $SKIP_AI -eq 0 ]] && ALL_REPOS+=("${AI_REPOS[@]}")
SERVERS=(audit secrets brain mind shell system media messaging calendar backup containers ebpf mcp-bundle memory orchestrator harness skills)

run_cmd() {
  if [[ $DRY -eq 1 ]]; then
    log_info "[dry-run] $*"
    return 0
  fi
  "$@"
}

record_failure() {
  FAILURES=$((FAILURES + 1))
}

preflight() {
  log_info "=== Shesh stack installer ==="
  command -v git >/dev/null 2>&1 || { log_err "git required"; return 1; }
  command -v uv >/dev/null 2>&1 || { log_err "uv required (install via shesh-desktop bootstrap step 2)"; return 1; }
  mkdir -p "$BIN_DIR" "$CFG_DIR" "$UNIT_DIR" "$VENV" "$(dirname "$ERR_FILE")" || return 1
  : > "$ERR_FILE" || return 1
  log_ok "preflight ok (venv=$VENV)"
}

clone_repos() {
  log_info "=== Clone component repos into $REPO_ROOT ==="
  mkdir -p "$REPO_ROOT" || { log_err "could not create $REPO_ROOT"; record_failure; return; }
  local pids=()
  local max_jobs=4
  for r in "${ALL_REPOS[@]}"; do
    if [[ -d "$REPO_ROOT/$r/.git" ]]; then
      log_info "using existing clone: $r"
      continue
    fi
    log_info "cloning $r"
    (
      if run_cmd git clone --depth 1 "https://github.com/gaganjainse/$r.git" "$REPO_ROOT/$r"; then
        log_ok "cloned $r"
        exit 0
      fi
      log_warn "clone failed for $r"
      exit 1
    ) &
    pids+=("$!")
    if (( ${#pids[@]} >= max_jobs )); then
      local next=()
      for pid in "${pids[@]}"; do
        if ! wait "$pid"; then record_failure; fi
      done
      pids=("${next[@]}")
    fi
  done
  for pid in "${pids[@]}"; do
    if ! wait "$pid"; then record_failure; fi
  done
}

install_venv() {
  log_info "=== Build venv + install components ($VENV) ==="
  if ! run_cmd uv venv "$VENV"; then
    log_warn "failed to create venv"
    record_failure
    return
  fi
  for r in "${ALL_REPOS[@]}"; do
    local d="$REPO_ROOT/$r"
    if [[ ! -d "$d" ]]; then
      log_warn "required component checkout missing: $r"
      record_failure
      continue
    fi
    log_info "installing $r"
    if run_cmd uv pip install --python "$VENV/bin/python" -e "$d" 2>"$ERR_FILE"; then
      log_ok "$r installed"
    else
      log_warn "$r install failed: $(tail -1 "$ERR_FILE" 2>/dev/null)"
      record_failure
    fi
  done

  log_info "linking MCP console scripts to $BIN_DIR"
  for f in "$VENV"/bin/shesh-*-mcp "$VENV"/bin/shesh-acp "$VENV"/bin/shesh-desktop-ctl*; do
    [[ -e "$f" ]] || continue
    if ! run_cmd ln -sf "$f" "$BIN_DIR/$(basename "$f")"; then
      log_warn "failed to link $(basename "$f")"
      record_failure
    fi
  done
a}

gen_config() {
  log_info "=== Generate MCP client configs ==="
  local gen="$SCRIPT_DIR/../scripts/generate_mcp_config.py"
  if [[ ! -f "$gen" ]]; then
    log_warn "generate_mcp_config.py not found at $gen"
    record_failure
    return
  fi
  local chan_args=()
  [[ -n "$CHANNEL" ]] && chan_args=(--channel "$CHANNEL")
  if run_cmd python3 "$gen" "${chan_args[@]}" --out "$CFG_DIR"; then
    log_ok "config written to $CFG_DIR"
  else
    log_warn "MCP config generation failed"
    record_failure
  fi
}

install_units() {
  log_info "=== Install systemd user units ==="
  local target="$UNIT_DIR/shesh-mcp.target"
  if [[ $DRY -eq 1 ]]; then
    log_info "[dry-run] write $target + per-server units"
  else
    if ! cat > "$target" <<TARGET
[Unit]
Description=Shesh MCP servers (Brain/Mind/Soma)
Documentation=https://github.com/gaganjainse/shesh-ecosystem
After=graphical-session.target
$(for s in "${SERVERS[@]}"; do echo "Wants=shesh-$s-mcp.service"; done)
[Install]
WantedBy=graphical-session.target
TARGET
    then
      log_warn "failed to write $target"
      record_failure
      return
    fi
  fi

  for s in "${SERVERS[@]}"; do
    local bin="$BIN_DIR/shesh-$s-mcp"
    if [[ ! -e "$bin" ]]; then
      log_warn "required console script missing: shesh-$s-mcp"
      record_failure
      continue
    fi
    local svc="$UNIT_DIR/shesh-$s-mcp.service"
    if [[ $DRY -eq 0 ]]; then
      if ! cat > "$svc" <<UNIT
[Unit]
Description=Shesh MCP: $s
After=network-online.target
PartOf=shesh-mcp.target

[Service]
Type=simple
ExecStart=$bin
Restart=on-failure
RestartSec=5
NoNewPrivileges=yes
CapabilityBoundingSet=
ProtectSystem=full
PrivateTmp=yes
PrivateDevices=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
ProtectProc=invisible
ProcSubset=pid
RestrictSUIDSGID=yes
LockPersonality=yes
RestrictRealtime=yes
RestrictNamespaces=yes
SystemCallArchitectures=native
SystemCallFilter=@system-service
SystemCallErrorNumber=EPERM
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
TasksMax=128
[Install]
WantedBy=shesh-mcp.target
UNIT
      then
        log_warn "failed to write $svc"
        record_failure
        continue
      fi
      if ! systemctl --user enable "shesh-$s-mcp.service"; then
        log_warn "enable failed: shesh-$s-mcp.service"
        record_failure
      fi
    fi
    log_ok "unit shesh-$s-mcp.service"
  done

  if [[ $DRY -eq 0 ]]; then
    if ! systemctl --user daemon-reload; then
      log_warn "systemd daemon-reload failed (no user session?)"
      record_failure
    fi
    if ! systemctl --user enable shesh-mcp.target; then
      log_warn "enable failed: shesh-mcp.target"
      record_failure
    fi
  fi
}

verify() {
  log_info "=== Verify ==="
  local missing=0
  for s in "${SERVERS[@]}"; do
    if ! command -v "shesh-$s-mcp" >/dev/null 2>&1; then
      log_warn "shesh-$s-mcp not on PATH"
      missing=$((missing + 1))
    fi
  done
  if [[ $missing -eq 0 ]]; then
    log_ok "all server scripts present"
  else
    log_warn "$missing server script(s) missing"
    FAILURES=$((FAILURES + missing))
  fi
}

main() {
  if ! preflight; then
    log_err "preflight failed"
    exit 1
  fi
  if [[ $NO_SYSUPGRADE -eq 0 ]]; then
    log_info "system update"
    if ! run_cmd sudo pacman -Syu --noconfirm; then
      log_warn "pacman -Syu failed"
      record_failure
    fi
  else
    log_info "skipping system update (--no-sysupgrade)"
  fi
  clone_repos
  install_venv
  gen_config
  install_units
  verify
  echo
  if [[ $FAILURES -gt 0 ]]; then
    log_err "=== Shesh stack incomplete: $FAILURES failure(s) ==="
    log_err "Review $ERR_FILE and the warnings above before starting shesh-mcp.target."
    exit 1
  fi
  log_ok "=== Shesh stack install complete ==="
  log_info "Start with: systemctl --user start shesh-mcp.target (needs a graphical session)"
}

main "$@"
