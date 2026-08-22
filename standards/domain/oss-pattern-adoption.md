# OSS Pattern Adoption Decision

**Класс:** method
**Дата:** 2026-08-22
**Статус:** adopted protocol only; no runtime dependency

## Decision

**Уверенность: 90%.** [I] The existing metadata-only receipt contract and
run-state implementation cover the demonstrated local need; importing a memory,
graph, checkpoint, or telemetry runtime has no current consumer proof.

Adopt the **minimum set** as protocol ideas only: metadata-only correlation;
append-only redacted/hash-linked evidence; immutable observations/provenance;
checkpoint/replay identity; and `candidate -> reviewed -> approved` memory
promotion. Reuse [Change Receipts Standard](change-receipts-standard.md); this
record does not redefine its envelope, storage, retention, or denylist.

No prompts, responses, transcripts, tool payloads, credentials, or environment
values may enter receipts, telemetry, or memory. Hashing prohibited content does
not make it recordable.

## Candidate decision

| pattern/project | primary source | local problem addressed | adopt now | reject/watch | integration cost | canary/evidence |
|---|---|---|---|---|---|---|
| EverOS | [memory design](https://github.com/EverMind-AI/EverOS/blob/main/docs/how-memory-works.md) | local Markdown episodes/index | no | watch: duplicate current evidence path; extraction is unproven | medium | future read-only projection must preserve source hash and project isolation |
| Ouroboros | [architecture](https://github.com/razzant/ouroboros/blob/main/docs/ARCHITECTURE.md) | durable agent history | no | reject: autonomous runtime/security burden | high | none until a bounded recovery gap is measured |
| G-Brain | [memory verbs](https://github.com/garrytan/gbrain/blob/master/docs/protocol/MEMORY_VERBS_v1.md) | provenance-aware notes | no | watch: database/cron cost and generated-memory review risk | high | future candidate-only import retains citation and approval status |
| OpenTelemetry | [context propagation](https://opentelemetry.io/docs/concepts/context-propagation/) | cross-runtime correlation | pattern only | reject exporter/collector: receipt contract is authoritative | low | synthetic child receipt shares `run_id`; denylist sentinel is absent |
| Soma | [journal and hash-chain design](https://github.com/radotsvetkov/soma/blob/622e4b7dca6c18b2ef9e99fe0ec4dc3286ee3012/README.md) | append-only hash links | pattern already adopted | watch project: local receipt contract already owns this seam; no runtime import | low | receipt checker validates parent/hash links; no runtime import |
| Neotoma | [observation architecture](https://github.com/markmhendrickson/neotoma/blob/5a50ea96503711f69c162298cd6b866d8d0a4eac/docs/subsystems/observation_architecture.md) | immutable provenance observations | pattern already adopted | watch project: local receipt contract already owns this seam; no runtime import | low | observation keeps source ID/hash and is never silently rewritten |
| LangGraph | [persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | resume/replay identity | pattern only | reject runtime: no measured checkpoint consumer | medium | kill a synthetic three-step run; resume once without repeating effects |
| LangMem | [concepts](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/) | memory lifecycle | pattern only | reject runtime: promotion governance remains local | medium | false candidate remains quarantined and unretrieved by default |
| Graphiti | [repository](https://github.com/getzep/graphiti) | temporal fact provenance | no | watch: graph/database cost without temporal-query evidence | high | require flat-receipt query failure before graph evaluation |
| Letta | [attaching and detaching memory blocks](https://docs.letta.com/tutorials/attaching-detaching-blocks/) | scoped persistent memory | no | watch: stateful platform exceeds current consumer need | medium | synthetic scope grant/revoke before reconsideration |

[O] `scripts/agent_run_state.py` already validates metadata-only operation
receipt fingerprints. [I] Its use and the receipt contract are the only present
integration seams; no table entry proves a deployed runtime consumer.

## Adopted seams and bounded proof

| adopted idea | seam now | bounded canary/evidence |
|---|---|---|
| metadata-only correlation and semantic fields | `change-receipts-standard.md` envelope (`run_id`, parent/event IDs, runtime, outcome) | synthetic parent/child JSONL records join by `run_id`; reject denylist sentinel |
| append-only redacted/hash-linked evidence | receipt hash chain | mutate a copied record and require hash-link failure; corrections append a new record |
| immutable observations/provenance | receipt `source_commit`, hashes, `evidence_refs` | verify one observation resolves only to content-free IDs/hashes and is not overwritten |
| checkpoint/replay identity | future work; no centralized checkpoint consumer | kill/resume synthetic three-step run; completed steps and external effects occur once |
| candidate -> reviewed -> approved memory promotion | future work; current `memory/` plus owner acceptance boundary | false candidate with source ID cannot alter canon or default retrieval before explicit approval |

Canaries remain offline and synthetic. A dependency, exporter, database,
collector, vector store, graph, or runtime needs **owner approval plus
executable proof** that the existing seams cannot meet the canary.

## Decision rules

1. [O] Receipts are append-only metadata outside Git; their privacy and replay
   rules are defined by the linked receipt standard.
2. [I] Treat derived memory as a candidate until review; only an explicit owner
   approval may promote it into canon. Supersede corrections; do not rewrite
   observations.
3. [I] A framework claim is not adoption evidence. Reconsider a watched project
   only after the named canary exposes a concrete gap and an executable,
   dependency-free baseline is retained for comparison.

## Source boundary

[O] Project claims above are limited to the linked primary documentation. [I]
The decisions are local recommendations, not benchmark results. [O] This
commit changes only this decision record; it introduces no candidate runtime,
dependency, adapter, or deployed setting.

## History

| Date | Change | Reason |
|---|---|---|
| 2026-08-22 | Record minimum OSS protocol adoption. | Preserve provenance and recovery options without importing a runtime. |
