# Memory candidate flow

**Статус:** executable local flow; global canon promotion is never automatic.

## Поток

```text
verified metadata receipt → candidate inbox → reviewer → owner approval
                                           ↘ reject
approved + matching scope → retrieval
approved → superseded / rollback overlay → excluded from retrieval
```

- Ledger lives outside the canonical repository and is append-only JSONL with a
  hash chain.
- A candidate stores only bounded redacted metadata, a short learning
  statement, scope, limits, and receipt/evidence references. Raw prompts,
  responses, transcripts, tool payloads, credentials, environment values and
  copied chat never enter the ledger.
- `reviewed` is not current guidance. Only `approved`, non-superseded and
  non-rolled-back notes are returned for the exact requested scope/project.
- Duplicate or contradictory active notes fail closed. A replacement must name
  the approved note it supersedes; old guidance then becomes unavailable.
- Rollback appends an audit event and disables retrieval without rewriting the
  history. It does not edit `rules/`, `standards/`, `skills/` or other canon.
- One writer holds a local OS lock. Parallel ledgers are not merged
  automatically; the owner decides how to reconcile them.

## Owner gate

Automation may create candidates and request review, but only the named owner
can approve. Canon promotion remains a separate owner-approved change with its
own receipt; this flow is memory retrieval, not silent rule compilation.
