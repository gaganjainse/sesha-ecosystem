"""Regression tests for tools/silent_failures.py — focus: SF4 inside
workflow YAML run: blocks (missed before 2026-08-13: swarm-scheduled.yml
seeded with `--dashboard || true` and the auditor waved it through)."""
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "silent_failures", Path(__file__).resolve().parents[1] / "tools" / "silent_failures.py")
sf = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sf  # dataclasses resolve string annotations via sys.modules
spec.loader.exec_module(sf)


def scan_workflow(text: str, tmp_path: Path):
    p = tmp_path / "w.yml"
    p.write_text(text)
    rep = sf.Report()
    sf._scan_workflow(p, text, rep)
    return rep


def test_sf4_block_scalar_run(tmp_path):
    rep = scan_workflow(
        "steps:\n"
        "  - run: |\n"
        "      set -e\n"
        "      python seed.py --dashboard || true\n", tmp_path)
    sf4 = [f for f in rep.errors if f.rule == "SF4"]
    assert len(sf4) == 1 and sf4[0].line == 4


def test_sf4_inline_run(tmp_path):
    rep = scan_workflow("steps:\n  - run: make maybe || true\n", tmp_path)
    assert [f.rule for f in rep.errors] == ["SF4"]


def test_sf4_clean_run_blocks_pass(tmp_path):
    rep = scan_workflow(
        "jobs:\n  t:\n    steps:\n"
        "      - run: |\n"
        "          set -euo pipefail\n"
        "          for r in $REPOS; do\n"
        "              pip install \"$r\"\n"
        "          done\n"
        "      - run: pytest tests/ -q\n"
        "      - name: truthful || die\n"
        "        run: grep -q ok out.txt\n", tmp_path)
    assert rep.errors == []


def test_sf4_unscanned_non_run_keys(tmp_path):
    # `|| true` outside run: blocks is shell-comment/script data, not CI shell
    rep = scan_workflow("env:\n  NOTE: \"|| true is banned\"\n", tmp_path)
    assert rep.errors == []


def test_sf3_continue_on_error_still_caught(tmp_path):
    rep = scan_workflow("steps:\n  - run: x\n    continue-on-error: true\n", tmp_path)
    assert [f.rule for f in rep.errors] == ["SF3"]


def test_sf4_shell_files_still_caught(tmp_path):
    p = tmp_path / "s.sh"
    p.write_text("#!/bin/sh\nfoo || true\n")
    rep = sf.Report()
    sf._scan_shell(p, p.read_text(), rep)
    assert [f.rule for f in rep.errors] == ["SF4"]


def test_sf1_python_still_caught(tmp_path):
    p = tmp_path / "m.py"
    p.write_text("try:\n    x()\nexcept Exception:\n    pass\n")
    rep = sf.Report()
    sf._scan_python(p, p.read_text(), rep)
    assert any(f.rule == "SF1" for f in rep.errors)
