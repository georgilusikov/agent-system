#!/usr/bin/env python3
"""End-to-end canary for the metadata-only memory candidate lifecycle."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

if __package__:
    from . import memory_candidates as memory
    from .change_receipts import ReceiptIntegrityError, validate_journal
    from .runtime_receipts import ReceiptContext
else:
    import memory_candidates as memory
    from change_receipts import ReceiptIntegrityError, validate_journal
    from runtime_receipts import ReceiptContext


def candidate(candidate_id: str, *, topic: str = "retry-safety", statement: str = "retry is safe",
              supersedes: str | None = None) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "topic": topic,
        "kind": "approach",
        "scope": "project",
        "project": "agent-system",
        "owner": "owner-1",
        "statement": statement,
        "applicability": "verified state transitions",
        "limits": "single-process ledger",
        "source_receipt": "receipt:run-step-1",
        "source_hash": hashlib.sha256(b"receipt").hexdigest(),
        "result_metric": "test:memory-canary",
        "evidence_refs": ["receipt:run-step-1", "test:memory-canary"],
        "contradicts": [],
        "supersedes": supersedes,
        "created_at": "2026-08-22T12:00:00Z",
        "redaction_status": "redacted",
    }


def receipt() -> dict[str, object]:
    return {
        "event_id": "run-step-1",
        "run_id": "run-1",
        "receipt_hash": hashlib.sha256(b"receipt").hexdigest(),
        "outcome": "verified",
        "redaction_status": "metadata-only",
        "evidence_refs": ["test:memory-canary"],
    }


def expect(error: type[Exception], action: object) -> None:
    try:
        action()  # type: ignore[operator]
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as directory:
        ledger = Path(directory) / "memory.jsonl"
        context = ReceiptContext(journal=Path(directory) / "receipts.jsonl", repo_root=repo,
                                 run_id="memory-run", actor="agent", runtime="codex", task_id="task-5")
        first = memory.create_candidate(ledger, candidate("mem-first"), receipt(), repo_root=repo,
                                        receipt_context=context)
        assert first["status"] == "draft"
        memory.review_candidate(ledger, "mem-first", decision="reviewed", reviewer_id="reviewer-1",
                                evidence_ref="test:memory-review", repo_root=repo, receipt_context=context)
        approved = memory.approve_candidate(ledger, "mem-first", owner_id="owner-1",
                                             evidence_ref="test:memory-approval", repo_root=repo,
                                             receipt_context=context)
        assert approved["status"] == "approved"
        assert len(memory.retrieve_current(ledger, scope="project", project="agent-system", repo_root=repo)) == 1

        expect(memory.CandidateConflictError,
               lambda: memory.create_candidate(ledger, candidate("mem-duplicate"), receipt(), repo_root=repo))
        expect(memory.CandidateConflictError,
               lambda: memory.create_candidate(ledger, candidate("mem-contradiction", statement="retry is unsafe"), receipt(), repo_root=repo))
        expect(memory.CandidateValidationError,
               lambda: memory.create_candidate(ledger, {**candidate("mem-private"), "statement": "store the prompt"}, receipt(), repo_root=repo))
        expect(memory.CandidateValidationError,
               lambda: memory.create_candidate(ledger, {**candidate("mem-wrong-receipt"), "source_receipt": "receipt:other"}, receipt(), repo_root=repo))
        expect(memory.CandidateValidationError,
               lambda: memory.create_candidate(ledger, {**candidate("mem-wrong-hash"), "source_hash": "a" * 64}, receipt(), repo_root=repo))

        replacement = memory.create_candidate(ledger, candidate("mem-replacement", statement="retry is safe after resume",
                                                                supersedes="mem-first"), receipt(), repo_root=repo)
        assert replacement["status"] == "draft"
        memory.review_candidate(ledger, "mem-replacement", decision="reviewed", reviewer_id="reviewer-1",
                                evidence_ref="test:memory-review-2", repo_root=repo)
        memory.approve_candidate(ledger, "mem-replacement", owner_id="owner-1",
                                 evidence_ref="test:memory-approval-2", repo_root=repo,
                                 receipt_context=context)
        current = memory.retrieve_current(ledger, scope="project", project="agent-system", repo_root=repo)
        assert [item["candidate_id"] for item in current] == ["mem-replacement"]
        memory.rollback_candidate(ledger, "mem-replacement", actor_id="owner-1",
                                  evidence_ref="test:memory-rollback", repo_root=repo, receipt_context=context)
        assert memory.retrieve_current(ledger, scope="project", project="agent-system", repo_root=repo) == []
        receipts = validate_journal(context.journal, repo_root=repo)
        assert [item["operation"] for item in receipts] == [
            "memory.create", "memory.review", "memory.approve", "memory.approve", "memory.rollback"]
        assert all(item["target"] == "class:memory-ledger" for item in receipts)
        assert all(item["before_hash"] != item["after_hash"] for item in receipts)
        assert all(set(item) <= {"event_id", "parent_event_id", "run_id", "actor", "runtime",
                                  "operation", "target", "source_commit", "before_hash", "after_hash",
                                  "outcome", "evidence_refs", "occurred_at", "redaction_status",
                                  "task_id", "receipt_hash", "previous_receipt_hash"} for item in receipts)

        memory.create_candidate(ledger, candidate("mem-rejected", topic="other-topic"), receipt(), repo_root=repo)
        memory.review_candidate(ledger, "mem-rejected", decision="rejected", reviewer_id="reviewer-1",
                                evidence_ref="test:memory-reject", repo_root=repo)
        assert memory.retrieve_current(ledger, scope="project", project="agent-system", repo_root=repo) == []
        expect(memory.CandidateValidationError,
               lambda: memory.create_candidate(repo / "memory.jsonl", candidate("mem-inside"), receipt(), repo_root=repo))

        invalid_ledger = Path(directory) / "invalid-memory.jsonl"
        invalid_journal = Path(directory) / "invalid-receipts.jsonl"
        invalid_journal.write_text("{not-json}\n", encoding="utf-8")
        invalid_context = ReceiptContext(journal=invalid_journal, repo_root=repo,
                                         run_id="invalid-run", actor="agent", runtime="codex",
                                         task_id="task-5")
        expect(ReceiptIntegrityError,
               lambda: memory.create_candidate(invalid_ledger, candidate("mem-invalid"), receipt(),
                                                repo_root=repo, receipt_context=invalid_context))
        assert not invalid_ledger.exists()

        retry_context = ReceiptContext(journal=Path(directory) / "retry-receipts.jsonl", repo_root=repo,
                                       run_id="retry-run", actor="agent", runtime="codex", task_id="task-5")
        original_emit = memory.emit_change
        failed = True
        def fail_once(*args: object, **kwargs: object) -> dict[str, object]:
            nonlocal failed
            if failed:
                failed = False
                raise OSError("one-time receipt failure")
            return original_emit(*args, **kwargs)  # type: ignore[arg-type]
        memory.emit_change = fail_once  # type: ignore[assignment]
        retry_ledger = Path(directory) / "retry-memory.jsonl"
        try:
            expect(OSError, lambda: memory.create_candidate(
                retry_ledger, candidate("mem-retry"), receipt(), repo_root=repo,
                receipt_context=retry_context))
            recovered = memory.create_candidate(
                retry_ledger, candidate("mem-retry"), receipt(), repo_root=repo,
                receipt_context=retry_context)
        finally:
            memory.emit_change = original_emit
        assert recovered["status"] == "draft"
        assert len(validate_journal(retry_context.journal, repo_root=repo)) == 1

        approval_retry_ledger = Path(directory) / "approval-retry-memory.jsonl"
        old_candidate = candidate("mem-approve-old")
        memory.create_candidate(approval_retry_ledger, old_candidate, receipt(), repo_root=repo)
        memory.review_candidate(approval_retry_ledger, "mem-approve-old", decision="reviewed",
                                reviewer_id="reviewer-1", evidence_ref="test:approval-review", repo_root=repo)
        memory.approve_candidate(approval_retry_ledger, "mem-approve-old", owner_id="owner-1",
                                 evidence_ref="test:approval-old", repo_root=repo)
        memory.create_candidate(approval_retry_ledger,
                                candidate("mem-approve-new", statement="retry is safe after approval",
                                          supersedes="mem-approve-old"), receipt(), repo_root=repo)
        memory.review_candidate(approval_retry_ledger, "mem-approve-new", decision="reviewed",
                                reviewer_id="reviewer-1", evidence_ref="test:approval-review-new", repo_root=repo)
        approval_context = ReceiptContext(
            journal=Path(directory) / "approval-retry-receipts.jsonl", repo_root=repo,
            run_id="approval-retry-run", actor="agent", runtime="codex", task_id="task-5",
        )
        original_emit = memory.emit_change
        failed = True

        def fail_approval_once(*args: object, **kwargs: object) -> dict[str, object]:
            nonlocal failed
            if failed:
                failed = False
                raise OSError("one-time approval receipt failure")
            return original_emit(*args, **kwargs)  # type: ignore[arg-type]

        memory.emit_change = fail_approval_once  # type: ignore[assignment]
        try:
            expect(OSError, lambda: memory.approve_candidate(
                approval_retry_ledger, "mem-approve-new", owner_id="owner-1",
                evidence_ref="test:approval-new", repo_root=repo, receipt_context=approval_context))
            recovered_approval = memory.approve_candidate(
                approval_retry_ledger, "mem-approve-new", owner_id="owner-1",
                evidence_ref="test:approval-new", repo_root=repo, receipt_context=approval_context)
        finally:
            memory.emit_change = original_emit
        assert recovered_approval["status"] == "approved"
        approval_events = memory._read_events(approval_retry_ledger)
        assert sum(event["candidate_id"] == "mem-approve-new" and event["action"] == "approved"
                   for event in approval_events) == 1
        assert len(validate_journal(approval_context.journal, repo_root=repo)) == 1

        created_event = memory._read_events(ledger)[0]
        bypass = Path(directory) / "bypass.jsonl"
        approved_event = {
            "event_id": "memory:mem-bypass:approved:2",
            "candidate_id": "mem-first",
            "action": "approved",
            "actor": "owner-1",
            "evidence_ref": "test:bypass",
            "occurred_at": "2026-08-22T12:00:00Z",
            "data": None,
            "previous_event_hash": created_event["event_hash"],
        }
        approved_event["event_hash"] = memory._event_hash(approved_event)
        bypass.write_text("\n".join(memory.json.dumps(item, sort_keys=True, separators=(",", ":"))
                          for item in (created_event, approved_event)) + "\n", encoding="utf-8")
        expect(memory.CandidateIntegrityError,
               lambda: memory.retrieve_current(bypass, scope="project", project="agent-system", repo_root=repo))
    print("PASS metadata-only memory candidate lifecycle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
