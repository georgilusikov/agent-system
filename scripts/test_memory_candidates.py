#!/usr/bin/env python3
"""End-to-end canary for the metadata-only memory candidate lifecycle."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

import memory_candidates as memory


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
        first = memory.create_candidate(ledger, candidate("mem-first"), receipt(), repo_root=repo)
        assert first["status"] == "draft"
        memory.review_candidate(ledger, "mem-first", decision="reviewed", reviewer_id="reviewer-1",
                                evidence_ref="test:memory-review", repo_root=repo)
        approved = memory.approve_candidate(ledger, "mem-first", owner_id="owner-1",
                                             evidence_ref="test:memory-approval", repo_root=repo)
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
                                 evidence_ref="test:memory-approval-2", repo_root=repo)
        current = memory.retrieve_current(ledger, scope="project", project="agent-system", repo_root=repo)
        assert [item["candidate_id"] for item in current] == ["mem-replacement"]
        memory.rollback_candidate(ledger, "mem-replacement", actor_id="owner-1",
                                  evidence_ref="test:memory-rollback", repo_root=repo)
        assert memory.retrieve_current(ledger, scope="project", project="agent-system", repo_root=repo) == []

        memory.create_candidate(ledger, candidate("mem-rejected", topic="other-topic"), receipt(), repo_root=repo)
        memory.review_candidate(ledger, "mem-rejected", decision="rejected", reviewer_id="reviewer-1",
                                evidence_ref="test:memory-reject", repo_root=repo)
        assert memory.retrieve_current(ledger, scope="project", project="agent-system", repo_root=repo) == []
        expect(memory.CandidateValidationError,
               lambda: memory.create_candidate(repo / "memory.jsonl", candidate("mem-inside"), receipt(), repo_root=repo))

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
