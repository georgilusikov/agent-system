---
skill_id: check
skill_name: Check — Result Verification
version: 1.0.0
category: dev
triggers:
  - "check"
  - "проверь"
  - "верификация"
  - "validate"
  - "test"
  - "quality check"
dependencies: []
description: "Verify a completed result before declaring done. Use after code changes, generated artifacts, task completion, or when the user asks to check/validate/test quality. Output MUST include expected state first, positive/negative/edge test cases, PASS/FAIL evidence, gap table, negative space, and confidence calibration."
---

# Check — Result Verification

Verify a claim against observable evidence. Do not use this for external second-opinion audit; use `bouncer` for that. Do not use it for process reflection; use `reflect`.

## Input Checklist

- [ ] Goal or claim is known.
- [ ] Artifacts, changed files, commands, or outputs to verify are known.
- [ ] Source of truth is available: file, command, log, screenshot, test output, or explicit user-provided artifact.
- [ ] High-risk areas are named, or explicitly marked `UNKNOWN`.

## §0. Expected State First

Before reading fresh evidence or running checks, write 3-7 observable expectations.

| E-ID | What must be true | Where to verify | Next action if unmet | Actor | Effort |
|---|---|---|---|---|---|
| E01 | ... | file / command / log / screenshot | ... | agent / owner / both | 0-100 |

Rules:
- Form expectations before actual evidence.
- Each expectation must pass the camera test: it can be observed.
- If expectations cannot be formed, stop and clarify the task or run discovery first.

## §1. Test Cases Before Verification

Define tests before executing them:

| Type | Test | Expected | Evidence source | Result |
|---|---|---|---|---|
| Positive | ... | ... | ... | PENDING |
| Negative | ... | ... | ... | PENDING |
| Edge | ... | ... | ... | PENDING |

Use `NOT CHECKED` when a test was not actually run or an artifact was not actually opened.

## §2. Observe Evidence Personally

Read artifacts, run commands, inspect logs, or capture screenshots as needed. Do not describe file contents, test results, versions, logs, parser behavior, server behavior, or UI behavior as fact without observing it in the current session.

Allowed evidence states:
- `OBSERVED` — directly seen in this session.
- `NOT CHECKED` — not inspected.
- `NEEDS PROBE` — a test or read must still be performed.
- `ASSUMPTION` — useful guess, not evidence.

## §3. Challenge

Answer briefly:
- What did the result achieve?
- What was missed or left unverified?
- What would be unclear to a manager, developer, or teammate?
- What are 3 ways this verdict could be falsified?

## §4. Gap Analysis

Include at least one row. If no gaps are found, use `G00 — gaps not found`.

| G-ID | E-ID ref | Expected | Actual | Root Cause | Fix / Next action | Actor | Effort |
|---|---|---|---|---|---|---|---|
| G00 | E01 | ... | ... | gaps not found | none | agent | 0 |

## §5. Negative Space

State what is absent and whether it matters: tests, migrations, error handling, logging, docs, rollback, secrets handling, `.env.example`, indexes, accessibility, performance, UI/browser verification.

## §6. Output Contract

Output MUST include:
- Expected State table.
- Positive / Negative / Edge tests with PASS / FAIL / NOT CHECKED.
- Gap table.
- Negative Space.
- Confidence: `[before]% -> [after]% — reason`.
- Artifact links or command names for everything checked.

## Definition of Done

- [ ] No verification claim is based on memory alone.
- [ ] Every PASS/FAIL has an evidence source.
- [ ] Gaps and unchecked areas are explicit.
- [ ] Final verdict is calibrated to the evidence actually observed.

## FORBIDDEN

- Start verification without §0 Expected State First.
- Claim `PASS`, `done`, or `verified` from memory.
- Invent logs, command outputs, file contents, versions, screenshots, or test results.
- Replace missing evidence with confidence.
- Hide `NOT CHECKED` items.

## Hard fail

- No Expected State table.
- No positive/negative/edge test cases.
- No gap table row.
- No confidence calibration.
- Any invented evidence.
