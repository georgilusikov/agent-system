# Shared task protocol

Load for modifications, delegated execution, acceptance/revision of accepted work,
canon updates or corrections/false completion/recurrence, read-only investigation,
batch/long work, or external/financial/irreversible actions.
Select the matching sections below. Resolve paths from the real source
directory of `AGENTS.md`, not cwd or an installed alias.

## Modify: lock, execute, stop

Before modifying any file, inspect current instructions, sources, runtime, and
consumers. For an important edit, inspect `git log -5 --oneline -- <file>`.
Declare all three fields before editing:

- TARGET: exact file/function and observable symptom or ticket.
- NON-GOALS: adjacent temptations found during inspection; no adjacent refactoring.
- STOP RECEIPT: exact command and expected output proving completion.

Touch only TARGET files; never expand scope silently. If an adjacent module
blocks execution, use a local shim of at most five lines rather than refactoring
that module. If completion requires forbidden paths, stop and ask the owner.
Report unrelated findings as follow-ups; fix one only when it blocks the target.
Before changing a shared resource (config, schema, base rules, common library,
pipeline contract), map all dependent consumers and verify their contracts.
Apply `CODING_STANDARDS.md` for construction and consumer verification.
Retry only with a changed root-cause hypothesis; escalate after three different
failures.

## Inspect and scale

Batch independent read-only probes and filter verbose output at the source.
Search with scoped `rg` / `rg --files`; never scan the whole home for common words.
Before a batch or long loop, measure time, tokens, and failures on one or two
items; extrapolate cost and feasibility from those measurements.
For external, financial, or irreversible impact: prove logic offline/dry-run,
execute one bounded live sample, and scale only after a verified receipt.
Use the current harness's inspection, editing, and waiting capabilities;
tool-specific recipes belong in harness adapters and apply only when available.

## Delegate: isolate and audit

The manager holds contracts and verifies; it never writes feature code.
Run each executor in an isolated `.worktrees/<task>` with an exclusive path
allowlist. Parallel workers never edit the same file simultaneously.
Briefs name goal, paths, prohibitions, output, checks, and evidence.
The orchestrator owns architecture, final acceptance, live actions, and owner
decisions. Before merging, it personally audits the diff against scope, runs the
acceptance command, and verifies consumer wiring; a worker's report is not proof.

## Accept: record and lock

When the owner accepts an artifact, record:

```text
ACCEPTED: <artifact|hash> · <date> · <by>
REOPEN ONLY IF: new owner complaint | changed source | failed regression
```

Before modifying completed work, check its acceptance record. Improve or
re-architect accepted work only when one of those reopen conditions fires.

## Learn: approve before canon

Use the canonical checkout identified in `AGENTS.md`.
Globally discoverable skills live only in `skills/`; domain libraries live in
`library/` and load through routers.
After a correction, false completion, or recurrence, propose a deduplicated,
evidence-backed canon update; persist it only with owner approval.
Durable shared learning must be reviewed, redacted, and evidence-backed before
entering `memory/`, `rules/`, `standards/`, or a skill.
Raw chats, rollout summaries, traces, caches, and project-specific memories stay
outside this repository. Give a learning ledger only one writer at a time.
Commit every approved canon change with what and why; Git history is the
changelog, without a second manual change ledger.
