#!/usr/bin/env python3
"""Executable metadata-only seam for verified memory candidates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping

try:
    from . import memory_candidates
except ImportError:
    import memory_candidates


MemoryCandidateError = memory_candidates.MemoryCandidateError


def capture_verified_candidate(
    ledger: Path,
    candidate: Mapping[str, Any],
    receipt: Mapping[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    """Capture one explicitly redacted candidate from one verified receipt."""
    if not isinstance(candidate, Mapping) or not isinstance(receipt, Mapping):
        raise memory_candidates.CandidateValidationError("candidate and receipt must be metadata mappings")
    return memory_candidates.create_candidate(ledger, candidate, receipt, repo_root=repo_root)


def _read_input(path: Path | None) -> Mapping[str, Any]:
    raw = path.read_text(encoding="utf-8") if path else sys.stdin.read()
    value = json.loads(raw)
    if not isinstance(value, dict) or set(value) != {"candidate", "receipt"}:
        raise memory_candidates.CandidateValidationError("input envelope is invalid")
    if not isinstance(value["candidate"], Mapping) or not isinstance(value["receipt"], Mapping):
        raise memory_candidates.CandidateValidationError("input envelope values are invalid")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="JSON envelope file; stdin when omitted")
    parser.add_argument("--ledger", type=Path, help="external ledger to append")
    args = parser.parse_args(argv)
    try:
        if args.ledger is None:
            raise memory_candidates.CandidateValidationError("--ledger is required")
        value = _read_input(args.input)
        result = capture_verified_candidate(
            args.ledger,
            value["candidate"],
            value["receipt"],
            repo_root=Path(__file__).resolve().parents[1],
        )
    except Exception as error:
        print(f"error={type(error).__name__}", file=sys.stderr)
        return 2
    print(f"candidate_id={result['candidate_id']} status={result['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
