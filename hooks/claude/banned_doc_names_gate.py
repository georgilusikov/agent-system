#!/usr/bin/env python3
"""banned_doc_names_gate — Claude Code PreToolUse Write|Edit hook.

Gates creation of report/summary-style .md files that agents love to spawn
(REPORT.md, SUMMARY.md, ANALYSIS_FINAL.md, SOMETHING_GUIDE.md, *_FIXED.md ...).
Findings belong in the chat reply, not in throwaway doc files; `_fixed`/`_final`
suffixes are banned outright by workspace rules.

Banned basename patterns (case-insensitive):
  REPORT | SUMMARY | ANALYSIS | FINDINGS | DIAGNOSIS | _FINAL | _FIXED | _NEW
  plus any *GUIDE* name.

Exceptions (always pass):
  - paths inside ~/.claude/
  - CHANGELOG.md / README.md
  - scratchpad / tmp paths

Phase 1 WARN by default: violation prints a warning to stderr, exit 0.
BANNED_DOC_ENFORCE=1 → hard BLOCK (exit 2).
Override: BANNED_DOC_ACK="<reason ≥12 chars>".
Fail-open: any internal error → exit 0.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ENFORCE_ENV = "BANNED_DOC_ENFORCE"
ACK_ENV = "BANNED_DOC_ACK"
ACK_MIN_CHARS = 12

BANNED = re.compile(r"(?i)(REPORT|SUMMARY|ANALYSIS|FINDINGS|DIAGNOSIS|_FINAL|_FIXED|_NEW|GUIDE)")
ALLOWED_BASENAMES = {"changelog.md", "readme.md"}


def _is_exempt(path_str: str) -> bool:
    p = Path(path_str).expanduser()
    try:
        resolved = str(p.resolve())
    except OSError:
        resolved = str(p)
    home_claude = str(Path.home() / ".claude")
    if resolved.startswith(home_claude + os.sep) or resolved == home_claude:
        return True
    lowered = resolved.lower()
    if "/scratchpad" in lowered or lowered.startswith("/tmp/") or lowered.startswith("/private/tmp/"):
        return True
    if p.name.lower() in ALLOWED_BASENAMES:
        return True
    return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    tool_name = payload.get("tool_name") or payload.get("toolName") or ""
    if tool_name not in ("Write", "Edit"):
        return 0
    tool_input = payload.get("tool_input") or payload.get("toolInput") or {}
    file_path = tool_input.get("file_path", "") or ""
    if not file_path or not file_path.lower().endswith(".md"):
        return 0
    if _is_exempt(file_path):
        return 0
    basename = Path(file_path).name
    if not BANNED.search(basename):
        return 0

    ack = os.environ.get(ACK_ENV, "").strip()
    if len(ack) >= ACK_MIN_CHARS:
        print(f"[banned-doc-names] ACK present ({ack[:40]}…) — allowed.", file=sys.stderr)
        return 0

    enforce = os.environ.get(ENFORCE_ENV, "").strip() == "1"
    verdict = "BLOCK" if enforce else "WARN (Phase 1, not blocking)"
    print(
        f"[banned-doc-names] {verdict} — .md file with a banned report-style name:\n"
        f"  {file_path}\n"
        "Findings/reports belong in the chat reply, not in throwaway .md files;\n"
        "_final/_fixed/_new suffixes are banned — edit the original instead.\n"
        f'Override: export {ACK_ENV}="<reason ≥{ACK_MIN_CHARS} chars>"',
        file=sys.stderr,
    )
    if not enforce:
        print(f"Phase 1 WARN mode: set {ENFORCE_ENV}=1 to make this a hard block.", file=sys.stderr)
    return 2 if enforce else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # pragma: no cover — fail open
        print(f"[banned-doc-names] internal error (fail-open): {exc}", file=sys.stderr)
        sys.exit(0)
