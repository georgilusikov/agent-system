#!/bin/bash
# Stop hook: run linter + tests if Python project before closing task.
# Outputs JSON with systemMessage on failure (informational, never blocks).
# Always exit 0 - this is informational only.

CWD="$(pwd)"

# Skip if not a Python project
if [ ! -f "$CWD/pyproject.toml" ] && [ ! -f "$CWD/requirements.txt" ] && [ ! -f "$CWD/setup.py" ]; then
  exit 0
fi

# Portable timeout: macOS doesn't have `timeout` by default.
# Use gtimeout (brew install coreutils) or fall back to no timeout.
if command -v gtimeout >/dev/null 2>&1; then
  TIMEOUT_CMD="gtimeout 30"
elif command -v timeout >/dev/null 2>&1; then
  TIMEOUT_CMD="timeout 30"
else
  TIMEOUT_CMD=""  # no timeout available, run without
fi

OUTPUT=""

# Run ruff if available
if command -v ruff >/dev/null 2>&1; then
  RUFF_OUT=$($TIMEOUT_CMD ruff check . 2>&1)
  RUFF_EXIT=$?
  if [ $RUFF_EXIT -ne 0 ]; then
    OUTPUT="${OUTPUT}⚠️ Ruff errors detected:
${RUFF_OUT}

"
  fi
fi

# Run pytest only when explicitly enabled (opt-in, same pattern as gemini-audit):
#   touch ~/.claude/.stop-pytest-enabled
# Rationale: pytest -x on EVERY Stop adds up to 30s latency + test output tokens
# even for doc-only edits. Ruff stays always-on (fast, cheap).
if [ -f "$HOME/.claude/.stop-pytest-enabled" ] && [ -d "$CWD/tests" ] && command -v pytest >/dev/null 2>&1; then
  PYTEST_OUT=$($TIMEOUT_CMD pytest -x -q --tb=short 2>&1)
  PYTEST_EXIT=$?
  if [ $PYTEST_EXIT -ne 0 ]; then
    OUTPUT="${OUTPUT}⚠️ Tests failing:
${PYTEST_OUT}"
  fi
fi

# Output JSON only if there's something to report
if [ -n "$OUTPUT" ]; then
  jq -n --arg msg "$OUTPUT" '{systemMessage: $msg}' 2>/dev/null || true
fi

exit 0
