---
name: decision-alternatives-standard
description: Conditional contract for comparing materially different decision options without exposing private reasoning.
version: 0.0.1
created: 2026-08-22
updated: 2026-08-22
scope: shared
status: active
owner: georgy
incident_trigger: Agents need a reusable alternative-selection contract, but routine reversible work must remain free of decision rituals.
---

# Decision Alternatives Standard

**Класс:** contract

## Contract

Use alternatives when the decision concerns architecture or design, an
irreversible or expensive change, an ambiguous goal, a high-risk outcome, or an
explicit request to compare alternatives/options. Otherwise skip the contract
and state briefly why no meaningful alternative exists.

When triggered, show 2–3 genuinely different options. For each option use the
same fields:

- **Outcome / fit** — what it achieves and where it fits.
- **Benefit** — the material upside.
- **Risk** — the material downside or failure mode.
- **Cost / latency** — implementation, operational, or decision cost.
- **Evidence** — observed source, check, or clearly labelled uncertainty.
- **Discriminating test / canary** — one bounded check that would distinguish it
  from the nearest option.

Pick one option with a short reason. Name why adjacent options were not chosen.
Do not list cosmetic variants, pad the count, or manufacture balance.

## Routing

- **Diagnosis:** use competing hypotheses already defined by `/debug`; do not
  turn a root-cause investigation into an architecture option list.
- **IKR-lite:** route through `/triz` → `ikr` → `resource_analysis` →
  `trimming`. State the result as “the result happens by itself without a new
  harmful stage” and perform a resource-path check. Apply the IKR body's Gate
  Check: “X САМО…”, not a disguised solution, based on available resources.
  If the canonical IKR body is unavailable, say so; do not reconstruct it.

## Owner-facing surface

Expose only the decision summary, evidence, uncertainty labels (`[O]`, `[I]`,
`[S]`, `[A]`), selected/rejected reasons, and next discriminating test. Keep
private chain-of-thought private. Never request, print, or log prompts, hidden
reasoning, transcripts, tool payloads, credentials, or environment values.

## Tiny golden/checklist

- [ ] Routine, reversible, well-specified one-path work: skipped with a reason.
- [ ] Triggered work: exactly 2–3 materially different options.
- [ ] Every option has outcome/fit, benefit, risk, cost/latency, evidence, and
      one discriminating test.
- [ ] Diagnosis routes to `/debug`; IKR-lite routes to `/triz` and checks the
      available-resource path.
- [ ] One option is selected; nearby options have explicit rejection reasons.
- [ ] The next test is bounded and can distinguish the leading options.
- [ ] No private chain-of-thought or sensitive payload is requested or exposed.

## Verification matrix

| Expected state | Check |
|---|---|
| Trigger and routine skip are discoverable | Read-as-agent assertion finds both rules |
| Contract fields are uniform | Assertion finds all six fields |
| Routes are wired | Assertion finds `/debug`, `/triz`, `ikr`, and resource-path language |
| Privacy boundary holds | Assertion finds chain-of-thought prohibition and no request language |
| Standard remains compact | Line-count assertion passes; `python3 scripts/check.py --repo` passes |

## FORBIDDEN

- Alternatives for routine reversible work as ritual.
- Cosmetic variants or fake balance.
- A choice without evidence, a rejection reason, or a discriminating test.
- A new TRIZ runtime, skill family, dependency, or private-reasoning policy.

## Hard fail

Triggered work without 2–3 materially different options, required fields, or a
bounded discriminating test is incomplete. IKR-lite without the canonical body
availability check is invalid.

## Related

- `skills/anti-bias/SKILL.md`
- `skills/debug/SKILL.md`
- `skills/triz/SKILL.md`
- `library/legacy-skills/triz/ikr/SKILL.md`
- `standards/operational/response-clarity-golden.md`
- `standards/operational/output-format.md`

## Changelog

- **0.0.1** (2026-08-22) — initial conditional alternatives contract with
  diagnosis, IKR-lite, and privacy routing.
