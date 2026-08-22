#!/bin/sh
set -eu

GUARD=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/context-budget-guard.sh
STATE=$(mktemp -d)
trap 'rm -rf "$STATE"' EXIT

run_goal() {
  turn=$1
  printf '{"session_id":"goal-session","prompt":"%s"}\n' \
    "$(if [ "$turn" -eq 1 ]; then printf '/goal ship milestone'; else printf 'continue'; fi)" |
    CBG_STATE_DIR="$STATE" CBG_WARN=999999999 CBG_HARD=999999999 \
      sh "$GUARD"
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
      sh "$GUARD" >/tmp/context-budget-guard.out
  test ! -s /tmp/context-budget-guard.out
  turn=$((turn + 1))
done

TRANSCRIPT="$STATE/claude.jsonl"
printf '%s\n' '{"message":{"usage":{"input_tokens":100,"cache_read_input_tokens":0,"cache_creation_input_tokens":0}}}' >"$TRANSCRIPT"
printf '{"session_id":"token-session","prompt":"ordinary","transcript_path":"%s"}\n' "$TRANSCRIPT" |
  CBG_STATE_DIR="$STATE" CBG_WARN=100 CBG_HARD=200 \
    sh "$GUARD" | grep -q 'CONTEXT BUDGET WARNING.*100'

printf '%s\n' '{"message":{"usage":{"input_tokens":200,"cache_read_input_tokens":0,"cache_creation_input_tokens":0}}}' >"$TRANSCRIPT"
printf '{"session_id":"ordinary-hard-session","prompt":"ordinary","transcript_path":"%s"}\n' "$TRANSCRIPT" |
  CBG_STATE_DIR="$STATE" CBG_WARN=100 CBG_HARD=200 \
    sh "$GUARD" |
  grep -q 'launch the continuation yourself.*not a blocked goal'

printf '{"session_id":"goal-hard-session","prompt":"/goal continue","transcript_path":"%s"}\n' "$TRANSCRIPT" |
  CBG_STATE_DIR="$STATE" CBG_WARN=100 CBG_HARD=200 \
    sh "$GUARD" |
  grep -q 'continue in the same task'

test -z "$(printf '%s\n' 'not-json' | sh "$GUARD")"
test -z "$(printf '{\"session_id\":\"disabled-session\",\"prompt\":\"/goal continue\",\"transcript_path\":\"%s\"}\n' "$TRANSCRIPT" |
  AI_MGMT_HOOKS=0 CBG_STATE_DIR="$STATE" CBG_WARN=100 CBG_HARD=200 \
  sh "$GUARD")"
