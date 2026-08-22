#!/usr/bin/env python3
"""Focused offline checks for agent_run_state."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import agent_run_state as state


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "run.json"
        created = state.create_run(path, run_id="run-1", bead_id="gl-ejw.16", source_commit="abc", opaque_goal_id="opaque")
        assert created["phase"] == "planned"
        assert "opaque" not in path.read_text(encoding="utf-8")
        assert state.start_run(path, operation_key="start") == state.start_run(path, operation_key="start")
        try:
            state.finish_run(path, "accepted")
        except state.IllegalTransitionError:
            pass
        else:
            raise AssertionError("finish before verification did not fail")
        first = state.record_verified_step(path, 1, evidence_refs=["check:1"], operation_key="step-1")
        assert first == state.record_verified_step(path, 1, evidence_refs=["check:1"], operation_key="step-1")
        state.load_state(path)
        try:
            state.record_verified_step(path, 2, operation_key="step-1")
        except state.StateConflictError:
            pass
        else:
            raise AssertionError("conflicting operation key did not fail closed")
        assert state.resume_run(path)["next_action"] == "verify step 2"
        state.record_verified_step(path, 2, evidence_refs=["check:2"])
        assert state.finish_run(path, "accepted", operation_key="finish-1")["status"] == "accepted"
        assert state.finish_run(path, "accepted", operation_key="finish-1")["status"] == "accepted"

        atomic = Path(directory) / "atomic.json"
        state.write_state(atomic, created)
        before = atomic.read_bytes()
        with patch("agent_run_state.os.replace", side_effect=OSError("simulated")):
            try:
                state.write_state(atomic, {**created, "next_action": "changed"})
            except OSError:
                pass
        assert atomic.read_bytes() == before

        malformed = Path(directory) / "malformed.json"
        malformed.write_text("{", encoding="utf-8")
        try:
            state.load_state(malformed)
        except state.MalformedStateError:
            pass
        else:
            raise AssertionError("malformed state did not fail closed")

        for name, change in (("boolean", {"attempt": True}), ("negative", {"retry_budget": -1}),
                             ("negative-step", {"last_verified_step": -1})):
            malformed_numeric = Path(directory) / f"malformed-{name}.json"
            malformed_numeric.write_text(json.dumps({**created, **change}), encoding="utf-8")
            try:
                state.load_state(malformed_numeric)
            except state.MalformedStateError:
                pass
            else:
                raise AssertionError(f"{name} numeric value did not fail closed")

        try:
            state.goal_fingerprint(redacted_goal_metadata={"prompt": None})
        except state.MalformedStateError:
            pass
        else:
            raise AssertionError("forbidden field was accepted")
        persisted = json.loads(path.read_text(encoding="utf-8"))
        assert "step-1" not in path.read_text(encoding="utf-8")
        assert not any("prompt" in key or "secret" in key for key in persisted)
        assert not any("token" in key or "environment" in key for key in persisted)
    print("PASS metadata-only run state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
