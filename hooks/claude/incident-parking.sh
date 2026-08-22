#!/usr/bin/env bash
# Stop hook: Incident Parking, mechanical channel.
#
# Reads only the tail of the session transcript to count error markers. Threshold
# reached -> parks ONE metadata-only line in ~/.claude/memory/incidents/parking.jsonl
# via ~/.claude/bin/park-incident.sh with source="hook". No transcript path,
# content, or line fragment is passed to the helper.
#
# The semantic channel (owner corrections, repeated mistakes, empty gates) is the
# agent's job — see ~/.claude/rules/incident-parking.md.
#
# Contract:
#   - always exit 0 (a hook must never break the session)
#   - stderr silent
#   - budget < 2s (reads at most the last 300 KB of the transcript)
#   - one hook line per session (dedup on session_id + source=hook)

set -u

exec 2>/dev/null

INPUT="$(cat 2>/dev/null || true)"
[ -n "$INPUT" ] || exit 0

PARK_HELPER="$HOME/.claude/bin/park-incident.sh"
PARKING_FILE="${INCIDENT_PARKING_FILE:-$HOME/.claude/memory/incidents/parking.jsonl}"
THRESHOLD="${INCIDENT_PARKING_THRESHOLD:-3}"

[ -x "$PARK_HELPER" ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

# Python side prints exactly three metadata-only lines when something must be parked:
#   line 1: session_id
#   line 2: marker count / signal class
#   line 3: fixed metadata-only note
# Prints nothing when there is nothing to park (below threshold, no transcript,
# or this session already has a hook line in the parking file).
RESULT="$(
  PARK_INPUT="$INPUT" \
  PARK_FILE="$PARKING_FILE" \
  PARK_THRESHOLD="$THRESHOLD" \
  python3 - <<'PY' || true
import json
import os
import re
import sys

THRESHOLD = int(os.environ.get("PARK_THRESHOLD") or 3)
PARKING = os.environ["PARK_FILE"]

try:
    data = json.loads(os.environ.get("PARK_INPUT") or "")
except (json.JSONDecodeError, ValueError):
    sys.exit(0)
if not isinstance(data, dict):
    sys.exit(0)

session_id = str(data.get("session_id") or "").strip()
transcript = str(data.get("transcript_path") or "").strip()
if not session_id or not transcript or not os.path.isfile(transcript):
    sys.exit(0)

# --- dedup: this session already parked by the hook? ---------------------------
try:
    with open(PARKING, "r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if session_id not in line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("session_id") == session_id and record.get("source") == "hook":
                sys.exit(0)
except FileNotFoundError:
    pass
except OSError:
    sys.exit(0)

# --- read the tail -------------------------------------------------------------
TAIL_BYTES = 300_000
try:
    size = os.path.getsize(transcript)
    with open(transcript, "rb") as handle:
        if size > TAIL_BYTES:
            handle.seek(-TAIL_BYTES, os.SEEK_END)
        tail = handle.read().decode("utf-8", errors="replace")
except OSError:
    sys.exit(0)

if not tail:
    sys.exit(0)

RE_IS_ERROR = re.compile(r'"is_error"\s*:\s*true')
RE_TRACEBACK = re.compile(r"Traceback")
RE_EXIT_CODE = re.compile(r"[Ee]xit code [1-9][0-9]*")


count = 0

for line in tail.splitlines():
    for pattern in (RE_IS_ERROR, RE_TRACEBACK, RE_EXIT_CODE):
        if pattern.search(line):
            count += 1

if count < THRESHOLD:
    sys.exit(0)

signal = f"mechanical: {count} error markers in session tail"
note = "metadata-only: transcript content withheld"

print(session_id)
print(signal)
print(note[:400])
PY
)"

[ -n "$RESULT" ] || exit 0

SESSION_ID="$(printf '%s\n' "$RESULT" | sed -n '1p')"
SIGNAL="$(printf '%s\n' "$RESULT" | sed -n '2p')"
NOTE="$(printf '%s\n' "$RESULT" | sed -n '3p')"

[ -n "$SESSION_ID" ] && [ -n "$SIGNAL" ] && [ -n "$NOTE" ] || exit 0

"$PARK_HELPER" \
  --source hook \
  --session-id "$SESSION_ID" \
  --signal "$SIGNAL" \
  --note "$NOTE" \
  --file "$PARKING_FILE" >/dev/null 2>&1 || true

exit 0
