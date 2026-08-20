#!/bin/bash
# SessionStart hook: read MEMORY.md from project memory folder if exists.
# Outputs JSON with additionalContext for the model.
# Never blocks the session - always exit 0.

CWD="$(pwd)"

# Strip git worktree suffix - worktrees share memory with their main project
# /path/to/project/.claude/worktrees/foo → /path/to/project
PROJECT_ROOT="${CWD%%/.claude/worktrees/*}"

# Use project root basename for path matching
BASENAME="$(basename "$PROJECT_ROOT")"

# Search ~/.claude/projects/ for MEMORY.md whose path contains the basename.
# More reliable than guessing Claude Code's path-sanitization algorithm
# (which handles Cyrillic / non-ASCII chars unpredictably on macOS BSD sed).
MEMORY_FILE=$(find "$HOME/.claude/projects/" -maxdepth 3 -path "*${BASENAME}*MEMORY.md" 2>/dev/null | head -1)

# Fallback: try original cwd basename (in case project is just one level)
if [ -z "$MEMORY_FILE" ]; then
  CWD_BASENAME="$(basename "$CWD")"
  if [ "$CWD_BASENAME" != "$BASENAME" ]; then
    MEMORY_FILE=$(find "$HOME/.claude/projects/" -maxdepth 3 -path "*${CWD_BASENAME}*MEMORY.md" 2>/dev/null | head -1)
  fi
fi

# Fallback for non-ASCII project names whose Claude directory becomes mostly dashes
# (for example /Users/.../Documents/курсор). Use the user's home-level memory
# rather than returning nothing; CLAUDE.md Memory preflight remains the real gate.
if [ -z "$MEMORY_FILE" ]; then
  HOME_MEMORY="$HOME/.claude/projects/-Users-$(basename "$HOME")/memory/MEMORY.md"
  if [ -f "$HOME_MEMORY" ]; then
    MEMORY_FILE="$HOME_MEMORY"
  fi
fi

# Output additionalContext if memory file found
if [ -n "$MEMORY_FILE" ] && [ -f "$MEMORY_FILE" ]; then
  CONTENT=$(cat "$MEMORY_FILE" 2>/dev/null || true)
  if [ -n "$CONTENT" ]; then
    jq -n \
      --arg ctx "📝 Memory loaded from $MEMORY_FILE (read this BEFORE starting new work to avoid repeating past sessions):

$CONTENT" \
      '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}' 2>/dev/null || true
  fi
fi

exit 0
