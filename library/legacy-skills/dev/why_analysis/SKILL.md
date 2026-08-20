---
skill_id: why_analysis
skill_name: Why Analysis (5 Whys)
version: 1.0.0
category: dev
triggers:
  - "why"
  - "почему"
  - "root cause"
  - "5 whys"
  - "rca"
dependencies: []
description: "Root Cause Analysis for one linear failure chain. Use when the user asks why/debug/root cause/RCA, a command has a clear error or traceback, or a selected triage hypothesis needs deep investigation. Output MUST include exact symptom, command/output evidence, anti-freeze check, 5 Whys with evidence, root cause, targeted fix, verification command, and document block."
---

# Root Cause Analysis (5 Whys)

Use this for one linear chain. If there are 3+ competing hypotheses, use `triage` first.

## Input Checklist

- [ ] Exact symptom or error is known.
- [ ] Triggering command, action, or user flow is known.
- [ ] Full output, traceback, log excerpt, or observable failure is available.
- [ ] Expected behavior is known.
- [ ] There are not 3+ competing causes; if there are, route to `triage`.

## §1. Gather Facts

Capture facts before analysis:

| Item | Value | Evidence source |
|---|---|---|
| Command/action | ... | command / user report |
| Error/symptom | ... | output / log / screenshot |
| Expected behavior | ... | spec / test / user request |
| Last known good | ... | git / test / log / `UNKNOWN` |

Use evidence states: `OBSERVED`, `NOT CHECKED`, `NEEDS PROBE`, `ASSUMPTION`.

## §1.1. Anti-Freeze Check

If any freeze signal appears, stop repeated retries:
- same attempt repeated 3+ times;
- timeout, killed process, hang, or waiting for input;
- loop of "try -> no new evidence -> same try";
- no new evidence after retry.

Record:

| Known item | Last observation | Where confirmed |
|---|---|---|
| Last known good state | ... | file / log / command |
| Last failed attempt | ... | command / output |
| Unknown | ... | needed probe |

Choose one new probe: minimal repro, verbose log, grep, isolation run, version check, permissions check, resource check. Until executed, probe result is `NEEDS PROBE`.

## §2. Five Whys With Evidence

Every why must cite observed evidence. Stop at `NEEDS PROBE` instead of guessing.

| # | Why question | Answer | Evidence |
|---|---|---|---|
| 1 | Why did the symptom occur? | ... | ... |
| 2 | Why did answer 1 happen? | ... | ... |
| 3 | Why did answer 2 happen? | ... | ... |
| 4 | Why did answer 3 happen? | ... | ... |
| 5 | Why did answer 4 happen? | ... | ... |

Root cause should be process/system/design level when the evidence supports it, not only the immediate thrown exception.

## §3. Fix

- Fix the root cause, not only the symptom.
- Prefer a targeted change over broad rewrites.
- Do not create alternative workarounds unless evidence shows the original path cannot be made correct.
- Verify assumptions with data before editing.

## §4. Verify

Repeat the command/action that triggered the issue when feasible. `Status: Verified` is allowed only when the command/action was rerun after the fix. If not rerun, use `Status: Needs probe`.

After a fix, use `check` to verify negative space and regressions.

## §5. Document

```text
Command: ...
Error: ...
Root Cause: ...
Fix: ...
Status: Verified / Still failing / Needs probe
```

If the root cause is process/systemic or repeated, record the learning in `_agent_shared/error_feedback/errors_YYYY-MM.md` or `_agent_shared/memory/patterns.md` when appropriate.

## Output Contract

Output MUST include:
- exact symptom and command/action;
- anti-freeze check result;
- 5 Whys table with evidence;
- root cause;
- targeted fix or next probe;
- verification command/action and result;
- document block.

## FORBIDDEN

- Invent command output, logs, file contents, versions, or test results.
- Write `Verified` without rerunning the relevant command/action after the fix.
- Present a hypothesis as root cause without evidence.
- Patch around the symptom while leaving the root cause unaddressed.

## Hard fail

- No exact symptom/command.
- Five Whys contain unsupported guesses.
- `Status: Verified` without observed rerun.
- Fix chosen while a required probe is still `NEEDS PROBE`.
