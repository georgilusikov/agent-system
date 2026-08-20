Parallel fix implementation: split by files so no file is touched by two agents.
SSH operations on a remote host and local code edits — always parallelize, they are independent.
Auditing a large codebase: 5+ agents with non-overlapping roles. Phase 1 = bugs, Phase 2 = improvements.

Multi-agent context OR goal='fresh main' + dirty/shared checkout → FIRST `git worktree add <path> -b <branch> <clean-base>`, THEN the first edit. One packet = one worktree = one branch = one agent. Before dispatch check active peers (claude-peers `list_peers`/`set_summary`).

IMPORTANT: Worktree created → every Edit/Write by absolute path MUST point into the worktree (`.../wt-<name>/...`), not the main checkout. The Edit tool is NOT bound to cwd. Symptom: verification in the worktree doesn't see your edits; `git status` shows the diff in the main tree. Prevention: on the first Edit of a worktree task verify via `wc -l`/unique marker that it landed in the worktree path. Recovery: `cp main/<file> wt/<file>` → `git checkout -- <file>` in main → continue in the worktree.

IMPORTANT: In a worktree NEVER `git add -A` / `git add .` — explicit paths only (`git add src/foo.py tests/test_foo.py`). A symlink/venv slips past the dir form of `.gitignore` (`.venv311/` ignores the DIRECTORY but NOT a same-named symlink file); a later `git merge --ff-only` then overwrites the real venv with the symlink and DELETES it. Prevention: explicit paths on add + both forms in `.gitignore` (`.venv311` AND `.venv311/`). Recovery: `git rm --cached` the symlink, rebuild the venv.

HEAD-pin guard: before any writing git operation verify `git symbolic-ref HEAD` matches the expected branch — a neighboring session may have switched HEAD in the shared .git.
Catastrophe-guard before push: deleted files == 0, deleted lines < 500, staged == changed — otherwise STOP.
Judge branch closure by files, not commits: N_files > N_commits×10 → STOP.

Case archive (nikita-video-engine 2026-06-04 5-agent collision, 2026-06-12 wrong-tree edit, 2026-06-13 venv deletion): `~/.claude/memory/incidents/2026-06-04-parallel-agents-collisions.md`
