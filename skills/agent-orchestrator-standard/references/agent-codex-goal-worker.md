# Codex Goal Worker Standard

Load this reference only when writing prompts for a Codex worker that will run
in Goal Mode or own a long unattended phase.

## When To Use

Use a Codex Goal worker for coherent phases that require restore, bounded
execution, verification, and durable reporting. Do not use Goal Mode for tiny
reads, one-file edits, or obvious checks where prompt/review overhead costs more
than direct execution.

## Prompt Header

```text
Goal Mode required.
Silent Orchestrator Mode is required.

You are the worker for <lane/wave>.
Work only in <repo/worktree>.
Do not commit, push, run destructive commands, or use live/paid providers unless explicitly authorized.
Do not paste worker prompts, transcripts, full logs, or full diffs into chat.
```

## Required Prompt Shape

Include:

- goal and exact scope;
- source-of-truth files to read first;
- worktree/repo path;
- forbidden actions;
- delegation policy and max worker count;
- efficiency budget;
- acceptance commands;
- required result files;
- stop conditions;
- final answer format.

## Delegation Policy

Tell the worker to delegate only when delegation is cheaper in main-agent tokens,
wall-clock time, context load, or risk. Prefer one coherent batched worker over
many tiny workers. If assigning and accepting a subtask costs about as much as
doing it directly, the worker should do it directly.

## Result Contract

Long Goal runs should write durable files, for example:

```text
tasks/<date>-<goal>/RUN_LOG.md
tasks/<date>-<goal>/GOAL_STATUS.yaml
tasks/<date>-<goal>/FINAL_SUMMARY.md
tasks/<date>-<goal>/final-summary.yaml
```

Final answer should be short, normally <=12 lines:

```text
Status: done|partial|blocked
Scoped outcome:
Changed files:
Checks:
Artifacts:
Delegation:
Residual tails:
Next action:
```
