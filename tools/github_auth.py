#!/usr/bin/env python3
"""Secure GitHub PAT loader — never logs secret value.

Order:
1. Env GITHUB_PAT > GH_TOKEN > GITHUB_TOKEN
2. File ~/.config/shesh/github.pat (must be 0600, refuses world-readable)
3. File ~/.config/shesh/github_token (legacy)
4. gh CLI hosts.yml (~/.config/gh/hosts.yml) — reads oauth_token for github.com

Usage:
  python tools/github_auth.py --check   # verifies loading, prints redacted
  python tools/github_auth.py --token   # prints token to stdout for scripting (use with care, pipes)
"""

from __future__ import annotations

import argparse
import os
import pathlib
import stat
import sys


def _check_perms(p: pathlib.Path) -> bool:
    try:
        st = p.stat()
        # Refuse if world-readable or group-readable
        if st.st_mode & stat.S_IRWXO:
            print(f"REFUSE world-readable {p} (chmod 600 required)", file=sys.stderr)
            return False
        if st.st_mode & stat.S_IRWXG:
            print(f"WARN group-readable {p}, should be 600", file=sys.stderr)
            # Allow but warn for group, refuse only other
        return True
    except Exception:
        return False


def load_pat() -> str | None:
    # 1. env
    for key in ("GITHUB_PAT", "GH_TOKEN", "GITHUB_TOKEN"):
        v = os.environ.get(key)
        if v and v.strip():
            return v.strip()

    # 2. file ~/.config/shesh/github.pat
    cfg_dir = pathlib.Path.home() / ".config/shesh"
    for fname in ("github.pat", "github_token", "pat"):
        p = cfg_dir / fname
        if p.exists():
            if not _check_perms(p):
                continue
            try:
                token = p.read_text().strip()
                if token:
                    return token
            except Exception:
                continue

    # 3. gh cli hosts.yml
    gh_hosts = pathlib.Path.home() / ".config/gh/hosts.yml"
    if gh_hosts.exists():
        try:
            txt = gh_hosts.read_text()
            # Minimal yaml parse: look for oauth_token
            for line in txt.splitlines():
                line = line.strip()
                if "oauth_token:" in line:
                    token = line.split("oauth_token:")[-1].strip().strip('"').strip("'")
                    if token:
                        return token
        except Exception:
            pass

    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="GitHub PAT loader")
    ap.add_argument("--check", action="store_true", help="check loading, redacted")
    ap.add_argument("--token", action="store_true", help="print raw token")
    args = ap.parse_args()

    pat = load_pat()
    if not pat:
        print("No PAT found. Set GITHUB_PAT env or create ~/.config/shesh/github.pat with chmod 600", file=sys.stderr)
        print("Or run: gh auth login", file=sys.stderr)
        return 1

    if args.token:
        print(pat)
        return 0

    if args.check:
        redacted = pat[:4] + "*" * (len(pat) - 8) + pat[-4:] if len(pat) > 8 else "****"
        print(f"PAT found: {redacted} (len {len(pat)})")
        print(f"Source: env or {pathlib.Path.home() / '.config/shesh/github.pat'} or gh hosts.yml")
        # Also check git remote
        try:
            import subprocess

            remote = subprocess.check_output(
                ["git", "-C", "/home/user", "remote", "get-url", "origin"],
                text=True,
            ).strip()
            print(f"git remote origin: {remote}")
        except Exception:
            pass
        return 0

    # default: check
    return main.__wrapped__ if False else 0


if __name__ == "__main__":
    # quick check if called without args
    if len(sys.argv) == 1:
        sys.argv.append("--check")
    sys.exit(main())
