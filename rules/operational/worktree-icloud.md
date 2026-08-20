# Worktrees outside ~/Documents (iCloud sync breaks git)

IMPORTANT: Create `git worktree add` **outside `~/Documents/`** (e.g. `~/code/`, `~/dev/`, `/tmp/`).
`~/Documents` is synced by iCloud Drive ("Desktop & Documents Folders") — it breaks git operations.

**Symptoms:**
- `git mv` of a directory inside the synced folder → iCloud makes a conflict copy with a ` 2` suffix. Working tree desyncs from the index (`RD` in `git status`), although **the index is intact** (`git cat-file -e :path` = 0).
- Turning off "Documents" sync in System Settings → **kills active Claude sessions** whose worktree is also under `~/Documents`. So sync can't simply be toggled off temporarily.

**If already stuck (` 2` appeared):**
1. Don't fight the daemon in a loop (3-strike). Verify the index: `git cat-file -e :<path>`.
2. The ` 2` copy = your content. Restore the name: `mv "dir 2" dir` (first `diff` against `git cat-file -p :<path>` — IDENTICAL = safe).
3. **Commit immediately** while the tree is clean — the index is correct, so the commit locks the right state into history even if sync makes ` 2` again. Push for triple insurance.
4. `git add` only with explicit paths (not `.`) — otherwise a ` 2` stray gets into the commit.

Кейс (standards-improvement 2026-06-11): `~/.claude/memory/incidents/2026-06-11-worktree-icloud.md`
