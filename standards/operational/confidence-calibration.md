---
name: confidence-calibration
description: Numeric confidence penalties for unverified claims in agent output.
version: 0.0.1
created: 2026-04-24
updated: 2026-04-24
scope: personal
status: active
owner: georgy
based_on: krasinsky-minimal-plus-pilot
applies_to:
  - /check
  - /falsify
  - /anti-bias
  - /pizdej
incident_trigger: Agents were overconfident when source, data, or tests were not actually checked.
---

# Confidence Calibration Standard

## 1. Job / JTBD
When an agent reports PASS, readiness, or a recommendation, confidence must reflect what was actually verified.

## 2. Protocol
Start from the honest initial confidence, then apply penalties:

| Missing verification | Penalty |
|---|---:|
| Code changed but not tested | `-50%` |
| Data claim not verified from source-of-truth | `-55%` |
| Referenced source/page/file not read | `-40%` |
| Visual/UI output not viewed after change | `-40%` |
| External dependency/version not checked when unstable | `-30%` |
| No negative/edge case considered | `-25%` |

Floor confidence at `0%`; cap at `95%` unless independently reproduced.

## 3. Expected State
- Confidence line explains the biggest penalty.
- `confidence <70%` cannot produce verdict `PASS`.
- If confidence is below `70%`, output names the next probe that would raise it.

## 4. FORBIDDEN
- Do not say PASS when the main source-of-truth was not read.
- Do not hide "not tested" behind soft wording.
- Do not use "should work" as a readiness verdict.

## 5. Hard Fail
- PASS with confidence below `70%`.
- PASS after code change with no test/probe and no explicit penalty.
