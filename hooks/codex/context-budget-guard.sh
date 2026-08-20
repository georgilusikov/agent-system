#!/bin/sh
[ "${AI_MGMT_HOOKS:-1}" = "0" ] && exit 0
# UserPromptSubmit: ratio-based context warning; periodic checkpoint for /goal.
INPUT=$(cat)
exec python3 - "$INPUT" <<'PY'
import hashlib
import json
import os
import re
import sys
from pathlib import Path

try:
    data = json.loads(sys.argv[1])
except (json.JSONDecodeError, IndexError):
    sys.exit(0)


def env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


session_id = str(data.get("session_id") or "")
prompt = str(data.get("prompt") or "")
goal_active = os.environ.get("CBG_LONG_RUN") == "1" or bool(
    re.match(r"^\s*/goal(?:\s|$)", prompt, re.IGNORECASE)
)
goal_turns = 0

if session_id:
    state_root = Path(
        os.environ.get("CBG_STATE_DIR", Path.home() / ".cache" / "context-budget-guard")
    ) / "codex"
    state_file = state_root / (hashlib.sha256(session_id.encode()).hexdigest()[:32] + ".json")
    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        state = {}
    goal_active = goal_active or bool(state.get("goal_active"))
    if goal_active:
        goal_turns = int(state.get("goal_turns", 0)) + 1
        state_root.mkdir(mode=0o700, parents=True, exist_ok=True)
        tmp = state_file.with_suffix(".tmp")
        tmp.write_text(
            json.dumps({"goal_active": True, "goal_turns": goal_turns}),
            encoding="utf-8",
        )
        tmp.replace(state_file)

ctx = 0
window = 0
transcript = data.get("transcript_path")
path = Path(transcript) if transcript else None
if path and path.exists():
    size = path.stat().st_size
    with path.open("rb") as handle:
        if size > 262_144:
            handle.seek(-262_144, 2)
        tail = handle.read().decode("utf-8", errors="replace")
    for line in reversed(tail.splitlines()):
        if '"token_count"' not in line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        info = (record.get("payload") or {}).get("info") or {}
        usage = info.get("last_token_usage") or {}
        if usage:
            ctx = int(usage.get("input_tokens", 0) or 0)
            window = int(info.get("model_context_window", 0) or 0)
            break

warn_ratio = 0.70 if goal_active else 0.50
hard_ratio = 0.90 if goal_active else 0.80
warn = env_int("CBG_WARN", int(window * warn_ratio) if window else 120_000)
hard = env_int("CBG_HARD", int(window * hard_ratio) if window else 200_000)

if ctx >= hard:
    if goal_active:
        print(
            f"CONTEXT BUDGET HARD LIMIT: last call carried {ctx:,} input tokens. "
            "Finish the current kill milestone, persist compact state, allow compaction, "
            "reread the compact state, and continue in the same task. Context rollover "
            "does not block an active goal."
        )
    else:
        print(
            f"CONTEXT BUDGET HARD LIMIT: last call carried {ctx:,} input tokens. "
            "Do not start new subtasks; finish the milestone, prepare a compact handoff, "
            "then launch the continuation yourself in a fresh thread/session with the "
            "available native transport. Do not ask the owner to move tabs. Keep an "
            "unfinished goal active/partial; context rollover is not a blocked goal."
        )
elif goal_turns and goal_turns % 20 == 0:
    print(
        f"GOAL CHECKPOINT {goal_turns}: verify the objective, completed milestone, decisions, "
        "checks, blockers, and whether to hand off early."
    )
elif ctx >= warn:
    if goal_active:
        print(
            f"CONTEXT BUDGET WARNING: last call carried {ctx:,} input tokens. "
            "Finish the current kill milestone, update compact state, and continue "
            "in the same task."
        )
    else:
        print(
            f"CONTEXT BUDGET WARNING: last call carried {ctx:,} input tokens. "
            "Wrap up the current milestone soon instead of adding subtasks."
        )
PY
