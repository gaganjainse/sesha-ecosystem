#!/usr/bin/env python3
"""tools/silent_failures.py — ecosystem silent-failure auditor.

Catches the failure-hidden patterns ruff/clippy cannot express blanket-wide:

  SF1 (error)   `except …:` whose body is only `pass` / `...`, unless an
                adjacent comment explains WHY silence is correct (daemon and
                probe boundaries are legitimate — they must say so).
  SF2 (error)   `contextlib.suppress()` with zero args or broad types
                (Exception/BaseException/bare) — a compact silent swallow.
  SF3 (error)   GitHub workflow steps with `continue-on-error: true`.
  SF4 (error)   shell scripts using `|| true` / `|| :` — a command whose
                failure is structurally invisible.
  SF5 (warn)    broad `except` (Exception/BaseException/bare) whose entire
                body returns a neutral value (None/{}/[]/""/0). Sometimes
                by design — listed for review, not gated.
  SF6 (warn)    Rust `#[allow(…)]` without an adjacent `//` reason comment.

Tracked files only (git ls-files) when inside a git repo, else filesystem
walk. Vendored trees (dotfiles forks, node_modules, caches) are excluded.

Exit 1 on any error-class finding; `-W` additionally fails on warnings.

Authoritative doc: docs/architecture/ (search "silent failure").
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "target",
    "dots", "sdata", ".config", "dist", "build", "out",
}
BROAD_TYPES = {"Exception", "BaseException", ""}  # "" = bare `except:`


@dataclass
class Finding:
    rule: str
    level: str  # "error" | "warn"
    path: Path
    line: int
    detail: str


@dataclass
class Report:
    errors: list[Finding] = field(default_factory=list)
    warnings: list[Finding] = field(default_factory=list)

    def record(self, f: Finding) -> None:
        (self.errors if f.level == "error" else self.warnings).append(f)


def _comment_near(lines: list[str], *idxs: int) -> str | None:
    """Return an explanatory comment at any source line (0-based candidates).

    Handles `#` (python/shell/yaml) and `//`, `///` (rust). A bare attribute
    marker (`#[allow(...)]`) is not a reason.
    """
    for i in idxs:
        if 0 <= i < len(lines):
            line = lines[i]
            m = re.search(r"#\s*(?!\[)(.+)$", line) or re.search(r"//[!/]?\s*(.+)$", line)
            if m and len(m.group(1).split()) >= 3:
                return m.group(1)
    return None


def _scan_python(path: Path, text: str, report: Report) -> None:
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        report.record(Finding("SF0", "error", path, e.lineno or 0,
                              f"unparseable: {e.msg}"))
        return
    lines = text.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            exc_type = ""
            if node.type is not None:
                exc_type = ast.unparse(node.type)
            body = node.body
            only_silence = (
                len(body) == 1
                and (isinstance(body[0], ast.Pass)
                     or (isinstance(body[0], ast.Expr)
                         and isinstance(body[0].value, ast.Constant)
                         and body[0].value.value is Ellipsis))
            )
            if only_silence:
                except_ln = node.lineno - 1
                pass_ln = body[0].lineno - 1
                reason = _comment_near(lines, except_ln, pass_ln, pass_ln - 1)
                if reason is None:
                    report.record(Finding(
                        "SF1", "error", path, node.lineno,
                        f"except ({exc_type or 'bare'}) swallowed with bare pass; "
                        f"fix it or explain the silence in an adjacent comment"))
            elif len(body) == 1 and isinstance(body[0], ast.Return):
                ret = body[0].value
                neutral = (
                    ret is None
                    or (isinstance(ret, ast.Constant) and ret.value in (None, "", 0))
                    or (isinstance(ret, (ast.Dict, ast.List)) and not ret.keys if isinstance(ret, ast.Dict) else isinstance(ret, ast.List) and not ret.elts)
                )
                if neutral and exc_type in BROAD_TYPES:
                    report.record(Finding(
                        "SF5", "warn", path, node.lineno,
                        f"broad except returns a neutral value "
                        f"({ast.unparse(body[0].value) if body[0].value is not None else 'None'})"))

        elif isinstance(node, ast.Call):
            fn = node.func
            is_suppress = (
                isinstance(fn, ast.Attribute) and fn.attr == "suppress"
                and isinstance(fn.value, ast.Name) and fn.value.id == "contextlib"
            ) or (isinstance(fn, ast.Name) and fn.id == "suppress")
            if is_suppress:
                if not node.args:
                    report.record(Finding("SF2", "error", path, node.lineno,
                                          "contextlib.suppress() with no arguments swallows everything"))
                else:
                    broad = any(
                        (isinstance(a, ast.Name) and a.id in ("Exception", "BaseException"))
                        for a in node.args
                    )
                    if broad:
                        report.record(Finding(
                            "SF2", "error", path, node.lineno,
                            f"contextlib.suppress({ast.unparse(node.args[0])}) is a compact silent failure; "
                            f"name the specific exceptions"))


def _scan_shell(path: Path, text: str, report: Report) -> None:
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        code = stripped.split("#", 1)[0].rstrip()
        if re.search(r"\|\|\s*(true|:)\s*$", code):
            report.record(Finding(
                "SF4", "error", path, i,
                "`|| true`/`|| :` makes a failure structurally invisible; "
                "make the step idempotent or handle the rc explicitly"))


def _scan_workflow(path: Path, text: str, report: Report) -> None:
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"continue-on-error\s*:\s*true", line):
            report.record(Finding("SF3", "error", path, i,
                                  "continue-on-error: true hides job failures"))


def _scan_rust(path: Path, text: str, report: Report) -> None:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if ("#[allow(" in line or "#[allow (" in line) and _comment_near(lines, i, i - 1, i - 2) is None:
            report.record(Finding(
                "SF6", "warn", path, i + 1,
                "#[allow(…)] without an adjacent reason comment"))


SCANNERS = {
    ".py": _scan_python,
    ".sh": _scan_shell,
    ".bash": _scan_shell,
    ".rs": _scan_rust,
}


def iter_files(root: Path) -> list[Path]:
    if (root / ".git").exists():
        try:
            # --cached + --others: tracked AND untracked-not-ignored. A bare
            # ls-files misses worktree files when the index lags the checkout
            # (e.g. after a sandbox snapshot rewound HEAD) — the audit must
            # never silently scan a stale subset.
            out = subprocess.run(
                ["git", "-C", str(root), "ls-files", "-z",
                 "--cached", "--others", "--exclude-standard"],
                capture_output=True, text=False, timeout=30, check=True).stdout
            paths = [root / p.decode() for p in out.split(b"\0") if p]
        except (OSError, subprocess.SubprocessError) as e:
            print(f"git ls-files failed for {root} ({e}); walking filesystem",
                  file=sys.stderr)
            paths = [p for p in root.rglob("*") if p.is_file()]
    else:
        paths = [p for p in root.rglob("*") if p.is_file()]
    result = []
    for p in paths:
        rel_parts = p.relative_to(root).parts if p.is_relative_to(root) else p.parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        if p.suffix in SCANNERS or p.suffix in (".yml", ".yaml"):
            result.append(p)
    return result


def scan_root(root: Path) -> Report:
    report = Report()
    for p in iter_files(root):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            report.record(Finding("SF0", "warn", p, 0, f"unreadable: {e}"))
            continue
        if p.suffix in (".yml", ".yaml") and (".github" in p.parts):
            _scan_workflow(p, text, report)
            continue
        scanner = SCANNERS.get(p.suffix)
        if scanner:
            scanner(p, text, report)
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", type=Path,
                    help="repo/component roots to scan (default: cwd)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("-W", "--warnings-as-errors", action="store_true")
    args = ap.parse_args()

    roots = args.paths or [Path.cwd()]
    findings: list[Finding] = []
    for root in roots:
        if not root.exists():
            print(f"missing root: {root}", file=sys.stderr)
            continue
        rep = scan_root(root)
        findings.extend(rep.errors)
        findings.extend(rep.warnings)

    if args.json:
        print(json.dumps([
            {"rule": f.rule, "level": f.level, "path": str(f.path),
             "line": f.line, "detail": f.detail}
            for f in findings
        ], indent=2))
    else:
        for f in findings:
            tag = "ERROR" if f.level == "error" else "warn "
            print(f"{tag} {f.rule} {f.path}:{f.line}: {f.detail}")
        print(f"\nsilent-failures: {sum(1 for f in findings if f.level == 'error')} errors, "
              f"{sum(1 for f in findings if f.level == 'warn')} warnings across {len(roots)} root(s)")

    n_err = sum(1 for f in findings if f.level == "error")
    n_warn = sum(1 for f in findings if f.level == "warn")
    if n_err or (args.warnings_as_errors and n_warn):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
