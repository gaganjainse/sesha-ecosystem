---
name: coding
description: Write, test, and refactor code safely. Always read before editing, run tests, and never push without review.
---

# Coding skill

When asked to write or change code:

1. **Understand first.** Read the relevant files. Use `git_status`/`git_log` to see context.
2. **Plan the diff.** State the files and approach before editing for non-trivial changes.
3. **Match the house style.** Rust: `cargo fmt`/`clippy`. Python: `ruff`. Lua: `stylua`.
   QML: `qmlformat`. Bash: `shellcheck`/`shfmt`.
4. **Small steps.** One logical change per commit; Conventional Commit messages
   (`feat:`, `fix:`, `docs:`, `chore(ci):`, `refactor:`).
5. **Test.** Run the component's `make test`/`pytest`/`cargo test`. Add a test for the fix.
6. **Never** force-push `main`, never `rm -rf`, never `sudo` unless explicitly asked.
7. For new dependencies, prefer the standard library; justify each new dependency and
   verify its license is GPL-3-compatible.

Model routing: implementation → code model (qwen2.5-coder:3b); review/planning → primary model.
