# Merge queue: checkpoints and verify-merge

Merging a queue of PRs sequentially (audit-followup, stacked PRs, multi-packet landing):

**Full pytest at checkpoints.** Run the full `pytest -q` after gate-changing PRs, not just each PR's targeted set — targeted tests don't catch **integration regressions** (gate ordering, env flags, a shared function changed by two packets). Minimum: full pytest after every PR that changes a gate / stage order / shared module. Fixing an integration regression = a test-only update for the intended (stricter) behavior, not weakening the gate.

**Verify-merge before landing a conflicting PR.** Before landing a PR touching a file already changed by a merged PR — **even if GitHub shows MERGEABLE CLEAN** — do a local verify-merge in a throwaway branch: `git merge --no-commit`, then `grep` for key markers of BOTH changes in the shared file + combined targeted tests. `CLEAN` = git auto-merged non-overlapping regions textually, ≠ semantically correct.

**Stacked PRs.** Retarget the base to main (`gh pr edit N --base main`) AFTER the base branch is merged. No squash + no `--delete-branch` until the stack is resolved (see `incident_stacked_pr_squash_delete_branch`).

Case (nikita-video-engine 2026-06-04, #125/#128/#129 owner-gate ordering): `~/.claude/memory/incidents/2026-06-04-merge-queue-checkpoints.md`
