#!/usr/bin/env bash
# Collect install-failure state and upload it as one URL.
#
# Read-only. Runs no installer, changes no config, needs no sudo.
# Redacts tokens, keys, and passwords before upload.
#
#   bash <(curl -fsSL <this-url>)
#
# Prints a paste URL at the end. Send that URL.

set -uo pipefail
OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT

s() { printf '\n===== %s =====\n' "$1" >>"$OUT"; }
c() { printf '$ %s\n' "$*" >>"$OUT"; "$@" >>"$OUT" 2>&1; printf '\n' >>"$OUT"; }

{
  printf 'shesh install report\n'
  printf 'generated: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >>"$OUT"

s "identity"
c uname -a
c cat /etc/os-release
[ -r /sys/class/dmi/id/product_name ] && c cat /sys/class/dmi/id/product_name
c id
printf 'XDG_SESSION_TYPE=%s XDG_CURRENT_DESKTOP=%s\n' \
  "${XDG_SESSION_TYPE:-unset}" "${XDG_CURRENT_DESKTOP:-unset}" >>"$OUT"

s "graphics"
c bash -c 'lspci -k | grep -EA3 "VGA|3D" || true'
c bash -c 'command -v nvidia-smi >/dev/null && nvidia-smi || echo "nvidia-smi: not installed"'
c bash -c 'cat /sys/module/nvidia_drm/parameters/modeset 2>/dev/null || echo "nvidia_drm: not loaded"'
c bash -c 'lsmod | grep -E "^nvidia|^i915" || echo "no nvidia/i915 modules loaded"'

s "compositor"
c bash -c 'command -v hyprctl >/dev/null && hyprctl version || echo "hyprctl: not installed"'
c bash -c 'command -v hyprctl >/dev/null && hyprctl monitors || true'
c bash -c 'systemctl --user --failed --no-pager || true'

s "packages and helpers"
for p in hyprland quickshell-git nvidia-dkms linux-cachyos-headers ollama; do
  printf '%-26s %s\n' "$p" "$(pacman -Q "$p" 2>/dev/null || echo 'NOT INSTALLED')" >>"$OUT"
done
c bash -c 'for h in paru yay shelly pipx; do printf "%-8s %s\n" "$h" "$(command -v $h || echo missing)"; done'

s "pacman tail (last 80 lines)"
c bash -c 'tail -n 80 /var/log/pacman.log 2>/dev/null || echo "no pacman.log"'

s "shesh-desktop checkout"
D="$HOME/Workspace/shesh-desktop"
if [ -d "$D" ]; then
  c git -C "$D" log --oneline -3
  c git -C "$D" status --porcelain
else
  printf 'not cloned at %s\n' "$D" >>"$OUT"
fi

s "recent boot errors (journal)"
c bash -c 'journalctl -p err -b --no-pager -n 60 2>/dev/null || echo "journal unavailable"'

s "disk and memory"
c bash -c 'df -h / /home 2>/dev/null'
c free -h

# Redact anything credential-shaped before it leaves the machine.
sed -E -i \
  -e 's/(gh[pousr]_[A-Za-z0-9]{10,})/[REDACTED-TOKEN]/g' \
  -e 's/(github_pat_[A-Za-z0-9_]{10,})/[REDACTED-TOKEN]/g' \
  -e 's/(AKIA[0-9A-Z]{16})/[REDACTED-AWS]/g' \
  -e 's/([Pp]assword[=: ]+)[^ ]+/\1[REDACTED]/g' \
  -e 's/(Bearer )[A-Za-z0-9._-]+/\1[REDACTED]/g' \
  -e 's#(-----BEGIN [A-Z ]*PRIVATE KEY-----).*#\1[REDACTED]#g' \
  "$OUT"

echo
echo "--- collected $(wc -l <"$OUT") lines, uploading ---"
URL=$(curl -sf --max-time 30 --data-binary @"$OUT" https://paste.rs/ 2>/dev/null)
[ -z "$URL" ] && URL=$(curl -sf --max-time 30 --upload-file "$OUT" https://paste.c-net.org/ 2>/dev/null)

if [ -n "$URL" ]; then
  echo
  echo "  Send this URL:  $URL"
  echo
else
  echo "Upload failed. Save and attach this file instead:"
  cp "$OUT" "$HOME/shesh-report.txt"; trap - EXIT
  echo "  $HOME/shesh-report.txt"
fi
