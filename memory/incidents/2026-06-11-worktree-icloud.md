# Worktrees outside ~/Documents (iCloud sync breaks git)

IMPORTANT: Create `git worktree add` **outside `~/Documents/`** (e.g. `~/code/`, `~/dev/`, `/tmp/`).
`~/Documents` is synced by iCloud Drive ("Desktop & Documents Folders") — it breaks git operations.

**Symptoms:**
- `git mv` of a directory inside the synced folder → iCloud makes a conflict copy with a ` 2` suffix (`krasinsky_unit_economics 2/`). Working tree desyncs from the index (`RD` in `git status`: staged rename + working-tree delete), although **the index is intact** (`git cat-file -e :path` = 0).
- Turning off "Documents" sync in System Settings → **kills active Claude sessions** whose worktree is also under `~/Documents` (`Working directory no longer exists`). So sync can't simply be toggled off temporarily.

**If already stuck (worktree in ~/Documents, ` 2` appeared):**
1. Don't fight the daemon in a loop (3-strike). Verify the index is intact: `git cat-file -e :<path>`.
2. The ` 2` copy = your content, sync renamed it. Restore the name: `mv "dir 2" dir` (first `diff` SKILL/file against `git cat-file -p :<path>` — IDENTICAL = safe).
3. **Commit immediately** while the tree is clean — the index is correct, `git commit` locks the right state into history even if sync makes ` 2` again. Push for triple insurance.
4. `git add` only with explicit paths (not `.`) — otherwise a ` 2` stray gets into the commit.

**Why:** standards-improvement session 2026-06-11 — worktree `~/Documents/курсор-standards-improvement`, iCloud renamed the moved krasinsky directory to ` 2` mid-task; disabling Documents sync crashed the session. Saved by the index holding the staged rename → the commit from the index came out clean.
