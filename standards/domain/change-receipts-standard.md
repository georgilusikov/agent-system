# Change Receipts Standard

**Класс:** contract
**Дата создания:** 2026-08-22

## Фундаментальное правило

Every state, task, hook, deployment, or projection mutation emits one
metadata-only receipt. Receipts join runtime evidence to stable backlog and
source identities; they never store conversation or execution content.

## Envelope

Each receipt is one JSON object in an append-only JSONL journal. Required
fields are:

| Field | Type / allowed value |
|---|---|
| `event_id` | unique opaque UUID or equivalent stable event identifier |
| `parent_event_id` | prior related `event_id`, or `null` for a root event |
| `run_id` | non-empty opaque correlation identifier |
| `task_id` / `bead_id` | non-empty opaque task identifier; use the system-native key and omit the other when unavailable |
| `actor` | `human`, `agent`, `hook`, or `system` |
| `runtime` | bounded runtime identifier, such as `codex`, `claude`, `gemini`, `git`, or `system` |
| `operation` | bounded dotted operation name, for example `state.saved` or `projection.deployed` |
| `target` | repository-relative path, opaque resource ID, or target class; never content |
| `source_commit` | full Git commit SHA, or `null` when no Git source exists |
| `before_hash` / `after_hash` | lowercase SHA-256 digest or `null` when no prior/resulting artifact exists |
| `outcome` | `attempted`, `applied`, `verified`, `failed`, `partial`, or `blocked` |
| `evidence_refs` | array of non-empty, content-free artifact IDs, paths, or digest references |
| `occurred_at` | UTC RFC 3339 timestamp ending in `Z` |
| `redaction_status` | exactly `metadata-only` |

Optional fields are `operation_key_fingerprint`, `operation_fingerprint`,
`receipt_hash`, `previous_receipt_hash`, and bounded error class. Hash fields
are lowercase 64-character SHA-256 hex. Operation keys are opaque inputs:
fingerprint them before storage and never store the raw key. This matches
`scripts/agent_run_state.py`'s accepted `operation_receipts` behavior:
`key_fingerprint` deduplicates an operation and `operation_fingerprint`
detects reuse with different details.

## Storage, access, and integrity

- Store journals outside Git, per runtime/project, with restrictive local
  access; Git must not track, render, or deploy the journal as source.
- Append synchronously after an attempted mutation; do not rewrite or delete
  records. Corrections, retention expiry, and redactions are new receipts.
- Retain only for the approved operational/audit period; access is limited to
  the owner and operators who need replay or incident review.
- If chaining, each receipt hashes its canonical metadata plus the previous
  receipt hash. A gap, mismatch, duplicate `event_id`, or invalid digest makes
  the affected segment untrusted and requires an incident receipt; preserve it
  for investigation rather than silently repairing it.

A receipt proves that its producer recorded the stated metadata and that a
verified hash chain was intact at inspection. It does not prove a provider
ran a hook, a remote effect occurred, ownership accepted a result, or that
metadata is truthful without the referenced consumer evidence.

## Privacy boundary

Never record prompts, responses, transcripts, tool payloads, credentials,
secrets, tokens, or environment values. Do not add free-text content fields;
use bounded identifiers, target classes, hashes, and `evidence_refs`. Reject
the event before persistence when a field name or value would cross this
boundary; hashing prohibited content is not permission to record it.

## Producers, consumers, and replay

Producers are state/task writers, lifecycle hooks, deployment/projection
writers, and runtime adapters. Consumers are checkers, replay canaries,
incident review, and derived read-only projections. A consumer must resolve
each configured hook or projection target to its canonical source and require
one production-shaped receipt showing it ran; file presence alone is not
proof.

The replay canary must use a synthetic bounded run, join records by `run_id`,
require unique `event_id`s and valid parent/hash links, verify matching source
and before/after hashes, and resume without repeating already verified work or
external effects. It must also prove the denylist is absent. Do not claim
runtime wiring or replay safety until that canary passes.

## System boundaries

- **Beads** is the backlog and work identity; it does not prove execution.
- **Git** is the versioned changelog; it does not prove a runtime consumed a
  revision.
- **Receipts** are runtime evidence linked to both; they do not replace either.
- **Owner acceptance** is a separate explicit decision linked by receipt or
  evidence reference; `outcome: verified` is not acceptance.

Borrow only small patterns: run/parent correlation from OpenTelemetry,
append-only hash-chained JSONL and redaction-before-disk from Soma, provenance
observations from Neotoma, and checkpoint/replay identity from LangGraph. Do
not import their runtimes or add an observability stack until a measured canary
shows this flat local contract is insufficient.

## Cross-references

- `agent-state-contract-standard.md` — task and result state boundaries.
- `../operational/incident-logging.md` — incident journal conventions.
- `../../scripts/agent_run_state.py` — accepted metadata-only operation receipt implementation.

## История изменений

| Дата | Изменение | Причина |
|---|---|---|
| 2026-08-22 | Создан контракт metadata-only receipts. | Связать runtime evidence со state, tasks, hooks, deployments и projections без хранения содержимого. |
