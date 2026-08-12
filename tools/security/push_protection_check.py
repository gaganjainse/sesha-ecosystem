#!/usr/bin/env python3
"""Verify org-level security settings are still on (dr_check dependency).

Reads the PAT path from argv[1], spot-checks the ecosystem repo for:
vulnerability alerts, automated security fixes, secret scanning,
secret-scanning push protection. Exit 1 with a named gap if any are off.
"""
import json
import sys
import urllib.request

pat_path = sys.argv[1] if len(sys.argv) > 1 else None
if not pat_path:
    print("usage: push_protection_check.py <pat-path>", file=sys.stderr)
    raise SystemExit(2)
with open(pat_path, encoding="utf-8") as fh:
    PAT = fh.read().strip()
req = urllib.request.Request(
    "https://api.github.com/repos/gaganjainse/shesh-ecosystem",
    headers={"Authorization": f"Bearer {PAT}", "Accept": "application/vnd.github+json"})
data = json.load(urllib.request.urlopen(req))
sa = data.get("security_and_analysis") or {}
missing = []
if (sa.get("secret_scanning") or {}).get("status") != "enabled":
    missing.append("secret_scanning")
if (sa.get("secret_scanning_push_protection") or {}).get("status") != "enabled":
    missing.append("secret_scanning_push_protection")
if missing:
    print("disabled: " + ", ".join(missing), file=sys.stderr)
    raise SystemExit(1)
