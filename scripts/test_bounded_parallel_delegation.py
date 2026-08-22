#!/usr/bin/env python3
"""Focused offline checks for bounded parallel delegation."""

from __future__ import annotations

import copy
import json
import math
import subprocess
import sys
from pathlib import Path

try:
    from scripts.check_bounded_parallel_delegation import validate
except ModuleNotFoundError:
    from check_bounded_parallel_delegation import validate


CHECKER = Path(__file__).with_name("check_bounded_parallel_delegation.py")


def document() -> dict[str, object]:
    run_id = "run-gl-ejw-15"
    return {
        "bead_id": "gl-ejw.15",
        "run_id": run_id,
        "capabilities": [
            {"id": "luna", "runtime": "codex", "channel": "codex", "model": "gpt-5.6-luna",
             "status": "available", "probe": {"status": "available", "exit_code": 0,
             "elapsed_seconds": 1, "canary": "PASS", "capability_id": "luna", "run_id": run_id}},
            {"id": "agy-flash", "runtime": "agy", "channel": "agy", "model": "gemini-flash",
             "status": "unavailable", "probe": {"status": "unavailable", "exit_code": None,
             "elapsed_seconds": 0, "canary": "NOT RUN", "capability_id": "agy-flash", "run_id": run_id}},
        ],
        "policy": {"max_lanes": 2, "timeout_seconds": 60, "quota_units": 2, "cost_cap_usd": 0,
                   "fallback": None},
        "lanes": [
            {"id": "luna-read", "capability_id": "luna", "mode": "read",
             "scope": ["standards/domain/agent_loops"], "dedupe_key": "luna-read-v1", "required": True},
            {"id": "agy-read", "capability_id": "agy-flash", "mode": "read",
             "scope": ["standards/domain/change-receipts-standard.md"], "dedupe_key": "agy-read-v1", "required": False},
        ],
        "outcomes": [{"lane_id": "luna-read", "status": "not_run"},
                     {"lane_id": "agy-read", "status": "not_run"}],
        "aggregate": {"status": "NOT RUN", "completed": 0, "not_run": 2,
                       "elapsed_seconds": 0, "quota_used": 0, "cost_usd": 0},
    }


def available(capability: dict[str, object]) -> None:
    capability["status"] = "available"
    probe = capability["probe"]
    assert isinstance(probe, dict)
    probe.update(status="available", exit_code=0, elapsed_seconds=1, canary="PASS")


def expect_failure(candidate: dict[str, object], reason: str | None = None) -> None:
    result = validate(candidate)
    assert result["status"] == "FAIL", result
    if reason:
        assert reason in result["reasons"], result


def main() -> int:
    assert validate(document())["status"] == "NOT RUN"

    verified = document()
    available(verified["capabilities"][1])  # type: ignore[index]
    verified["outcomes"] = [{"lane_id": "luna-read", "status": "verified"},
                             {"lane_id": "agy-read", "status": "verified"}]
    verified["aggregate"] = {"status": "PASS", "completed": 2, "not_run": 0,
                              "elapsed_seconds": 30, "quota_used": 2, "cost_usd": 0}
    assert validate(verified)["status"] == "PASS"

    optional_not_run = copy.deepcopy(verified)
    optional_not_run["outcomes"] = [{"lane_id": "luna-read", "status": "verified"},
                                     {"lane_id": "agy-read", "status": "not_run"}]
    optional_not_run["capabilities"][1]["status"] = "unavailable"  # type: ignore[index]
    optional_not_run["capabilities"][1]["probe"].update(  # type: ignore[index]
        status="unavailable", exit_code=None, elapsed_seconds=0, canary="NOT RUN")
    optional_not_run["aggregate"] = {"status": "PASS", "completed": 1, "not_run": 1,
                                      "elapsed_seconds": 1, "quota_used": 1, "cost_usd": 0}
    assert validate(optional_not_run)["status"] == "PASS"

    required_not_run = document()
    required_not_run["aggregate"]["status"] = "PASS"  # type: ignore[index]
    expect_failure(required_not_run, "AGGREGATE_STATUS_MISMATCH")

    duplicate = document()
    duplicate["lanes"][1]["dedupe_key"] = "luna-read-v1"  # type: ignore[index]
    expect_failure(duplicate)

    overlap = document()
    overlap["lanes"][1]["scope"] = ["standards/domain/./agent_loops/child"]  # type: ignore[index]
    expect_failure(overlap, "OVERLAPPING_SCOPE")

    missing = document()
    missing["lanes"][1]["capability_id"] = "missing"  # type: ignore[index]
    expect_failure(missing, "CAPABILITY_REFERENCE_MISSING")

    fallback = document()
    fallback["policy"]["fallback"] = {"capability_id": "luna", "max_attempts": 1}  # type: ignore[index]
    expect_failure(fallback, "FALLBACK_SAME_AS_PRIMARY")

    over_cap = document()
    over_cap["aggregate"]["elapsed_seconds"] = 61  # type: ignore[index]
    expect_failure(over_cap, "ELAPSED_SECONDS_CAP_EXCEEDED")

    for value in (math.inf, math.nan):
        non_finite = document()
        non_finite["policy"]["timeout_seconds"] = value  # type: ignore[index]
        expect_failure(non_finite, "INVALID_TIMEOUT_SECONDS")

    zero_lanes = document()
    zero_lanes.update(lanes=[], outcomes=[], aggregate={"status": "PASS", "completed": 0, "not_run": 0,
                                                        "elapsed_seconds": 0, "quota_used": 0, "cost_usd": 0})
    expect_failure(zero_lanes, "NO_LANES")

    for field, value in (("debug", "content"), ("token", "opaque")):
        forbidden = document()
        forbidden["outcomes"][0][field] = value  # type: ignore[index]
        expect_failure(forbidden)

    fake_probe = document()
    fake_probe["capabilities"][0]["probe"] = "fake"  # type: ignore[index]
    expect_failure(fake_probe, "INVALID_CAPABILITY_PROBE")

    stale_probe = document()
    stale_probe["capabilities"][0]["probe"]["run_id"] = "other-run"  # type: ignore[index]
    expect_failure(stale_probe, "INVALID_CAPABILITY_PROBE")

    bad_verified = document()
    bad_verified["capabilities"][0]["probe"]["canary"] = "NOT RUN"  # type: ignore[index]
    bad_verified["outcomes"][0]["status"] = "verified"  # type: ignore[index]
    bad_verified["aggregate"] = {"status": "PASS", "completed": 1, "not_run": 1,
                                  "elapsed_seconds": 1, "quota_used": 1, "cost_usd": 0}
    expect_failure(bad_verified, "INVALID_CAPABILITY_PROBE")

    malformed_membership_cases = (
        ("lane capability_id", lambda candidate, value: candidate["lanes"][0].update(capability_id=value)),
        ("lane mode", lambda candidate, value: candidate["lanes"][0].update(mode=value)),
        ("capability status", lambda candidate, value: candidate["capabilities"][0].update(status=value)),
        ("outcome status", lambda candidate, value: candidate["outcomes"][0].update(status=value)),
        ("aggregate status", lambda candidate, value: candidate["aggregate"].update(status=value)),
        ("probe canary", lambda candidate, value: candidate["capabilities"][0]["probe"].update(canary=value)),
    )
    for label, mutate in malformed_membership_cases:
        for value in ([], {}):
            malformed = document()
            mutate(malformed, value)
            result = validate(malformed)
            assert set(result) == {"status", "reasons", "redaction_status"}, (label, value, result)
            assert result["status"] == "FAIL", (label, value, result)
            assert result["reasons"], (label, value, result)

    malformed_cli = copy.deepcopy(document())
    malformed_cli["aggregate"]["status"] = []  # type: ignore[index]
    cli_result = subprocess.run([sys.executable, str(CHECKER)], input=json.dumps(malformed_cli), text=True,
                                capture_output=True, check=False)
    assert cli_result.returncode == 1, cli_result
    assert not cli_result.stderr, cli_result
    assert json.loads(cli_result.stdout)["status"] == "FAIL", cli_result.stdout

    invalid_cli = subprocess.run([sys.executable, str(CHECKER)], input="{", text=True,
                                 capture_output=True, check=False)
    assert invalid_cli.returncode != 0, invalid_cli
    valid_cli = subprocess.run([sys.executable, str(CHECKER)], input=json.dumps(document()), text=True,
                               capture_output=True, check=False)
    assert valid_cli.returncode == 0, valid_cli
    print("PASS bounded parallel delegation checker")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
