# Merge queue: checkpoints and verify-merge

When merging a queue of PRs sequentially (audit-followup, stacked PRs, multi-packet landing):

## Full pytest at checkpoints
Run the full `pytest -q` after gate-changing PRs, not just each PR's targeted set. A PR's targeted tests don't catch **integration regressions** — behavior that only surfaces when branches combine.

**Why:** merging nikita-video-engine 2026-06-04, after #129 the full pytest produced 2 failures in `test_plan_quality.py` that ALL targeted sets of #125/#128/#129 missed: PR1's owner gate (`NVP_ALLOW_REAL_RENDER`) started preceding the quality gate, and tests called `run_real_proof` without the env → `status="blocked"` instead of the expected. Classic integration misses: gate ordering, env flags, a shared function changed by two packets.

**How:** full pytest at minimum after every PR that changes a gate / stage order / shared module. Fixing an integration regression = a test-only update for the intended (stricter) behavior, not weakening the gate.

## Verify-merge before landing a conflicting PR
Before landing a PR that touches a file already changed by a merged PR — **even if GitHub shows MERGEABLE CLEAN** — do a local verify-merge in a throwaway branch: `git merge --no-commit`, then `grep` for key markers of BOTH changes in the shared file + combined targeted tests. Only then land.

**Why:** `CLEAN` = git auto-merged non-overlapping regions textually, ≠ semantically correct. On #127 (PR5) release_gate.py and production_pipeline.py had region-disjoint edits from PR2/PR1/PR5 — auto-merge passed, but I grep-verified that BOTH gates survived (PR2 truth-parity markers + PR5 license markers) + ran 81 combined tests before landing.

## Stacked PRs
Stacked PR (base = another feature branch) → before merging, retarget the base to main (`gh pr edit N --base main`) AFTER the base branch is merged. No squash + no `--delete-branch` until the stack is resolved (squash+delete breaks the stack — see incident_stacked_pr_squash_delete_branch).
