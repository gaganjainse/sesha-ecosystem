# Recovery Runbook — when the ground moves

Canonical recovery doc. Tested against four real sandbox-restore incidents
in one week (2026-08-08 → 2026-08-13) plus two ghost-commit resurrections.
Every step below has been executed against the live estate.

## Invariants that make recovery cheap

- **GitHub is the ground truth.** Nothing precious lives only locally;
  `archive/` is the single local-only store and is itself documented.
- **Archive-not-delete:** anything risky lands in `~/archive/` first.
- **Oracle question, not suppression:** if recovery surprises you, stop and
  document (this file), never `|| true` past it.

## Incident class A — environment restore wiped local state

Symptoms: `origin` remotes vanish from clones, exec bits stripped
(~/.local/bin, scripts), `/tmp` wiped (venvs die), PAT file perms reset to
644, git HEAD refs rewound while worktrees keep newer content.

Runbook (exact order):

```bash
# 0. PAT + askpass hygiene (push fails 'could not read Password' without this)
chmod 600 ~/.config/shesh/github.pat
chmod +x /home/user/shesh-ecosystem/tools/git_askpass.py ~/.local/bin/*

# 1. Per clone: restore remote, fetch, verify against GitHub truth
cd <repo>
git remote add origin https://github.com/gaganjainse/<repo>.git 2>/dev/null || \
  git remote set-url origin https://github.com/gaganjainse/<repo>.git
export GIT_ASKPASS=<eco>/tools/git_askpass.py GIT_TERMINAL_PROMPT=0
git fetch origin

# 2. NEVER reset --hard before checking for unpushed work
git rev-list origin/<default-branch>..HEAD   # expect 0; if >0 → archive those commits first

# 3. Mixed reset: refs catch up to origin, worktree content is untouched
git reset -q origin/<default-branch>

# 4. Exec bits come from git as ground truth (not the other way around)
git ls-files -s | awk '$1==100755 {print $4}' | xargs -r chmod +x

# 5. If a local commit was built on the rewound base (tree correct, parent stale):
NEW=$(git commit-tree HEAD^{tree} -p origin/<branch> -m "<orig message>")
git reset -q "$NEW"   # identical tree grafted onto the true tip; safe push
```

## Incident class B — secret exposure (PAT leaked in a transcript)

1. Rotate at GitHub → fine-grained PAT, same minimal scopes.
2. Write to `~/.config/shesh/github.pat`, `chmod 600`.
3. `tools/dr_check.sh` must pass.
4. gitleaks history scan of every repo (the gate proves no new leaks; the
   one-off scan proves the leak never touched git).
5. Close the tracking issue with the rotation commit reference.

## Incident class C — a component goes red after a rolling update

1. `docs/policies/DEPENDENCY_POLICY.md` downgrade-one protocol: revert the
   single offending version move, verify green, then re-approach.
2. If the failure is fundamental (upstream removed behavior we depend on):
   replace the dependency per the policy's replacement rule — do not pin
   forever and do not fork impulsively.
3. Post-mortem into docs/history/incidents/ with the exact failing gate output.

## Incident class D — audit ledger verification fails

1. `python -m shesh_audit.tool_pins` is NOT the tool here: the ledger lives in
   `shesh_audit`'s log; run its `verify()` against the day's file.
2. A broken chain means events were dropped or reordered after the break —
   the break point IS the forensic boundary. Record it; do not splice.

## tools/dr_check.sh

`tools/dr_check.sh` asserts the recovery prerequisites: remotes present, PAT
perms 600, askpass executable, push protection enabled (spot repo),
archive dir present, audit verify passing. Run after any incident class.
