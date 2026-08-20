---
name: no-fabricated-evidence
description: Evidence boundary for verification, RCA, triage, and self-review outputs.
version: 0.0.1
created: 2026-04-24
updated: 2026-04-24
scope: personal
status: active
owner: georgy
based_on: krasinsky-minimal-plus-pilot
applies_to:
  - /check
  - /why
  - /triage
  - /anti-bias
  - /pizdej
  - /falsify
incident_trigger: A/B and self-falsify tests found pseudo-rigor: structured protocols can invent evidence unless honest-ignorance states are explicit.
---

# No Fabricated Evidence Standard

## 1. Job / JTBD
When a skill needs evidence, it must separate observed facts from missing data so rigor does not become invented proof.

## 2. Protocol
Use these states:
- `OBSERVED`: file/command/log/output was actually read or run in this session.
- `NOT CHECKED`: expected evidence exists in theory, but was not read/run.
- `NEEDS PROBE`: next command/read needed before root cause or verdict.
- `ASSUMPTION`: accepted temporarily and labeled as not evidence.

Rules:
- Line numbers, logs, command output, file contents, counts, and `Status: Verified` require `OBSERVED`.
- `PASS` is forbidden for high-stakes claims with `NOT CHECKED` primary evidence.
- If tool access is unavailable, the honest result is `PARTIAL / NEEDS EVIDENCE`, not synthetic PASS/FAIL.
- Zero `NOT CHECKED` markers in a complex or high-stakes audit is a warning sign: inferred data without direct observation must be labeled `ASSUMPTION`.

## 3. FORBIDDEN
- Claiming a precedent scan ran when it did not.
- Quoting unread MEMORY, logs, files, or reports.
- Treating user claims as observed evidence.
- Filling protocol tables with invented facts to satisfy format.

## 4. Hard Fail
- Any invented file content, log line, count, command result, or line number.
- `Verified` without rerunning or observing the verification command.
