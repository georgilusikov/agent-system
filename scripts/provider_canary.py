#!/usr/bin/env python3
"""Metadata-only, zero-cost runtime capability canary."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Sequence


_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+\-]{0,127}$")
_FORBIDDEN = re.compile(
    r"(?:argv|credential|environment|payload|prompt|response|stderr|stdout|token|transcript)",
    re.IGNORECASE,
)
_CLI_FLAGS = {"--version", "-v", "--help", "-h"}


def _validate_id(name: str, value: str) -> None:
    if not isinstance(value, str) or not _ID.fullmatch(value) or _FORBIDDEN.search(value):
        raise ValueError(f"invalid {name}")


def _validate_executable(value: str) -> None:
    if not isinstance(value, str) or not value or len(value) > 4096 or _FORBIDDEN.search(value):
        raise ValueError("invalid executable")


def _validate_argv(argv: Sequence[str]) -> tuple[str, ...]:
    if isinstance(argv, (str, bytes)) or not argv or not all(isinstance(item, str) for item in argv):
        raise ValueError("argv must be a non-empty sequence of strings")
    return tuple(argv)


def run_canary(
    executable: str,
    argv: Sequence[str],
    provider: str,
    runtime: str,
    model: str,
    timeout_seconds: float,
    run_id: str,
    evidence_ref: str,
) -> dict[str, object]:
    """Run one bounded command and return metadata only."""
    _validate_executable(executable)
    for name, value in (("provider", provider), ("runtime", runtime), ("model", model),
                        ("run_id", run_id), ("evidence_ref", evidence_ref)):
        _validate_id(name, value)
    args = _validate_argv(argv)
    if not isinstance(timeout_seconds, (int, float)) or isinstance(timeout_seconds, bool):
        raise ValueError("timeout_seconds must be numeric")
    if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive and finite")

    result: dict[str, object] = {
        "provider": provider,
        "runtime": runtime,
        "model": model,
        "status": "NOT RUN",
        "canary": "NOT RUN",
        "exit_code": None,
        "elapsed_ms": 0,
        "reason": "missing-executable",
        "redaction_status": "metadata-only",
    }
    resolved = shutil.which(executable)
    if resolved is None:
        return result

    started = time.monotonic()
    try:
        completed = subprocess.run(
            [resolved, *args], shell=False, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, timeout=timeout_seconds, check=False,
        )
    except subprocess.TimeoutExpired:
        result["reason"] = "timeout"
    except OSError:
        result["reason"] = "execution-error"
    else:
        result["exit_code"] = completed.returncode
        result["status"] = result["canary"] = "PASS" if completed.returncode == 0 else "FAIL"
        result["reason"] = "ok" if completed.returncode == 0 else "nonzero-exit"
    finally:
        result["elapsed_ms"] = max(0, round((time.monotonic() - started) * 1000))
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", required=True)
    parser.add_argument("--argv", required=True, choices=sorted(_CLI_FLAGS))
    parser.add_argument("--provider", required=True)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--timeout-seconds", required=True, type=float)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--evidence-ref", required=True)
    parser.add_argument("--output", type=Path)
    options = parser.parse_args(argv)
    document = run_canary(
        options.executable, (options.argv,), options.provider, options.runtime,
        options.model, options.timeout_seconds, options.run_id, options.evidence_ref,
    )
    encoded = json.dumps(document, sort_keys=True, separators=(",", ":"))
    if options.output is None:
        print(encoded)
    else:
        options.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
