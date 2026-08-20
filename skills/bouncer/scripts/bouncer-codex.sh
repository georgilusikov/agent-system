#!/usr/bin/env bash
# Codex-backed audit for bouncer.
# Reads JSON {assistant_text, diff_text, context, cwd, mode} from stdin.
# Emits Codex verdict to stdout.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v codex >/dev/null 2>&1; then
  echo "ERROR: codex CLI not installed. Install via: npm install -g @openai/codex" >&2
  exit 1
fi

bash "$SCRIPT_DIR/check-updates.sh" || true

INPUT="$(cat)"
MODE="$(printf '%s' "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("mode","quick"))')"
ASSISTANT="$(printf '%s' "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("assistant_text",""))')"
DIFF="$(printf '%s' "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("diff_text",""))')"
CONTEXT="$(printf '%s' "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("context",""))')"

PROMPT="You are an independent reviewer. Audit the following work.

## Summary
${ASSISTANT}

## Diff
${DIFF}

## Project context (CLAUDE.md)
${CONTEXT}

## Task
Score the work 1-10 and list: gaps, risks, suggestions, blocking issues.
Return JSON: {score, gaps[], risks[], suggestions[], blocking[], verdict: APPROVED|NEEDS_REVISION}"

case "$MODE" in
  quick|deep)
    printf '%s' "$PROMPT" | codex exec --sandbox read-only - 2>&1
    ;;
  plan-review)
    # Iterative up to 3 cycles. Called externally in a loop per cycle.
    printf '%s' "$PROMPT" | codex exec --sandbox read-only - 2>&1
    ;;
  *)
    echo "ERROR: unknown mode: $MODE (expected quick|deep|plan-review)" >&2
    exit 2
    ;;
esac
