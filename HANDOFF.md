# HANDOFF.md

How to pick up work in this fleet, whether you are a new session, a different
agent, or a person returning after a break.

Read this file first. It is the entry point; everything else is one link away.

---

## 1. Orient

The fleet is a local-first agent system for Arch-based Linux. Three layers:
a deterministic governance kernel (**Brain**), model-driven reasoning (**Mind**),
and tool servers that sense and act (**Soma**). Models propose actions; the
kernel validates, executes, and records them.

| Read this | For |
|---|---|
| [AGENTS.md](AGENTS.md) | Conventions, gate, judgment boundaries. **Mandatory.** |
| [shesh-docs](https://github.com/gaganjainse/shesh-docs) | Architecture, procedures, reference |
| [STATE.md](STATE.md) | What is in flight right now. Generated, never hand-edited. |
| [TODO.md](TODO.md) | The backlog |

Do not read the archive to find current state. It is a record, not a status.

---

## 2. The product and factory split

**This is the distinction most easily lost between sessions.** Getting it wrong
means shipping development tooling to users, or applying release gates to
throwaway scripts.

| | Product | Factory |
|---|---|---|
| **Question** | Does a user install this? | Does this only help us build? |
| **Repositories** | `shesh-core`, `shesh-memory`, `shesh-orchestrator`, `shesh-harness`, `shesh-phone`, `shesh-omniroute`, `shesh-voice`, `shesh-desktop`, `shesh-skills`, `SheshAOS` | `shesh-workspace` |
| **Composition** | `shesh-ecosystem` — manifest, lockfiles, gates | — |
| **Documentation** | `shesh-docs` | `shesh-workspace/docs` |
| **Release channels** | Yes: `devel` → `canary` → `stable` | No |
| **Gate** | `make check` must pass before promotion | Tests only |
| **Standard** | Production. No stubs, no placeholders. | Pragmatic. May be rough. |

**The rule:** if a change would appear on a user's machine, it is product and it
passes the gate. If it only helps build the product, it is factory and it stays
in `shesh-workspace`.

Never move factory tooling into a product repository to make an import work.
Never apply the session protocol to product code.

`shesh-docs-archive` is neither. It is a read-only record.

---

## 3. Before you touch anything

```bash
git -C <repo> status --short          # a dirty tree means work in progress
cat STATE.md                          # generated inventory
make check                            # must be green before you start
```

If `make check` is red on arrival, **fix that first or report it**. Do not build
on a broken gate; you will not know which failure is yours.

---

## 4. Where a change belongs

| Change | Repository |
|---|---|
| A tool server or governance primitive | `shesh-core` |
| Memory, orchestration, refinement, phone, routing | The matching service repository |
| Component versions, channels, licence gate | `shesh-ecosystem` |
| Architecture, procedures, reference, policy | `shesh-docs` |
| A skill served to agents | `shesh-skills` |
| Build tooling, session tooling, parallel agents | `shesh-workspace` |
| A superseded record | `shesh-docs-archive` |

**Do not span repositories in one change.** Sequence them and state the order.
A component change and its manifest bump are two changes, in that order.

---

## 5. The work loop

1. **Take one item** from `TODO.md`. If it is ambiguous, ask rather than guess.
2. **Branch** as `feat/<slug>` or `fix/<slug>`. Never work on `main`.
3. **Read before editing.** Every file you will change.
4. **State the plan** for anything non-trivial: files, approach, risk.
5. **Implement** the smallest change that completes the item.
6. **Test.** `make check`. A red gate ends the task; do not weaken a test.
7. **Commit** with a Conventional Commit message.
8. **Record** the outcome so the next session does not re-derive it.

---

## 6. Stop and ask when

- The gate fails and the cause is not obvious.
- The task needs a credential, a purchase, or an irreversible action.
- The task requires deleting data or rewriting history.
- You have looped three times without landing a change.
- Two documents disagree and you cannot tell which is current.
- The change would span product and factory.

**Stopping and reporting is a success. Guessing is not.**

---

## 7. Handing off

Before the session ends, or when context is nearly exhausted:

```bash
python3 tools/handoff.py
```

This regenerates `STATE.md` from the actual repositories — branches, dirty
trees, gate status, recent commits — so the next session reads fact rather than
recollection. It is also run by CI, so `STATE.md` is never stale for long.

Leave the tree in one of two states: **committed on a branch**, or **clean**.
Never leave uncommitted work with no note; the next session cannot tell an
experiment from an unfinished fix.

---

## 8. What never happens

- No credential in a file, a commit, a log, or a chat message.
- No force-push, no rewriting published history, no pushing to `main`.
- No weakening a test, a gate, or a policy rule to make a task pass.
- No writing to `~/.ssh`, `~/.gnupg`, vaults, or employer directories.
- No reporting a test as passing without running it.
- No claiming a component does something without reading the code.
- No volatile counts in documentation.

---

## 9. Automation you do not need to run by hand

| What | When it runs | What it keeps in sync |
|---|---|---|
| `tools/handoff.py` | Session end, and in CI | `STATE.md` |
| `tools/sync_fleet.py` | CI on every push | Boilerplate, workflows, `.gitignore`, agent files |
| `tools/generate_components.py` | CI in `shesh-docs` | The component catalogue, from the manifest |
| `tools/check_docs.py` | CI in `shesh-docs` | Documentation style and links |
| `pytest tests/test_skills_spec.py` | CI in `shesh-skills` | Skill specification conformance |

If you find yourself editing generated content by hand, that is a defect in the
generator. Fix the generator.
