#!/usr/bin/env python3
"""Deterministic, provider-free checker for bounded parallel delegation."""

from __future__ import annotations

import argparse
import json
import math
import posixpath
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

try:
    from scripts.agent_execution_governor import FORBIDDEN_FIELD_PARTS
except ModuleNotFoundError:
    from agent_execution_governor import FORBIDDEN_FIELD_PARTS


CAPABILITY_STATUSES = frozenset({"available", "unavailable", "quota_exhausted", "not_run"})
OUTCOME_STATUSES = frozenset({"verified", "failed", "timeout", "quota_exhausted", "not_run", "blocked"})
AGGREGATE_STATUSES = frozenset({"PASS", "NOT RUN", "FAIL", "BLOCKED"})
PROBE_CANARIES = frozenset({"PASS", "NOT RUN"})
PROBE_MAX_SECONDS = 30
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,63}$")
SCOPE_PATH = re.compile(r"^[A-Za-z0-9._/-]+$")

TOP_LEVEL_KEYS = frozenset({"bead_id", "run_id", "capabilities", "policy", "lanes", "outcomes", "aggregate"})
CAPABILITY_KEYS = frozenset({"id", "runtime", "channel", "model", "status", "probe"})
PROBE_KEYS = frozenset({"status", "exit_code", "elapsed_seconds", "canary", "capability_id", "run_id"})
POLICY_KEYS = frozenset({"max_lanes", "timeout_seconds", "quota_units", "cost_cap_usd", "fallback"})
FALLBACK_KEYS = frozenset({"capability_id", "max_attempts"})
LANE_KEYS = frozenset({"id", "capability_id", "mode", "scope", "dedupe_key", "required"})
OUTCOME_KEYS = frozenset({"lane_id", "status"})
AGGREGATE_KEYS = frozenset({"status", "completed", "not_run", "elapsed_seconds", "quota_used", "cost_usd"})


def validate(document: Any) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(document, Mapping) or _has_forbidden_field(document):
        return _result("FAIL", ["INVALID_METADATA"])
    if set(document) != TOP_LEVEL_KEYS:
        errors.append("INVALID_METADATA_SCHEMA")

    capabilities = document.get("capabilities")
    lanes = document.get("lanes")
    policy = document.get("policy")
    aggregate = document.get("aggregate")
    outcomes = document.get("outcomes")
    if not all(isinstance(value, list) for value in (capabilities, lanes, outcomes)):
        return _result("FAIL", ["INVALID_SHAPE"])
    if not isinstance(policy, Mapping) or not isinstance(aggregate, Mapping):
        return _result("FAIL", ["INVALID_SHAPE"])
    if set(policy) != POLICY_KEYS or set(aggregate) != AGGREGATE_KEYS:
        errors.append("INVALID_METADATA_SCHEMA")
    if not _identifier(document.get("bead_id")) or not _identifier(document.get("run_id")):
        errors.append("MISSING_IDENTITY")
    run_id = document.get("run_id")

    max_lanes = policy.get("max_lanes")
    if not _integer_between(max_lanes, 1, 3):
        errors.append("INVALID_MAX_LANES")
    for key in ("timeout_seconds", "quota_units", "cost_cap_usd"):
        if not _nonnegative_number(policy.get(key)):
            errors.append(f"INVALID_{key.upper()}")

    capability_map: dict[str, Mapping[str, Any]] = {}
    for capability in capabilities:
        if not isinstance(capability, Mapping) or set(capability) != CAPABILITY_KEYS:
            errors.append("INVALID_METADATA_SCHEMA")
            continue
        capability_id = capability.get("id")
        if not _identifier(capability_id):
            errors.append("INVALID_CAPABILITY")
            continue
        if capability_id in capability_map:
            errors.append("DUPLICATE_CAPABILITY")
        capability_map[capability_id] = capability
        if (not _identifier(capability.get("runtime")) or not _identifier(capability.get("channel"))
                or not _identifier(capability.get("model"))
                or capability.get("status") not in CAPABILITY_STATUSES):
            errors.append("INVALID_CAPABILITY")
        elif not _valid_probe(capability, run_id):
            errors.append("INVALID_CAPABILITY_PROBE")

    lane_ids: set[str] = set()
    dedupe_keys: set[str] = set()
    scopes: list[tuple[str, ...]] = []
    lane_by_id: dict[str, Mapping[str, Any]] = {}
    primary_capabilities: set[str] = set()
    for lane in lanes:
        if not isinstance(lane, Mapping) or set(lane) != LANE_KEYS:
            errors.append("INVALID_METADATA_SCHEMA")
            continue
        lane_id = lane.get("id")
        dedupe_key = lane.get("dedupe_key")
        if (not _identifier(lane_id) or lane_id in lane_ids or not _identifier(dedupe_key)
                or dedupe_key in dedupe_keys or not isinstance(lane.get("required"), bool)):
            errors.append("INVALID_LANE")
        if isinstance(lane_id, str):
            lane_ids.add(lane_id)
            lane_by_id[lane_id] = lane
        if isinstance(dedupe_key, str):
            dedupe_keys.add(dedupe_key)
        capability_id = lane.get("capability_id")
        if _identifier(capability_id):
            primary_capabilities.add(capability_id)
        normalized_scope = _normalized_scope(lane.get("scope"))
        if lane.get("mode") not in {"read", "write"} or normalized_scope is None:
            errors.append("INVALID_LANE_SCOPE")
        elif any(_scopes_overlap(normalized_scope, previous) for previous in scopes):
            errors.append("OVERLAPPING_SCOPE")
        elif len(set(normalized_scope)) != len(normalized_scope):
            errors.append("DUPLICATE_SCOPE")
        else:
            scopes.append(normalized_scope)
        if capability_id not in capability_map:
            errors.append("CAPABILITY_REFERENCE_MISSING")

    if not lanes:
        errors.append("NO_LANES")
    if not _integer_between(max_lanes, 1, 3) or len(lanes) > max_lanes:
        errors.append("LANE_LIMIT_EXCEEDED")

    fallback = policy.get("fallback")
    if fallback is not None:
        if not isinstance(fallback, Mapping) or set(fallback) != FALLBACK_KEYS or not _identifier(fallback.get("capability_id")):
            errors.append("INVALID_FALLBACK")
        else:
            fallback_id = fallback["capability_id"]
            if fallback_id not in capability_map:
                errors.append("FALLBACK_CAPABILITY_MISSING")
            if fallback_id in primary_capabilities:
                errors.append("FALLBACK_SAME_AS_PRIMARY")
            if fallback.get("max_attempts") != 1:
                errors.append("FALLBACK_NOT_BOUNDED")
            fallback_capability = capability_map.get(fallback_id)
            if fallback_capability and (fallback_capability.get("status") != "available"
                                        or not _valid_probe(fallback_capability, run_id)):
                errors.append("FALLBACK_NOT_PROBED")

    outcome_map: dict[str, Mapping[str, Any]] = {}
    for outcome in outcomes:
        if not isinstance(outcome, Mapping) or set(outcome) != OUTCOME_KEYS:
            errors.append("INVALID_METADATA_SCHEMA")
            continue
        lane_id = outcome.get("lane_id")
        if not _identifier(lane_id) or lane_id in outcome_map or lane_id not in lane_ids:
            errors.append("OUTCOME_LANE_MISMATCH")
        if outcome.get("status") not in OUTCOME_STATUSES:
            errors.append("INVALID_OUTCOME")
        if isinstance(lane_id, str):
            outcome_map[lane_id] = outcome
    if set(outcome_map) != lane_ids:
        errors.append("OUTCOME_COUNT_MISMATCH")

    statuses = [outcome.get("status") for outcome in outcome_map.values()]
    required_not_run = any(
        lane_by_id[lane_id].get("required") is True
        and (outcome.get("status") == "not_run"
             or capability_map.get(lane_by_id[lane_id].get("capability_id"), {}).get("status") != "available")
        for lane_id, outcome in outcome_map.items() if lane_id in lane_by_id
    )
    required_blocked = any(lane_by_id[lane_id].get("required") is True and outcome.get("status") == "blocked"
                           for lane_id, outcome in outcome_map.items() if lane_id in lane_by_id)
    if required_blocked:
        expected_status = "BLOCKED"
    elif required_not_run:
        expected_status = "NOT RUN"
    elif any(status in {"failed", "timeout", "quota_exhausted", "blocked"} for status in statuses):
        expected_status = "FAIL"
    else:
        expected_status = "PASS"
    if aggregate.get("status") not in AGGREGATE_STATUSES:
        errors.append("INVALID_AGGREGATE_STATUS")
    elif aggregate.get("status") != expected_status:
        errors.append("AGGREGATE_STATUS_MISMATCH")
    if aggregate.get("completed") != sum(status == "verified" for status in statuses):
        errors.append("AGGREGATE_COMPLETED_MISMATCH")
    if aggregate.get("not_run") != sum(status == "not_run" for status in statuses):
        errors.append("AGGREGATE_NOT_RUN_MISMATCH")
    if not _nonnegative_int(aggregate.get("completed")) or not _nonnegative_int(aggregate.get("not_run")):
        errors.append("INVALID_AGGREGATE_COUNT")
    for usage_key, policy_key in (("elapsed_seconds", "timeout_seconds"),
                                  ("quota_used", "quota_units"), ("cost_usd", "cost_cap_usd")):
        usage = aggregate.get(usage_key)
        if not _nonnegative_number(usage):
            errors.append(f"INVALID_{usage_key.upper()}")
        elif _nonnegative_number(policy.get(policy_key)) and usage > policy[policy_key]:
            errors.append(f"{usage_key.upper()}_CAP_EXCEEDED")

    for lane in lanes:
        if not isinstance(lane, Mapping):
            continue
        capability = capability_map.get(lane.get("capability_id"))
        outcome = outcome_map.get(lane.get("id"))
        if capability and outcome and outcome.get("status") == "verified":
            if capability.get("status") != "available" or not _valid_probe(capability, run_id):
                errors.append("UNSUPPORTED_VERIFIED_OUTCOME")

    if errors:
        return _result("FAIL", sorted(set(errors)))
    if expected_status == "NOT RUN":
        return _result("NOT RUN", ["NO_ELIGIBLE_CANARY"])
    if expected_status == "BLOCKED":
        return _result("BLOCKED", ["REQUIRED_LANE_BLOCKED"])
    return _result("PASS", ["BOUNDED_CONTRACT_VALID"])


def _result(status: str, reasons: list[str]) -> dict[str, Any]:
    return {"status": status, "reasons": reasons, "redaction_status": "metadata-only"}


def _has_forbidden_field(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(any(part in str(key).lower() for part in FORBIDDEN_FIELD_PARTS)
                   or _has_forbidden_field(nested) for key, nested in value.items())
    return isinstance(value, list) and any(_has_forbidden_field(item) for item in value)


def _identifier(value: Any) -> bool:
    return isinstance(value, str) and bool(IDENTIFIER.fullmatch(value))


def _normalized_scope(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not value:
        return None
    normalized: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item or not SCOPE_PATH.fullmatch(item) or item.startswith("/"):
            return None
        path = posixpath.normpath(item)
        if path in {"", "."} or path.startswith("../") or path == ".." or "/../" in f"/{path}/":
            return None
        normalized.append(path)
    return tuple(normalized)


def _scopes_overlap(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    return any(_path_is_ancestor(a, b) for a in left for b in right)


def _path_is_ancestor(left: str, right: str) -> bool:
    left_parts = left.split("/")
    right_parts = right.split("/")
    return left_parts == right_parts[:len(left_parts)] or right_parts == left_parts[:len(right_parts)]


def _valid_probe(capability: Mapping[str, Any], run_id: Any) -> bool:
    probe = capability.get("probe")
    if not isinstance(probe, Mapping) or set(probe) != PROBE_KEYS:
        return False
    status = capability.get("status")
    if (probe.get("status") != status or probe.get("capability_id") != capability.get("id")
            or probe.get("run_id") != run_id or probe.get("canary") not in PROBE_CANARIES
            or not _nonnegative_number(probe.get("elapsed_seconds"))
            or probe.get("elapsed_seconds") > PROBE_MAX_SECONDS):
        return False
    exit_code = probe.get("exit_code")
    if exit_code is not None and not _nonnegative_int(exit_code):
        return False
    if status == "available":
        return exit_code == 0 and probe.get("canary") == "PASS"
    return probe.get("canary") == "NOT RUN"


def _nonnegative_number(value: Any) -> bool:
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value >= 0)


def _nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _integer_between(value: Any, lower: int, upper: int) -> bool:
    return _nonnegative_int(value) and lower <= value <= upper


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, help="JSON file; stdin when omitted")
    args = parser.parse_args()
    try:
        raw = args.source.read_text(encoding="utf-8") if args.source else sys.stdin.read()
        document = json.loads(raw)
    except (OSError, json.JSONDecodeError):
        document = None
    result = validate(document)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
