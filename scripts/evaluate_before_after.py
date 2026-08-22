#!/usr/bin/env python3
"""Create or validate metadata-only before/after evaluation results."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Mapping

if __package__:
    from .agent_run_state import FORBIDDEN_FIELD_PARTS, _reject_forbidden_fields
    from .runtime_receipts import ReceiptContext, emit_change, file_hash
else:
    from agent_run_state import FORBIDDEN_FIELD_PARTS, _reject_forbidden_fields
    from runtime_receipts import ReceiptContext, emit_change, file_hash


TASK_IDS = {
    "simple_explanation": "gl-ejw.12.simple-explanation",
    "architecture_choice": "gl-ejw.12.architecture-choice",
    "diagnosis": "gl-ejw.12.diagnosis",
    "research": "gl-ejw.12.research",
    "code_change": "gl-ejw.12.code-change",
}
DIMENSIONS = (
    "correctness", "safety", "clarity", "context", "terminology", "evidence",
    "decision_quality", "owner_effort", "latency", "cost",
)
VERDICTS = frozenset({"confirmed", "partially", "falsified", "not_run"})
OBSERVED_VERDICTS = VERDICTS - {"not_run"}
RECORD_FIELDS = frozenset({
    "run_id", "task_id", "task_class", "variant", "commit_sha", "config_sha",
    "status", "verdict", "dimensions", "evidence_refs", "latency_ms", "cost_usd",
    "not_run_reason",
})
COMPARISON_FIELDS = frozenset({"task_id", "task_class", "baseline", "treatment", "verdict"})
VARIANT_FIELDS = frozenset({"commit_sha", "config_sha", "verdict"})
ENVELOPE_FIELDS = frozenset({
    "schema_version", "run_id", "hypothesis_id", "change_type", "supersedes_run_id",
    "status", "redaction_status", "records", "comparisons",
})
SHA = re.compile(r"[0-9a-f]{7,64}\Z")
OPAQUE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{0,63}\Z")
EVIDENCE_REF = re.compile(
    r"(?:check|artifact|receipt|test):[a-z0-9][a-z0-9_.-]{0,31}"
    r":[a-z0-9][a-z0-9_.-]{0,31}:[a-z0-9][a-z0-9_.-]{0,31}\Z"
)
MAX_EVIDENCE_REF_LENGTH = 128


class EvaluationError(ValueError):
    """Input cannot be trusted as a metadata-only evaluation result."""


def build_not_run(*, run_id: str, hypothesis_id: str, change_type: str,
                  supersedes_run_id: str | None, baseline_commit: str,
                  treatment_commit: str, baseline_config: str,
                  treatment_config: str) -> dict[str, Any]:
    meta = _run_metadata(run_id, hypothesis_id, change_type, supersedes_run_id,
                         baseline_commit, treatment_commit, baseline_config, treatment_config)
    records = [
        _record(run_id, task_class, variant, commit_sha, config_sha, "not_run")
        for task_class, task_id in TASK_IDS.items()
        for variant, commit_sha, config_sha in (
            ("baseline", baseline_commit, baseline_config),
            ("treatment", treatment_commit, treatment_config),
        )
    ]
    return _envelope(meta, "not_run", records,
                     _comparisons(records, {task_id: "not_run" for task_id in TASK_IDS.values()}))


def build_observed(*, run_id: str, hypothesis_id: str, change_type: str,
                   supersedes_run_id: str | None, baseline_commit: str,
                   treatment_commit: str, baseline_config: str,
                   treatment_config: str, records: list[Mapping[str, Any]],
                   comparison_verdicts: Mapping[str, str]) -> dict[str, Any]:
    meta = _run_metadata(run_id, hypothesis_id, change_type, supersedes_run_id,
                         baseline_commit, treatment_commit, baseline_config, treatment_config)
    if not isinstance(records, list) or any(not isinstance(record, Mapping) for record in records):
        raise EvaluationError("records must be a list of objects")
    if not isinstance(comparison_verdicts, Mapping):
        raise EvaluationError("comparison verdicts must be an object")
    expected = {(task_id, variant) for task_id in TASK_IDS.values() for variant in ("baseline", "treatment")}
    normalized = [dict(record) for record in records]
    if len(normalized) != len(expected):
        raise EvaluationError("records must contain one baseline and treatment per task")
    for record in normalized:
        _validate_record(record, run_id, baseline_commit, treatment_commit, baseline_config, treatment_config)
    if {(record["task_id"], record["variant"]) for record in normalized} != expected:
        raise EvaluationError("records must contain one baseline and treatment per task")
    if set(comparison_verdicts) != set(TASK_IDS.values()):
        raise EvaluationError("comparison verdicts must cover all five stable task IDs")
    for verdict in comparison_verdicts.values():
        _one_of(verdict, OBSERVED_VERDICTS, "observed comparison verdict")
    return _envelope(meta, "observed", normalized, _comparisons(normalized, comparison_verdicts))


def validate_envelope(envelope: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(envelope, Mapping) or set(envelope) != ENVELOPE_FIELDS:
        raise EvaluationError("result fields do not match metadata-only contract")
    _reject_forbidden(envelope)
    if (not isinstance(envelope["schema_version"], int)
            or isinstance(envelope["schema_version"], bool)
            or envelope["schema_version"] != 1
            or not isinstance(envelope["redaction_status"], str)
            or envelope["redaction_status"] != "metadata-only"):
        raise EvaluationError("unsupported schema or redaction status")
    _opaque(envelope["run_id"], "run_id")
    _opaque(envelope["hypothesis_id"], "hypothesis_id")
    _run_metadata(envelope["run_id"], envelope["hypothesis_id"], envelope["change_type"],
                  envelope["supersedes_run_id"], "a" * 40, "b" * 40, "a" * 64, "b" * 64)
    _one_of(envelope["status"], {"observed", "not_run"}, "status")
    if not isinstance(envelope["records"], list):
        raise EvaluationError("invalid result status or records")
    if not isinstance(envelope["comparisons"], list) or len(envelope["comparisons"]) != len(TASK_IDS):
        raise EvaluationError("result must contain five comparisons")
    if len(envelope["records"]) != len(TASK_IDS) * 2:
        raise EvaluationError("result must contain ten task records")
    for record in envelope["records"]:
        if not isinstance(record, Mapping):
            raise EvaluationError("record must be an object")
        _validate_record(record, envelope["run_id"], None, None, None, None)
    _validate_run_identity(envelope["records"])
    statuses = {record["status"] for record in envelope["records"]}
    if statuses != {envelope["status"]}:
        raise EvaluationError("envelope status must match every record")
    _validate_comparisons(envelope["comparisons"], envelope["records"], envelope["status"])
    return dict(envelope)


def write_result(path: Path, result: Mapping[str, Any], *, receipt_context: ReceiptContext | None = None) -> None:
    if not isinstance(path, Path):
        raise EvaluationError("path must be a pathlib.Path")
    result = validate_envelope(result)
    if path.exists():
        if load_result(path) == result:
            return
        raise EvaluationError("result exists; use a new run_id for rollback or changed hypothesis")
    path.parent.mkdir(parents=True, exist_ok=True)
    before_hash = file_hash(path) if path.exists() else None
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(result, stream, sort_keys=True, separators=(",", ":"))
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        if receipt_context is not None:
            event_id = "evaluation-" + hashlib.sha256(
                f"{receipt_context.run_id}:evaluation.write:{path}".encode()).hexdigest()
            emit_change(receipt_context, event_id, "evaluation.write", "class:evaluation-result",
                        before_hash, file_hash(path), "applied")
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def load_result(path: Path) -> dict[str, Any]:
    if not isinstance(path, Path):
        raise EvaluationError("path must be a pathlib.Path")
    try:
        return validate_envelope(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        raise EvaluationError("result is unreadable") from error


def _run_metadata(run_id: str, hypothesis_id: str, change_type: str,
                  supersedes_run_id: str | None, baseline_commit: str,
                  treatment_commit: str, baseline_config: str,
                  treatment_config: str) -> dict[str, Any]:
    _opaque(run_id, "run_id")
    _opaque(hypothesis_id, "hypothesis_id")
    _one_of(change_type, {"initial", "changed_hypothesis", "rollback"}, "change_type")
    if change_type == "initial" and supersedes_run_id is not None:
        raise EvaluationError("initial run cannot supersede another run")
    if change_type != "initial":
        _opaque(supersedes_run_id, "supersedes_run_id")
        if supersedes_run_id == run_id:
            raise EvaluationError("run cannot supersede itself")
    for value, name in ((baseline_commit, "baseline_commit"), (treatment_commit, "treatment_commit"),
                        (baseline_config, "baseline_config"), (treatment_config, "treatment_config")):
        if not isinstance(value, str) or not SHA.fullmatch(value):
            raise EvaluationError(f"{name} must be a lowercase commit/config SHA")
    if baseline_commit == treatment_commit or baseline_config == treatment_config:
        raise EvaluationError("baseline and treatment commit/config SHAs must differ")
    return {"run_id": run_id, "hypothesis_id": hypothesis_id, "change_type": change_type,
            "supersedes_run_id": supersedes_run_id, "baseline_commit": baseline_commit,
            "treatment_commit": treatment_commit, "baseline_config": baseline_config,
            "treatment_config": treatment_config}


def _record(run_id: str, task_class: str, variant: str, commit_sha: str,
            config_sha: str, status: str) -> dict[str, Any]:
    return {"run_id": run_id, "task_id": TASK_IDS[task_class], "task_class": task_class,
            "variant": variant, "commit_sha": commit_sha, "config_sha": config_sha,
            "status": status, "verdict": "not_run", "dimensions": dict.fromkeys(DIMENSIONS, "not_run"),
            "evidence_refs": [], "latency_ms": None, "cost_usd": None,
            "not_run_reason": "live_consumer_unavailable"}


def _envelope(meta: Mapping[str, Any], status: str, records: list[dict[str, Any]],
              comparisons: list[dict[str, Any]]) -> dict[str, Any]:
    result = {"schema_version": 1, "run_id": meta["run_id"], "hypothesis_id": meta["hypothesis_id"],
              "change_type": meta["change_type"], "supersedes_run_id": meta["supersedes_run_id"],
              "status": status, "redaction_status": "metadata-only", "records": records,
              "comparisons": comparisons}
    for record in records:
        _validate_record(record, meta["run_id"], meta["baseline_commit"], meta["treatment_commit"],
                          meta["baseline_config"], meta["treatment_config"])
    return result


def _comparisons(records: list[Mapping[str, Any]], verdicts: Mapping[str, str]) -> list[dict[str, Any]]:
    by_key = {(record["task_id"], record["variant"]): record for record in records}
    return [{"task_id": task_id, "task_class": task_class,
             "baseline": {key: by_key[(task_id, "baseline")][key] for key in ("commit_sha", "config_sha", "verdict")},
             "treatment": {key: by_key[(task_id, "treatment")][key] for key in ("commit_sha", "config_sha", "verdict")},
             "verdict": verdicts[task_id]}
            for task_class, task_id in TASK_IDS.items()]


def _validate_comparisons(comparisons: list[Mapping[str, Any]], records: list[Mapping[str, Any]],
                          status: str) -> None:
    by_key = {(record["task_id"], record["variant"]): record for record in records}
    if set(by_key) != {(task_id, variant) for task_id in TASK_IDS.values() for variant in ("baseline", "treatment")}:
        raise EvaluationError("records do not form five baseline/treatment pairs")
    seen: set[str] = set()
    for comparison in comparisons:
        if not isinstance(comparison, Mapping) or set(comparison) != COMPARISON_FIELDS:
            raise EvaluationError("comparison fields do not match metadata-only contract")
        task_id = comparison["task_id"]
        if not isinstance(task_id, str):
            raise EvaluationError("comparison task ID is invalid")
        task_class = next((name for name, value in TASK_IDS.items() if value == task_id), None)
        if (task_class is None or not isinstance(comparison["task_class"], str)
                or comparison["task_class"] != task_class or task_id in seen):
            raise EvaluationError("comparison has an unknown or duplicate stable task ID")
        seen.add(task_id)
        for variant in ("baseline", "treatment"):
            value = comparison[variant]
            if not isinstance(value, Mapping) or set(value) != VARIANT_FIELDS:
                raise EvaluationError("comparison variant fields are invalid")
            record = by_key[(task_id, variant)]
            if any(value[key] != record[key] for key in VARIANT_FIELDS):
                raise EvaluationError("comparison does not match its task record")
        baseline = by_key[(task_id, "baseline")]
        treatment = by_key[(task_id, "treatment")]
        if baseline["commit_sha"] == treatment["commit_sha"] or baseline["config_sha"] == treatment["config_sha"]:
            raise EvaluationError("comparison baseline and treatment SHAs must differ")
        _one_of(comparison["verdict"],
                OBSERVED_VERDICTS if status == "observed" else {"not_run"},
                "comparison verdict")
    if seen != set(TASK_IDS.values()):
        raise EvaluationError("comparisons must cover all five stable task IDs")


def _validate_run_identity(records: list[Mapping[str, Any]]) -> None:
    for variant in ("baseline", "treatment"):
        identities = {(record["commit_sha"], record["config_sha"])
                      for record in records if record["variant"] == variant}
        if len(identities) != 1:
            raise EvaluationError("all task records must share one run identity per variant")


def _validate_record(record: Mapping[str, Any], run_id: str, baseline_commit: str | None,
                     treatment_commit: str | None, baseline_config: str | None,
                     treatment_config: str | None) -> None:
    if set(record) != RECORD_FIELDS:
        raise EvaluationError("record fields do not match metadata-only contract")
    _reject_forbidden(record)
    _opaque(record["run_id"], "record.run_id")
    if (record["run_id"] != run_id or not isinstance(record["task_id"], str)
            or record["task_id"] not in TASK_IDS.values()):
        raise EvaluationError("record has an unknown run or stable task ID")
    task_class = next((name for name, task_id in TASK_IDS.items() if task_id == record["task_id"]), None)
    if not isinstance(record["task_class"], str) or task_class != record["task_class"]:
        raise EvaluationError("record task class or variant is invalid")
    _one_of(record["variant"], {"baseline", "treatment"}, "record variant")
    expected_commit = baseline_commit if record["variant"] == "baseline" else treatment_commit
    expected_config = baseline_config if record["variant"] == "baseline" else treatment_config
    if expected_commit is not None and record["commit_sha"] != expected_commit:
        raise EvaluationError("record commit SHA does not match run metadata")
    if expected_config is not None and record["config_sha"] != expected_config:
        raise EvaluationError("record config SHA does not match run metadata")
    _sha(record["commit_sha"], "record commit_sha")
    _sha(record["config_sha"], "record config_sha")
    status = _one_of(record["status"], {"observed", "not_run"}, "record status")
    verdict = _one_of(record["verdict"], VERDICTS, "record verdict")
    if not isinstance(record["dimensions"], Mapping) or set(record["dimensions"]) != set(DIMENSIONS):
        raise EvaluationError("record dimensions are incomplete")
    for dimension, value in record["dimensions"].items():
        _one_of(value, VERDICTS, f"record dimension {dimension}")
    refs = record["evidence_refs"]
    if not isinstance(refs, list) or not all(_evidence_ref(ref) for ref in refs):
        raise EvaluationError("evidence_refs must be bounded metadata references")
    _metric(record["latency_ms"], "latency_ms")
    _metric(record["cost_usd"], "cost_usd")
    if status == "not_run":
        if verdict != "not_run" or any(value != "not_run" for value in record["dimensions"].values()):
            raise EvaluationError("NOT RUN records cannot contain quality verdicts")
        if refs or record["latency_ms"] is not None or record["cost_usd"] is not None:
            raise EvaluationError("NOT RUN records cannot contain observed evidence or metrics")
        if record["not_run_reason"] != "live_consumer_unavailable":
            raise EvaluationError("NOT RUN reason must be explicit")
    else:
        if verdict not in OBSERVED_VERDICTS or not refs or record["not_run_reason"] is not None:
            raise EvaluationError("observed records need verdict, evidence, and no NOT RUN reason")
        if any(value not in OBSERVED_VERDICTS for value in record["dimensions"].values()):
            raise EvaluationError("observed records need complete dimension verdicts")
        for dimension in ("latency", "cost"):
            metric = record["latency_ms"] if dimension == "latency" else record["cost_usd"]
            if metric is None:
                raise EvaluationError(f"{dimension} verdict needs an observed metric")


def _metric(value: Any, name: str) -> None:
    if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool)
                              or not math.isfinite(value) or value < 0):
        raise EvaluationError(f"{name} must be a non-negative number or null")


def _sha(value: Any, name: str) -> str:
    if not isinstance(value, str) or not SHA.fullmatch(value):
        raise EvaluationError(f"{name} is invalid")
    return value


def _one_of(value: Any, allowed: frozenset[str] | set[str], name: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise EvaluationError(f"{name} is invalid")
    return value


def _opaque(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value or not OPAQUE.fullmatch(value):
        raise EvaluationError(f"{name} must be an opaque metadata ID")
    if any(part in value.lower() for part in FORBIDDEN_FIELD_PARTS):
        raise EvaluationError(f"{name} contains a forbidden data marker")
    return value


def _evidence_ref(value: Any) -> str:
    if (not isinstance(value, str) or len(value) > MAX_EVIDENCE_REF_LENGTH
            or not EVIDENCE_REF.fullmatch(value)):
        return ""
    if any(part in value.lower() for part in FORBIDDEN_FIELD_PARTS):
        return ""
    return value


def _reject_forbidden(value: Mapping[str, Any]) -> None:
    try:
        _reject_forbidden_fields(value)
    except ValueError as error:
        raise EvaluationError("forbidden metadata field") from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--hypothesis-id", required=True)
    parser.add_argument("--change-type", choices=("initial", "changed_hypothesis", "rollback"), default="initial")
    parser.add_argument("--supersedes-run-id")
    parser.add_argument("--baseline-commit", required=True)
    parser.add_argument("--treatment-commit", required=True)
    parser.add_argument("--baseline-config", required=True)
    parser.add_argument("--treatment-config", required=True)
    parser.add_argument("--consumer-available", action="store_true")
    parser.add_argument("--records", type=Path)
    parser.add_argument("--comparison-verdicts", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--receipt-journal", type=Path)
    parser.add_argument("--receipt-run-id")
    parser.add_argument("--receipt-task-id")
    parser.add_argument("--receipt-bead-id")
    args = parser.parse_args()
    try:
        common = vars(args).copy()
        common.pop("consumer_available")
        records_path = common.pop("records")
        comparisons_path = common.pop("comparison_verdicts")
        output = common.pop("output")
        common.pop("receipt_journal")
        common.pop("receipt_run_id")
        common.pop("receipt_task_id")
        common.pop("receipt_bead_id")
        if args.receipt_journal and (not args.receipt_run_id or not (args.receipt_task_id or args.receipt_bead_id)):
            raise EvaluationError(
                "--receipt-journal requires --receipt-run-id and --receipt-task-id or --receipt-bead-id")
        receipt_context = ReceiptContext(
            journal=args.receipt_journal, repo_root=Path(__file__).resolve().parents[1],
            run_id=args.receipt_run_id, actor="system", runtime="codex",
            task_id=args.receipt_task_id, bead_id=args.receipt_bead_id,
        ) if args.receipt_journal else None
        if records_path is None:
            if args.consumer_available or comparisons_path is not None:
                raise EvaluationError("consumer records are required when consumer is available")
            result = build_not_run(**common)
        else:
            if not args.consumer_available or comparisons_path is None:
                raise EvaluationError("observed mode requires --consumer-available and comparison verdicts")
            records = json.loads(records_path.read_text(encoding="utf-8"))
            comparisons = json.loads(comparisons_path.read_text(encoding="utf-8"))
            if not isinstance(records, list) or not isinstance(comparisons, Mapping):
                raise EvaluationError("input records and comparisons have invalid shapes")
            result = build_observed(**common, records=records, comparison_verdicts=comparisons)
        if output is None:
            print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        else:
            write_result(output, result, receipt_context=receipt_context)
    except (EvaluationError, OSError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
