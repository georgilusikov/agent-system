---
skill_id: measure
name: measure
description: 'Use for trustworthy comparison or evaluation: "measure", "compare two variants", "A/B result", "eval harness", "judge calibration". Routes to existing experiment_designer and ab_testing_calculator after measurement-validity gates. NOT for verifying a finished artifact without comparison (use check) or diagnosing a concrete failure (use why_analysis/triage).'
category: dev
triggers:
  - "measure"
  - "compare two variants"
  - "A/B result"
  - "eval harness"
  - "judge calibration"
dependencies: ["experiment_designer", "ab_testing_calculator"]
---

# Measure

Thin public router/gate. It adds no measurement methodology: use
`triz/experiment_designer` to design the falsifying experiment and
`business/ab_testing_calculator` for sample/MDE/CI/power arithmetic.

## Input checklist

- Claim, alternatives, unit of analysis, metric, and decision are explicit.
- Raw observations and variant provenance are available or marked missing.
- A failure threshold and maximum budget/window can be preregistered.

## Validity gate (before running)

Record PASS/FAIL/UNKNOWN for every key below. Any FAIL/UNKNOWN blocks a causal
or superiority verdict; it does not block a diagnostic pilot.

1. `construct_validity` — metric measures the claimed outcome, not a proxy drift.
2. `no_change_repeat_baseline` — repeat the unchanged condition; quantify harness noise.
3. `isolation_leakage` — variants do not share inputs/cache/state and provenance differs.
4. `randomization_blinding` — assignment/order is randomized; judge is blind where possible.
5. `judge_calibration` — judge beats the preregistered floor on labeled controls.
6. `variance_power` — variance, MDE, sample size, power, and uncertainty are decision-ready.
7. `preregistered_stop_rule` — sample/window, peeking policy, exclusions, and verdict rule are fixed.

## Route

- No observations yet or mechanism/design uncertain → `experiment_designer`.
- Two randomized arms with metric data → `ab_testing_calculator`.
- Model/judge eval → both: experiment design first, calculator for uncertainty.
- Paired/non-random benchmark → experiment design; calculator only if its assumptions hold.

## Protocol

1. Write the claim and the cheapest result that would falsify it.
2. Run the no-change repeat before comparing variants.
3. Pass the seven-item validity gate; repair the first failed upstream item.
4. Route to the existing skill(s), preserving raw observations and provenance.
5. Stop only by the preregistered rule; emit the receipt below.

## machine-readable receipt

```json
{
  "schema_version": 1,
  "claim": "",
  "decision": "",
  "variants": [{"id": "", "provenance": ""}],
  "unit_of_analysis": "",
  "metric": {"name": "", "construct": "", "mde": null},
  "validity": {
    "construct_validity": {"status": "PASS|FAIL|UNKNOWN", "evidence": ""},
    "no_change_repeat_baseline": {"status": "PASS|FAIL|UNKNOWN", "evidence": ""},
    "isolation_leakage": {"status": "PASS|FAIL|UNKNOWN", "evidence": ""},
    "randomization_blinding": {"status": "PASS|FAIL|UNKNOWN", "evidence": ""},
    "judge_calibration": {"status": "PASS|FAIL|NA|UNKNOWN", "evidence": ""},
    "variance_power": {"status": "PASS|FAIL|UNKNOWN", "evidence": ""},
    "preregistered_stop_rule": {"status": "PASS|FAIL|UNKNOWN", "evidence": ""}
  },
  "sample": {"planned": null, "observed": null},
  "result": {"effect": null, "interval": null, "verdict": "blocked|no-difference|better|worse"},
  "artifacts": [],
  "stopped_by": ""
}
```

## Definition of Done

- All seven validity items and evidence are in the JSON receipt.
- The chosen downstream skill and its output are named.
- Verdict strength does not exceed the weakest validity status.

## FORBIDDEN / hard fail

- No superiority claim without the no-change baseline and isolation proof.
- No model-judge verdict without calibration controls.
- No stopping because a desired result appeared.
- Missing/invalid JSON receipt = incomplete run.
