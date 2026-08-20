#!/usr/bin/env python3
"""Small executable fixture set for the Gemini guard."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


GUARD = Path(__file__).with_name("guard.py")


def run(payload: object, **env: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(GUARD)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        env={**os.environ, **env},
        check=False,
    )


class GuardTest(unittest.TestCase):
    bad = {
        "hook_event_name": "BeforeTool",
        "tool_name": "run_shell_command",
        "tool_input": {"command": "git worktree add --no-checkout /tmp/wt"},
    }

    def test_safe_command_passes(self) -> None:
        self.assertEqual(run({**self.bad, "tool_input": {"command": "git status"}}).returncode, 0)

    def test_violation_warns_by_default(self) -> None:
        result = run(self.bad)
        self.assertEqual(result.returncode, 0)
        self.assertIn("WARN", result.stderr)

    def test_enforcement_blocks(self) -> None:
        self.assertEqual(run(self.bad, GEMINI_WORKTREE_ENFORCE="1").returncode, 2)

    def test_meaningful_ack_overrides(self) -> None:
        result = run(self.bad, GEMINI_WORKTREE_ENFORCE="1", GEMINI_WORKTREE_ACK="reason: deliberate sparse docs checkout")
        self.assertEqual(result.returncode, 0)
        self.assertIn("ACK accepted", result.stderr)

    def test_invalid_input_fails_open(self) -> None:
        result = subprocess.run(["python3", str(GUARD)], input="not-json", text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0)

    def test_precompress_injects_once_on_next_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = {"GEMINI_GUARD_STATE_DIR": tmp}
            pre = run({"hook_event_name": "PreCompress", "session_id": "s", "trigger": "auto"}, **env)
            first = run({"hook_event_name": "BeforeAgent", "session_id": "s"}, **env)
            second = run({"hook_event_name": "BeforeAgent", "session_id": "s"}, **env)
        self.assertIn("checkpoint", pre.stdout)
        self.assertIn("additionalContext", first.stdout)
        self.assertEqual(second.stdout, "")


if __name__ == "__main__":
    unittest.main()
