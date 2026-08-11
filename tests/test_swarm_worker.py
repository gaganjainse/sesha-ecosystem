from __future__ import annotations

from pathlib import Path
import subprocess

import tools.github_auth as github_auth
import tools.swarm.github_queue as github_queue
import tools.swarm.orchestrator as orchestrator
import tools.swarm.worker_github as worker_github


def test_git_environment_uses_askpass_without_remote_token() -> None:
    env = github_auth.git_environment("secret-token")

    assert env["GITHUB_PAT"] == "secret-token"
    assert env["GH_TOKEN"] == "secret-token"
    assert env["GIT_TERMINAL_PROMPT"] == "0"
    assert env["GIT_ASKPASS"].endswith("tools/git_askpass.py")


def test_askpass_reads_token_only_in_child_process() -> None:
    env = github_auth.git_environment("secret-token")
    helper = env["GIT_ASKPASS"]

    username = subprocess.run(
        [helper, "Username for github"],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    password = subprocess.run(
        [helper, "Password for github"],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    assert username.stdout.strip() == "x-access-token"
    assert password.stdout.strip() == "secret-token"
    assert "secret-token" not in password.stderr


def test_git_repo_root_does_not_assume_home_directory() -> None:
    root = github_auth.git_repo_root(Path(__file__).resolve().parents[1])

    assert root == Path(__file__).resolve().parents[1]


def test_todo_parser_excludes_indented_blocked_items(tmp_path: Path) -> None:
    todo = tmp_path / "TODO.md"
    todo.write_text(
        """## Brain
- 🔴 kernel merge is blocked
  - ⬜ hidden task
- 🟡 status prose, not a new assignment
- ⬜ visible platform task
"""
    )

    tasks = orchestrator.parse_todos(todo)

    assert [task["title"] for task in tasks] == ["visible platform task"]
    assert tasks[0]["blocked"] is False


def test_blocked_issue_detection_and_priority() -> None:
    blocked = {"title": "Do not force this", "labels": [], "body": ""}
    p0 = {"number": 2, "labels": [{"name": "P0"}]}
    p2 = {"number": 1, "labels": [{"name": "P2"}]}

    assert github_queue.is_blocked_issue(blocked)
    assert github_queue._priority_key(p0) < github_queue._priority_key(p2)


def test_executor_result_is_strict_about_none() -> None:
    assert worker_github._executor_result((True, "done")) == (True, "done")
    assert worker_github._executor_result(False) == (False, "executor returned failure")
    assert worker_github._executor_result(None) == (False, "executor returned no result")
