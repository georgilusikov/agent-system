#!/usr/bin/env bash
# Gemini-backed DEEP audit via Gemini CLI (subscription, no API key).
# Gemini runs agentic loop with read-only tools: reads files, greps code, runs tests.
# Reads JSON {assistant_text, diff_text, context, cwd} from stdin.
#
# Uses `gemini --prompt` headless + yolo + sandbox (seatbelt on macOS isolates writes).
# System prompt enforces READ-ONLY discipline.

set -u
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v gemini >/dev/null 2>&1; then
  echo "ERROR: gemini CLI not installed. Install via: npm install -g @google/gemini-cli" >&2
  exit 1
fi

bash "$SCRIPT_DIR/check-updates.sh" || true

INPUT="$(cat)"

read_field() {
  printf '%s' "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('$1',''))"
}

ASSISTANT="$(read_field assistant_text)"
DIFF_TEXT="$(read_field diff_text)"
CONTEXT="$(read_field context)"
CWD_IN="$(read_field cwd)"
[ -n "$CWD_IN" ] || CWD_IN="$(pwd)"

if [ -z "$ASSISTANT" ] && [ -z "$DIFF_TEXT" ]; then
  echo "Nothing to audit: no summary and no diff provided."
  exit 0
fi

ASSISTANT_T="$(printf '%s' "$ASSISTANT" | head -c 100000)"
DIFF_TEXT_T="$(printf '%s' "$DIFF_TEXT" | head -c 50000)"
CONTEXT_T="$(printf '%s' "$CONTEXT" | head -c 30000)"

CONTEXT_SECTION=""
[ -n "$CONTEXT_T" ] && CONTEXT_SECTION="PROJECT RULES (CLAUDE.md):
$CONTEXT_T
"

DIFF_SECTION="(no diff provided)"
[ -n "$DIFF_TEXT_T" ] && DIFF_SECTION="GIT DIFF:
$DIFF_TEXT_T"

PROMPT="$(cat <<PROMPT_EOF
You are an independent code auditor running in READ-ONLY mode. Another AI agent (Claude) claims to have
completed some work. Your job is to INDEPENDENTLY VERIFY every claim by inspecting the repo.

ABSOLUTE RULES (READ-ONLY AUDIT):
- NEVER call write_file, replace, edit, or any mutating tool. You are a reviewer, not a contributor.
- For run_shell_command: only read-only commands — ls, cat, grep, rg, git log/diff/show, pytest, npm test, node --check, go test, cargo check. NEVER rm/mv/cp/chmod/git commit/git push/git reset/git checkout -- or anything that mutates repo.
- If a claim requires a mutating test to verify — mark it "unverified" and explain why.

AUDIT PROCESS:
1. Read the agent's summary to understand what it claims to have done
2. Check the git diff to see what actually changed
3. Read the changed files to verify the code is correct
4. Run tests if they exist (look for test files, package.json scripts, pytest, etc.) — read-only
5. Check for common issues: security vulnerabilities, broken imports, missing error handling
6. Verify specific claims ("tests pass", "builds succeed", "bug is fixed")
7. Check if CLAUDE.md rules were followed (if provided)

BE THOROUGH. Take your time. Call multiple tools. Read multiple files.

PROJECT ROOT: $CWD_IN

$CONTEXT_SECTION
WHAT THE AGENT CLAIMS:
$ASSISTANT_T

$DIFF_SECTION

Now verify these claims independently. Read the actual files, run the tests, check the code.
Start by listing the project files and reading the diff.

WHEN DONE, output your final report in EXACTLY this format:
SCORE: X/10
VERIFIED:
- [claim] -> [verified/unverified/false] [evidence]
ISSUES:
- [issue description]
VERDICT: PASS or FAIL
PROMPT_EOF
)"

START_TS=$(date +%s)

# Run gemini with yolo (auto-approve) + sandbox (seatbelt read-only-ish on macOS).
# Change cwd so gemini's file ops resolve against the audited project.
RAW_OUT="$(cd "$CWD_IN" && printf '%s' "$PROMPT" | gemini --prompt "" --approval-mode yolo --sandbox --output-format json 2>/dev/null || true)"

END_TS=$(date +%s)
ELAPSED=$((END_TS - START_TS))

if [ -z "$RAW_OUT" ]; then
  echo "ERROR: gemini CLI returned no output. Check 'gemini' authentication (run 'gemini' interactively once)." >&2
  exit 2
fi

# Parse JSON response + tool stats.
PARSED="$(printf '%s' "$RAW_OUT" | python3 <<'PY'
import json, sys
raw = sys.stdin.read()
i = raw.find('{')
if i < 0:
    print('ERROR_NO_JSON')
    print(raw[:500], file=sys.stderr)
    sys.exit(3)
try:
    d = json.loads(raw[i:])
except json.JSONDecodeError as e:
    print('ERROR_PARSE')
    print(f'{e}', file=sys.stderr)
    print(raw[i:i+500], file=sys.stderr)
    sys.exit(3)
resp = d.get('response', '').strip()
tools = d.get('stats', {}).get('tools', {})
total = tools.get('totalCalls', 0)
names = ",".join(tools.get('byName', {}).keys())
print(f'TOOLS:{total}:{names}')
print('---RESPONSE---')
print(resp)
PY
)"
RC=$?
if [ "$RC" -ne 0 ]; then
  exit "$RC"
fi

TOOLS_LINE="$(printf '%s' "$PARSED" | head -1)"
RESULT="$(printf '%s' "$PARSED" | awk 'f{print} /^---RESPONSE---$/{f=1}')"

SCORE="$(printf '%s' "$RESULT" | awk '/^SCORE:/ {split($2,a,"/"); print a[1]; exit}')"

# Banner with reaction table (parity with old bouncer-deep.py).
banner() {
  local score="$1" elapsed="$2" tools="$3"
  declare -A LABELS=(
    [10]="VIP ENTRY|velvet rope parts"
    [9]="GUEST LIST|almost flawless"
    [8]="STAMP APPROVED|solid work, minor nits"
    [7]="SIDE ENTRANCE|decent but gaps showing"
    [6]="PAT DOWN|needs another pass"
    [5]="HELD AT DOOR|half-baked"
    [4]="TURNED AWAY|come back dressed better"
    [3]="BANNED TONIGHT|serious problems"
    [2]="LIFETIME BAN|what happened here"
    [1]="CALLING POLICE|everything is wrong"
  )
  local entry="${LABELS[$score]:-???|}"
  local label="${entry%%|*}" quip="${entry##*|}"
  local filled=$((score * 3))
  local empty=$((30 - filled))
  local bar
  bar="[$(printf '#%.0s' $(seq 1 $filled 2>/dev/null))$(printf '.%.0s' $(seq 1 $empty 2>/dev/null))]"
  echo ""
  printf '  %s\n' "$(printf '~%.0s' $(seq 1 42))"
  printf '    BOUNCER DEEP AUDIT  %s  %s/10\n' "$bar" "$score"
  printf '    %s: %s\n' "$label" "$quip"
  printf '    Verified in %ss  |  %s\n' "$elapsed" "$tools"
  printf '  %s\n' "$(printf '~%.0s' $(seq 1 42))"
  echo ""
}

if [ -n "$SCORE" ]; then
  banner "$SCORE" "$ELAPSED" "$TOOLS_LINE"
else
  echo ""
  echo "(Could not parse score, audit took ${ELAPSED}s, $TOOLS_LINE)"
  echo ""
fi

printf '%s\n' "$RESULT"
