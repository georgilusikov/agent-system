#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
STATE=$(mktemp -d)
trap 'rm -rf "$STATE"' EXIT

assert_not_contains() {
  needle=$1
  file=$2
  if grep -Fq -- "$needle" "$file"; then
    exit 1
  fi
}

HOME_DIR=$STATE/home
mkdir -p "$HOME_DIR/.claude/bin"
TRANSCRIPT=$STATE/private-transcript.jsonl
PARKING=$STATE/parking.jsonl
PARK_ARGS=$STATE/park-args
printf '%s\n' \
  '{"is_error":true,"detail":"TRANSCRIPT_PRIVATE_SENTINEL"}' \
  'Traceback: TRANSCRIPT_PRIVATE_SENTINEL' \
  'Exit code 1: TRANSCRIPT_PRIVATE_SENTINEL' >"$TRANSCRIPT"
printf '%s\n' \
  '#!/bin/sh' \
  'printf "%s\\n" "$@" >"$PARK_CAPTURE"' >"$HOME_DIR/.claude/bin/park-incident.sh"
chmod +x "$HOME_DIR/.claude/bin/park-incident.sh"

printf '{"session_id":"privacy-session","transcript_path":"%s"}\n' "$TRANSCRIPT" |
  HOME="$HOME_DIR" \
  PARK_CAPTURE="$PARK_ARGS" \
  INCIDENT_PARKING_FILE="$PARKING" \
  INCIDENT_PARKING_THRESHOLD=3 \
  bash "$ROOT/hooks/claude/incident-parking.sh"

test "$(sed -n '1p' "$PARK_ARGS")" = "--source"
test "$(sed -n '2p' "$PARK_ARGS")" = "hook"
test "$(sed -n '3p' "$PARK_ARGS")" = "--session-id"
test "$(sed -n '4p' "$PARK_ARGS")" = "privacy-session"
test "$(sed -n '5p' "$PARK_ARGS")" = "--signal"
test "$(sed -n '6p' "$PARK_ARGS")" = "mechanical: 3 error markers in session tail"
test "$(sed -n '7p' "$PARK_ARGS")" = "--note"
test "$(sed -n '8p' "$PARK_ARGS")" = "metadata-only: transcript content withheld"
test "$(sed -n '9p' "$PARK_ARGS")" = "--file"
test "$(sed -n '10p' "$PARK_ARGS")" = "$PARKING"
assert_not_contains "TRANSCRIPT_PRIVATE_SENTINEL" "$PARK_ARGS"
assert_not_contains "$TRANSCRIPT" "$PARK_ARGS"

REPO=$STATE/repo
mkdir -p "$REPO"
git init -q "$REPO" >/dev/null 2>&1
git -C "$REPO" config user.email privacy-test@example.invalid
git -C "$REPO" config user.name privacy-test
printf '%s\n' tracked >"$REPO/tracked.txt"
git -C "$REPO" add tracked.txt
git -C "$REPO" commit -qm initial
printf '%s\n' dirty >>"$REPO/tracked.txt"

printf '%s\n' 'TRANSCRIPT_PRIVATE_SENTINEL' >"$TRANSCRIPT"
printf '{"cwd":"%s","trigger":"auto","transcript_path":"%s"}\n' "$REPO" "$TRANSCRIPT" |
  python3 "$ROOT/hooks/claude/precompact_handoff.py" 2>"$STATE/precompact.stderr"

HANDOFF_DIR=$REPO/.claude/handoffs
HANDOFF=$(find "$HANDOFF_DIR" -type f -name 'HANDOFF_*.md' -print -quit)
test -n "$HANDOFF"
grep -Fq 'trigger: auto' "$HANDOFF"
grep -Fq 'transcript_available: true' "$HANDOFF"
grep -Fq 'branch:' "$HANDOFF"
grep -Fq 'sha:' "$HANDOFF"
grep -Fq 'dirty_status:' "$HANDOFF"
grep -Fq 'last_commits:' "$HANDOFF"
assert_not_contains "$TRANSCRIPT" "$HANDOFF"
assert_not_contains "TRANSCRIPT_PRIVATE_SENTINEL" "$HANDOFF"
assert_not_contains 'Repo / worktree' "$HANDOFF"
assert_not_contains 'Session cwd' "$HANDOFF"
assert_not_contains '## Transcript' "$HANDOFF"

SESSION_START=$STATE/session-start.json
printf '{"cwd":"%s"}\n' "$REPO" |
  python3 "$ROOT/hooks/claude/session_start_handoff.py" >"$SESSION_START"
grep -Fq '<handoff_from_previous_session' "$SESSION_START"
grep -Fq 'transcript_available: true' "$SESSION_START"
assert_not_contains "$TRANSCRIPT" "$SESSION_START"
assert_not_contains "TRANSCRIPT_PRIVATE_SENTINEL" "$SESSION_START"

printf '{"cwd":"%s","trigger":"manual"}\n' "$REPO" |
  python3 "$ROOT/hooks/claude/precompact_handoff.py" 2>"$STATE/precompact.stderr"
HANDOFF_FALSE=$HANDOFF_DIR/HANDOFF_autocompact_$(date +%Y-%m-%d)_seq2.md
grep -Fq 'trigger: manual' "$HANDOFF_FALSE"
grep -Fq 'transcript_available: false' "$HANDOFF_FALSE"

printf '{"cwd":"%s","trigger":"UNEXPECTED_TRIGGER_SENTINEL"}\n' "$REPO" |
  python3 "$ROOT/hooks/claude/precompact_handoff.py" 2>"$STATE/precompact.stderr"
HANDOFF_UNKNOWN=$HANDOFF_DIR/HANDOFF_autocompact_$(date +%Y-%m-%d)_seq3.md
grep -Fq 'trigger: unknown' "$HANDOFF_UNKNOWN"
assert_not_contains 'UNEXPECTED_TRIGGER_SENTINEL' "$HANDOFF_UNKNOWN"
