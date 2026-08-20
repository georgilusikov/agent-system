#!/usr/bin/env python3
"""Gemini PreCompress handoff and unsafe partial-worktree warning."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


BAD_WORKTREE = re.compile(
    r"\bgit\b[^\n]*\bworktree\s+add\b[^\n]*(?:--no-checkout|--sparse|--orphan)\b"
)
ACK = re.compile(r"^(?=.{12,})(?=.*[A-Za-z]{3,}).+[\s\-_:]+.+$")


def state_path(payload: dict[str, object], namespace: str = "gemini") -> Path | None:
    session = str(payload.get("session_id") or payload.get("conversationId") or "")
    if not session:
        return None
    root = Path(
        os.environ.get(
            "GEMINI_GUARD_STATE_DIR", Path.home() / ".cache" / "gemini-guard"
        )
    )
    digest = hashlib.sha256(session.encode()).hexdigest()[:32]
    return root / f"{namespace}-{digest}.json"


def precompress(payload: dict[str, object]) -> int:
    path = state_path(payload)
    if path:
        try:
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            path.write_text(
                json.dumps(
                    {
                        "pending": True,
                        "trigger": payload.get("trigger"),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                ),
                encoding="utf-8",
            )
        except OSError:
            pass
    print(json.dumps({"systemMessage": "Context compression checkpoint recorded."}))
    return 0


def before_agent(payload: dict[str, object]) -> int:
    path = state_path(payload)
    if not path or not path.exists():
        return 0
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        path.unlink()
    except (OSError, json.JSONDecodeError):
        return 0
    if state.get("pending"):
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "additionalContext": (
                            "Context was compressed. Reconfirm the objective, decisions, "
                            "completed checks, and next milestone before expanding scope."
                        )
                    }
                }
            )
        )
    return 0


def before_tool(payload: dict[str, object], agy: bool = False) -> int:
    if agy:
        tool_call = payload.get("toolCall") or {}
        tool = str(tool_call.get("name") or "") if isinstance(tool_call, dict) else ""
        args = tool_call.get("args") or {} if isinstance(tool_call, dict) else {}
        command = str(args.get("CommandLine") or "") if isinstance(args, dict) else ""
    else:
        tool = str(payload.get("tool_name") or payload.get("toolName") or "")
        tool_input = payload.get("tool_input") or payload.get("toolInput") or {}
        command = str(tool_input.get("command") or "") if isinstance(tool_input, dict) else ""
    if tool not in {"run_shell_command", "run_command", "Bash"}:
        if agy:
            print('{"decision":"allow"}')
        return 0
    if not BAD_WORKTREE.search(command):
        if agy:
            print('{"decision":"allow"}')
        return 0
    reason = os.environ.get("GEMINI_WORKTREE_ACK", "").strip()
    if ACK.match(reason):
        print("[gemini-worktree] ACK accepted.", file=sys.stderr)
        if agy:
            print('{"decision":"allow"}')
        return 0
    enforce = os.environ.get("GEMINI_WORKTREE_ENFORCE") == "1"
    verdict = "BLOCK" if enforce else "WARN (Phase 1)"
    print(
        f"[gemini-worktree] {verdict}: partial worktree checkout can turn "
        "blanket staging into mass deletion. Use a complete checkout, or set "
        "GEMINI_WORKTREE_ACK to a real reason (12+ chars).",
        file=sys.stderr,
    )
    if agy:
        decision = "deny" if enforce else "allow"
        print(json.dumps({"decision": decision, "reason": "Use a complete worktree checkout."}))
        return 0
    return 2 if enforce else 0


def agy_pre(payload: dict[str, object]) -> int:
    try:
        warn = int(os.environ.get("AGY_CONTEXT_WARN_STEPS", "80"))
        steps = int(payload.get("initialNumSteps") or 0)
    except (TypeError, ValueError):
        print("{}")
        return 0
    path = state_path(payload, "agy")
    if steps < warn or not path or path.exists():
        print("{}")
        return 0
    try:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        path.write_text(json.dumps({"warnedAtSteps": steps}), encoding="utf-8")
    except OSError:
        pass
    print(
        json.dumps(
            {
                "injectSteps": [
                    {
                        "ephemeralMessage": (
                            f"Trajectory context has {steps} steps. Finish the current "
                            "milestone, persist decisions and checks, and avoid scope expansion."
                        )
                    }
                ]
            }
        )
    )
    return 0


def agy_stop(payload: dict[str, object]) -> int:
    if payload.get("fullyIdle") is False:
        print(json.dumps({"decision": "continue", "reason": "Background tasks are still active."}))
    else:
        print('{"decision":"stop"}')
    return 0


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "gemini"
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return 0
        if mode == "agy-pre":
            return agy_pre(payload)
        if mode == "agy-tool":
            return before_tool(payload, agy=True)
        if mode == "agy-stop":
            return agy_stop(payload)
        event = payload.get("hook_event_name")
        if event == "PreCompress":
            return precompress(payload)
        if event == "BeforeAgent":
            return before_agent(payload)
        if event == "BeforeTool":
            return before_tool(payload)
        return 0
    except Exception as exc:  # fail-open: hooks must not strand a session
        print(f"[gemini-guard] internal error (fail-open): {exc}", file=sys.stderr)
        if mode == "agy-tool":
            print('{"decision":"allow"}')
        elif mode == "agy-stop":
            print('{"decision":"stop"}')
        elif mode == "agy-pre":
            print("{}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
