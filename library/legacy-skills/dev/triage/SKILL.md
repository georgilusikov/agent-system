---
skill_id: triage
skill_name: Triage — Competing Hypotheses
version: 1.0.0
category: dev
triggers:
  - "triage"
  - "flaky"
  - "race"
  - "inconsistent"
  - "multi-cause"
  - "несколько причин"
  - "гипотезы"
  - "то падает то нет"
dependencies:
  - "why_analysis"
  - "check"
description: "Abductive/Bayesian triage for incidents or debugging when 3+ competing causes are plausible. Use for flaky tests, race conditions, inconsistent failures, timeouts with multiple possible causes, multi-symptom production incidents, or when it is unclear which hypothesis to test first. Output MUST include 3+ hypotheses, priors, observed evidence, discriminating tests, first-test choice, posterior update, and handoff."
---

# Triage — Competing Hypotheses

Use this before root-cause analysis when the situation has competing explanations. For one linear failure chain, use `why_analysis` directly.

## Input Checklist

- [ ] At least 3 plausible hypotheses can be named.
- [ ] Each hypothesis is falsifiable.
- [ ] Evidence sources exist: code, logs, metrics, command output, tests, history, or user artifacts.
- [ ] At least one discriminating test can distinguish the top hypotheses.

## §1. Freeze Context

For flaky, stuck, timeout, killed, or repeated-failure cases, record:

| Known item | Last observation | Where confirmed |
|---|---|---|
| Last known good state | ... | file / log / command |
| Last failed attempt | ... | command / output |
| Unknown | ... | needed probe |

Do not retry the same action blindly. Choose a probe that changes information.

## §2. Generate Hypotheses

List at least 3 hypotheses. Include common classes for flaky/race issues when relevant:
- race or shared-state leak;
- fixture or order dependence;
- network or external service;
- timezone/time/randomness/cache;
- permissions/resource limits/version mismatch.

## §3. Triage Table

| H-ID | Hypothesis | Prior | Evidence for | Evidence against | Discriminating test |
|---|---|---:|---|---|---|
| H1 | ... | ... | `OBSERVED` / `NOT CHECKED` | ... | ... |

Prior is base rate for this class of system, not gut feeling about this incident. If unknown, use a range and say why.

Evidence rules:
- Use only observed facts in evidence columns.
- Mark guesses as `ASSUMPTION`, not evidence.
- Do not update posterior from `NOT CHECKED` or `NEEDS PROBE`.

## §4. Choose First Test

Pick the test with maximum information per effort:
- cheap and highly discriminating first;
- expensive stress tests later;
- if information value ties, prefer the highest-prior hypothesis.

Write: `First test: X, because it distinguishes H1 from H2 in about N minutes.`

## §5. Posterior Update

After the test:
- `Falsified` — evidence decisively contradicts hypothesis.
- `Supported` — posterior increases with observed likelihood.
- `Inconclusive` — no posterior update; choose another test.

Stop when one hypothesis has posterior >=80% and passed a discriminating test, or when evidence is sufficient for a reversible action. Do not fix at posterior <60% unless the action is explicitly exploratory and safe.

## §6. Handoff

- Top hypothesis >=80%: hand off to `why_analysis`.
- No hypothesis >=60%: gather new evidence; do not fix by intuition.
- Fix applied: hand off to `check`.
- High-stakes release readiness: hand off to `bouncer` for independent review if requested.

## Output Contract

Output MUST include:
- 3+ hypotheses.
- Prior for every hypothesis.
- Evidence states for every important claim.
- Discriminating test for each top hypothesis.
- First-test choice with rationale.
- Posterior update after the test, or `NEEDS PROBE`.
- Handoff recommendation.

## FORBIDDEN

- Collapse a 3+ hypothesis situation into one favorite cause without triage.
- Use assumed facts as observed evidence.
- Retry a flaky/timeout command repeatedly without a new probe.
- Stop on posterior <60% and present it as root cause.

## Hard fail

- Fewer than 3 hypotheses.
- No discriminating test.
- Posterior updated from unobserved evidence.
- Fix recommended without evidence level and confidence.
