#!/usr/bin/env python3
"""Focused offline checks for agent_execution_governor."""

from __future__ import annotations

import json

import agent_execution_governor as governor


def request(**changes: object) -> dict[str, object]:
    document: dict[str, object] = {
        "issues": [
            {"id": "gl.10", "priority": 2, "status": "open", "dependency_count": 0, "labels": []},
            {"id": "gl.2", "priority": 1, "status": "open", "dependency_count": 0, "labels": []},
            {"id": "gl.1", "priority": 1, "status": "open", "dependency_count": 0, "labels": []},
            {"id": "gl.blocked", "priority": 0, "status": "open", "dependency_count": 1, "labels": []},
            {"id": "gl.not-ready", "priority": 0, "status": "open", "ready": False, "dependency_count": 0, "labels": []},
            {"id": "gl.closed", "priority": 0, "status": "closed", "dependency_count": 0, "labels": []},
        ],
        "active_runs": [],
        "wip_count": 0,
        "capabilities": {"beads": {"status": "available", "valid_until": 101}},
        "permissions": {"repo-write": {"status": "granted", "valid_until": 101}},
        "allowed_paths": {"/repo": {"status": "allowed", "valid_until": 101}},
        "policy": {
            "as_of": 100,
            "wip_limit": 1,
            "required_capabilities": ["beads"],
            "required_permissions": ["repo-write"],
            "requested_path": "/repo",
            "budget": {"attempts_used": 0, "attempt_limit": 1, "elapsed_seconds": 0,
                       "timeout_seconds": 60, "tokens_used": 0, "token_budget": 100},
        },
    }
    document.update(changes)
    return document


def assert_forbidden_free(value: object) -> None:
    forbidden = ("prompt", "response", "transcript", "payload", "credential", "secret", "environment")
    if isinstance(value, dict):
        assert not any(any(word in str(key).lower() for word in forbidden) for key in value)
        for nested in value.values():
            assert_forbidden_free(nested)
    elif isinstance(value, list):
        for nested in value:
            assert_forbidden_free(nested)


def main() -> int:
    chosen = governor.decide(request())
    assert chosen["action"] == "allow" and chosen["selected_issue"] == "gl.1"
    assert governor.decide(request()) == chosen  # deterministic, including evidence order
    assert governor.decide(request(wip_count=1))["reason"] == "WIP_LIMIT_REACHED"

    expired = request()
    expired["capabilities"] = {"beads": {"status": "available", "valid_until": 100}}
    assert governor.decide(expired)["reason"] == "CAPABILITY_UNAVAILABLE"
    assert governor.decide(request(permissions={}))["reason"] == "PERMISSION_UNAVAILABLE"
    unauthorized = request(allowed_paths={"/repo": {"status": "allowed", "valid_until": 100}})
    assert governor.decide(unauthorized)["reason"] == "PATH_UNAUTHORIZED"

    no_ready = request(issues=[])
    fallback = governor.decide({**no_ready, "fallback": {"id": "offline-check", "safe": True, "attempts_used": 0}})
    exhausted = governor.decide({**no_ready, "fallback": {"id": "offline-check", "safe": True, "attempts_used": 1}})
    assert fallback["action"] == "allow" and fallback["next_action"] == "RUN_SAFE_FALLBACK"
    assert exhausted["action"] == "escalate" and exhausted["next_action"] == "OWNER_QUEUE"

    duplicate = request(active_runs=[{"issue_id": "gl.1", "status": "running"}])
    assert governor.decide(duplicate)["selected_issue"] == "gl.2"
    assert governor.decide(request(active_runs=[{"issue_id": "gl.1", "status": "unknown"}]))["selected_issue"] == "gl.2"
    for key, reason in (("attempts_used", "RETRY_BUDGET_EXHAUSTED"), ("elapsed_seconds", "TIMEOUT_BUDGET_EXHAUSTED"),
                        ("tokens_used", "TOKEN_BUDGET_EXHAUSTED")):
        limited = request()
        budget = dict(limited["policy"]["budget"])  # type: ignore[index]
        budget[key] = budget[{"attempts_used": "attempt_limit", "elapsed_seconds": "timeout_seconds", "tokens_used": "token_budget"}[key]]
        limited["policy"] = {**limited["policy"], "budget": budget}  # type: ignore[arg-type,index]
        assert governor.decide(limited)["reason"] == reason

    assert chosen["fanout"] == {"allowed": False, "condition": "not-requested", "lane_limit": 1}
    missing_fanout = request()
    missing_fanout["policy"] = {**missing_fanout["policy"], "fanout": {"requested": True, "trigger": "bounded-review", "lane_limit": 2}}  # type: ignore[arg-type,index]
    assert governor.decide(missing_fanout)["fanout"]["condition"] == "fanout-capability-unavailable"
    fanout = request()
    fanout["capabilities"] = {"beads": {"status": "available", "valid_until": 101},
                              "fanout": {"status": "available", "valid_until": 101}}
    fanout["policy"] = {**fanout["policy"], "fanout": {"requested": True, "trigger": "bounded-review", "lane_limit": 2}}  # type: ignore[arg-type,index]
    assert governor.decide(fanout)["fanout"] == {"allowed": True, "condition": "explicit-bounded-trigger", "lane_limit": 2}
    assert_forbidden_free(chosen)
    assert "gl.1" not in json.dumps(governor.decide({**request(), "secret": "not-output"}))
    assert governor.decide({**request(), "secret": "not-output"})["action"] == "escalate"
    print("PASS metadata-only execution governor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
