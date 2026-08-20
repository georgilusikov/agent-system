#!/usr/bin/env python3
"""worktree_isolation_gate — Claude Code PreToolUse Bash hook.

Main checkout of a workspace is READ-ONLY for agents when parallel sessions
are active. Gates branch-switching / history-rewriting / tree-destroying git
ops executed from the SHARED workspace root while >1 Claude session is active,
because that destroys another agent's uncommitted work.

Allowed in shared root: read-only git + incremental `git add <path> && commit`.
Required instead: work inside `git worktree` / isolated `git clone --local`.

Parallel-session detection: Claude Code keeps per-session dirs under
/private/tmp/claude-<uid>/<workspace-slug>/<session-uuid>/, where the slug is
the workspace path with every non-alphanumeric char replaced by `-`. Sessions
whose dir mtime is within the last 10 minutes count as active. Override the
base dir for tests via CLAUDE_SESSIONS_ROOT.

Phase 1 WARN by default: violations print a warning to stderr and exit 0.
Set WORKTREE_ISOLATION_ENFORCE=1 to actually BLOCK (exit 2).
Override: env WORKTREE_ISOLATION_ACK (≥12 chars) OR sentinel
<workspace>/.claude/.destructive_ack with a fresh (≤10 min) line
`WORKTREE_ISOLATION_ACK: <reason ≥12 chars> @ <iso>`.

Fail-open: any internal error → exit 0.

Exit codes: 0 = pass / WARN; 2 = BLOCK (ENFORCE=1).
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

ENFORCE_ENV = "WORKTREE_ISOLATION_ENFORCE"
ACK_ENV = "WORKTREE_ISOLATION_ACK"
ACK_MIN_CHARS = 12


def _repo_root() -> Path:
    """Nearest git root above cwd (the workspace this Bash command runs in)."""
    cwd = Path.cwd().resolve()
    for candidate in [cwd, *cwd.parents]:
        if (candidate / ".git").exists():
            return candidate
    return cwd


WORKSPACE = _repo_root()
SENTINEL = WORKSPACE / ".claude" / ".destructive_ack"

# git ops that mutate branch/HEAD/tree (unsafe in shared root under parallel work)
RISKY = re.compile(
    r"\bgit\s+(?:-C\s+\S+\s+|--git-dir\S*\s+|-c\s+\S+\s+)*"
    r"(?:checkout\s+(?!-b\b)(?!-{0,2}\s*$)\S|switch\s+(?!-c\b)\S|"
    r"reset\s+--hard|clean\s+-\w*[fdx]|rebase\b|merge\s+(?!--abort)\S|"
    r"branch\s+-\w*D|stash\s+(?:pop|drop|clear))"
)
# `git stash push -u` WITHOUT a pathspec (bare global) also wipes shared state
BARE_STASH_U = re.compile(r"\bgit\s+stash\s+push\b[^\n]*\s-\w*u\w*\b(?![^\n]*\s--\s)")
SAFE_READONLY = re.compile(
    r"\bgit\s+(?:status|log|diff|show|cat-file|ls-tree|ls-files|"
    r"rev-parse|rev-list|fetch|branch\s*$|branch\s+-(?:-list|v|a|r)|"
    r"for-each-ref|worktree\s+(?:list|add)|tag\s+(?:-l|--list)|remote|config\s+--get)"
)


def _enforce() -> bool:
    return os.environ.get(ENFORCE_ENV, "").strip() == "1"


def _in_shared_root(cmd: str) -> bool:
    """True if the op targets the shared workspace root (not a worktree / /tmp clone)."""
    if "/tmp/" in cmd or ".claude/worktrees/" in cmd or "git clone" in cmd:
        return False
    try:
        cwd = os.getcwd()
    except OSError:
        return True
    if ".claude/worktrees/" in cwd or cwd.startswith("/tmp/") or cwd.startswith("/private/tmp/"):
        return False
    return cwd == str(WORKSPACE)


def _workspace_slug() -> str:
    """Claude Code session-dir slug: workspace path, non-alphanumerics → `-`."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(WORKSPACE))


def _sessions_root() -> Path:
    override = os.environ.get("CLAUDE_SESSIONS_ROOT", "").strip()
    if override:
        return Path(override)
    return Path(f"/private/tmp/claude-{os.getuid()}")


def _parallel_sessions() -> int:
    """Count active Claude sessions for this workspace (mtime within 10 min).

    Matches both the workspace slug itself and its worktree slugs
    (<slug>--claude-worktrees-...), because worktree sessions still share the
    same physical main checkout.
    """
    try:
        slug = _workspace_slug()
        cutoff = time.time() - 600
        n = 0
        root = _sessions_root()
        if not root.is_dir():
            return 0
        for parent in root.glob(f"{slug}*"):
            if not parent.is_dir():
                continue
            for d in parent.iterdir():
                try:
                    if d.is_dir() and d.stat().st_mtime > cutoff:
                        n += 1
                except OSError:
                    continue
        return n
    except OSError:
        return 0


def _ack_ok() -> bool:
    if len(os.environ.get(ACK_ENV, "").strip()) >= ACK_MIN_CHARS:
        return True
    try:
        if not SENTINEL.exists() or time.time() - SENTINEL.stat().st_mtime > 600:
            return False
        for line in SENTINEL.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("WORKTREE_ISOLATION_ACK:"):
                reason = line.split(":", 1)[1].split("@")[0].strip()
                if len(reason) >= ACK_MIN_CHARS:
                    return True
    except OSError:
        return False
    return False


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)
    cmd = (payload.get("tool_input", {}) or {}).get("command", "")
    if not cmd.strip():
        sys.exit(0)
    is_risky = bool(RISKY.search(cmd) or BARE_STASH_U.search(cmd))
    if not is_risky:
        sys.exit(0)
    if SAFE_READONLY.search(cmd) and not (RISKY.search(cmd) or BARE_STASH_U.search(cmd)):
        sys.exit(0)
    if not _in_shared_root(cmd):
        sys.exit(0)  # already isolated (worktree / /tmp clone)
    n_sessions = _parallel_sessions()
    if n_sessions <= 1:
        sys.exit(0)  # single session — shared root acceptable
    if _ack_ok():
        print("worktree-isolation: ACK accepted — override applied", file=sys.stderr)
        sys.exit(0)
    enforce = _enforce()
    verdict = "BLOCK" if enforce else "WARN (Phase 1, not blocking)"
    bar = "=" * 72
    print(bar, file=sys.stderr)
    print(f"WORKTREE-ISOLATION {verdict}", file=sys.stderr)
    print("Branch-switch / history-rewrite / tree-destroy git op in SHARED ROOT", file=sys.stderr)
    print(f"while {n_sessions} parallel Claude sessions are active.", file=sys.stderr)
    print("This class of op destroys other sessions' uncommitted work.", file=sys.stderr)
    print(bar, file=sys.stderr)
    print("REQUIRED: work in an isolated copy, not the shared root:", file=sys.stderr)
    print("  git worktree add .claude/worktrees/<task> -b <branch>   # then cd there", file=sys.stderr)
    print("  OR  git clone --local --no-hardlinks . /tmp/<wt>        # PR from there", file=sys.stderr)
    print("Override (only if you verified no parallel uncommitted work):", file=sys.stderr)
    print(f'  export {ACK_ENV}="<reason ≥{ACK_MIN_CHARS} chars>"', file=sys.stderr)
    if not enforce:
        print(f"Phase 1 WARN mode: set {ENFORCE_ENV}=1 to make this a hard block.", file=sys.stderr)
    print(bar, file=sys.stderr)
    sys.exit(2 if enforce else 0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover — fail open
        print(f"[worktree-isolation] internal error (fail-open): {exc}", file=sys.stderr)
        sys.exit(0)
