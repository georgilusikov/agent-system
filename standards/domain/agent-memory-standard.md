# Agent Memory Standard

**Класс:** contract
**Дата создания:** 2026-08-22
**Статус:** declarative governance; native-runtime wiring is not implemented

## 1. Назначение и storage boundary

Память агента — проверяемые заметки, а не второй источник процедурного
канона. Candidate/reviewed note не меняет молча `rules/`, `standards/`,
`skills/` или другой canon. Изменение canon — отдельный проверенный change с
owner approval.

В global canon допустимы только reviewed, redacted, evidence-backed global
approaches и существующие `memory/incidents/`/`memory/learnings/`:

```text
memory/
  candidate/inbox/       # новые global candidates; visibly untrusted
  reviewed/approaches/   # reviewed global approaches; ещё не canon
  incidents/             # existing operational RCA/history
  learnings/             # existing reusable learnings/feedback
```

Project/session memory, raw notes и their content живут вне
`/Users/georgijlusikov/code/agent-system`. Canon может хранить только
content-free pointer/receipt: opaque external reference, scope/project id,
allowed metadata hashes и evidence refs; он не копирует note text, summary,
prompt, transcript или payload. `memory/projects/<project>/` не является
допустимым storage location в этом repository.

## 2. Versioned schema

Новая note имеет front matter или эквивалентную machine-readable запись:

```yaml
schema_version: 1
id: mem-<stable-id>
kind: incident|learning|approach|fact|procedure|external_pointer
scope: global|project|session
project: <project-id-or-null>
owner: <owner-id>                 # acceptance authority, not reviewer
status: draft|reviewed|approved|superseded|rejected|expired
created_at: <UTC-RFC3339>
updated_at: <UTC-RFC3339>
source_evidence: [<receipt-ref-or-repository-relative-path>]
source_hash: <sha256-or-commit>
result_metric: <bounded-result-or-null>
applicability: <where-and-when>
limits: <known-ceiling-and-non-cases>
supersedes: <note-id-or-null>
contradicts: [<note-id>]
retention_review_at: <UTC-RFC3339-or-null>
redaction_status: pending|redacted
reviewed_by: <reviewer-id-or-null>
reviewed_at: <UTC-RFC3339-or-null>
review_evidence: [<evidence-ref>]
approved_by: <owner-id-or-null>
approved_at: <UTC-RFC3339-or-null>
approval_evidence: [<owner-decision-or-receipt-ref>]
rejected_by: <reviewer-or-owner-id-or-null>
rejected_at: <UTC-RFC3339-or-null>
rejection_reason: <bounded-reason-or-null>
rejection_evidence: [<evidence-ref>]
transitions: [{from: <status>, to: <status>, at: <UTC-RFC3339>, by: <id>, evidence: <ref>}]
external_note_ref: <opaque-ref-or-null>
```

`id` is stable. `applicability`, `limits`, `supersedes` and `contradicts` use
explicit `null`/`[]` where applicable. A reviewer validates evidence, scope,
contradictions and redaction; only `owner` may approve, so `approved_by` must
equal `owner`. Every status change appends one complete `transitions` record.
An `external_pointer` has no copied external content; `external_note_ref` is
an opaque locator, never a body or summary.

## 3. Lifecycle and gates

`redaction_status: pending` is quarantined: it is neither retrievable nor
reviewable/approvable. `redacted` is required for `reviewed` and `approved`.

| From | To | Required condition |
| --- | --- | --- |
| `draft` | `reviewed` | redacted; source/scope/limits/contradictions checked; `reviewed_*` fields and transition evidence present |
| `reviewed` | `approved` | redacted; measurable result or explicit non-applicability; owner approval (`approved_by == owner`) and evidence present |
| `approved` | `superseded` | new note names this id in `supersedes`; transition evidence present |
| `draft` or `reviewed` | `rejected` | rejection actor, reason and evidence present |
| `reviewed` or `approved` | `expired` | retention review is due; transition evidence present |
| `expired` | `reviewed` | a new complete review, redaction and review evidence |

The table is exhaustive: only the listed source/status pairs are valid; every
other pair is invalid, including `approved → reviewed`, `draft → superseded`,
`rejected → draft`, and every self-transition unless a new record explicitly
states why it is permitted. `transitions[-1].to` must equal the current
`status`. `draft → approved` is therefore impossible. `rejected` and
`superseded` are audit-only terminal states. Promotion also requires
repeatability, or an explicit reason why it does not apply, and a contradiction
check against approved/reviewed notes. A note never authorizes a canon change
by itself.

## 4. Retrieval, legacy, and evidence

- `draft`, `pending`, `rejected`, `superseded` and `expired` are excluded from
  default retrieval; audit/contradiction review may find them.
- `reviewed` is visibly untrusted (status, scope, source, limits shown).
  `approved` remains scoped; project/session pointers cannot enter global
  retrieval as content.
- Existing `memory/incidents/` and `memory/learnings/` are preserved without
  backfill. Their own existing standards govern legacy records. Legacy notes
  lacking `schema_version` are not silently approved memory and are excluded
  from this standard's promotion/retrieval gates until newly reviewed as a new
  versioned note.
- Evidence uses metadata-only run/change receipt terminology from
  `change-receipts-standard.md`: receipt ref, commit/path/hash and test or
  consumer/replay evidence. A receipt proves recorded metadata, not owner
  acceptance or consumer execution. File presence, intent/config, agent claim,
  LLM summary or similarity hit are insufficient.

## 5. Privacy and document canary

Never store raw prompts, responses, transcripts, tool payloads, credentials,
secrets, tokens, environment values or sensitive copied data. Hashing them is
not permission to retain them. Redact before persistence; `pending` remains
quarantined.

Before promotion, run a synthetic document canary that asserts: schema version
and audit fields; the exhaustive matrix (including rejection of an unlisted
transition and no `draft → approved`); scope boundary and opaque-pointer-only
project/session references; legacy exclusion; denylist; README/rule
registration; and this no-runtime claim. It checks the declarative
standard/manual workflow only, not an executable schema or consumer.

## Cross-references

- `change-receipts-standard.md` — metadata-only evidence and owner acceptance.
- `../operational/incident-logging.md` — existing incident-record conventions.
- `../../rules/operational/incident-parking.md` — candidate capture entrypoint.

## История изменений

| Дата | Изменение | Причина |
| --- | --- | --- |
| 2026-08-22 | Defined versioned, auditable memory governance. | Keep shared learning reviewable without storing project/session content in canon. |
