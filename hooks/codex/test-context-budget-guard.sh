#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
STATE=$(mktemp -d)
trap 'rm -rf "$STATE"' EXIT

run_goal() {
  turn=$1
  printf '{"session_id":"goal-session","prompt":"%s"}\n' \
    "$(if [ "$turn" -eq 1 ]; then printf '/goal ship milestone'; else printf 'continue'; fi)" |
    CBG_STATE_DIR="$STATE" CBG_WARN=999999999 CBG_HARD=999999999 \
      sh "$ROOT/hooks/context-budget-guard.sh"
}

turn=1
while [ "$turn" -lt 20 ]; do
  test -z "$(run_goal "$turn")"
  turn=$((turn + 1))
done
run_goal 20 | grep -q 'GOAL CHECKPOINT.*20'

turn=21
while [ "$turn" -lt 25 ]; do
  test -z "$(run_goal "$turn")"
  turn=$((turn + 1))
done
test -z "$(run_goal 25)"
test -z "$(run_goal 26)"

turn=1
while [ "$turn" -le 26 ]; do
  printf '{"session_id":"normal-session","prompt":"ordinary question"}\n' |
    CBG_STATE_DIR="$STATE" CBG_WARN=999999999 CBG_HARD=999999999 \
      sh "$ROOT/hooks/context-budget-guard.sh" >/tmp/context-budget-guard.out
  test ! -s /tmp/context-budget-guard.out
  turn=$((turn + 1))
done

TRANSCRIPT="$STATE/codex.jsonl"
printf '%s\n' '{"payload":{"type":"token_count","info":{"last_token_usage":{"input_tokens":120,"cached_input_tokens":0}}}}' >"$TRANSCRIPT"
printf '{"session_id":"token-session","prompt":"ordinary","transcript_path":"%s"}\n' "$TRANSCRIPT" |
  CBG_STATE_DIR="$STATE" CBG_WARN=120 CBG_HARD=240 \
      sh "$ROOT/hooks/context-budget-guard.sh" | grep -q 'CONTEXT BUDGET WARNING.*120'

printf '%s\n' '{"payload":{"type":"token_count","info":{"last_token_usage":{"input_tokens":240,"cached_input_tokens":0}}}}' >"$TRANSCRIPT"
printf '{"session_id":"hard-token-session","prompt":"ordinary","transcript_path":"%s"}\n' "$TRANSCRIPT" |
  CBG_STATE_DIR="$STATE" CBG_WARN=120 CBG_HARD=240 \
      sh "$ROOT/hooks/context-budget-guard.sh" |
  grep -q 'launch the continuation yourself.*not a blocked goal'

printf '%s\n' '{"payload":{"type":"token_count","info":{"last_token_usage":{"input_tokens":499,"cached_input_tokens":499},"model_context_window":1000}}}' >"$TRANSCRIPT"
test -z "$(
  printf '{"session_id":"ratio-below-session","prompt":"ordinary","transcript_path":"%s"}\n' "$TRANSCRIPT" |
    CBG_STATE_DIR="$STATE" sh "$ROOT/hooks/context-budget-guard.sh"
)"

printf '%s\n' '{"payload":{"type":"token_count","info":{"last_token_usage":{"input_tokens":500,"cached_input_tokens":500},"model_context_window":1000}}}' >"$TRANSCRIPT"
printf '{"session_id":"ratio-warn-session","prompt":"ordinary","transcript_path":"%s"}\n' "$TRANSCRIPT" |
  CBG_STATE_DIR="$STATE" sh "$ROOT/hooks/context-budget-guard.sh" |
  grep -q 'CONTEXT BUDGET WARNING.*500'

printf '%s\n' '{"payload":{"type":"token_count","info":{"last_token_usage":{"input_tokens":800,"cached_input_tokens":800},"model_context_window":1000}}}' >"$TRANSCRIPT"
printf '{"session_id":"ratio-hard-session","prompt":"ordinary","transcript_path":"%s"}\n' "$TRANSCRIPT" |
  CBG_STATE_DIR="$STATE" sh "$ROOT/hooks/context-budget-guard.sh" |
  grep -q 'CONTEXT BUDGET HARD LIMIT.*800.*launch the continuation yourself'

printf '%s\n' '{"payload":{"type":"token_count","info":{"last_token_usage":{"input_tokens":699,"cached_input_tokens":699},"model_context_window":1000}}}' >"$TRANSCRIPT"
test -z "$(
  printf '{"session_id":"goal-ratio-below-session","prompt":"/goal continue","transcript_path":"%s"}\n' "$TRANSCRIPT" |
    CBG_STATE_DIR="$STATE" sh "$ROOT/hooks/context-budget-guard.sh"
)"

printf '%s\n' '{"payload":{"type":"token_count","info":{"last_token_usage":{"input_tokens":700,"cached_input_tokens":700},"model_context_window":1000}}}' >"$TRANSCRIPT"
printf '{"session_id":"goal-ratio-warn-session","prompt":"/goal continue","transcript_path":"%s"}\n' "$TRANSCRIPT" |
  CBG_STATE_DIR="$STATE" sh "$ROOT/hooks/context-budget-guard.sh" |
  grep -q 'CONTEXT BUDGET WARNING.*700.*continue in the same task'

printf '%s\n' '{"payload":{"type":"token_count","info":{"last_token_usage":{"input_tokens":900,"cached_input_tokens":900},"model_context_window":1000}}}' >"$TRANSCRIPT"
printf '{"session_id":"goal-ratio-hard-session","prompt":"/goal continue","transcript_path":"%s"}\n' "$TRANSCRIPT" |
  CBG_STATE_DIR="$STATE" sh "$ROOT/hooks/context-budget-guard.sh" >"$STATE/goal-hard.out"
grep -q 'CONTEXT BUDGET HARD LIMIT.*900.*continue in the same task' "$STATE/goal-hard.out"
! grep -Eqi 'fresh (thread|session)|new tab|create_thread' "$STATE/goal-hard.out"

test -z "$(printf '%s\n' 'not-json' | sh "$ROOT/hooks/context-budget-guard.sh")"
test -z "$(printf '{\"session_id\":\"disabled-session\",\"prompt\":\"/goal continue\",\"transcript_path\":\"%s\"}\n' "$TRANSCRIPT" |
  AI_MGMT_HOOKS=0 CBG_STATE_DIR="$STATE" sh "$ROOT/hooks/context-budget-guard.sh")"
printf '%s\n' '{}' | sh "$ROOT/hooks/response-contract-reminder.sh" | grep -q 'REMINDER:'
test -z "$(printf '%s\n' '{}' | AI_MGMT_HOOKS=0 sh "$ROOT/hooks/response-contract-reminder.sh")"
