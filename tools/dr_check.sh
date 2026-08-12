#!/usr/bin/env bash
# tools/dr_check.sh — disaster-recovery readiness gate.
# Every check names the doc that defines it. Failures print the fix.
set -euo pipefail

ECO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fail=0

check() { # name, cmd..., fix-hint
    local name="$1"; shift
    if "$@" >/dev/null 2>&1; then
        echo "ok   $name"
    else
        echo "FAIL $name — $1"
        fail=1
    fi
}

check "PAT perms 600"       test "$(stat -c '%a' "$HOME/.config/shesh/github.pat")" = 600 \
      "chmod 600 ~/.config/shesh/github.pat"
check "askpass executable"  test -x "$ECO/tools/git_askpass.py" \
      "chmod +x tools/git_askpass.py (exec bits are restore-fragile)"
check "archive dir exists"  test -d "$HOME/archive" \
      "mkdir ~/archive — archive-not-delete needs its home"
check "ecosystem remote"    git -C "$ECO" remote get-url origin \
      "re-add origin (RECOVERY.md incident class A)"
check "push protection on"  python3 "$ECO/tools/security/push_protection_check.py" \
      "$HOME/.config/shesh/github.pat" \
      "re-enable secret scanning push protection via the org API"

python3 - "$ECO" <<'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).parent / "src" / "shesh-audit" / "src"))
try:
    from shesh_audit.log import AuditLog  # noqa: F401
    print("ok   shesh-audit importable (ledger tooling intact)")
except ImportError as e:
    print(f"FAIL shesh-audit import: {e} — pip install -e src/shesh-audit")
    sys.exit(1)
EOF

[ "$fail" -eq 0 ] && echo "DR-CHECK PASS" || { echo "DR-CHECK FAIL"; exit 1; }
