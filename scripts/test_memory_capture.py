#!/usr/bin/env python3
"""Self-check for the metadata-only verified memory capture seam."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from . import memory_capture as capture
except ImportError:
    import memory_capture as capture


def candidate(candidate_id: str = "mem-capture") -> dict[str, object]:
    receipt_hash = hashlib.sha256(b"capture-receipt").hexdigest()
    return {
        "candidate_id": candidate_id,
        "topic": "capture-safety",
        "kind": "approach",
        "scope": "project",
        "project": "agent-system",
        "owner": "owner-1",
        "statement": "verified metadata can enter the review queue",
        "applicability": "metadata-only capture",
        "limits": "draft until review and owner approval",
        "source_receipt": "receipt:capture-step-1",
        "source_hash": receipt_hash,
        "result_metric": "test:memory-capture",
        "evidence_refs": ["receipt:capture-step-1", "test:memory-capture"],
        "contradicts": [],
        "supersedes": None,
        "created_at": "2026-08-22T12:00:00Z",
        "redaction_status": "redacted",
    }


def receipt() -> dict[str, object]:
    return {
        "event_id": "capture-step-1",
        "run_id": "capture-run-1",
        "receipt_hash": hashlib.sha256(b"capture-receipt").hexdigest(),
        "outcome": "verified",
        "redaction_status": "metadata-only",
        "evidence_refs": ["test:memory-capture"],
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
        root = Path(directory)
        ledger = root / "memory.jsonl"
        created = capture.capture_verified_candidate(ledger, candidate(), receipt(), repo_root=repo)
        assert created["candidate_id"] == "mem-capture"
        assert created["status"] == "draft"

        before = ledger.read_bytes()
        forbidden = {**candidate("mem-forbidden"), "statement": "save the prompt"}
        expect(capture.MemoryCandidateError,
               lambda: capture.capture_verified_candidate(ledger, forbidden, receipt(), repo_root=repo))
        assert ledger.read_bytes() == before

        cli_input = json.dumps({"candidate": candidate("mem-cli"), "receipt": receipt()})
        cli_ledger = root / "cli-memory.jsonl"
        command = [sys.executable, str(Path(__file__).with_name("memory_capture.py")),
                   "--ledger", str(cli_ledger)]
        result = subprocess.run(command, input=cli_input, text=True, capture_output=True, check=False)
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == "candidate_id=mem-cli status=draft"
        assert cli_ledger.exists()

        no_ledger = root / "not-created.jsonl"
        result = subprocess.run([sys.executable, "-m", "scripts.memory_capture"],
                                cwd=repo, input=cli_input, text=True,
                                capture_output=True, check=False)
        assert result.returncode != 0
        assert not no_ledger.exists()
        assert "prompt" not in result.stdout.lower() + result.stderr.lower()
    print("PASS metadata-only memory capture seam")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
