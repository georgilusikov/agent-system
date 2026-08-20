#!/usr/bin/env python3
r"""git_worktree_completeness_gate — Claude Code PreToolUse Bash hook.

THE UPSTREAM «trusted working tree» INVARIANT.

Closes the catastrophe class: a worktree created with `--no-checkout` / sparse /
partial checkout leaves the working directory MISSING most of the base tree,
while HEAD still points at the full tree. A subsequent blanket stage
(`git add -A`, `git commit -a`) then records every absent file as an intentional
DELETION, producing a commit that wipes thousands of files.

This hook enforces ONE invariant at TWO source touchpoints:

  Family 1 — worktree creation that breaks completeness:
    `git worktree add ... --no-checkout` (or `--sparse` / `--orphan`)
    → gate unless WORKTREE_COMPLETENESS_ACK (≥12 chars, real reason).

  Family 2 — blanket stage/commit of mass phantom deletions:
    `git add -A|--all|.|-u` / `git commit -a|-am|--all` / `git commit`
    → compute the deletions this op would stage/commit; gate if deletions
      ≥ WORKTREE_DELETION_ABSOLUTE (default 100) OR ≥ WORKTREE_DELETION_FRACTION
      (default 0.25) of base tree with ≥ WORKTREE_DELETION_FRACTION_FLOOR files.

Phase 1 WARN by default: violations print a warning to stderr and exit 0.
Set WORKTREE_COMPLETENESS_ENFORCE=1 to actually BLOCK (exit 2).
Override (both families): WORKTREE_COMPLETENESS_ACK="<reason ≥12 chars>".

Universal: no client hardcodes, no project paths. Works in any git repo.
Fail-open: any internal error → exit 0. A gate must never break the owner's
git over its own bug.

Exit codes:
  0 = pass (rule N/A, invariant holds, ACK present, or Phase 1 WARN)
  2 = BLOCK (ENFORCE=1, invariant violated, no ACK) — verdict to stderr
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

DELETION_ABSOLUTE = int(os.environ.get("WORKTREE_DELETION_ABSOLUTE", "100"))
DELETION_FRACTION = float(os.environ.get("WORKTREE_DELETION_FRACTION", "0.25"))
DELETION_FRACTION_FLOOR = int(os.environ.get("WORKTREE_DELETION_FRACTION_FLOOR", "10"))
ACK_ENV = "WORKTREE_COMPLETENESS_ACK"
ENFORCE_ENV = "WORKTREE_COMPLETENESS_ENFORCE"
ACK_MIN_CHARS = 12

# A real reason: ≥12 chars, has a 3+ letter word, and a separator.
ACK_VALID = re.compile(r"^(?=.{12,})(?=.*[A-Za-z]{3,}).+[\s\-_:]+.+$")

# Family 1: worktree creation with a completeness-breaking flag.
WORKTREE_INCOMPLETE = re.compile(r"\bgit\b[^\n]*\bworktree\s+add\b[^\n]*" r"(?:--no-checkout|--sparse|--orphan)\b")

# Family 2: blanket staging / committing ops. The flag may be quoted
# (`git add '-A'`), combined (`-Av`), `-u`/`--update`, the `stage` alias, or
# separated from `add` by other flags. Matched anywhere within one command
# (no crossing `&&`/`;`/`|`); quoted flag tokens are normalised before match.
BLANKET_ADD = re.compile(
    r"\bgit\b(?:\s+-[Cc]\s+\S+)*\s+(?:add|stage)\b"
    r"(?:\s+[^\s&;|]+)*?"
    r"\s(?:-\w*[Au]\w*|--all|--update|\.)(?:\s|$|&|;|\|)"
)
COMMIT_ALL = re.compile(r"\bgit\b(?:\s+-[Cc]\s+\S+)*\s+commit\b[^\n]*" r"(?:\s-\w*a\w*|\s--all)\b")
COMMIT_ANY = re.compile(r"\bgit\b(?:\s+-[Cc]\s+\S+)*\s+commit\b")

# --- text-emit / quoting guards ---
TEXT_EMIT_PREFIXES = re.compile(r"^\s*(?:echo\b|printf\b|cat\s+(?:>>?|<<<?|<)|#|//|export\s+[A-Z_]+=)")
QUOTED_SPAN = re.compile(r"""(?:'[^']*'|"[^"]*"|`[^`]*`)""")
# A quoted token that is EXACTLY a flag (`'-A'`, `"--all"`, `'.'`) is
# shell-equivalent to the bare flag — un-quote it so flag detection isn't
# defeated by quoting. Message strings (`-m "git add -A"`) stay quoted.
QUOTED_FLAG = re.compile(r"""(['"])(-{1,2}[A-Za-z][A-Za-z-]*|\.)\1""")
HEREDOC_START = re.compile(r"<<-?\s*[\"']?(?P<delim>[A-Za-z_][A-Za-z0-9_]*)[\"']?")
CD_PREFIX = re.compile(r"^\s*cd\s+(?P<dir>'[^']*'|\"[^\"]*\"|[^\s;&|]+)\s*(?:&&|;)")
GIT_C_FLAG = re.compile(r"\bgit\s+(?:-c\s+\S+\s+)*-C\s+(?P<dir>'[^']*'|\"[^\"]*\"|[^\s;&|]+)")


def _enforce() -> bool:
    return os.environ.get(ENFORCE_ENV, "").strip() == "1"


def _verdict(message: str) -> int:
    """Emit the verdict. Phase 1 (default): WARN to stderr, exit 0.
    ENFORCE=1: BLOCK, exit 2."""
    if _enforce():
        sys.stderr.write("\n[worktree-completeness] BLOCK — " + message)
        return 2
    sys.stderr.write("\n[worktree-completeness] WARN (Phase 1, not blocking) — " + message)
    sys.stderr.write(f"\nPhase 1 WARN mode: set {ENFORCE_ENV}=1 to make this a hard block.\n")
    return 0


def _strip_text(command: str) -> str:
    """Normalise quoted flags, then remove heredoc bodies + quoted spans so git
    tokens inside DATA don't trigger while quoted FLAGS still do."""
    cleaned = QUOTED_FLAG.sub(lambda m: m.group(2), command)
    hd = HEREDOC_START.search(cleaned)
    if hd:
        delim = hd.group("delim")
        end = re.compile(rf"^\s*{re.escape(delim)}\s*$", re.MULTILINE).search(cleaned, hd.end())
        cleaned = cleaned[: hd.start()] + (cleaned[end.end() :] if end else "")
    return QUOTED_SPAN.sub(" ", cleaned)


def _is_text_emit(command: str) -> bool:
    return bool(TEXT_EMIT_PREFIXES.match(command))


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] in "'\"" and s[-1] == s[0]:
        return s[1:-1]
    return s


def _git_cwd(command: str, residue: str) -> Path | None:
    """Resolve the directory the git op actually runs in: `cd X &&` or `git -C X`."""
    m = GIT_C_FLAG.search(residue)
    if m:
        p = Path(_unquote(m.group("dir")))
        return p if p.is_absolute() else (Path.cwd() / p)
    m = CD_PREFIX.match(command)
    if m:
        p = Path(_unquote(m.group("dir")))
        return p if p.is_absolute() else (Path.cwd() / p)
    return Path.cwd()


def _run(args: list[str], cwd: Path) -> str:
    try:
        r = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True, timeout=30, check=False)
        return r.stdout if r.returncode == 0 else ""
    except (subprocess.TimeoutExpired, OSError):
        return ""


def _count(out: str) -> int:
    return len([ln for ln in out.splitlines() if ln.strip()])


def _ack_ok() -> bool:
    reason = os.environ.get(ACK_ENV, "").strip()
    return bool(reason) and bool(ACK_VALID.match(reason))


def _creation_message(command: str) -> str:
    return (
        "`git worktree add` with an incomplete-checkout flag "
        "(--no-checkout/--sparse/--orphan).\n\n"
        f"  command: {command[:200]}{'...' if len(command) > 200 else ''}\n\n"
        "Why gated: a partial checkout leaves the working tree MISSING base\n"
        "files. A later `git add -A` / `git commit -a` then records them as\n"
        "DELETIONS — a commit that wipes thousands of files.\n\n"
        "Use the safe full-checkout pattern instead:\n"
        "  git worktree add <path> -b <branch>\n"
        "  # then verify completeness before any commit:\n"
        '  test "$(git -C <wt> ls-files | wc -l)" -ge "$(($(git ls-tree -r --name-only HEAD | wc -l)*95/100))"\n\n'
        f"If a partial checkout is INTENTIONAL (≥{ACK_MIN_CHARS} chars, real reason):\n"
        f'  export {ACK_ENV}="reason: deliberate sparse checkout of <subtree>"\n'
    )


def _deletions_message(command: str, n_del: int, base: int, frac: float, what: str) -> str:
    return (
        f"{what} would record {n_del} file "
        f"DELETIONS ({frac:.0%} of the {base}-file base tree).\n\n"
        f"  command: {command[:200]}{'...' if len(command) > 200 else ''}\n\n"
        "Why gated: deleting this large a fraction of the repo in one blanket\n"
        "op is the signature of a broken/partial worktree checkout being staged.\n"
        "A faithful 1-file edit stages 0 deletions.\n\n"
        "Required — pick ONE:\n"
        "  1. Verify your worktree is a COMPLETE checkout of its base:\n"
        "     git ls-files | wc -l        # vs:\n"
        "     git ls-tree -r --name-only HEAD | wc -l   # should be ~equal\n"
        "     If far fewer → recreate the worktree WITHOUT --no-checkout/--sparse.\n"
        "  2. Stage explicit paths instead of a blanket add:\n"
        "     git add <path-1> <path-2> ...   # never `git add -A` on a broken tree\n"
        f"  3. If this mass deletion is INTENTIONAL (≥{ACK_MIN_CHARS} chars, real reason):\n"
        f'     export {ACK_ENV}="reason: removing vendored <dir>, superseded by ..."\n\n'
        f"Thresholds: WORKTREE_DELETION_ABSOLUTE={DELETION_ABSOLUTE}, "
        f"WORKTREE_DELETION_FRACTION={DELETION_FRACTION} "
        f"(floor {DELETION_FRACTION_FLOOR}).\n"
    )


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except (json.JSONDecodeError, ValueError):
        return 0

    if (payload.get("tool_name") or payload.get("toolName") or "") != "Bash":
        return 0
    command = (payload.get("tool_input") or payload.get("toolInput") or {}).get("command", "") or ""
    if not command.strip() or _is_text_emit(command):
        return 0

    residue = _strip_text(command)

    # --- Family 1: incomplete worktree creation ---
    if WORKTREE_INCOMPLETE.search(residue):
        if _ack_ok():
            sys.stderr.write("[worktree-completeness] ACK present — partial checkout allowed.\n")
            return 0
        return _verdict(_creation_message(command))

    # --- Family 2: blanket stage / commit of mass deletions ---
    is_add = bool(BLANKET_ADD.search(residue))
    is_commit_all = bool(COMMIT_ALL.search(residue))
    is_commit = bool(COMMIT_ANY.search(residue))
    if not (is_add or is_commit_all or is_commit):
        return 0

    cwd = _git_cwd(command, residue)
    if cwd is None or not cwd.exists():
        return 0
    if not _run(["git", "rev-parse", "--is-inside-work-tree"], cwd).strip() == "true":
        return 0

    base = _count(_run(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd))
    if base <= 0:
        return 0  # empty repo / no HEAD — nothing to protect

    staged_del = _count(_run(["git", "diff", "--cached", "--name-only", "--diff-filter=D"], cwd))
    unstaged_del = _count(_run(["git", "diff", "--name-only", "--diff-filter=D"], cwd))

    if is_add or is_commit_all:
        n_del = staged_del + unstaged_del
        what = "this blanket `git add`/`git commit -a`"
    else:  # plain `git commit` — only what is already staged gets committed
        n_del = staged_del
        what = "this `git commit` (already-staged deletions)"

    frac = n_del / base
    absolute_hit = n_del >= DELETION_ABSOLUTE
    fractional_hit = frac >= DELETION_FRACTION and n_del >= DELETION_FRACTION_FLOOR
    if not (absolute_hit or fractional_hit):
        return 0

    if _ack_ok():
        sys.stderr.write(
            f"[worktree-completeness] ACK present — {n_del} deletions ({frac:.0%} of base) allowed intentionally.\n"
        )
        return 0
    return _verdict(_deletions_message(command, n_del, base, frac, what))


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # pragma: no cover — fail open
        sys.stderr.write(f"[worktree-completeness] internal error (fail-open): {exc}\n")
        sys.exit(0)
