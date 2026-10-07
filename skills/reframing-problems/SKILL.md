---
name: reframing-problems
description: Use when a request may be solving the wrong problem, mistakes a symptom for the task, assumes a particular means too early, hides a conflict between requirements, or has a cheaper route to the same outcome. Run one lightweight problem-selection pass before solving; do not replace a user's long-term intent.
---

# Reframing Problems

## Overview

Do not optimize the first formulation by default. First check whether the requested task is merely one way to achieve a more important outcome.

**Core principle:** improve the problem before spending effort improving the solution.

## When to Use

Use when:
- the user asks *how* to do something but the underlying *why* may admit better routes;
- the proposed means looks expensive, complex, slow, or over-constrained;
- several correct solutions may exist, including a non-obvious one with much higher leverage;
- the user asks for strategy, architecture, optimization, product decisions, workflows, or invention.

Do **not** use for simple factual lookup, exact calculation, direct transformation, or when the user explicitly requires a fixed method and no alternative framing is useful.

## Boundary: tactical framing, not strategy

This skill chooses **which task to solve now**. If a broader strategic intent or `intent.md` exists, use it as a constraint, not as a document to rewrite. Do not invent a new life/business direction, change the success criterion, or silently overrule an explicit user choice. Treat explicit metrics, deadlines, named deliverables, and mandatory methods as binding unless the user says they are flexible. A conjectured higher-level outcome (e.g. faster publishing) is not permission to substitute a different metric (e.g. renderer throughput). If a materially better frame changes the user's stated goal, present the trade-off and ask at most one targeted question.

## Creative-Situation Scan (selective)

Run this only when the problem is vague, a fix keeps failing, the proposed means are unusually costly, or there are plausible competing problems. Pick **two or three** questions that could change the selected task; these are internal prompts, **not** a mandatory user questionnaire:

- **Observed effect:** What happened, where/when, to whom, and by what observable measure? What is reported evidence versus a hypothesized explanation?
- **Actual obstruction:** What specifically prevents the desired outcome? If the named symptom vanished tomorrow, would the outcome improve? Do not confuse a root-cause hypothesis with an observed fact.
- **Alternative tasks:** Could we change a component, the workflow/system, or its surrounding system instead? Could we remove the need for the harmful interaction or achieve the goal by a different route?
- **Conflict:** What useful effect does the current approach produce, and what does it worsen? If two requirements genuinely clash, state both directions of the trade-off; do not force a technical or physical contradiction onto a social or simple task.
- **Localize:** If the conflict matters, where and when does it actually occur? Is it present everywhere or only under particular conditions?
- **Available resources:** What existing people, time, data, tools, capacity, relationships, permissions, or unused functions could deliver the outcome without adding a new component or process?
- **Avoid the task:** If the requested action were impossible or free, which other task would become sensible? What happens if we do nothing, defer, or make the need disappear?
- **Decisive uncertainty:** Which one cheap observation or reversible test would distinguish the leading problem formulations?

Stop when you can state one concrete task worth solving and why it is preferable to the literal one. If evidence is missing, mark the alternative as a hypothesis, not a discovered root cause. Use extreme size/time/cost thought experiments only if ordinary reframing fails and a real new task might emerge.

## Meta-Frame Pass

Before solving, perform this once:

1. **Literal task** — What did the user explicitly ask to do?
2. **Outcome** — What real effect or state do they appear to want?
3. **Hard constraints vs assumed means** — Separate requirements from the current proposed method.
   - When the situation is ambiguous or the fix keeps failing, run the selective Creative-Situation Scan above before choosing what to solve.
4. **Step up** — Ask: *Why is this outcome valuable? What is the goal one abstraction level higher?*
5. **Escape** — Ask: *Can the outcome be achieved without doing the literal task at all?*
6. **Conditions** — Ask: *Could we create conditions under which the desired result happens with less intervention?*
7. **Ideality** — Ask: *What would it look like if the useful function happened with near-zero cost, complexity, delay, or maintenance?* Check whether an existing resource could perform the function.
8. **Generate at most 3 frames:**
   - **Original** — solve the task as asked;
   - **Higher-level** — solve the underlying outcome;
   - **Leap** — qualitatively different, simpler, cheaper, or more leveraged formulation.

## Select the Problem Before Solving

For each viable frame, articulate the **task to solve** in one sentence and check: Is it connected to the user's outcome? Does it attack an observed obstruction rather than only a symptom? Does it preserve hard constraints and existing strategic intent? Can the task be tested or acted on now?

Default to the original task if a new frame is only interesting, not materially better. If the user gave a measurable outcome or explicitly fixed the task, execute that task first; present a different objective only as an optional alternative, not as the replacement answer. Do not ask the user to reconfirm an already stated goal. If a key causal assumption is unverified and would change the task choice, propose the cheapest discriminating test; do not claim to have found the root cause. Separate problem selection from the subsequent solution work.

## Choose the Frame

Compare frames on:
- goal satisfaction;
- quality;
- time;
- cost/effort;
- risk;
- reversibility/optionality;
- hidden assumptions;
- observable basis for the chosen problem and cheapest decisive test when uncertain;
- reuse of existing resources instead of adding unnecessary machinery.

Prefer a frame only when it is **materially better**, not merely more novel.

If the best frame changes the user's intent or violates a hard constraint, ask **one targeted question** before proceeding.

## Choose the Route

For the chosen frame, take the cheapest route that fully reaches the outcome:
**avoid** the work → **reuse** existing resources → **adopt** a ready solution → **build**.
Count adoption, integration, and maintenance, not only build time.
If no route is obvious, name the function (action → object → measurable effect) and
search analogues via `triz` chain C11 (`benchmarking → fos → oas_transfer`);
verify transfer with the smallest local test.

## Solve

After selecting the frame:
- solve it normally;
- state briefly when you intentionally changed the problem formulation;
- preserve the original route as fallback when useful.

## Escalation

Default: **one Meta-Frame pass + one solve**.

Escalate to deeper critique, multiple agents, evidence checks, or deliberation only when:
- frames are close in value;
- stakes are high;
- key assumptions are uncertain;
- external evidence determines which frame is valid.

Do not run debate merely to make the answer look rigorous.

## Failure Modes

- **Premature solving:** optimizing the requested method before identifying the outcome.
- **Fake reframing:** paraphrasing the same task three ways.
- **Novelty bias:** preferring a clever route that is worse operationally.
- **Constraint deletion:** treating real requirements as optional assumptions.
- **Infinite why-chain:** climb only until a more useful decision space appears.
- **Symptom as cause:** claiming a root cause from a complaint without evidence.
- **Contradiction theater:** inventing opposing requirements when none are established.
- **Strategy drift:** replacing the user's long-term intent with the agent's preferred goal.
- **Questionnaire overload:** asking every scan question instead of selecting the few that matter.
- **Overhead explosion:** spending more on reframing than the task is worth.

## Output Pattern

For non-trivial cases, internally produce:

```text
Literal task:
Underlying outcome:
Observed effect / uncertainty (if relevant):
Hard constraints:
Assumed means:
Higher-level goal:
Key obstruction / conflict (if relevant):
Existing resources (if relevant):

Candidate frames:
A. Original:
B. Higher-level:
C. Leap:

Selected task:
Best frame / why:
Cheapest decisive test (if needed):
Route (avoid/reuse/adopt/build):
Solve / one clarifying question:
```

Keep this scratch structure internal unless showing it would help the user.