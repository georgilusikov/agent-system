#!/usr/bin/env python3
"""Focused offline checks for the runtime receipt adapter."""

from __future__ import annotations

import tempfile
from pathlib import Path

if __package__:
    from . import change_receipts
    from .runtime_receipts import ReceiptContext, emit_change, preflight
else:
    import change_receipts
    from runtime_receipts import ReceiptContext, emit_change, preflight


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "repo"
        root.mkdir()
        journal = Path(directory) / "receipts.jsonl"
        context = ReceiptContext(
            journal=journal, repo_root=root, run_id="run-1", actor="agent", runtime="codex",
            task_id="task-1", source_commit="a" * 40,
        )
        first = emit_change(
            context, "event-1", "state.create", "class:agent-run-state", None, "b" * 64,
            "applied", evidence_refs=("id:check-1",),
        )
        second = emit_change(
            context, "event-2", "state.start", "class:agent-run-state", "b" * 64, "c" * 64,
            "verified",
        )
        records = change_receipts.validate_journal(journal, repo_root=root)
        assert records == [first, second]
        assert second["parent_event_id"] == "event-1"
        assert first["evidence_refs"] == ["id:check-1"]
        assert set(first) <= change_receipts.ALLOWED_FIELDS | {"receipt_hash", "previous_receipt_hash"}
        assert all("prompt" not in record for record in records)
        assert emit_change(
            context, "event-1", "state.create", "class:agent-run-state", None, "b" * 64,
            "applied", evidence_refs=["id:check-1"],
        ) == first
        change_receipts.disable_journal(journal, repo_root=root)
        assert preflight(context, "event-1") == first
        try:
            preflight(context, "event-3")
        except change_receipts.ReceiptDisabledError:
            pass
        else:
            raise AssertionError("disabled journal allowed a new receipt event")
        change_receipts.enable_journal(journal, repo_root=root)
        try:
            emit_change(context, "event-3", "state.create", "class:agent-run-state", None, None,
                        "applied", evidence_refs=["prompt:never"])
        except change_receipts.ReceiptValidationError:
            pass
        else:
            raise AssertionError("forbidden receipt metadata was accepted")
        try:
            emit_change(
                ReceiptContext(journal=root / "receipts.jsonl", repo_root=root, run_id="run-2",
                               actor="agent", runtime="codex", task_id="task-2"),
                "event-4", "state.create", "class:agent-run-state", None, None, "applied",
            )
        except change_receipts.ReceiptValidationError:
            pass
        else:
            raise AssertionError("in-repo journal was accepted")
    print("PASS runtime receipt adapter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
