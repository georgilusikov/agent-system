#!/usr/bin/env python3
"""Small metadata-only adapter for runtime change receipts."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import change_receipts


@dataclass(frozen=True)
class ReceiptContext:
    journal: Path
    repo_root: Path
    run_id: str
    actor: str
    runtime: str
    task_id: str | None = None
    bead_id: str | None = None
    source_commit: str | None = None


def emit_change(context: ReceiptContext, event_id: str, operation: str, target: str,
                before_hash: str | None, after_hash: str | None, outcome: str,
                evidence_refs: Iterable[str] = (), error_class: str | None = None) -> dict[str, object]:
    """Append a validated metadata receipt using the journal's existing parent chain."""
    records = change_receipts.validate_journal(context.journal, repo_root=context.repo_root)
    existing = next((record for record in records if record["event_id"] == event_id), None)
    occurred_at = (existing["occurred_at"] if existing is not None
                   else datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z"))
    record: dict[str, object] = {
        "event_id": event_id,
        "parent_event_id": (existing["parent_event_id"] if existing is not None
                            else records[-1]["event_id"] if records else None),
        "run_id": context.run_id,
        "actor": context.actor,
        "runtime": context.runtime,
        "operation": operation,
        "target": target,
        "source_commit": context.source_commit,
        "before_hash": before_hash,
        "after_hash": after_hash,
        "outcome": outcome,
        "evidence_refs": list(evidence_refs),
        "occurred_at": occurred_at,
        "redaction_status": "metadata-only",
    }
    if context.task_id is not None:
        record["task_id"] = context.task_id
    if context.bead_id is not None:
        record["bead_id"] = context.bead_id
    if error_class is not None:
        record["error_class"] = error_class
    return change_receipts.append_receipt(context.journal, record, repo_root=context.repo_root)


def file_hash(path: Path) -> str:
    """Hash an explicitly supplied file, without exposing its contents."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
