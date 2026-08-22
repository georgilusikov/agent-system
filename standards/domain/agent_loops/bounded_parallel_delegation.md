# Bounded Parallel Delegation Standard

**Класс:** contract
**Дата:** 2026-08-22

## Outcome

Use bounded fan-out only when each lane is independently useful and its
capability has passed a live, metadata-only probe. A missing runtime is
`NOT RUN`, never a synthetic success.

## Contract

The dispatcher accepts one JSON document with these fields:

```json
{
  "bead_id": "gl-ejw.15",
  "run_id": "opaque-run-id",
  "capabilities": [{
    "id": "luna",
    "runtime": "codex",
    "channel": "codex",
    "model": "gpt-5.6-luna",
    "status": "available",
    "probe": {"status": "available", "exit_code": 0, "elapsed_seconds": 1,
              "canary": "PASS", "capability_id": "luna", "run_id": "opaque-run-id"}
  }],
  "policy": {
    "max_lanes": 3,
    "timeout_seconds": 60,
    "quota_units": 3,
    "cost_cap_usd": 0,
    "fallback": null
  },
  "lanes": [{
    "id": "audit-a",
    "capability_id": "luna",
    "mode": "read",
    "scope": ["standards/domain/agent_loops"] ,
    "dedupe_key": "audit-a-v1",
    "required": true
  }],
  "outcomes": [{"lane_id": "audit-a", "status": "not_run"}],
  "aggregate": {"status": "NOT RUN", "completed": 0, "not_run": 1,
                 "elapsed_seconds": 0, "quota_used": 0, "cost_usd": 0}
}
```

Required invariants:

- `1..max_lanes`, with `max_lanes <= 3`; every lane has a unique `id` and
  `dedupe_key`.
- `mode=read` is read-only. `mode=write` requires an exclusive `scope`.
  All lane scopes are disjoint, so a read lane cannot silently overlap a
  writer or another lane.
- A lane may dispatch only to a capability whose bounded probe has
  `status=available`, `exit_code=0`, `canary=PASS`, matching `capability_id`,
  and matching current `run_id`. Capability ids, runtime, channel, model, and
  probe result are metadata; prompts, outputs, payloads, credentials, tokens,
  unknown fields, and free-text values are forbidden.
- `timeout_seconds`, `quota_units`, and `cost_cap_usd` are hard upper bounds.
  `cost_cap_usd=0` is the safe offline default. No retry is implicit.
- The aggregate must report `elapsed_seconds`, `quota_used`, and `cost_usd`;
  each value must be non-negative and no greater than its policy cap.
- `fallback` is either `null` or one alternate capability with
  `max_attempts=1`; it must be different from every primary lane capability
  and pass the same current-run probe before use. There is no fallback chain.
- Each lane has exactly one outcome. The parent aggregates only statuses and
  bounded counters. An absent or unprobed capability yields `NOT RUN`; it
  cannot produce `verified`. Required lanes with missing or `not_run`
  capabilities aggregate to `NOT RUN`; required blocked lanes aggregate to
  `BLOCKED`; optional `not_run` lanes do not prevent `PASS`. A timeout, quota
  exhaustion, or failed lane aggregates to `FAIL`, never to `PASS`.

## Capability matrix

Populate this matrix from the current runtime, not from the cached registry:

| capability | runtime/channel | model | probe | status | canary |
|---|---|---|---|---|---|
| opaque id | command/channel | live model name | bounded status, exit code, elapsed time, current-run identity | `available`, `unavailable`, `quota_exhausted`, or `not_run` | `PASS` or `NOT RUN` |

The probe may check command presence and a bounded `--version`, `--help`, or
model-list operation. It must not send a task prompt. Record only the status,
exit code, elapsed time, and a content-free reason code.

## Dispatch and receipts

1. Validate the document and deduplication/scope invariants.
2. Probe each selected capability once and cache the result for this run.
3. Dispatch only eligible independent lanes in parallel.
4. On timeout, quota, or capability failure, use the single predeclared
   fallback once; otherwise mark the lane `not_run` or `blocked`.
5. Aggregate lane statuses and write metadata-only receipts using
   [change-receipts-standard.md](../change-receipts-standard.md). A receipt
   proves recording, not provider execution or owner acceptance.

The offline checker is
`scripts/check_bounded_parallel_delegation.py`; it validates the contract and
returns `PASS`, `NOT RUN`, `BLOCKED`, or `FAIL`. It does not invoke a provider
or act as an adapter, and it does not claim live Luna, AGY, or Gemini
execution. Probe evidence must come from a separate bounded runtime channel;
when no such channel exists, record `unavailable` or `not_run` with
`canary=NOT RUN`.

## Verification

```bash
python3 scripts/test_bounded_parallel_delegation.py
printf '%s' '<metadata-only JSON>' | python3 scripts/check_bounded_parallel_delegation.py
```

The test must cover a valid `NOT RUN`, duplicate work, overlapping scopes,
missing capability, fallback cardinality, and forbidden metadata fields.
