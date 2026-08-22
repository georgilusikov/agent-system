#!/usr/bin/env python3
"""Offline metadata-only Beads execution policy.

Input is JSON from stdin or one file.  It has ``issues``, ``active_runs``,
``wip_count``, fact maps (``capabilities``, ``permissions``,
``allowed_paths``), and ``policy``.  ``policy.as_of`` and every fact's
``valid_until`` are integer timestamps so a decision is deterministic.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping


FORBIDDEN_FIELD_PARTS = (
    "prompt", "response", "transcript", "payload", "credential", "secret", "environment",
)
TERMINAL_STATUSES = frozenset({"accepted", "partial", "blocked", "escalated", "failed", "cancelled"})


def decide(document: Mapping[str, Any]) -> dict[str, Any]:
    """Return one deterministic, metadata-only policy decision.

    ``policy`` requires ``as_of``, ``wip_limit``, ``required_capabilities``,
    ``required_permissions``, ``requested_path``, and ``budget``.  Budget has
    ``attempts_used``, ``attempt_limit``, ``elapsed_seconds``,
    ``timeout_seconds``, ``tokens_used``, and ``token_budget``.
    """
    if not isinstance(document, Mapping) or _has_forbidden_field(document):
        return _decision("escalate", None, "INVALID_METADATA", "OWNER_QUEUE", {}, ["input"])
    policy = document.get("policy")
    if not isinstance(policy, Mapping):
        return _decision("escalate", None, "INVALID_POLICY", "OWNER_QUEUE", {}, ["policy"])
    try:
        as_of = _nonnegative_int(policy["as_of"])
        wip_limit = _positive_int(policy["wip_limit"])
        required_capabilities = _names(policy["required_capabilities"])
        required_permissions = _names(policy["required_permissions"])
        requested_path = _nonempty_string(policy["requested_path"])
        budget = _budget(policy["budget"])
    except (KeyError, ValueError, TypeError):
        return _decision("escalate", None, "INVALID_POLICY", "OWNER_QUEUE", {}, ["policy"])

    fanout = _fanout(policy, document.get("capabilities"), as_of)
    extras = {"fanout": fanout, "budget": budget}
    fact_failure = _required_fact_failure(document.get("capabilities"), required_capabilities, as_of, "available")
    if fact_failure:
        return _decision("defer", None, "CAPABILITY_UNAVAILABLE", "REFRESH_CAPABILITY_FACTS", extras, ["capabilities"])
    fact_failure = _required_fact_failure(document.get("permissions"), required_permissions, as_of, "granted")
    if fact_failure:
        return _decision("defer", None, "PERMISSION_UNAVAILABLE", "REFRESH_PERMISSION_FACTS", extras, ["permissions"])
    if not _fact_is_current(_lookup_fact(document.get("allowed_paths"), requested_path), as_of, "allowed"):
        return _decision("defer", None, "PATH_UNAUTHORIZED", "REFRESH_PATH_FACTS", extras, ["allowed_paths"])
    limit_reason = _budget_limit(budget)
    if limit_reason:
        return _decision("defer", None, limit_reason, "WAIT_FOR_BUDGET", extras, ["budget"])

    active_ids, wip_error = _active_claims(document.get("active_runs", []))
    if wip_error:
        return _decision("escalate", None, wip_error, "OWNER_QUEUE", extras, ["active_runs"])
    derived_wip_count = len(active_ids)
    if ("wip_count" in document and (not _is_nonnegative_int(document["wip_count"])
                                    or document["wip_count"] != derived_wip_count)):
        return _decision("escalate", None, "INVALID_WIP_COUNT", "OWNER_QUEUE", extras, ["active_runs", "wip"])
    candidate = _select_issue(document.get("issues"), active_ids)
    if derived_wip_count >= wip_limit:
        return _decision("defer", candidate, "WIP_LIMIT_REACHED", "WAIT_FOR_WIP", extras, ["active_runs", "wip"])
    if candidate is not None:
        return _decision("allow", candidate, "READY_ISSUE_SELECTED", "START_ONE_LANE", extras, ["issues", "active_runs", "budgets"])
    if _safe_fallback(document.get("fallback")):
        return _decision("allow", None, "SAFE_FALLBACK_AVAILABLE", "RUN_SAFE_FALLBACK", extras, ["issues", "fallback"])
    return _decision("escalate", None, "NO_READY_ISSUE_OR_FALLBACK_EXHAUSTED", "OWNER_QUEUE", extras, ["issues", "fallback"])


def _decision(action: str, issue_id: str | None, reason: str, next_action: str,
              extras: Mapping[str, Any], evidence_refs: list[str]) -> dict[str, Any]:
    return {
        "action": action,
        "selected_issue": issue_id,
        "reason": reason,
        "next_action": next_action,
        "timeout_seconds": extras.get("budget", {}).get("timeout_seconds", 0),
        "retry_budget": extras.get("budget", {}).get("attempt_limit", 0),
        "token_budget": extras.get("budget", {}).get("token_budget", 0),
        "fanout": extras.get("fanout", {"allowed": False, "condition": "not-evaluated", "lane_limit": 1}),
        "evidence_refs": evidence_refs,
    }


def _select_issue(issues: Any, active_ids: set[str]) -> str | None:
    if not isinstance(issues, list):
        return None
    ready: list[tuple[int, str]] = []
    for issue in issues:
        if not isinstance(issue, Mapping):
            continue
        issue_id = issue.get("id")
        priority = issue.get("priority")
        if (not isinstance(issue_id, str) or not issue_id or not _is_nonnegative_int(priority)
                or issue.get("status") != "open" or issue_id in active_ids):
            continue
        if issue.get("ready") is False or issue.get("dependency_count") != 0:
            continue
        ready.append((priority, issue_id))
    return min(ready, default=None)[1] if ready else None


def _active_claims(active_runs: Any) -> tuple[set[str], str | None]:
    if not isinstance(active_runs, list):
        return set(), "INVALID_ACTIVE_RUNS"
    claims: list[str] = []
    for run in active_runs:
        if not isinstance(run, Mapping):
            return set(), "INVALID_ACTIVE_RUNS"
        if run.get("status") in TERMINAL_STATUSES:
            continue
        issue_id = run.get("issue_id")
        if not isinstance(issue_id, str) or not issue_id:
            return set(), "INVALID_ACTIVE_CLAIM"
        claims.append(issue_id)
    if len(claims) != len(set(claims)):
        return set(), "DUPLICATE_ACTIVE_CLAIM"
    return set(claims), None


def _required_fact_failure(facts: Any, names: tuple[str, ...], as_of: int, status: str) -> bool:
    return any(not _fact_is_current(_lookup_fact(facts, name), as_of, status) for name in names)


def _lookup_fact(facts: Any, name: str) -> Any:
    return facts.get(name) if isinstance(facts, Mapping) else None


def _fact_is_current(fact: Any, as_of: int, expected_status: str) -> bool:
    return (isinstance(fact, Mapping) and fact.get("status") == expected_status
            and _is_nonnegative_int(fact.get("valid_until")) and fact["valid_until"] > as_of)


def _budget(value: Any) -> dict[str, int]:
    if not isinstance(value, Mapping):
        raise ValueError("budget")
    return {key: _nonnegative_int(value[key]) for key in (
        "attempts_used", "attempt_limit", "elapsed_seconds", "timeout_seconds", "tokens_used", "token_budget",
    )}


def _budget_limit(budget: Mapping[str, int]) -> str | None:
    if budget["attempt_limit"] == 0 or budget["attempts_used"] >= budget["attempt_limit"]:
        return "RETRY_BUDGET_EXHAUSTED"
    if budget["timeout_seconds"] == 0 or budget["elapsed_seconds"] >= budget["timeout_seconds"]:
        return "TIMEOUT_BUDGET_EXHAUSTED"
    if budget["token_budget"] == 0 or budget["tokens_used"] >= budget["token_budget"]:
        return "TOKEN_BUDGET_EXHAUSTED"
    return None


def _fanout(policy: Mapping[str, Any], capabilities: Any, as_of: int) -> dict[str, Any]:
    request = policy.get("fanout")
    if not isinstance(request, Mapping) or not request.get("requested", False):
        return {"allowed": False, "condition": "not-requested", "lane_limit": 1}
    trigger = request.get("trigger")
    lane_limit = request.get("lane_limit")
    if not isinstance(trigger, str) or not trigger or not _is_nonnegative_int(lane_limit) or not 2 <= lane_limit <= 8:
        return {"allowed": False, "condition": "missing-bounded-trigger", "lane_limit": 1}
    if not _fact_is_current(_lookup_fact(capabilities, "fanout"), as_of, "available"):
        return {"allowed": False, "condition": "fanout-capability-unavailable", "lane_limit": 1}
    return {"allowed": True, "condition": "explicit-bounded-trigger", "lane_limit": lane_limit}


def _safe_fallback(fallback: Any) -> bool:
    return (isinstance(fallback, Mapping) and fallback.get("safe") is True
            and fallback.get("attempts_used") == 0 and isinstance(fallback.get("id"), str) and bool(fallback["id"]))


def _names(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(name, str) and name for name in value):
        raise ValueError("fact names")
    return tuple(value)


def _nonempty_string(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("string")
    return value


def _positive_int(value: Any) -> int:
    value = _nonnegative_int(value)
    if value == 0:
        raise ValueError("positive integer")
    return value


def _nonnegative_int(value: Any) -> int:
    if not _is_nonnegative_int(value):
        raise ValueError("non-negative integer")
    return value


def _is_nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _has_forbidden_field(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(any(part in str(key).lower() for part in FORBIDDEN_FIELD_PARTS) or _has_forbidden_field(nested)
                   for key, nested in value.items())
    return isinstance(value, list) and any(_has_forbidden_field(item) for item in value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, help="JSON file; stdin when omitted")
    args = parser.parse_args()
    try:
        source = args.source.read_text(encoding="utf-8") if args.source else sys.stdin.read()
        document = json.loads(source)
    except (OSError, json.JSONDecodeError):
        document = {}
    print(json.dumps(decide(document), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
