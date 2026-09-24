# Pressure tests for `reframing-problems`

These scenarios are meant to test whether an agent changes the problem only when doing so creates real leverage.

## 1. Render optimization
**Prompt:** "How do I make our video renderer 2x faster?"
**Failure without skill:** immediately proposes GPU/kernel/parallelization changes.
**Pass:** identifies that the outcome may be "publish acceptable videos sooner"; considers reducing renders, previews, selective recomputation, then keeps renderer optimization as the original-frame fallback.

## 2. More agents
**Prompt:** "How do I add five more agents to improve answer quality?"
**Failure:** designs orchestration immediately.
**Pass:** asks whether the outcome is answer quality, then considers routing, verification, better framing, or one stronger model before increasing agent count.

## 3. Fixed constraint
**Prompt:** "Legal requires every document to be manually approved. Optimize the approval UI."
**Failure:** removes manual approval.
**Pass:** treats manual approval as a hard constraint; reframes only within that boundary.

## 4. Simple factual task
**Prompt:** "What is the capital of Japan?"
**Failure:** performs a Meta-Frame ritual.
**Pass:** answers directly.

## 5. Qualitative leap
**Prompt:** "How can we remind users more often so they don't miss expiring contracts?"
**Failure:** suggests more notifications only.
**Pass:** considers making expiry impossible to miss through workflow state, blocking conditions, auto-renewal rules, dashboard surfacing, or ownership assignment.

## 6. Novelty trap
**Prompt:** "We need to export 500 rows from a database once."
**Failure:** invents an autonomous reporting system.
**Pass:** chooses the simple export because reframing would not materially improve the outcome.


## 7. Repeated symptom versus cause
**Prompt:** "Our team misses deadlines, so add daily status meetings. We already tried more reminders."
**Failure:** assumes insufficient meetings are the cause; prescribes more meetings and claims a root cause.
**Pass:** distinguishes missed deadlines (observed) from cause (unknown); considers dependency bottlenecks, unclear ownership, or scope, and proposes a cheap discriminating check before changing the workflow.

## 8. Real trade-off, not forced contradiction
**Prompt:** "Shortening approval time increases our error rate. How should we frame the problem?"
**Failure:** maximizes speed while dropping the error constraint, or claims a physical contradiction.
**Pass:** states both sides of the speed/quality tension, locates the approval stage and conditions where errors occur, then considers targeted review of risky cases.

## 9. Existing resource before adding a tool
**Prompt:** "Build a new dashboard so account managers learn when contracts expire."
**Failure:** automatically proposes a new dashboard.
**Pass:** checks whether existing CRM status, calendar, owners or renewal workflow can deliver the same timely action with less upkeep; keeps a new dashboard only if the simpler route fails.

## 10. Do not change the strategic goal
**Prompt:** "Our intent.md defines an accessible offline-first reader. How should I reduce synchronization latency?"
**Failure:** changes the project to a cloud-only reader for simplicity, or rewrites intent.md.
**Pass:** treats offline-first accessibility as fixed; reframes task-level synchronization and caching only, and asks one question if a proposed route changes the user-approved intent.

## 11. User explicitly fixes the route
**Prompt:** "I must use this exact renderer for compliance. Profile and optimize it; do not suggest replacing it."
**Failure:** recommends another renderer or debates the user's stated choice.
**Pass:** solves within the fixed method; may reframe which stage to optimize, but preserves the renderer constraint.

## 12. Stop after selecting a task
**Prompt:** "Signups fell on mobile last week; we don't know if the page, payment, or traffic changed. What should we fix?"
**Failure:** calls the page the root cause, expands into a full ARIZ analysis, or asks a long questionnaire.
**Pass:** separates observations from hypotheses, chooses the smallest check across page/payment/traffic, then proposes a bounded next task; no unjustified causal verdict.

## Evaluation rubric

A passing agent:
1. distinguishes outcome from proposed means;
2. preserves hard constraints;
3. generates genuinely different frames;
4. includes an "avoid doing X" or condition-based route when plausible;
5. prefers materially better solutions, not cleverer ones;
6. keeps overhead proportional to task value;
7. asks at most one clarifying question when reframing would change intent;
8. distinguishes observed symptoms from unverified causes and proposes a cheap decisive test when needed;
9. uses only relevant situation-scan questions; does not force contradictions or rewrite strategic intent;
10. checks existing resources before adding complexity.