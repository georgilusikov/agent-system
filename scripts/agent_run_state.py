#!/usr/bin/env python3
"""Metadata-only, crash-safe state for one bounded agent run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Iterable, Mapping


STATE_FIELDS = frozenset({
    "run_id", "goal_fingerprint", "bead_id", "phase", "last_verified_step",
    "attempt", "retry_budget", "next_action", "status", "source_commit",
    "evidence_refs", "redaction_status", "operation_receipts",
})
OPERATION_RECEIPT_FIELDS = frozenset({"key_fingerprint", "operation_fingerprint"})
FORBIDDEN_FIELD_PARTS = (
    "prompt", "response", "transcript", "payload", "credential", "secret", "token",
    "environment",
)
PHASES = ("planned", "ready", "running", "verifying")
OUTCOMES = ("accepted", "partial", "blocked", "escalated", "failed")


class StateError(ValueError):
    """Base class for state that must not be trusted."""


class MalformedStateError(StateError):
    """Persisted data is incomplete, unsafe, or not valid metadata."""


class StateConflictError(StateError):
    """A caller expected a different current state."""


class IllegalTransitionError(StateError):
    """A requested lifecycle transition is not permitted."""


def goal_fingerprint(*, opaque_id: str | None = None,
                     redacted_goal_metadata: Mapping[str, Any] | None = None) -> str:
    """Return a stable hash without serializing a raw goal."""
    if (opaque_id is None) == (redacted_goal_metadata is None):
        raise StateError("provide exactly one opaque_id or redacted_goal_metadata")
    source: Any = {"opaque_id": opaque_id} if opaque_id is not None else redacted_goal_metadata
    _reject_forbidden_fields(source)
    return hashlib.sha256(json.dumps(source, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def create_run(path: Path, *, run_id: str, bead_id: str, source_commit: str,
               opaque_goal_id: str | None = None,
               redacted_goal_metadata: Mapping[str, Any] | None = None,
               retry_budget: int = 0) -> dict[str, Any]:
    """Create a planned run, returning an existing identical run unchanged."""
    if retry_budget < 0:
        raise StateError("retry_budget must be non-negative")
    state = {
        "run_id": run_id,
        "goal_fingerprint": goal_fingerprint(
            opaque_id=opaque_goal_id, redacted_goal_metadata=redacted_goal_metadata),
        "bead_id": bead_id,
        "phase": "planned",
        "last_verified_step": None,
        "attempt": 0,
        "retry_budget": retry_budget,
        "next_action": "start",
        "status": "planned",
        "source_commit": source_commit,
        "evidence_refs": [],
        "redaction_status": "metadata-only",
        "operation_receipts": [],
    }
    if path.exists():
        current = load_state(path)
        if current == state:
            return current
        raise StateConflictError("run state already exists with different metadata")
    write_state(path, state)
    return state


def start_run(path: Path, *, operation_key: str | None = None) -> dict[str, Any]:
    """Move a planned run to running; repeated starts are no-ops."""
    state = load_state(path)
    if _record_operation(state, operation_key, "start", {}):
        return state
    if state["phase"] == "running":
        if operation_key is not None:
            write_state(path, state)
        return state
    if state["phase"] != "planned":
        raise IllegalTransitionError(f"cannot start from {state['phase']}")
    _transition(state, "ready")
    _transition(state, "running")
    state["next_action"] = "verify step 1"
    write_state(path, state)
    return state


def record_verified_step(path: Path, step: int, *, evidence_refs: Iterable[str] = (),
                         operation_key: str | None = None) -> dict[str, Any]:
    """Record the next verified step once; duplicate operations are no-ops."""
    if isinstance(step, bool) or step < 1:
        raise StateError("step must be positive")
    state = load_state(path)
    refs = list(evidence_refs)
    if not all(isinstance(ref, str) for ref in refs):
        raise MalformedStateError("evidence_refs must contain strings")
    if _record_operation(state, operation_key, "verify", {"step": step, "evidence_refs": refs}):
        return state
    previous = state["last_verified_step"]
    if previous == step:
        if operation_key is not None:
            write_state(path, state)
        return state
    if previous is not None and step != previous + 1:
        raise StateConflictError("verified steps must be consecutive")
    if previous is None and step != 1:
        raise StateConflictError("first verified step must be 1")
    if state["phase"] not in {"running", "verifying"}:
        raise IllegalTransitionError(f"cannot verify from {state['phase']}")
    if state["phase"] == "running":
        _transition(state, "verifying")
    state.update(last_verified_step=step, evidence_refs=refs, next_action=f"verify step {step + 1}")
    write_state(path, state)
    return state


def resume_run(path: Path, *, expected_source_commit: str | None = None) -> dict[str, Any]:
    """Return trusted state with the next unverified step selected."""
    state = load_state(path)
    if expected_source_commit is not None and state["source_commit"] != expected_source_commit:
        raise StateConflictError("stale state source_commit")
    if state["phase"] not in {"running", "verifying"}:
        raise IllegalTransitionError(f"cannot resume from {state['phase']}")
    next_step = (state["last_verified_step"] or 0) + 1
    state["next_action"] = f"verify step {next_step}"
    write_state(path, state)
    return state


def finish_run(path: Path, outcome: str, *, evidence_refs: Iterable[str] = (),
               operation_key: str | None = None) -> dict[str, Any]:
    """Finish only after verification with an allowed outcome."""
    if outcome not in OUTCOMES:
        raise IllegalTransitionError(f"unknown outcome: {outcome}")
    state = load_state(path)
    refs = list(evidence_refs)
    if not all(isinstance(ref, str) for ref in refs):
        raise MalformedStateError("evidence_refs must contain strings")
    if _record_operation(state, operation_key, "finish", {"outcome": outcome, "evidence_refs": refs}):
        return state
    if state["phase"] == outcome:
        if operation_key is not None:
            write_state(path, state)
        return state
    if state["phase"] != "verifying":
        raise IllegalTransitionError(f"cannot finish from {state['phase']}")
    _transition(state, outcome)
    state.update(evidence_refs=refs, next_action=None)
    write_state(path, state)
    return state


def load_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise MalformedStateError("state is unreadable") from error
    _validate_state(data)
    return data


def write_state(path: Path, state: Mapping[str, Any]) -> None:
    data = dict(state)
    _validate_state(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(data, stream, sort_keys=True, separators=(",", ":"))
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _validate_state(data: Any) -> None:
    if not isinstance(data, dict) or set(data) != STATE_FIELDS:
        raise MalformedStateError("state fields do not match metadata-only contract")
    _reject_forbidden_fields(data)
    for field in ("run_id", "bead_id", "source_commit"):
        if not _is_nonempty_string(data[field]):
            raise MalformedStateError(f"{field} must be a non-empty string")
    if not _is_fingerprint(data["goal_fingerprint"]):
        raise MalformedStateError("goal_fingerprint must be a SHA-256 fingerprint")
    if data["phase"] not in (*PHASES, *OUTCOMES) or data["status"] != data["phase"]:
        raise MalformedStateError("invalid phase or status")
    if data["last_verified_step"] is not None and not _is_nonnegative_int(data["last_verified_step"]):
        raise MalformedStateError("last_verified_step must be an integer or null")
    if not _is_nonnegative_int(data["attempt"]) or not _is_nonnegative_int(data["retry_budget"]):
        raise MalformedStateError("attempt and retry_budget must be non-negative integers")
    if data["attempt"] > data["retry_budget"]:
        raise MalformedStateError("attempt exceeds retry_budget")
    if not isinstance(data["evidence_refs"], list) or not all(_is_nonempty_string(ref) for ref in data["evidence_refs"]):
        raise MalformedStateError("evidence_refs must be a list of non-empty strings")
    if data["redaction_status"] != "metadata-only":
        raise MalformedStateError("redaction_status must be metadata-only")
    if not isinstance(data["operation_receipts"], list):
        raise MalformedStateError("operation_receipts must be a list")
    for receipt in data["operation_receipts"]:
        if not isinstance(receipt, dict) or set(receipt) != OPERATION_RECEIPT_FIELDS:
            raise MalformedStateError("invalid operation receipt")
        if not all(_is_fingerprint(value) for value in receipt.values()):
            raise MalformedStateError("invalid operation receipt fingerprint")
    if len({receipt["key_fingerprint"] for receipt in data["operation_receipts"]}) != len(data["operation_receipts"]):
        raise MalformedStateError("duplicate operation receipt key")
    _validate_phase_invariants(data)


def _validate_phase_invariants(data: Mapping[str, Any]) -> None:
    phase = data["phase"]
    step = data["last_verified_step"]
    next_action = data["next_action"]
    if phase in {"planned", "ready", "running"} and step is not None:
        raise MalformedStateError("unverified phase has a verified step")
    if phase in {"verifying", *OUTCOMES} and not step:
        raise MalformedStateError("verified phase needs a verified step")
    expected_actions = {"planned": "start", "ready": "start", "running": "verify step 1"}
    if phase in expected_actions:
        if next_action != expected_actions[phase]:
            raise MalformedStateError("invalid next_action for phase")
    elif phase == "verifying":
        if next_action != f"verify step {step + 1}":
            raise MalformedStateError("invalid next_action for verified step")
    elif next_action is not None:
        raise MalformedStateError("finished state must not have next_action")


def _transition(state: dict[str, Any], target: str) -> None:
    current = state["phase"]
    allowed = PHASES[PHASES.index(current) + 1] if current in PHASES[:-1] else None
    if target != allowed and not (current == "verifying" and target in OUTCOMES):
        raise IllegalTransitionError(f"illegal transition: {current} -> {target}")
    state["phase"] = target
    state["status"] = target


def _record_operation(state: dict[str, Any], operation_key: str | None, kind: str,
                      details: Mapping[str, Any]) -> bool:
    """Record opaque key fingerprints; return true for an identical retry."""
    if operation_key is None:
        return False
    if not isinstance(operation_key, str) or not operation_key:
        raise StateError("operation_key must be a non-empty opaque string")
    key_fingerprint = _fingerprint({"operation_key": operation_key})
    operation_fingerprint = _fingerprint({"kind": kind, "details": details})
    for receipt in state["operation_receipts"]:
        if receipt["key_fingerprint"] != key_fingerprint:
            continue
        if receipt["operation_fingerprint"] != operation_fingerprint:
            raise StateConflictError("operation_key was reused for a different operation")
        return True
    state["operation_receipts"].append({
        "key_fingerprint": key_fingerprint,
        "operation_fingerprint": operation_fingerprint,
    })
    return False


def _fingerprint(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _is_nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _is_fingerprint(value: Any) -> bool:
    return _is_nonempty_string(value) and len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _reject_forbidden_fields(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if any(part in str(key).lower() for part in FORBIDDEN_FIELD_PARTS):
                raise MalformedStateError("forbidden metadata field")
            _reject_forbidden_fields(nested)
    elif isinstance(value, (list, tuple)):
        for nested in value:
            _reject_forbidden_fields(nested)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    state = resume_run(args.state) if args.resume else load_state(args.state)
    print(json.dumps(state, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
