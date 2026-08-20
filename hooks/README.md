# Hook policy

Hook implementations live here, but each runtime keeps its native event wiring.

- Codex uses `hooks/codex/` through `~/.codex/hooks/`.
- Claude-compatible consumers use `hooks/claude/` through `~/.claude/hooks/`.
- Grok keeps its native JSON adapters and currently consumes the compatible hooks.
- Gemini uses `hooks/gemini/` for context/worktree guards and the shared Python stop
  check; Nodeterm still owns lifecycle status reporting.

Do not compile one runtime's event schema into another. `context-budget-guard.sh`
has separate Codex and Claude implementations because their transcript payloads differ.
