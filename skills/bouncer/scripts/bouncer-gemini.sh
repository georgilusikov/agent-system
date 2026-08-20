#!/usr/bin/env bash
# Gemini-backed quick audit for bouncer via Gemini CLI (subscription, no API key).
# Reads JSON {assistant_text, diff_stat, diff_text, context, cwd, mode} from stdin.
# Emits Gemini verdict to stdout.
#
# Uses `gemini --prompt` (headless), OAuth subscription, sandbox + plan mode (read-only).

set -u
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v gemini >/dev/null 2>&1; then
  echo "ERROR: gemini CLI not installed. Install via: npm install -g @google/gemini-cli" >&2
  exit 1
fi

# Fire-and-forget update check (prints to stderr, never blocks).
bash "$SCRIPT_DIR/check-updates.sh" || true

INPUT="$(cat)"

# Extract fields via python (safe for multi-line strings).
read_field() {
  printf '%s' "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('$1',''))"
}

ASSISTANT="$(read_field assistant_text)"
DIFF_STAT="$(read_field diff_stat)"
DIFF_TEXT="$(read_field diff_text)"
CONTEXT="$(read_field context)"

if [ -z "$ASSISTANT" ] && [ -z "$DIFF_STAT" ] && [ -z "$DIFF_TEXT" ]; then
  echo "Nothing to audit: no summary and no diff provided."
  exit 0
fi

# Truncate fields to budget.
truncate_field() {
  local field="$1" limit="$2"
  printf '%s' "$field" | head -c "$limit"
}

ASSISTANT_T="$(truncate_field "$ASSISTANT" 200000)"
DIFF_STAT_T="$(truncate_field "$DIFF_STAT" 5000)"
DIFF_TEXT_T="$(truncate_field "$DIFF_TEXT" 50000)"
CONTEXT_T="$(truncate_field "$CONTEXT" 50000)"

DIFF_SECTION=""
if [ -n "$DIFF_STAT_T" ] || [ -n "$DIFF_TEXT_T" ]; then
  DIFF_SECTION="$(cat <<EOF

CODE CHANGES (git diff --stat):
$DIFF_STAT_T

CODE CHANGES (diff):
$DIFF_TEXT_T
EOF
)"
else
  DIFF_SECTION="
(No code diff available. Score based on the agent's response quality, completeness, and whether claims seem credible.)
"
fi

CONTEXT_SECTION=""
if [ -n "$CONTEXT_T" ]; then
  CONTEXT_SECTION="$(cat <<EOF

TASK CONTEXT (project rules from CLAUDE.md):
$CONTEXT_T
EOF
)"
fi

PROMPT="$(cat <<PROMPT_EOF
You are an independent reviewer auditing an AI agent's output.
Score the output 1-10 and list specific issues. Be harsh but fair.

FIRST: Determine the TASK TYPE from the agent's summary:
- CODING: writing/editing code, fixing bugs, configuration, deployment
- ADVISORY: answering questions, giving advice, strategy, negotiation, legal guidance, analysis, research, explanations
- CREATIVE: writing content (posts, copy, emails), creating videos, designing visuals, crafting social media, storytelling
- OPERATIONS: deploying, server config, Docker, CI/CD, infrastructure, DevOps, database migrations
- RESEARCH: exploring codebases, investigating bugs, finding information, reading docs, analyzing data

SCORING CRITERIA FOR CODING TASKS:
- 10/10: Code changes verified working (tests pass, builds succeed), every claim backed by evidence
- 8-9/10: Good work but has gaps (untested changes, unverified claims)
- 6-7/10: Notable problems (incomplete, missing verification)
- 1-5/10: Broken, wrong, or fabricated

SCORING CRITERIA FOR ADVISORY TASKS:
- 10/10: Accurate, complete, actionable advice that fully addresses the user's question. Covers all angles. No factual errors.
- 8-9/10: Good advice but misses an important angle or has minor gaps
- 6-7/10: Partially addresses the question, vague, or missing key considerations
- 1-5/10: Wrong, misleading, or unhelpful

SCORING CRITERIA FOR CREATIVE TASKS:
- 10/10: Compelling, authentic, well-crafted output that achieves its goal. Matches intended tone and audience.
- 8-9/10: Good but could be more original or polished
- 6-7/10: Generic, formulaic, or misses the audience/tone
- 1-5/10: Off-brand, tone-deaf, or low effort

SCORING CRITERIA FOR OPERATIONS TASKS:
- 10/10: Successfully completed with verification. Idempotent, no side effects.
- 8-9/10: Completed but missing verification or minor gaps in rollback
- 6-7/10: Partially done, untested, or risky
- 1-5/10: Broke something, wrong config, or dangerous

SCORING CRITERIA FOR RESEARCH TASKS:
- 10/10: Thorough, accurate findings with clear conclusions. Actionable summary.
- 8-9/10: Good but missed an obvious source or unanswered question
- 6-7/10: Shallow, incomplete, or inconclusive
- 1-5/10: Wrong conclusions or missed critical information

FOR ADVISORY / CREATIVE / RESEARCH TASKS: Do NOT demand command output, code verification, or test results.
IMPORTANT RULES:
- The git diff may be UNRELATED to the current response. Do NOT penalize for mismatch unless the agent claims specific code changes that aren't in the diff.
- Score on OWN merits: accuracy, completeness, helpfulness, specificity.
- Tool output IS evidence: when the agent mentions tool results (command output, file reads, test results), treat them as verified evidence.
- Self-scoring is expected: don't penalize self-assessments, verify them.
$CONTEXT_SECTION
WHAT THE AGENT DID (agent's own summary):
$ASSISTANT_T
$DIFF_SECTION
RESPOND IN EXACTLY THIS FORMAT (no markdown, no extra text):
SCORE: X/10
ISSUES:
- issue 1
- issue 2
- issue 3
VERDICT: PASS or FAIL
PROMPT_EOF
)"

# Call gemini CLI. Use plan mode (read-only), text output for direct parse.
# 2>/dev/null suppresses warnings + MCP noise; any error surfaces via exit code.
RAW_OUT="$(printf '%s' "$PROMPT" | gemini --prompt "" --approval-mode plan --output-format json 2>/dev/null || true)"

if [ -z "$RAW_OUT" ]; then
  echo "ERROR: gemini CLI returned no output. Check 'gemini' is authenticated (run 'gemini' interactively once to login)." >&2
  exit 2
fi

# Strip pre-JSON noise (MCP/skill warnings print to stdout before JSON), parse response.
RESULT="$(printf '%s' "$RAW_OUT" | python3 -c "
import json, sys
raw = sys.stdin.read()
i = raw.find('{')
if i < 0:
    print('ERROR: no JSON in gemini output', file=sys.stderr)
    print(raw, file=sys.stderr)
    sys.exit(3)
try:
    d = json.loads(raw[i:])
except json.JSONDecodeError as e:
    print(f'ERROR: gemini JSON parse failed: {e}', file=sys.stderr)
    print(raw[i:i+500], file=sys.stderr)
    sys.exit(3)
print(d.get('response', '').strip())
")"
RC=$?
if [ "$RC" -ne 0 ]; then
  exit "$RC"
fi

# Parse score for banner.
SCORE="$(printf '%s' "$RESULT" | awk '/^SCORE:/ {split($2,a,"/"); print a[1]; exit}')"

if [ -n "$SCORE" ]; then
  echo ""
  echo "========================================"
  echo "  BOUNCER AUDIT: $SCORE/10"
  echo "========================================"
  echo ""
fi

printf '%s\n' "$RESULT"
