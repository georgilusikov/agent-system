# Hook policy

Hook implementations live here, but each runtime keeps its native event wiring.

- Codex uses `hooks/codex/` through `~/.codex/hooks/`.
- Claude-compatible consumers use `hooks/claude/` through `~/.claude/hooks/`.
- Grok keeps its native JSON adapters and currently consumes the compatible hooks.
- AGY uses `hooks/gemini/guard.py` only for its camelCase `PreToolUse` worktree
  guard in `~/.gemini/config/hooks.json`.

The AGY worktree gate stays WARN-by-default through at least
2026-09-03; enable enforcement only after reviewing live receipts.

The Claude Gemini audit is content-bearing and therefore requires both its
explicit flag and `GEMINI_AUDIT_ALLOW_CONTENT=1`; the default path sends no
session content to an external provider.

Do not compile one runtime's event schema into another. Context continuity uses
native compaction lifecycle events and never token or step thresholds.
