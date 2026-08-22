#!/usr/bin/env python3
"""Focused checks for the metadata-only provider canary."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

if __package__:
    from .provider_canary import run_canary
else:
    from provider_canary import run_canary


ROOT = Path(__file__).resolve().parents[1]
CANARY = ROOT / "scripts" / "provider_canary.py"


def call(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "executable": sys.executable,
        "argv": ("--version",),
        "provider": "test-provider",
        "runtime": "python",
        "model": "test-model",
        "timeout_seconds": 2,
        "run_id": "run-1",
        "evidence_ref": "evidence-1",
    }
    values.update(overrides)
    return run_canary(**values)


def main() -> int:
    expected = {"provider", "runtime", "model", "status", "canary", "exit_code",
                "elapsed_ms", "reason", "redaction_status"}

    passed = call()
    assert set(passed) == expected
    assert passed["status"] == "PASS" and passed["canary"] == "PASS"
    assert passed["exit_code"] == 0 and passed["redaction_status"] == "metadata-only"
    assert isinstance(passed["elapsed_ms"], int) and passed["elapsed_ms"] >= 0

    missing = call(executable="definitely-not-a-real-provider-command")
    assert missing["status"] == missing["canary"] == "NOT RUN"
    assert missing["exit_code"] is None

    failed = call(argv=("-c", "raise SystemExit(3)"))
    assert failed["status"] == "FAIL" and failed["canary"] == "FAIL"
    assert failed["exit_code"] == 3

    timed_out = call(argv=("-c", "import time; time.sleep(2)"), timeout_seconds=0.05)
    assert timed_out["status"] == timed_out["canary"] == "NOT RUN"
    assert timed_out["exit_code"] is None

    for field, value in (("provider", "prompt:secret"), ("model", "response"),
                         ("run_id", "run id"), ("evidence_ref", "stdout:leak")):
        try:
            call(**{field: value})
        except ValueError:
            pass
        else:
            raise AssertionError(f"forbidden {field} was accepted")

    for flag in ("-h", "--help", "-v", "--version"):
        result = subprocess.run(
            [sys.executable, str(CANARY), "--executable", sys.executable, f"--argv={flag}",
             "--provider", "test-provider", "--runtime", "python", "--model", "test-model",
             "--timeout-seconds", "2", "--run-id", "run-1", "--evidence-ref", "evidence-1"],
            check=True, capture_output=True, text=True,
        )
        document = json.loads(result.stdout)
        assert set(document) == expected

    print("PASS provider canary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
