"""Offline safety tests for the GitHub swarm queue."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "swarm"))

import github_queue as queue  # noqa: E402


def test_component_worker_does_not_fall_back_to_other_components(monkeypatch):
    issues = [
        {"number": 1, "labels": [{"name": "component:shesh-kernel"}]},
        {"number": 2, "labels": [{"name": "component:general"}]},
    ]
    monkeypatch.setattr(queue, "_pat", lambda: "test-token")
    monkeypatch.setattr(queue, "_request", lambda *_args, **_kwargs: (200, issues))

    assert queue.list_pending_issues("shesh-system") == [issues[1]]


def test_component_worker_waits_when_no_matching_or_general_issue(monkeypatch):
    issues = [{"number": 1, "labels": [{"name": "component:shesh-kernel"}]}]
    monkeypatch.setattr(queue, "_pat", lambda: "test-token")
    monkeypatch.setattr(queue, "_request", lambda *_args, **_kwargs: (200, issues))

    assert queue.list_pending_issues("shesh-system") == []
