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
| `event_id` | unique UUID or opaque ID matching `[A-Za-z0-9][A-Za-z0-9._:-]{0,127}` |
| `parent_event_id` | prior `event_id`, or `null` only for a root event |
| `run_id` | non-empty opaque ID matching the `event_id` grammar |
| `task_id` / `bead_id` | at least one required, each matching the `event_id` grammar; omit the unavailable native key, never use `null` |
| `actor` | `human`, `agent`, `hook`, or `system` |
| `runtime` | required, non-null `[a-z][a-z0-9_-]{0,31}`; use a registered runtime such as `codex`, `claude`, `gemini`, `git`, or `system` |
| `operation` | required, non-null, ≤64 chars: `[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*){1,3}` |
| `target` | required, non-null, ≤256 chars, and exactly one of the enforceable alternatives below; never content |
| `source_commit` | full Git commit SHA, or `null` when no Git source exists |
| `before_hash` / `after_hash` | lowercase SHA-256 digest or `null` when no prior/resulting artifact exists |
| `outcome` | `attempted`, `applied`, `verified`, `failed`, `partial`, or `blocked` |
| `evidence_refs` | required array of 0–32 content-free refs, each ≤256 chars and matching the `target` grammar; empty only when no evidence artifact exists |
| `occurred_at` | UTC RFC 3339 timestamp ending in `Z` |
| `redaction_status` | exactly `metadata-only` |

`target` is one of:

- `path:<path>` — `<path>` is ≤251 chars, repository-relative, and contains
  only non-empty segments separated by single `/`; reject absolute paths,
  backslashes, duplicate separators, and `.` or `..` segments. Validate by
  resolving it under the repository root and reject it unless the resolved
  location remains under that root; resolution must not follow a symlink
  escape.
- `id:<id>` — `<id>` is a ≤253-char opaque ID matching
  `[A-Za-z0-9][A-Za-z0-9._:@-]{0,252}`.
- `class:<class>` — `<class>` is a ≤250-char target class matching
  `[a-z][a-z0-9_-]{0,249}`.

Optional envelope fields are `receipt_hash`, `previous_receipt_hash`, and
`error_class`. `error_class` is omitted unless the outcome is `failed`,
`partial`, or `blocked`; when present it matches `[a-z][a-z0-9_-]{0,31}`.
Hash fields are lowercase 64-character SHA-256 hex.

## Run-state operation receipt embedding

The outer JSONL receipt envelope has no generic `operation_receipts` shape.
When embedding receipts in the accepted run state from
`scripts/agent_run_state.py`, `operation_receipts` is required and always a
list: `[]` when there is no operation key. Each item has exactly
`key_fingerprint` and `operation_fingerprint`, both lowercase SHA-256 hex,
and all `key_fingerprint` values are unique. Raw operation keys or content
never persist.

For that embedding, fingerprint the exact compact sorted-key JSON preimages
used by the implementation: SHA-256 over
`json.dumps({"operation_key": key}, sort_keys=True, separators=(",", ":")).encode()`
for `key_fingerprint`, and SHA-256 over
`json.dumps({"kind": kind, "details": details}, sort_keys=True, separators=(",", ":")).encode()`
for `operation_fingerprint`. The first deduplicates retries; reuse with a
different second fingerprint is a conflict. Do not call this run-state shape
the outer-envelope shape unless an adapter maps it explicitly.

## Storage, access, and integrity

- Store journals outside Git, per runtime/project, with restrictive local
  access; Git must not track, render, or deploy the journal as source.
- Append synchronously after an attempted mutation; do not rewrite or delete
  records. Corrections and redactions are new receipts.
- Retain each active journal for 90 days, then rotate it unchanged to an
  owner-controlled archive for 365 days. Access is limited to the owner and
  operators assigned replay or incident review. The owner may adopt a stricter
  written policy before production where the system requires it.
- At archive expiry, the owner-controlled final disposition is deletion of
  ordinary journal segments. Incident and tamper evidence are exceptions:
  preserve them in the case archive until explicit owner disposition. If
  archival or final disposition cannot occur, block deletion and append an
  incident receipt.
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
external effects. It must prove the denylist is absent only from its generated
journal/artifacts and explicitly inspected consumer path; it does not prove
all runtime history is clean. Do not claim runtime wiring or replay safety
until that canary passes.

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
| 2026-08-22 | Создан контракт metadata-only receipts; уточнены schema, run-state embedding, target и retention. | Связать runtime evidence со state, tasks, hooks, deployments и projections без хранения содержимого. |
