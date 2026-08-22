#!/usr/bin/env python3
"""Synthetic, temporary-journal canary for metadata-only change receipts."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

if __package__:
    from . import agent_run_state as state
    from . import change_receipts as receipts
else:
    import agent_run_state as state
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        for field, value in (("actor", []), ("runtime", []), ("operation", {}), ("outcome", [])):
            expect(receipts.ReceiptValidationError,
                   lambda field=field, value=value: receipts.append_receipt(
                       journal, {**receipt("event-3"), field: value}, repo_root=repo))

        operation_limits = Path(directory) / "operation-limits.jsonl"
        receipts.append_receipt(operation_limits, receipt("operation-64") | {
            "operation": "a" * 62 + ".b"}, repo_root=repo)
        expect(receipts.ReceiptValidationError,
               lambda: receipts.append_receipt(operation_limits, receipt("operation-65") | {
                   "parent_event_id": "operation-64", "operation": "a" * 63 + ".b"}, repo_root=repo))

        expect(receipts.ReceiptValidationError,
               lambda: receipts.append_receipt(repo / "receipts.jsonl", receipt("inside-repo"), repo_root=repo))
        linked_repo = Path(directory) / "linked-repo"
        linked_repo.symlink_to(repo, target_is_directory=True)
        expect(receipts.ReceiptValidationError,
               lambda: receipts.append_receipt(linked_repo / "receipts.jsonl", receipt("symlink-inside"), repo_root=repo))

        before_disable = journal.read_bytes()
        receipts.disable_journal(journal, repo_root=repo)
        expect(receipts.ReceiptDisabledError,
               lambda: receipts.append_receipt(journal, receipt("event-3", "event-2"), repo_root=repo))
        assert journal.read_bytes() == before_disable
        receipts.enable_journal(journal, repo_root=repo)
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

        duplicate_key = Path(directory) / "duplicate-key.jsonl"
        duplicate_key.write_bytes(before_disable.splitlines(keepends=True)[0].replace(
            b'"outcome":"verified"', b'"outcome":"failed","outcome":"verified"'))
        expect(receipts.ReceiptIntegrityError, lambda: receipts.validate_journal(duplicate_key, repo_root=repo))

        state_path = Path(directory) / "adapter-state.json"
        source_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
        state.create_run(state_path, run_id="run-adapter", bead_id="gl-ejw.6",
                         source_commit=source_commit, opaque_goal_id="adapter-goal")
        state.start_run(state_path, operation_key="adapter-start")
        before_hash = sha256(state_path)
        state.record_verified_step(state_path, 1, evidence_refs=["id:state-step-1"],
                                   operation_key="adapter-step-1")
        after_hash = sha256(state_path)
        adapter_receipt = receipt("adapter-step-1") | {
            "run_id": "run-adapter",
            "operation": "state.verify",
            "target": "class:agent-run-state",
            "source_commit": source_commit,
            "before_hash": before_hash,
            "after_hash": after_hash,
            "evidence_refs": ["id:state-step-1"],
        }
        adapter_journal = Path(directory) / "adapter-receipts.jsonl"
        appended = receipts.append_receipt(adapter_journal, adapter_receipt, repo_root=repo)
        joined = [record for record in receipts.validate_journal(adapter_journal, repo_root=repo)
                  if record["run_id"] == "run-adapter"]
        assert joined == [appended]
        assert joined[0]["source_commit"] == source_commit
        assert joined[0]["before_hash"] == before_hash and joined[0]["after_hash"] == after_hash
        assert state.resume_run(state_path, expected_source_commit=source_commit)["next_action"] == "verify step 2"
        state_before_retry = state_path.read_bytes()
        assert state.record_verified_step(state_path, 1, evidence_refs=["id:state-step-1"],
                                          operation_key="adapter-step-1")
        assert state_path.read_bytes() == state_before_retry
        journal_before_retry = adapter_journal.read_bytes()
        assert receipts.append_receipt(adapter_journal, adapter_receipt, repo_root=repo) == appended
        assert adapter_journal.read_bytes() == journal_before_retry
        banned = ("prompt", "response", "transcript", "payload", "credential", "secret", "token", "environment")
        assert not any(word in journal.read_text(encoding="utf-8").lower() for word in banned)
    print("PASS metadata-only change receipts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
