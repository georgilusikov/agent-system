# Cursor Composer / Agent Standard

Load this reference only when launching or writing instructions for Cursor
Composer/Agent implementation lanes.

## When To Use

Use Cursor for narrow implementation when file scope is clear, local validation
commands exist, and the expected diff is concrete. Avoid Cursor for broad
triage, final verification, or ambiguous product judgment.

Good lanes:

- one ticket or failure cluster;
- one small set of files/modules;
- production wiring where the target consumer is known;
- tests already exist or can be added in the same lane.

## Launch

Prefer Herdr so the orchestrator can inspect status/output and close the pane
when the task is accepted or no report is needed:

```bash
herdr agent start <agent-name> --cwd <worktree> -- cursor agent '<prompt>'
```

If Cursor is started manually in an IDE, paste the same bounded prompt and ask
for a short final report plus changed file paths.

## Prompt Contract

```text
You are Cursor Composer/Agent 2.5 implementer.
Work only in this isolated worktree: <path>.
Goal: <ticket/wave>.

Read the task contract, current code, and targeted tests before editing.
Implement the minimal production path. No unrelated refactor. No destructive git.
Do not commit unless explicitly asked. Do not touch unrelated files.
Do not print long reasoning, full diffs, full logs, or repeated progress notes.

If the ticket is already implemented, prove it with focused tests and status sync.
If implementation is missing, wire the smallest production path that makes it non-inert.

Before final:
- git diff --check
- targeted tests for touched behavior
- lint/format changed files when the project has such a command
- validate changed JSON/YAML/structured files

Final short report, max 8 lines:
- status: done|partial|blocked
- changed files
- tests/commands
- evidence that production path is wired
- residual risks
```

## Acceptance

Cursor output is not evidence by itself. Accept only after inspecting:

- `git status --short --branch`;
- `git diff --stat` and key hunks for the touched files;
- targeted tests or a production-shaped proof;
- final report claims against actual files.

Escalate to a verifier when the change affects user-visible behavior, shared
contracts, release gates, security, billing, provider calls, or backlog closure.

## Common Mistakes

- Launching plain `cursor` instead of `cursor agent` in a headless CLI context.
- Giving Cursor broad backlog cleanup with no exact path scope.
- Letting Cursor edit backlog status before code evidence exists.
- Accepting "already works" without a consumer-path proof.
- Running full suites inside Cursor for every small edit.
- Reusing a dirty shared worktree for overlapping implementation lanes.
- Leaving completed Cursor panes open after the final output was inspected and
  no durable report is needed.
