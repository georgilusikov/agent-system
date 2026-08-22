#!/usr/bin/env python3
"""Focused offline checks for the before/after evaluation contract."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import evaluate_before_after as evaluation


SHA = "a" * 40
CONFIG_SHA = "b" * 64


def args(**changes: object) -> dict[str, object]:
    document: dict[str, object] = {
        "run_id": "run-1",
        "hypothesis_id": "hypothesis-1",
        "change_type": "initial",
        "supersedes_run_id": None,
        "baseline_commit": SHA,
        "treatment_commit": "c" * 40,
        "baseline_config": CONFIG_SHA,
        "treatment_config": "d" * 64,
    }
    document.update(changes)
    return document


def main() -> int:
    not_run = evaluation.build_not_run(**args())
    assert not_run["status"] == "not_run"
    assert len(not_run["records"]) == 10
    assert {record["task_id"] for record in not_run["records"]} == set(evaluation.TASK_IDS.values())
    assert all(record["verdict"] == "not_run" for record in not_run["records"])
    assert all(set(record["dimensions"]) == set(evaluation.DIMENSIONS) for record in not_run["records"])
    assert {"clarity", "context", "terminology"} <= set(evaluation.DIMENSIONS)
    assert "clarity_context_terminology" not in evaluation.DIMENSIONS
    assert all(record["latency_ms"] is None and record["cost_usd"] is None for record in not_run["records"])
    assert all(pair["verdict"] == "not_run" for pair in not_run["comparisons"])

    observed_records = []
    for task_class, task_id in evaluation.TASK_IDS.items():
        for variant, commit_sha, config_sha in (
            ("baseline", SHA, CONFIG_SHA),
            ("treatment", "c" * 40, "d" * 64),
        ):
            observed_records.append({
                "run_id": "run-1",
                "task_id": task_id,
                "task_class": task_class,
                "variant": variant,
                "commit_sha": commit_sha,
                "config_sha": config_sha,
                "status": "observed",
                "verdict": "confirmed" if variant == "treatment" else "partially",
                "dimensions": {dimension: "confirmed" for dimension in evaluation.DIMENSIONS},
                "evidence_refs": [f"check:run-1:{variant}:{task_class}"],
                "latency_ms": 12.5,
                "cost_usd": 0.01,
                "not_run_reason": None,
            })
    comparisons = {task_id: "confirmed" for task_id in evaluation.TASK_IDS.values()}
    observed = evaluation.build_observed(
        **args(), records=observed_records, comparison_verdicts=comparisons)
    assert observed["status"] == "observed"
    assert all(pair["verdict"] == "confirmed" for pair in observed["comparisons"])
    assert evaluation.validate_envelope(observed) == observed
    tampered = json.loads(json.dumps(observed))
    tampered["comparisons"][0]["baseline"]["commit_sha"] = "e" * 40
    try:
        evaluation.validate_envelope(tampered)
    except evaluation.EvaluationError:
        pass
    else:
        raise AssertionError("tampered comparison was accepted")

    mixed_identity = json.loads(json.dumps(not_run))
    mixed_record = next(record for record in mixed_identity["records"] if record["variant"] == "treatment")
    mixed_record["commit_sha"] = "e" * 40
    mixed_record["config_sha"] = "f" * 64
    mixed_comparison = next(pair for pair in mixed_identity["comparisons"]
                            if pair["task_id"] == mixed_record["task_id"])
    mixed_comparison["treatment"] = {
        "commit_sha": mixed_record["commit_sha"],
        "config_sha": mixed_record["config_sha"],
        "verdict": mixed_record["verdict"],
    }
    try:
        evaluation.validate_envelope(mixed_identity)
    except evaluation.EvaluationError:
        pass
    else:
        raise AssertionError("mixed run identity was accepted")

    incomplete = json.loads(json.dumps(observed_records))
    incomplete[0]["dimensions"]["correctness"] = "not_run"
    try:
        evaluation.build_observed(**args(), records=incomplete, comparison_verdicts=comparisons)
    except evaluation.EvaluationError:
        pass
    else:
        raise AssertionError("observed record with a not_run dimension was accepted")

    for field in ("treatment_commit", "treatment_config"):
        baseline_field = "baseline_" + field.split("_", 1)[1]
        try:
            evaluation.build_not_run(**args(**{field: args()[baseline_field]}))
        except evaluation.EvaluationError:
            pass
        else:
            raise AssertionError(f"identical {field} identity was accepted")

    same_identity = json.loads(json.dumps(not_run))
    for record in same_identity["records"]:
        if record["variant"] == "treatment":
            record["commit_sha"], record["config_sha"] = SHA, CONFIG_SHA
    for comparison in same_identity["comparisons"]:
        comparison["treatment"] = dict(comparison["baseline"])
    try:
        evaluation.validate_envelope(same_identity)
    except evaluation.EvaluationError:
        pass
    else:
        raise AssertionError("identical NOT RUN comparison identities were accepted")

    changed = evaluation.build_not_run(
        **args(change_type="changed_hypothesis", supersedes_run_id="run-0"))
    assert changed["change_type"] == "changed_hypothesis"
    try:
        evaluation.build_not_run(**args(change_type="rollback"))
    except evaluation.EvaluationError:
        pass
    else:
        raise AssertionError("rollback without superseded run was accepted")

    unsafe = json.loads(json.dumps(observed_records))
    for evidence_ref in (
        "prompt:raw text",
        "this-is-a-full-user-message-without-forbidden-keywords",
        "note:abc:def:ghi",
        "check:run-1:baseline:" + "a" * 200,
    ):
        unsafe[0]["evidence_refs"] = [evidence_ref]
        try:
            evaluation.build_observed(**args(), records=unsafe, comparison_verdicts=comparisons)
        except evaluation.EvaluationError:
            pass
        else:
            raise AssertionError(f"unsafe evidence reference was accepted: {evidence_ref!r}")

    for malformed in ([None], [1]):
        try:
            evaluation.build_observed(**args(), records=malformed, comparison_verdicts=comparisons)
        except evaluation.EvaluationError:
            pass
        else:
            raise AssertionError(f"malformed records escaped EvaluationError: {malformed!r}")

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "result.json"
        evaluation.write_result(path, not_run)
        assert evaluation.load_result(path) == not_run
        assert "prompt" not in path.read_text(encoding="utf-8")
        mixed_path = Path(directory) / "mixed.json"
        mixed_path.write_text(json.dumps(mixed_identity), encoding="utf-8")
        try:
            evaluation.load_result(mixed_path)
        except evaluation.EvaluationError:
            pass
        else:
            raise AssertionError("load_result accepted mixed run identity")

    for invalid_path in (None, "result.json"):
        try:
            evaluation.write_result(invalid_path, not_run)  # type: ignore[arg-type]
        except evaluation.EvaluationError:
            pass
        else:
            raise AssertionError(f"write_result accepted invalid path: {invalid_path!r}")
        try:
            evaluation.load_result(invalid_path)  # type: ignore[arg-type]
        except evaluation.EvaluationError:
            pass
        else:
            raise AssertionError(f"load_result accepted invalid path: {invalid_path!r}")
    print("PASS before/after metadata-only evaluation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
