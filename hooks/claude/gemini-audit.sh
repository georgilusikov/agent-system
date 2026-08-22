#!/bin/bash
# Gemini independent audit - Stop hook wrapper
# Content-bearing audit is opt-in twice: touch ~/.claude/.gemini-audit-enabled
# and set GEMINI_AUDIT_ALLOW_CONTENT=1 for that invocation. Without both gates
# no prompt, response, transcript, tool payload, or diff leaves the runtime.

# Quick check before spawning Python
[ -f "$HOME/.claude/.gemini-audit-enabled" ] || exit 0
[ "${GEMINI_AUDIT_ALLOW_CONTENT:-}" = "1" ] || exit 0

# Source shell profile for env vars (GEMINI_API_KEY)
[ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc" 2>/dev/null
[ -f "$HOME/.zshrc" ] && source "$HOME/.zshrc" 2>/dev/null

# Pass stdin through to Python
exec python3 "$HOME/.claude/hooks/gemini-audit.py"
