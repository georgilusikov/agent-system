---
name: before-after-evaluation-standard
description: Metadata-only before/after evaluation contract for five task classes.
version: 0.0.1
created: 2026-08-22
updated: 2026-08-22
scope: shared
status: active
owner: georgy
---

# Before/After Evaluation Standard

## Purpose

Compare a baseline and treatment without storing model content or inventing
quality scores. The canonical offline entrypoint is:

```text
python3 scripts/evaluate_before_after.py --run-id ... --hypothesis-id ... \
  --baseline-commit <sha> --treatment-commit <sha> \
  --baseline-config <sha> --treatment-config <sha>
```

Without `--consumer-available` and externally supplied metadata records, this
command emits an honest `status: not_run` result for both variants. It never
invokes a model or treats missing evidence as a score.

## Stable task set

The evaluator always covers exactly these IDs:

| Class | Stable task ID |
|---|---|
| Simple explanation | `gl-ejw.12.simple-explanation` |
| Architecture choice | `gl-ejw.12.architecture-choice` |
| Diagnosis | `gl-ejw.12.diagnosis` |
| Research | `gl-ejw.12.research` |
| Code change | `gl-ejw.12.code-change` |

Each run has one baseline and one treatment record per task. A record carries
`run_id`, `task_id`, `task_class`, `variant`, `commit_sha`, `config_sha`,
`status`, `verdict`, `dimensions`, `evidence_refs`, `latency_ms`, `cost_usd`,
and `not_run_reason`. The result envelope is `redaction_status:
metadata-only`.

## Verdicts and dimensions

`verdict` is exactly one of `confirmed`, `partially`, `falsified`, or
`not_run`. The required dimensions are:

```text
correctness, safety, clarity, context, terminology, evidence,
decision_quality, owner_effort, latency, cost
```

Observed records require an explicit non-`not_run` verdict for every dimension,
at least one evidence reference matching the bounded
`kind:run:variant:item` metadata grammar, and observed numeric measurements for
`latency` and `cost`. No numeric quality score, prose rationale, prompt,
response, transcript, tool payload, credential, or environment value is allowed.

When a consumer is unavailable, every dimension and comparison verdict is
`not_run`, metrics are `null`, and `not_run_reason` is
`live_consumer_unavailable`. This is a valid result, not a failure disguised
as zero quality.

## Comparison and change handling

Comparison verdicts are supplied separately as metadata and must cover all
five stable task IDs. The evaluator does not infer that treatment is better
from dimension labels. Both variants must retain distinct commit and config
SHAs; identical baseline and treatment identities are rejected even for a
`not_run` result.

Results are append-only. A rollback or changed hypothesis creates a new
`run_id`, sets `change_type` to `rollback` or `changed_hypothesis`, and names
the prior run in `supersedes_run_id`. Existing result files are never replaced;
the script rejects a different result at an existing path. To revert, choose
the prior known-good SHA/config in the new run; to retry a hypothesis, change
the hypothesis/run identity and record the new evidence.

Persisted results require one uniform commit/config identity for all five
baseline records and one uniform commit/config identity for all five treatment
records.

## Verification

```text
python3 scripts/test_evaluate_before_after.py
python3 scripts/check.py --repo
```

The self-check covers all five IDs, both variants, metadata-only rejection,
observed metrics, NOT RUN, and changed-hypothesis/rollback handling.
