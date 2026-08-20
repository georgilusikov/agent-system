#!/usr/bin/env python3
"""precompact_handoff — PreCompact hook: snapshot session state before compaction.

Closes the «context compacted, nobody ran /handoff» class: autocompaction fires
without warning, the branch/sha/dirty-file state of the session is gone, and the
next session reconstructs it by guessing.

Behavior (PreCompact event):
- Reads stdin JSON payload from Claude Code (`cwd`, `trigger`,
  `transcript_path`).
- Only acts inside a git repo — never litters unrelated directories.
- Appends a NEW file `.claude/handoffs/HANDOFF_autocompact_<date>_seq<N>.md`
  holding the deterministic snapshot (branch, short sha, dirty files, last
  commits, transcript path) plus empty placeholders that /handoff fills in.
- Never overwrites an existing file: seq is the next free number.

This hook is a writer, not a gate: it never blocks compaction and has no
ENFORCE mode. The override analogue is PRECOMPACT_HANDOFF_DISABLE=1.

Env:
- PRECOMPACT_HANDOFF_DISABLE=1 — write nothing

Fail-open: any internal error → exit 0, compaction proceeds untouched.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

GIT_TIMEOUT_S = 10


def read_payload() -> dict:
    try:
        raw = sys.stdin.read()
    except OSError:
        return {}
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def git(cwd: Path, *args: str) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_S,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return proc.stdout.strip() if proc.returncode == 0 else ""


def next_seq(handoff_dir: Path, stem: str) -> int:
    existing = list(handoff_dir.glob(f"{stem}_seq*.md"))
    return len(existing) + 1


def snapshot(cwd: Path, repo_root: Path, payload: dict) -> str:
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    branch = git(cwd, "rev-parse", "--abbrev-ref", "HEAD") or "unknown"
    sha = git(cwd, "rev-parse", "--short", "HEAD") or "unknown"
    dirty = git(cwd, "status", "--short") or "clean"
    log = git(cwd, "log", "--oneline", "-5") or "no commits"
    trigger = str(payload.get("trigger", "unknown"))
    transcript = str(payload.get("transcript_path", "unknown"))

    return f"""# Handoff — autocompact — {now}

**Written by:** `precompact_handoff.py` (compaction trigger: `{trigger}`)
**Status:** deterministic snapshot only — the narrative sections below are
placeholders. Run `/handoff` to fill them from the live conversation, or read
the transcript at the path below.

## Git state
- Repo / worktree: {repo_root}
- Session cwd: {cwd}
- Branch: {branch} @ {sha}
- Uncommitted:
```
{dirty}
```
- Last commits:
```
{log}
```

## Transcript
- {transcript}

## Goal
_(placeholder — fill with /handoff)_

## Done
_(placeholder)_

## Not done
_(placeholder)_

## What did NOT work — do not repeat
_(placeholder)_

## Key decisions
_(placeholder)_

## Next steps
_(placeholder)_
"""


def main() -> int:
    if os.environ.get("PRECOMPACT_HANDOFF_DISABLE") == "1":
        return 0

    payload = read_payload()
    cwd_raw = payload.get("cwd") or os.getcwd()
    cwd = Path(str(cwd_raw))
    if not cwd.is_dir():
        return 0

    top = git(cwd, "rev-parse", "--show-toplevel")
    if not top:
        return 0
    repo_root = Path(top)

    handoff_dir = cwd / ".claude" / "handoffs"
    handoff_dir.mkdir(parents=True, exist_ok=True)

    stem = f"HANDOFF_autocompact_{datetime.now().strftime('%Y-%m-%d')}"
    target = handoff_dir / f"{stem}_seq{next_seq(handoff_dir, stem)}.md"
    if target.exists():  # paranoia: never overwrite
        return 0

    target.write_text(snapshot(cwd, repo_root, payload), encoding="utf-8")
    sys.stderr.write(f"[precompact_handoff] snapshot written: {target}\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001 — fail-open: never break compaction
        sys.exit(0)
