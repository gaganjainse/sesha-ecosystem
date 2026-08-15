#!/usr/bin/env python3
"""a11y_check — find interactive QML elements missing accessibility names.

Scans a Quickshell/QtQuick QML tree for interactive components that have no
`accessibleName` and no `Accessible` block. Report-only by default (the shell
UI cannot be rendered in CI, so findings are a human checklist, not a gate).
Exit code 0 with a baseline summary; --strict exits 1 if any interactive
element is unlabelled.

Usage:
  python tools/a11y_check.py [--root DIR] [--strict]
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

# Components that are interactive in QtQuick/Quickshell.
INTERACTIVE = {
    "Button", "ToolButton", "TextField", "TextArea", "Slider", "Switch",
    "CheckBox", "RadioButton", "ComboBox", "SpinBox", "Dial", "Menu",
    "MenuItem", "TabButton", "RangeSlider", "DelayButton", "Tumbler",
}

# Any component with one of these signal handlers is interactive too.
INTERACTIVE_HANDLERS = {"onClicked", "onActivated", "onToggled", "onAccepted", "onTriggered"}

OPEN_RE = re.compile(r"\b([A-Za-z][A-Za-z0-9]*)\s*\{")
HANDLER_RE = re.compile(r"\b(on[A-Z][A-Za-z0-9]*)\s*[:(]")
ACCESSIBLE_RE = re.compile(r"\baccessibleName\s*[:=]|\bAccessible\s*\{")


def scan_file(path: pathlib.Path) -> list[str]:
    """Return (file:line) strings for interactive elements without a11y attrs."""
    try:
        lines = path.read_text("utf-8", errors="replace").splitlines()
    except OSError:
        return []
    findings: list[str] = []
    in_comment = False
    for i, raw in enumerate(lines, start=1):
        line = raw.strip()
        if line.startswith("/*"):
            in_comment = True
        if in_comment:
            if line.endswith("*/") or "*/" in line:
                in_comment = False
            continue
        if line.startswith("//") or line.startswith("*"):
            continue
        if ACCESSIBLE_RE.search(line):
            continue  # this line already declares accessibility
        # interactive element opened on this line?
        if OPEN_RE.search(line) and not line.startswith(("import", "pragma")):
            comp = OPEN_RE.search(line).group(1)
            if comp in INTERACTIVE:
                # scan a generous window around the element (accessibleName
                # can be declared right after the open brace or before the
                # handler a dozen lines down)
                block = "\n".join(lines[max(0, i - 20) : min(len(lines), i + 20)])
                if not ACCESSIBLE_RE.search(block):
                    findings.append(f"{path}:{i}: {comp}")
        for h in INTERACTIVE_HANDLERS:
            if HANDLER_RE.search(line) and h in line:
                block = "\n".join(lines[max(0, i - 20) : min(len(lines), i + 20)])
                if not ACCESSIBLE_RE.search(block):
                    findings.append(f"{path}:{i}: handler {h}")
                break
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=pathlib.Path, default=pathlib.Path("."))
    ap.add_argument("--strict", action="store_true", help="exit 1 when findings exist")
    args = ap.parse_args()

    qml_files = sorted(args.root.rglob("*.qml"))
    if not qml_files:
        print(f"no .qml files under {args.root}")
        return 1

    findings: list[str] = []
    for f in qml_files:
        findings.extend(scan_file(f))

    total_interactive = len(findings)
    print(f"QML files scanned: {len(qml_files)}")
    print(f"interactive elements without a11y attrs: {total_interactive}")
    if findings:
        print("\nBaseline (file:line):")
        for f in findings[:200]:
            print(f"  {f}")
        if len(findings) > 200:
            print(f"  ... and {len(findings) - 200} more")
        print("\nFix pattern (QtQuick):")
        print('  Button { accessibleName: "Close"; ... }')
        print("  or")
        print("  Accessible.role: Accessible.Button; Accessible.name: 'Close'")
    return 1 if (args.strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
