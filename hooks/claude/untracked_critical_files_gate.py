#!/usr/bin/env python3
r"""untracked_critical_files_gate — Claude Code PreToolUse Bash hook.

Closes the «uncommitted code lost on branch switch» class: hours of work in
untracked files destroyed by a single `git checkout <branch>` / `git reset
--hard` / rebase, because incremental-commit discipline was declarative, not
mechanical.

Behavior (PreToolUse event for Bash):
- Reads stdin JSON payload from Claude Code PreToolUse event.
- Extracts tool_name = "Bash" + tool_input.command.
- If command matches a risky branch-switching pattern — scans the repo for
  untracked .py/.md files >100 LOC in critical dirs (src/, scripts/, tests/,
  repo root), mtime older than N minutes (default 120 = 2h).
- If such files ≥1 — gate: the message tells the agent to `git add` +
  `git commit` BEFORE the branch switch.

Risky git patterns (branch-switching = working tree replaced):
- `git checkout <branch>` (not `git checkout <file>` — anchored by context)
- `git switch <branch>` and `git switch -c`
- `git rebase` / `git pull --rebase`
- `git worktree add` (carries dirty state to new worktree)
- `git reset --hard`

Phase 1 WARN by default: violations print a warning to stderr and exit 0.
Set UNTRACKED_CRITICAL_ENFORCE=1 to actually BLOCK (exit 2).
Override: UNTRACKED_CRITICAL_ACK=<reason> (12+ chars with letters + separator).

Universal — no client hardcodes; works in any git repo. Thresholds via env:
- UNTRACKED_CRITICAL_MIN_LOC (default 100)
- UNTRACKED_CRITICAL_MIN_AGE_MIN (default 120 = 2h)

Fail-open: any internal error → exit 0.

Exit codes:
  0 = pass (no critical untracked files, rule N/A, ACK, or Phase 1 WARN)
  2 = block (ENFORCE=1 and ≥1 critical untracked file) — message to stderr
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

MIN_LOC = int(os.environ.get("UNTRACKED_CRITICAL_MIN_LOC", "100"))
MIN_AGE_MINUTES = int(os.environ.get("UNTRACKED_CRITICAL_MIN_AGE_MIN", "120"))
OVERRIDE_ENV_VAR = "UNTRACKED_CRITICAL_ACK"
ENFORCE_ENV = "UNTRACKED_CRITICAL_ENFORCE"

RISKY_GIT_PATTERNS = [
    # Branch switch (named branch arg, not file arg)
    re.compile(r"\bgit\s+checkout\s+(?!--|\.|-b\b)[A-Za-z0-9_/-]+"),
    re.compile(r"\bgit\s+switch\s+(?!-c\b)[A-Za-z0-9_/-]+"),
    re.compile(r"\bgit\s+switch\s+-c\b"),
    # Rebase replaces commits/working tree
    re.compile(r"\bgit\s+rebase\b"),
    re.compile(r"\bgit\s+pull\s+(?:[^|;&]*\s+)?--rebase\b"),
    # Worktree add carries dirty state
    re.compile(r"\bgit\s+worktree\s+add\b"),
    # Reset --hard destroys uncommitted work
    re.compile(r"\bgit\s+reset\s+--hard\b"),
]

TEXT_EMIT_PREFIXES = re.compile(r"^\s*(?:echo\b|printf\b|cat\s+(?:>>?|<<<?|<)|#|//|export\s+[A-Z_]+=)")
QUOTED_SPAN = re.compile(r"""(?:'[^']*'|"[^"]*"|`[^`]*`)""")
HEREDOC_START = re.compile(r"<<-?\s*[\"']?(?P<delim>[A-Za-z_][A-Za-z0-9_]*)[\"']?")

# Critical dir patterns — universal for any repo, matched against the
# repo-relative path of the untracked file: src/, scripts/, tests/ (any depth)
# and the repo root (top-level .py/.md files).
CRITICAL_DIR_PATTERNS = [
    re.compile(r"^src/.+\.(py|md)$"),
    re.compile(r"^scripts/.+\.(py|md)$"),
    re.compile(r"^tests?/.+\.(py|md)$"),
    re.compile(r"^[^/]+\.(py|md)$"),
]

OVERRIDE_VALID = re.compile(r"^(?=.{12,})(?=.*[A-Za-z]{3,}).+[\s\-_:]+.+$")


def _enforce() -> bool:
    return os.environ.get(ENFORCE_ENV, "").strip() == "1"


def is_text_emit(command: str) -> bool:
    return bool(TEXT_EMIT_PREFIXES.match(command))


def has_risky_git_op_outside_quotes(command: str) -> bool:
    """Strip quoted spans and heredoc bodies; check if any RISKY pattern matches."""
    cleaned = command
    heredoc_match = HEREDOC_START.search(cleaned)
    if heredoc_match:
        delim = heredoc_match.group("delim")
        end_pat = re.compile(rf"^\s*{re.escape(delim)}\s*$", re.MULTILINE)
        end_match = end_pat.search(cleaned, heredoc_match.end())
        if end_match:
            cleaned = cleaned[: heredoc_match.start()] + cleaned[end_match.end() :]
        else:
            cleaned = cleaned[: heredoc_match.start()]
    cleaned = QUOTED_SPAN.sub(" ", cleaned)
    return any(pat.search(cleaned) for pat in RISKY_GIT_PATTERNS)


def find_repo_root(start: Path | None = None) -> Path | None:
    cwd = (start or Path.cwd()).resolve()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def list_untracked(repo_root: Path) -> list[str]:
    """Return list of untracked repo-relative paths."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        if result.returncode != 0:
            return []
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        return []


def is_critical(rel_path: str) -> bool:
    return any(pat.match(rel_path) for pat in CRITICAL_DIR_PATTERNS)


def file_meets_thresholds(abs_path: Path, min_loc: int, min_age_min: int) -> bool:
    """Return True if file ≥ min_loc lines AND mtime older than min_age_min."""
    try:
        if not abs_path.is_file():
            return False
        stat = abs_path.stat()
        age_min = (time.time() - stat.st_mtime) / 60.0
        if age_min < min_age_min:
            return False
        with abs_path.open("rb") as f:
            loc = sum(1 for _ in f)
        return loc >= min_loc
    except Exception:
        return False


def find_critical_untracked(repo_root: Path) -> list[tuple[str, int, float]]:
    """Return list of (rel_path, loc, age_minutes) for critical untracked files
    that meet both thresholds."""
    out: list[tuple[str, int, float]] = []
    for rel in list_untracked(repo_root):
        abs_path = repo_root / rel
        if not abs_path.is_file():
            continue
        if not is_critical(rel):
            continue
        if not file_meets_thresholds(abs_path, MIN_LOC, MIN_AGE_MINUTES):
            continue
        try:
            stat = abs_path.stat()
            with abs_path.open("rb") as f:
                loc = sum(1 for _ in f)
            age_min = (time.time() - stat.st_mtime) / 60.0
            out.append((rel, loc, age_min))
        except Exception:
            continue
    return out


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    tool_name = payload.get("tool_name", "")
    if tool_name != "Bash":
        return 0
    command = (payload.get("tool_input") or {}).get("command", "") or ""
    if not command.strip() or is_text_emit(command):
        return 0
    if not has_risky_git_op_outside_quotes(command):
        return 0

    # Check override
    override = os.environ.get(OVERRIDE_ENV_VAR, "").strip()
    if override and OVERRIDE_VALID.match(override):
        print(
            f"[untracked-critical-files-gate] OVERRIDE acked: {override} — bypassing",
            file=sys.stderr,
        )
        return 0

    repo_root = find_repo_root()
    if repo_root is None:
        return 0

    critical = find_critical_untracked(repo_root)
    if not critical:
        return 0

    enforce = _enforce()
    verdict = "BLOCK" if enforce else "WARN (Phase 1, not blocking)"
    lines = [
        f"untracked-critical-files-gate: {verdict} — untracked critical .py/.md "
        f"files > {MIN_LOC} LOC older than {MIN_AGE_MINUTES} min in critical dirs:",
        "",
    ]
    for rel, loc, age_min in sorted(critical, key=lambda x: -x[1]):
        lines.append(f"  · {rel} ({loc} LOC, age {age_min:.0f} min)")
    lines += [
        "",
        "Branch switch / rebase / reset --hard поверх этих файлов = потеря работы.",
        "",
        "Recovery: выполни `git add` + `git commit` для перечисленных файлов ДО risky операции,",
        f"ИЛИ установи `{OVERRIDE_ENV_VAR}=<reason>` (12+ chars с letters + separator),",
        "если carry-over намеренный (например stash без сохранения).",
    ]
    if not enforce:
        lines.append(f"Phase 1 WARN mode: set {ENFORCE_ENV}=1 to make this a hard block.")
    print("\n".join(lines), file=sys.stderr)
    return 2 if enforce else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # pragma: no cover — fail open
        print(f"[untracked-critical-files-gate] internal error (fail-open): {exc}", file=sys.stderr)
        sys.exit(0)
