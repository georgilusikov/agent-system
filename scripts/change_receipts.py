#!/usr/bin/env python3
"""Local, metadata-only append-only JSONL change receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


REQUIRED_FIELDS = frozenset({
    "event_id", "parent_event_id", "run_id", "actor", "runtime", "operation", "target",
    "source_commit", "before_hash", "after_hash", "outcome", "evidence_refs", "occurred_at",
    "redaction_status",
})
OPTIONAL_FIELDS = frozenset({"task_id", "bead_id", "receipt_hash", "previous_receipt_hash", "error_class"})
ALLOWED_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS
FORBIDDEN_PARTS = (
    "prompt", "response", "transcript", "payload", "credential", "secret", "token", "environment",
)
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
TARGET_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:@-]{0,252}\Z")
TARGET_CLASS = re.compile(r"[a-z][a-z0-9_-]{0,249}\Z")
RUNTIME = re.compile(r"[a-z][a-z0-9_-]{0,31}\Z")
OPERATION = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){1,3}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
GIT_SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
ERROR_CLASS = re.compile(r"[a-z][a-z0-9_-]{0,31}\Z")
UTC_RFC3339 = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\Z")
OUTCOMES = frozenset({"attempted", "applied", "verified", "failed", "partial", "blocked"})
FAILURE_OUTCOMES = frozenset({"failed", "partial", "blocked"})


class ReceiptError(ValueError):
    """Base class for receipt data that cannot be trusted."""


class ReceiptValidationError(ReceiptError):
    """The requested metadata is not an allowed receipt envelope."""


class ReceiptIntegrityError(ReceiptError):
    """The persisted append-only segment has an invalid chain."""


class ReceiptConflictError(ReceiptError):
    """An event id was reused for different metadata."""


class ReceiptDisabledError(ReceiptError):
    """The journal is intentionally disabled for new appends."""


class _DuplicateJsonKeyError(ValueError):
    """A persisted JSON object has ambiguous duplicate keys."""


def append_receipt(journal: Path, receipt: Mapping[str, Any], *, repo_root: Path) -> dict[str, Any]:
    """Append one receipt, or return its existing identical event-id retry.

    ``event_id`` is the opaque idempotency key.  A conflicting reuse fails
    closed and the journal is never rewritten.
    """
    root = _resolved_root(repo_root)
    journal = _external_journal(journal, root)
    metadata = dict(receipt)
    _validate_envelope(metadata, root, allow_hashes=False)
    records = validate_journal(journal, repo_root=root)
    for existing in records:
        if existing["event_id"] != metadata["event_id"]:
            continue
        if _without_hashes(existing) == metadata:
            return existing
        raise ReceiptConflictError("event id conflicts with existing receipt")
    if is_journal_disabled(journal, repo_root=root):
        raise ReceiptDisabledError("journal is disabled; history remains intact")
    expected_parent = records[-1]["event_id"] if records else None
    if metadata["parent_event_id"] != expected_parent:
        raise ReceiptValidationError("parent event does not continue the journal")
    record = {
        **metadata,
        "previous_receipt_hash": records[-1]["receipt_hash"] if records else None,
    }
    record["receipt_hash"] = _receipt_hash(record)
    _append_line(journal, record)
    return record


def validate_journal(journal: Path, *, repo_root: Path) -> list[dict[str, Any]]:
    """Return trusted records, rejecting tampering, gaps, and duplicate ids."""
    root = _resolved_root(repo_root)
    journal = _external_journal(journal, root)
    if not journal.exists():
        return []
    try:
        lines = journal.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ReceiptIntegrityError("journal is unreadable") from error
    records: list[dict[str, Any]] = []
    event_ids: set[str] = set()
    previous: dict[str, Any] | None = None
    for line in lines:
        if not line:
            raise ReceiptIntegrityError("journal contains an invalid gap")
        try:
            record = json.loads(line, object_pairs_hook=_unique_object)
        except (json.JSONDecodeError, _DuplicateJsonKeyError) as error:
            raise ReceiptIntegrityError("journal contains invalid JSON") from error
        if not isinstance(record, dict):
            raise ReceiptIntegrityError("journal record is not an object")
        try:
            _validate_envelope(record, root, allow_hashes=True)
        except ReceiptValidationError as error:
            raise ReceiptIntegrityError("journal record violates the receipt contract") from error
        if record["event_id"] in event_ids:
            raise ReceiptIntegrityError("journal contains a duplicate event id")
        expected_parent = previous["event_id"] if previous else None
        expected_hash = previous["receipt_hash"] if previous else None
        if record["parent_event_id"] != expected_parent or record["previous_receipt_hash"] != expected_hash:
            raise ReceiptIntegrityError("journal chain has a gap")
        if record["receipt_hash"] != _receipt_hash(record):
            raise ReceiptIntegrityError("journal receipt hash does not match")
        event_ids.add(record["event_id"])
        records.append(record)
        previous = record
    return records


def disable_journal(journal: Path, *, repo_root: Path) -> None:
    """Disable only new appends; this never alters receipt history."""
    _write_mode(_external_journal(journal, _resolved_root(repo_root)), "disabled")


def enable_journal(journal: Path, *, repo_root: Path) -> None:
    """Re-enable new appends without cleaning or changing receipt history."""
    _write_mode(_external_journal(journal, _resolved_root(repo_root)), "enabled")


def is_journal_disabled(journal: Path, *, repo_root: Path) -> bool:
    """Return whether new appends are blocked by the local mode sidecar."""
    path = _mode_path(_external_journal(journal, _resolved_root(repo_root)))
    if not path.exists():
        return False
    try:
        return path.read_text(encoding="utf-8") != "enabled\n"
    except OSError as error:
        raise ReceiptDisabledError("journal mode is unreadable") from error


def _validate_envelope(record: Mapping[str, Any], root: Path, *, allow_hashes: bool) -> None:
    _reject_private(record)
    fields = set(record)
    if not REQUIRED_FIELDS <= fields or not fields <= ALLOWED_FIELDS:
        raise ReceiptValidationError("receipt fields do not match the contract")
    if not allow_hashes and fields & {"receipt_hash", "previous_receipt_hash"}:
        raise ReceiptValidationError("writer computes receipt hashes")
    if ("task_id" not in record and "bead_id" not in record
            or any(key in record and not _valid_id(record[key]) for key in ("event_id", "run_id", "task_id", "bead_id"))):
        raise ReceiptValidationError("receipt ids are invalid")
    if record["parent_event_id"] is not None and not _valid_id(record["parent_event_id"]):
        raise ReceiptValidationError("parent event id is invalid")
    actor = record["actor"]
    runtime = record["runtime"]
    operation = record["operation"]
    outcome = record["outcome"]
    if not isinstance(actor, str) or actor not in {"human", "agent", "hook", "system"}:
        raise ReceiptValidationError("actor is invalid")
    if (not isinstance(runtime, str) or not isinstance(operation, str)
            or len(operation) > 64 or not _matches(RUNTIME, runtime)
            or not _matches(OPERATION, operation)):
        raise ReceiptValidationError("runtime or operation is invalid")
    _validate_target(record["target"], root)
    if record["source_commit"] is not None and not _matches(GIT_SHA, record["source_commit"]):
        raise ReceiptValidationError("source commit is invalid")
    if any(record[field] is not None and not _matches(SHA256, record[field]) for field in ("before_hash", "after_hash")):
        raise ReceiptValidationError("artifact hash is invalid")
    if not isinstance(outcome, str) or outcome not in OUTCOMES:
        raise ReceiptValidationError("outcome is invalid")
    refs = record["evidence_refs"]
    if not isinstance(refs, list) or len(refs) > 32:
        raise ReceiptValidationError("evidence references are invalid")
    for reference in refs:
        _validate_target(reference, root)
    if not _valid_utc(record["occurred_at"]) or record["redaction_status"] != "metadata-only":
        raise ReceiptValidationError("timestamp or redaction status is invalid")
    if "error_class" in record and (record["outcome"] not in FAILURE_OUTCOMES
                                     or not _matches(ERROR_CLASS, record["error_class"])):
        raise ReceiptValidationError("error class is invalid")
    if allow_hashes:
        if not {"receipt_hash", "previous_receipt_hash"} <= fields:
            raise ReceiptValidationError("persisted receipt hash fields are missing")
        if record["previous_receipt_hash"] is not None and not _matches(SHA256, record["previous_receipt_hash"]):
            raise ReceiptValidationError("previous receipt hash is invalid")
        if not _matches(SHA256, record["receipt_hash"]):
            raise ReceiptValidationError("receipt hash is invalid")


def _validate_target(value: Any, root: Path) -> None:
    if not isinstance(value, str) or len(value) > 256 or ":" not in value:
        raise ReceiptValidationError("target is invalid")
    kind, target = value.split(":", 1)
    if kind == "id" and _matches(TARGET_ID, target):
        return
    if kind == "class" and _matches(TARGET_CLASS, target):
        return
    if kind == "path" and target and len(target) <= 251 and _safe_path(target, root):
        return
    raise ReceiptValidationError("target is invalid")


def _safe_path(value: str, root: Path) -> bool:
    if value.startswith("/") or "\\" in value or "//" in value:
        return False
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return False
    try:
        (root / value).resolve().relative_to(root)
    except ValueError:
        return False
    return True


def _external_journal(journal: Path, root: Path) -> Path:
    """Resolve a local journal and reject paths that would enter the repository."""
    try:
        path = journal.resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise ReceiptValidationError("journal path is unreadable") from error
    try:
        path.relative_to(root)
    except ValueError:
        return path
    raise ReceiptValidationError("journal must be outside the repository")


def _reject_private(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if _is_private(str(key)):
                raise ReceiptValidationError("receipt contains forbidden metadata")
            _reject_private(nested)
    elif isinstance(value, list):
        for nested in value:
            _reject_private(nested)
    elif isinstance(value, str) and _is_private(value):
        raise ReceiptValidationError("receipt contains forbidden metadata")


def _is_private(value: str) -> bool:
    lowered = value.lower()
    return any(part in lowered for part in FORBIDDEN_PARTS)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    record: dict[str, Any] = {}
    for key, value in pairs:
        if key in record:
            raise _DuplicateJsonKeyError("duplicate JSON key")
        record[key] = value
    return record


def _receipt_hash(record: Mapping[str, Any]) -> str:
    canonical = {key: value for key, value in record.items() if key != "receipt_hash"}
    return hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _without_hashes(record: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key not in {"receipt_hash", "previous_receipt_hash"}}


def _append_line(journal: Path, record: Mapping[str, Any]) -> None:
    journal.parent.mkdir(parents=True, exist_ok=True)
    # ponytail: single-process local journal; add file locking only for concurrent writers.
    descriptor = os.open(journal, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    os.chmod(journal, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def _mode_path(journal: Path) -> Path:
    return journal.with_name(f"{journal.name}.mode")


def _write_mode(journal: Path, mode: str) -> None:
    path = _mode_path(journal)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.chmod(path, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        stream.write(f"{mode}\n")
        stream.flush()
        os.fsync(stream.fileno())


def _resolved_root(repo_root: Path) -> Path:
    try:
        return repo_root.resolve(strict=True)
    except OSError as error:
        raise ReceiptValidationError("repository root is unreadable") from error


def _matches(pattern: re.Pattern[str], value: Any) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def _valid_id(value: Any) -> bool:
    return _matches(ID, value)


def _valid_utc(value: Any) -> bool:
    if not _matches(UTC_RFC3339, value):
        return False
    try:
        datetime.strptime(value[:19], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("journal", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--disable", action="store_true", help="block new appends without erasing history")
    action.add_argument("--enable", action="store_true", help="allow new appends without cleaning history")
    action.add_argument("--validate", action="store_true", help="validate the append-only JSONL chain")
    args = parser.parse_args()
    if args.disable:
        disable_journal(args.journal, repo_root=args.repo_root)
        print("disabled: no new appends; receipt history remains intact")
    elif args.enable:
        enable_journal(args.journal, repo_root=args.repo_root)
        print("enabled: receipt history remains intact")
    else:
        print(f"valid:{len(validate_journal(args.journal, repo_root=args.repo_root))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
