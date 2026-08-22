#!/usr/bin/env python3
"""Executable metadata-only acceptance chain for one isolated temp run."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

if __package__:
    from . import agent_run_state as run_state
    from . import change_receipts, evaluate_before_after, memory_capture, provider_canary
    from .runtime_receipts import ReceiptContext, emit_change
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import agent_run_state as run_state
    import change_receipts, evaluate_before_after, memory_capture, provider_canary
    from runtime_receipts import ReceiptContext, emit_change


FORBIDDEN = ("prompt", "response", "transcript", "payload", "credential", "secret", "token", "environment")


def _assert_clean(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            assert not any(marker in str(key).lower() for marker in FORBIDDEN), key
            _assert_clean(nested)
    elif isinstance(value, list):
        for nested in value:
            _assert_clean(nested)
    elif isinstance(value, str):
        assert not any(marker in value.lower() for marker in FORBIDDEN), value


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        state_path = root / "run.json"
        journal = root / "receipts.jsonl"
        ledger = root / "memory.jsonl"
        context = ReceiptContext(
            journal=journal, repo_root=repo, run_id="acceptance-run", actor="agent",
            runtime="codex", task_id="acceptance-task", bead_id="acceptance-bead",
            source_commit="a" * 40,
        )

        created = run_state.create_run(
            state_path, run_id="acceptance-run", bead_id="acceptance-bead",
            source_commit="a" * 40, opaque_goal_id="acceptance-goal", receipt_context=context,
        )
        started = run_state.start_run(state_path, operation_key="start-1", receipt_context=context)
        verified = run_state.record_verified_step(
            state_path, 1, evidence_refs=["id:runtime-acceptance"],
            operation_key="verify-1", receipt_context=context,
        )
        finished = run_state.finish_run(
            state_path, "accepted", evidence_refs=["id:runtime-acceptance"],
            operation_key="finish-1", receipt_context=context,
        )
        assert created["phase"] == "planned"
        assert started["phase"] == "running"
        assert verified["last_verified_step"] == 1
        assert finished["status"] == "accepted"
        assert run_state.load_state(state_path) == finished

        final_receipt = emit_change(
            context, "acceptance-verified", "acceptance.verify", "class:runtime-acceptance",
            hashlib.sha256(state_path.read_bytes()).hexdigest(), None, "verified",
            evidence_refs=["id:runtime-acceptance"],
        )
        receipts = change_receipts.validate_journal(journal, repo_root=repo)
        assert receipts[-1] == final_receipt
        assert [record["operation"] for record in receipts] == [
            "state.create", "state.start", "state.verify", "state.finish", "acceptance.verify",
        ]

        candidate = {
            "candidate_id": "mem-runtime-acceptance",
            "topic": "runtime-acceptance",
            "kind": "procedure",
            "scope": "project",
            "project": "agent-system",
            "owner": "owner-1",
            "statement": "verified runtime metadata can produce a draft memory candidate",
            "applicability": "offline acceptance checks",
            "limits": "draft only until review and approval",
            "source_receipt": "receipt:acceptance-verified",
            "source_hash": final_receipt["receipt_hash"],
            "result_metric": "test:runtime-acceptance",
            "evidence_refs": ["receipt:acceptance-verified", "test:runtime-acceptance"],
            "contradicts": [],
            "supersedes": None,
            "created_at": "2026-08-22T12:00:00Z",
            "redaction_status": "redacted",
        }
        captured = memory_capture.capture_verified_candidate(
            ledger, candidate, final_receipt, repo, receipt_context=context
        )
        assert captured["candidate_id"] == candidate["candidate_id"]
        assert captured["status"] == "draft"
        memory_record = json.loads(ledger.read_text(encoding="utf-8").splitlines()[0])
        assert memory_record["data"]["source_hash"] == final_receipt["receipt_hash"]

        evaluation = evaluate_before_after.build_not_run(
            run_id="acceptance-eval",
            hypothesis_id="acceptance-hypothesis",
            change_type="initial",
            supersedes_run_id=None,
            baseline_commit="a" * 40,
            treatment_commit="b" * 40,
            baseline_config="c" * 64,
            treatment_config="d" * 64,
        )
        evaluation_path = root / "evaluation.json"
        evaluate_before_after.write_result(
            evaluation_path, evaluation, receipt_context=context
        )
        assert evaluate_before_after.load_result(evaluation_path) == evaluation

        canary = provider_canary.run_canary(
            str(root / "missing-provider-executable"), ("--version",), "provider", "codex", "model",
            0.1, "acceptance-run", "test:runtime-acceptance",
        )
        assert canary["status"] == canary["canary"] == "NOT RUN"
        assert canary["reason"] == "missing-executable"

        receipts = change_receipts.validate_journal(journal, repo_root=repo)
        assert [record["operation"] for record in receipts] == [
            "state.create", "state.start", "state.verify", "state.finish", "acceptance.verify",
            "memory.create", "evaluation.write",
        ]
        for path in (state_path, journal, ledger, evaluation_path):
            for line in path.read_text(encoding="utf-8").splitlines():
                _assert_clean(json.loads(line))
        _assert_clean(canary)
        assert "NOT RUN" in json.dumps(canary, sort_keys=True)

    print("PASS metadata-only runtime acceptance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
