#!/usr/bin/env python3
"""Synthetic, temporary-journal canary for metadata-only change receipts."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

import change_receipts as receipts


def receipt(event_id: str, parent_event_id: str | None = None) -> dict[str, object]:
    return {
        "event_id": event_id,
        "parent_event_id": parent_event_id,
        "run_id": "run-gl-ejw-6",
        "task_id": "gl-ejw.6",
        "actor": "agent",
        "runtime": "codex",
        "operation": "receipt.append",
        "target": "path:scripts/agent_run_state.py",
        "source_commit": "a" * 40,
        "before_hash": "b" * 64,
        "after_hash": "c" * 64,
        "outcome": "verified",
        "evidence_refs": ["id:check-gl-ejw-6"],
        "occurred_at": "2026-08-22T12:00:00Z",
        "redaction_status": "metadata-only",
    }


def expect(error: type[Exception], action: object) -> None:
    try:
        action()  # type: ignore[operator]
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")


def receipt_hash(record: dict[str, object]) -> str:
    canonical = {key: value for key, value in record.items() if key != "receipt_hash"}
    return hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as directory:
        journal = Path(directory) / "receipts.jsonl"
        first = receipts.append_receipt(journal, receipt("event-1"), repo_root=repo)
        second = receipts.append_receipt(journal, receipt("event-2", "event-1"), repo_root=repo)
        assert second["previous_receipt_hash"] == first["receipt_hash"]
        assert len(receipts.validate_journal(journal, repo_root=repo)) == 2

        duplicate = receipts.append_receipt(journal, receipt("event-1"), repo_root=repo)
        assert duplicate == first and len(journal.read_text(encoding="utf-8").splitlines()) == 2
        expect(receipts.ReceiptConflictError,
               lambda: receipts.append_receipt(journal, {**receipt("event-1"), "outcome": "failed"}, repo_root=repo))
        expect(receipts.ReceiptValidationError,
               lambda: receipts.append_receipt(journal, {**receipt("event-3"), "prompt": "never-store"}, repo_root=repo))
        expect(receipts.ReceiptValidationError,
               lambda: receipts.append_receipt(journal, {**receipt("event-3"), "target": "path:/outside"}, repo_root=repo))
        expect(receipts.ReceiptValidationError,
               lambda: receipts.append_receipt(journal, {**receipt("event-3"), "occurred_at": "2026-08-22T12:00Z"}, repo_root=repo))

        before_disable = journal.read_bytes()
        receipts.disable_journal(journal)
        expect(receipts.ReceiptDisabledError,
               lambda: receipts.append_receipt(journal, receipt("event-3", "event-2"), repo_root=repo))
        assert journal.read_bytes() == before_disable
        receipts.enable_journal(journal)
        receipts.append_receipt(journal, receipt("event-3", "event-2"), repo_root=repo)

        deterministic = Path(directory) / "deterministic.jsonl"
        receipts.append_receipt(deterministic, receipt("event-1"), repo_root=repo)
        receipts.append_receipt(deterministic, receipt("event-2", "event-1"), repo_root=repo)
        assert deterministic.read_bytes() == before_disable

        records = [json.loads(line) for line in before_disable.decode().splitlines()]
        tampered = Path(directory) / "tampered.jsonl"
        records[0]["outcome"] = "failed"
        tampered.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")
        expect(receipts.ReceiptIntegrityError, lambda: receipts.validate_journal(tampered, repo_root=repo))

        gap = Path(directory) / "gap.jsonl"
        records = [json.loads(line) for line in before_disable.decode().splitlines()]
        records[1]["parent_event_id"] = "event-missing"
        records[1]["receipt_hash"] = receipt_hash(records[1])
        gap.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")
        expect(receipts.ReceiptIntegrityError, lambda: receipts.validate_journal(gap, repo_root=repo))

        repeated = Path(directory) / "duplicate.jsonl"
        repeated.write_bytes(before_disable + before_disable.splitlines(keepends=True)[0])
        expect(receipts.ReceiptIntegrityError, lambda: receipts.validate_journal(repeated, repo_root=repo))
        banned = ("prompt", "response", "transcript", "payload", "credential", "secret", "token", "environment")
        assert not any(word in journal.read_text(encoding="utf-8").lower() for word in banned)
    print("PASS metadata-only change receipts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
