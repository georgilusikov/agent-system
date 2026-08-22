#!/usr/bin/env python3
"""Metadata-only memory candidates: inbox, review, promotion, retrieval."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping

if __package__:
    from .runtime_receipts import ReceiptContext, emit_change, file_hash, preflight
else:
    from runtime_receipts import ReceiptContext, emit_change, file_hash, preflight


class MemoryCandidateError(ValueError):
    """Base error for untrusted candidate or ledger data."""


class CandidateValidationError(MemoryCandidateError):
    """Candidate or receipt metadata violates the bounded contract."""


class CandidateConflictError(MemoryCandidateError):
    """A duplicate or contradictory candidate would be written."""


class CandidateIntegrityError(MemoryCandidateError):
    """The append-only candidate ledger is damaged or ambiguous."""


ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
CANDIDATE_ID = re.compile(r"mem-[A-Za-z0-9][A-Za-z0-9._:-]{0,95}\Z")
REF = re.compile(r"(?:receipt|test|check|bead|commit|id):[A-Za-z0-9._:/-]{1,127}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")
FORBIDDEN = ("prompt", "response", "transcript", "payload", "credential", "secret", "token", "environment")
KINDS = frozenset({"incident", "learning", "approach", "fact", "procedure", "external_pointer"})
SCOPES = frozenset({"global", "project", "session"})
ACTIONS = frozenset({"created", "reviewed", "approved", "rejected", "superseded", "rolled_back"})
EVENT_FIELDS = frozenset({
    "event_id", "candidate_id", "action", "actor", "evidence_ref", "occurred_at",
    "data", "previous_event_hash", "event_hash",
})
REQUIRED_CANDIDATE_FIELDS = frozenset({
    "candidate_id", "topic", "kind", "scope", "project", "owner", "statement",
    "applicability", "limits", "source_receipt", "source_hash", "result_metric",
    "evidence_refs", "contradicts", "supersedes", "created_at", "redaction_status",
})


def create_candidate(
    ledger: Path,
    candidate: Mapping[str, Any],
    receipt: Mapping[str, Any],
    *,
    repo_root: Path,
    receipt_context: ReceiptContext | None = None,
) -> dict[str, Any]:
    """Put one verified, redacted candidate in the external inbox."""
    data = dict(candidate)
    _validate_candidate(data)
    _validate_receipt(receipt)
    if data["source_receipt"] != f"receipt:{receipt['event_id']}":
        raise CandidateValidationError("candidate source receipt does not match the verified receipt")
    if data["source_hash"] != receipt["receipt_hash"]:
        raise CandidateValidationError("candidate source hash does not match the verified receipt")
    root = _resolved_root(repo_root)
    event_id = _receipt_event_id(receipt_context, "create", data["candidate_id"])
    existing_receipt = preflight(receipt_context, event_id) if receipt_context else None
    with _locked(ledger, root) as path:
        events = _read_events(path)
        before_hash = file_hash(path) if path.exists() else None
        candidate_id = data["candidate_id"]
        states = _states(events)
        if candidate_id in states:
            if existing_receipt is not None and _recoverable(events, candidate_id, "created", "system", data):
                return states[candidate_id]
            if _recoverable(events, candidate_id, "created", "system", data) and existing_receipt is None:
                _emit_receipt(receipt_context, "create", candidate_id, None, file_hash(path))
                return states[candidate_id]
            raise CandidateConflictError("candidate id already exists")
        _check_create_conflict(data, states)
        _append_event(path, events, candidate_id, "created", "system", data["source_receipt"], data)
        _emit_receipt(receipt_context, "create", candidate_id, before_hash, file_hash(path))
        return _states(_read_events(path))[candidate_id]


def review_candidate(
    ledger: Path,
    candidate_id: str,
    *,
    decision: str,
    reviewer_id: str,
    evidence_ref: str,
    repo_root: Path,
    receipt_context: ReceiptContext | None = None,
) -> dict[str, Any]:
    """Move a draft to reviewed or rejected; owner approval is separate."""
    _validate_id(candidate_id, CANDIDATE_ID, "candidate_id")
    _validate_id(reviewer_id, ID, "reviewer_id")
    _validate_ref(evidence_ref)
    if decision not in {"reviewed", "rejected"}:
        raise CandidateValidationError("review decision is invalid")
    root = _resolved_root(repo_root)
    event_id = _receipt_event_id(receipt_context, "review", candidate_id)
    existing_receipt = preflight(receipt_context, event_id) if receipt_context else None
    with _locked(ledger, root) as path:
        events = _read_events(path)
        before_hash = file_hash(path)
        state = _require_state(_states(events), candidate_id)
        if state["status"] != "draft":
            if (existing_receipt is not None and state["status"] in {"reviewed", "rejected"}
                    and _recoverable(events, candidate_id,
                                     "reviewed" if decision == "reviewed" else "rejected",
                                     reviewer_id, evidence_ref)):
                return state
            if (state["status"] in {"reviewed", "rejected"} and existing_receipt is None
                    and _recoverable(events, candidate_id, "reviewed" if decision == "reviewed" else "rejected",
                                     reviewer_id, evidence_ref)):
                _emit_receipt(receipt_context, "review", candidate_id, None, file_hash(path))
                return state
            raise CandidateValidationError("only draft candidates can be reviewed")
        action = "reviewed" if decision == "reviewed" else "rejected"
        _append_event(path, events, candidate_id, action, reviewer_id, evidence_ref)
        _emit_receipt(receipt_context, "review", candidate_id, before_hash, file_hash(path))
        return _states(_read_events(path))[candidate_id]


def approve_candidate(
    ledger: Path,
    candidate_id: str,
    *,
    owner_id: str,
    evidence_ref: str,
    repo_root: Path,
    receipt_context: ReceiptContext | None = None,
) -> dict[str, Any]:
    """Promote only a reviewed candidate after explicit owner approval."""
    _validate_id(candidate_id, CANDIDATE_ID, "candidate_id")
    _validate_id(owner_id, ID, "owner_id")
    _validate_ref(evidence_ref)
    root = _resolved_root(repo_root)
    event_id = _receipt_event_id(receipt_context, "approve", candidate_id)
    existing_receipt = preflight(receipt_context, event_id) if receipt_context else None
    with _locked(ledger, root) as path:
        events = _read_events(path)
        before_hash = file_hash(path)
        states = _states(events)
        state = _require_state(states, candidate_id)
        if state["status"] != "reviewed":
            if (existing_receipt is not None and state["status"] == "approved"
                    and _recoverable(events, candidate_id, "approved", owner_id, evidence_ref)):
                return state
            if (state["status"] == "approved" and existing_receipt is None
                    and _recoverable(events, candidate_id, "approved", owner_id, evidence_ref)):
                _emit_receipt(receipt_context, "approve", candidate_id, None, file_hash(path))
                return state
            raise CandidateValidationError("only reviewed candidates can be approved")
        if state["owner"] != owner_id:
            raise CandidateValidationError("only the owner can approve a candidate")
        supersedes = state["supersedes"]
        for other_id, other in states.items():
            if other_id == candidate_id or other.get("rolled_back"):
                continue
            if other["status"] != "approved" or not _same_topic(state, other):
                continue
            if supersedes != other_id:
                raise CandidateConflictError("approved candidates contradict on the same topic")
        if supersedes is not None:
            old = _require_state(states, supersedes)
            if old["status"] != "approved" or not _same_topic(state, old):
                raise CandidateValidationError("superseded candidate is not an approved matching note")
        _append_event(path, events, candidate_id, "approved", owner_id, evidence_ref)
        if supersedes is not None:
            _append_event(path, _read_events(path), supersedes, "superseded", owner_id, evidence_ref)
        _emit_receipt(receipt_context, "approve", candidate_id, before_hash, file_hash(path))
        return _states(_read_events(path))[candidate_id]


def rollback_candidate(
    ledger: Path,
    candidate_id: str,
    *,
    actor_id: str,
    evidence_ref: str,
    repo_root: Path,
    receipt_context: ReceiptContext | None = None,
) -> dict[str, Any]:
    """Revoke retrieval without rewriting history or changing global canon."""
    _validate_id(candidate_id, CANDIDATE_ID, "candidate_id")
    _validate_id(actor_id, ID, "actor_id")
    _validate_ref(evidence_ref)
    root = _resolved_root(repo_root)
    event_id = _receipt_event_id(receipt_context, "rollback", candidate_id)
    existing_receipt = preflight(receipt_context, event_id) if receipt_context else None
    with _locked(ledger, root) as path:
        events = _read_events(path)
        before_hash = file_hash(path)
        state = _require_state(_states(events), candidate_id)
        if state["status"] not in {"reviewed", "approved"} or state.get("rolled_back"):
            if (existing_receipt is not None and state.get("rolled_back")
                    and _recoverable(events, candidate_id, "rolled_back", actor_id, evidence_ref)):
                return state
            if (state.get("rolled_back") and existing_receipt is None
                    and _recoverable(events, candidate_id, "rolled_back", actor_id, evidence_ref)):
                _emit_receipt(receipt_context, "rollback", candidate_id, None, file_hash(path))
                return state
            raise CandidateValidationError("only active reviewed or approved notes can be rolled back")
        _append_event(path, events, candidate_id, "rolled_back", actor_id, evidence_ref)
        _emit_receipt(receipt_context, "rollback", candidate_id, before_hash, file_hash(path))
        return _states(_read_events(path))[candidate_id]


def _emit_receipt(context: ReceiptContext | None, action: str, candidate_id: str,
                  before_hash: str | None, after_hash: str) -> None:
    if context is None:
        return
    event_id = _receipt_event_id(context, action, candidate_id)
    emit_change(context, event_id, f"memory.{action}", "class:memory-ledger",
                before_hash, after_hash, "applied")


def _receipt_event_id(context: ReceiptContext | None, action: str, candidate_id: str) -> str:
    if context is None:
        return ""
    return "memory-" + hashlib.sha256(
        f"{context.run_id}:memory.{action}:{candidate_id}".encode()).hexdigest()


def _recoverable(events: list[dict[str, Any]], candidate_id: str, action: str,
                 actor: str, evidence: Any) -> bool:
    if not events:
        return False
    event = events[-1]
    if action == "created":
        return (event["candidate_id"] == candidate_id and event["action"] == action
                and event["actor"] == actor and event["data"] == evidence
                and event["evidence_ref"] == evidence["source_receipt"])
    return (event["candidate_id"] == candidate_id and event["action"] == action
            and event["actor"] == actor and event["evidence_ref"] == evidence)


def retrieve_current(
    ledger: Path,
    *,
    scope: str,
    project: str | None = None,
    repo_root: Path,
) -> list[dict[str, Any]]:
    """Return approved, non-superseded, non-rolled-back notes for one scope."""
    if scope not in SCOPES:
        raise CandidateValidationError("scope is invalid")
    if project is not None:
        _validate_id(project, ID, "project")
    root = _resolved_root(repo_root)
    path = _external_ledger(ledger, root)
    states = _states(_read_events(path))
    return sorted(
        [
            state for state in states.values()
            if state["status"] == "approved"
            and not state.get("rolled_back")
            and state["scope"] == scope
            and state["project"] == project
        ],
        key=lambda item: item["candidate_id"],
    )


def _validate_candidate(data: Mapping[str, Any]) -> None:
    if set(data) != REQUIRED_CANDIDATE_FIELDS:
        raise CandidateValidationError("candidate fields do not match the contract")
    _validate_id(data["candidate_id"], CANDIDATE_ID, "candidate_id")
    _validate_id(data["topic"], ID, "topic")
    if data["kind"] not in KINDS or data["scope"] not in SCOPES:
        raise CandidateValidationError("candidate kind or scope is invalid")
    project = data["project"]
    if data["scope"] == "global" and project is not None:
        raise CandidateValidationError("global candidates cannot carry a project")
    if data["scope"] != "global" and project is None:
        raise CandidateValidationError("project/session candidates need a project")
    if project is not None:
        _validate_id(project, ID, "project")
    _validate_id(data["owner"], ID, "owner")
    for field, limit in (("statement", 320), ("applicability", 180), ("limits", 180)):
        _validate_text(data[field], field, limit)
    if data["result_metric"] is not None:
        _validate_text(data["result_metric"], "result_metric", 160)
    _validate_ref(data["source_receipt"])
    if not _matches(SHA256, data["source_hash"]):
        raise CandidateValidationError("source_hash is invalid")
    refs = data["evidence_refs"]
    if not isinstance(refs, list) or not 1 <= len(refs) <= 8:
        raise CandidateValidationError("evidence_refs are invalid")
    for reference in refs:
        _validate_ref(reference)
    contradictions = data["contradicts"]
    if not isinstance(contradictions, list) or len(contradictions) > 8:
        raise CandidateValidationError("contradicts is invalid")
    for candidate_id in contradictions:
        _validate_id(candidate_id, CANDIDATE_ID, "contradicts")
    supersedes = data["supersedes"]
    if supersedes is not None:
        _validate_id(supersedes, CANDIDATE_ID, "supersedes")
    if not _matches(UTC, data["created_at"]) or data["redaction_status"] != "redacted":
        raise CandidateValidationError("created_at or redaction_status is invalid")


def _validate_receipt(receipt: Mapping[str, Any]) -> None:
    if not isinstance(receipt, Mapping):
        raise CandidateValidationError("receipt must be metadata mapping")
    _reject_private(receipt)
    if receipt.get("outcome") != "verified" or receipt.get("redaction_status") != "metadata-only":
        raise CandidateValidationError("candidate source receipt must be verified metadata")
    for field in ("event_id", "run_id"):
        _validate_id(receipt.get(field), ID, field)
    if not _matches(SHA256, receipt.get("receipt_hash")):
        raise CandidateValidationError("receipt hash is invalid")
    refs = receipt.get("evidence_refs")
    if not isinstance(refs, list) or len(refs) > 32:
        raise CandidateValidationError("receipt evidence is invalid")
    for reference in refs:
        _validate_ref(reference)


def _check_create_conflict(data: Mapping[str, Any], states: Mapping[str, dict[str, Any]]) -> None:
    for state in states.values():
        if state.get("rolled_back") or state["status"] in {"rejected", "superseded"}:
            continue
        if not _same_topic(data, state):
            continue
        if data["supersedes"] == state["candidate_id"]:
            continue
        if data["statement"] == state["statement"] and data["source_hash"] == state["source_hash"]:
            raise CandidateConflictError("duplicate active candidate")
        raise CandidateConflictError("contradictory active candidate")


def _same_topic(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    return left["topic"] == right["topic"] and left["scope"] == right["scope"] and left["project"] == right["project"]


def _states(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    states: dict[str, dict[str, Any]] = {}
    for event in events:
        candidate_id = event["candidate_id"]
        action = event["action"]
        if action == "created":
            if candidate_id in states or not isinstance(event["data"], dict):
                raise CandidateIntegrityError("candidate creation is duplicated or malformed")
            try:
                _validate_candidate(event["data"])
            except CandidateValidationError as error:
                raise CandidateIntegrityError("persisted candidate payload is invalid") from error
            if event["data"]["candidate_id"] != candidate_id:
                raise CandidateIntegrityError("candidate event and payload ids differ")
            states[candidate_id] = {**event["data"], "status": "draft", "rolled_back": False}
            continue
        state = _require_state(states, candidate_id)
        if action == "reviewed":
            if state["status"] != "draft":
                raise CandidateIntegrityError("reviewed event has an invalid predecessor")
            state["status"] = "reviewed"
            state["reviewed_by"] = event["actor"]
        elif action == "approved":
            if state["status"] != "reviewed" or event["actor"] != state["owner"]:
                raise CandidateIntegrityError("approved event lacks review or owner approval")
            state["status"] = "approved"
            state["approved_by"] = event["actor"]
        elif action == "rejected":
            if state["status"] not in {"draft", "reviewed"}:
                raise CandidateIntegrityError("rejected event has an invalid predecessor")
            state["status"] = "rejected"
        elif action == "superseded":
            if state["status"] != "approved":
                raise CandidateIntegrityError("superseded event has an invalid predecessor")
            state["status"] = "superseded"
        elif action == "rolled_back":
            if state["status"] not in {"reviewed", "approved"} or state.get("rolled_back"):
                raise CandidateIntegrityError("rollback event has an invalid predecessor")
            state["rolled_back"] = True
        else:
            raise CandidateIntegrityError("unknown candidate action")
    return states


def _require_state(states: Mapping[str, dict[str, Any]], candidate_id: str) -> dict[str, Any]:
    try:
        return states[candidate_id]
    except KeyError as error:
        raise CandidateValidationError("candidate does not exist") from error


def _append_event(
    path: Path,
    events: list[dict[str, Any]],
    candidate_id: str,
    action: str,
    actor: str,
    evidence_ref: str,
    data: Mapping[str, Any] | None = None,
) -> None:
    event = {
        "event_id": f"memory:{candidate_id}:{action}:{len(events) + 1}",
        "candidate_id": candidate_id,
        "action": action,
        "actor": actor,
        "evidence_ref": evidence_ref,
        "occurred_at": _now(),
        "data": dict(data) if data is not None else None,
        "previous_event_hash": events[-1]["event_hash"] if events else None,
    }
    event["event_hash"] = _event_hash(event)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    os.chmod(path, 0o600)
    with os.fdopen(descriptor, "a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def _read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise CandidateIntegrityError("memory ledger is unreadable") from error
    events: list[dict[str, Any]] = []
    event_ids: set[str] = set()
    previous_hash: str | None = None
    for line in lines:
        if not line:
            raise CandidateIntegrityError("memory ledger contains an empty line")
        try:
            event = json.loads(line, object_pairs_hook=_unique_object)
        except (json.JSONDecodeError, _DuplicateKeyError) as error:
            raise CandidateIntegrityError("memory ledger contains invalid JSON") from error
        if not isinstance(event, dict) or set(event) != EVENT_FIELDS:
            raise CandidateIntegrityError("memory event fields are invalid")
        _reject_private(event)
        if event["event_id"] in event_ids or not _matches(ID, event["event_id"]):
            raise CandidateIntegrityError("memory event id is duplicated or invalid")
        if event["action"] not in ACTIONS or not _matches(ID, event["candidate_id"]):
            raise CandidateIntegrityError("memory event action or candidate is invalid")
        _validate_id(event["actor"], ID, "event actor")
        _validate_ref(event["evidence_ref"])
        if not _matches(UTC, event["occurred_at"]):
            raise CandidateIntegrityError("memory event timestamp is invalid")
        if event["previous_event_hash"] != previous_hash or event["event_hash"] != _event_hash(event):
            raise CandidateIntegrityError("memory event hash chain is invalid")
        event_ids.add(event["event_id"])
        events.append(event)
        previous_hash = event["event_hash"]
    return events


@contextmanager
def _locked(ledger: Path, root: Path) -> Iterator[Path]:
    path = _external_ledger(ledger, root)
    lock_path = path.with_name(f"{path.name}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(lock_path, os.O_WRONLY | os.O_CREAT, 0o600)
    os.chmod(lock_path, 0o600)
    with os.fdopen(descriptor, "a", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            yield path
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _external_ledger(ledger: Path, root: Path) -> Path:
    if not isinstance(ledger, Path):
        raise CandidateValidationError("ledger must be a Path")
    try:
        path = ledger.resolve(strict=False)
        path.relative_to(root)
    except ValueError:
        return path
    except (OSError, RuntimeError) as error:
        raise CandidateValidationError("ledger path is unreadable") from error
    raise CandidateValidationError("memory ledger must be outside the canonical repository")


def _resolved_root(repo_root: Path) -> Path:
    try:
        return repo_root.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise CandidateValidationError("repository root is unreadable") from error


def _event_hash(event: Mapping[str, Any]) -> str:
    body = {key: value for key, value in event.items() if key != "event_hash"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError("duplicate JSON key")
        result[key] = value
    return result


class _DuplicateKeyError(ValueError):
    pass


def _reject_private(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if _private(str(key)):
                raise CandidateValidationError("forbidden metadata field")
            _reject_private(nested)
    elif isinstance(value, list):
        for nested in value:
            _reject_private(nested)
    elif isinstance(value, str) and _private(value):
        raise CandidateValidationError("forbidden metadata content")


def _private(value: str) -> bool:
    lowered = value.lower()
    return any(part in lowered for part in FORBIDDEN)


def _validate_text(value: Any, field: str, limit: int) -> None:
    if not isinstance(value, str) or not 1 <= len(value) <= limit or "\n" in value or "\r" in value:
        raise CandidateValidationError(f"{field} is invalid")
    if _private(value):
        raise CandidateValidationError(f"{field} contains forbidden content")


def _validate_id(value: Any, pattern: re.Pattern[str], field: str) -> None:
    if not _matches(pattern, value):
        raise CandidateValidationError(f"{field} is invalid")


def _validate_ref(value: Any) -> None:
    if not _matches(REF, value) or _private(value):
        raise CandidateValidationError("evidence reference is invalid")


def _matches(pattern: re.Pattern[str], value: Any) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
