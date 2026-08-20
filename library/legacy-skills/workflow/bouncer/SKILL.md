---
skill_id: bouncer
skill_name: Bouncer — Independent Quality Audit
version: 1.0.0
category: workflow
triggers:
  - "bouncer"
  - "audit"
  - "score"
  - "second opinion"
  - "dual review"
  - "review plan"
  - "cross-check plan"
  - "quality audit"
dependencies:
  - "check"
description: "Independent quality audit for work products, code changes, plans, research, or creative output. Use when the user asks for bouncer/audit/score/second opinion/dual review/cross-check plan or explicitly wants external review beyond local verification. Output MUST include audit context, backend/mode choice, per-audit verdicts, consensus, blockers, and next action."
---

# Bouncer — Independent Quality Audit

Use after or alongside local `check` when the user wants a second opinion. This skill is for independent review, not solo verification.

## Input Checklist

- [ ] Artifact or claim to audit is known.
- [ ] Audit mode is known or can be inferred: quick, deep, or plan-review.
- [ ] Candidate backends are available or explicitly unavailable.
- [ ] Context can be summarized without secrets.

## §1. Invocation

| User signal | Mode | Default backend plan |
|---|---|---|
| bouncer, score, audit | quick | one available independent reviewer |
| deep audit, verify everything | deep | one available reviewer with evidence checks |
| dual review, review plan, cross-check plan | plan-review | Codex/agent reviewer if available |
| both models, Gemini + Codex, consensus | quick/deep | requested backends, cap 3 per backend |

If backend/mode/count is ambiguous and matters, ask one concise question.

## §2. Gather Shared Context

Collect once:
- `git diff --stat --no-color` and relevant diff when auditing code;
- changed files and commands run;
- goal, audience, assumptions, risks;
- source instructions such as `AGENTS.md` / `CLAUDE.md` when relevant;
- user's claimed outcome.

Build a compact audit payload:

```json
{
  "assistant_text": "...",
  "diff_stat": "...",
  "diff_text": "...",
  "context": "...",
  "cwd": "/abs/path",
  "mode": "quick|deep|plan-review"
}
```

## §3. Dispatch Reviewers

Use available Codex/runtime tools only. If external scripts or model CLIs are unavailable, report that limitation instead of inventing an external verdict.

When the user explicitly asked for dual/parallel/external review and the runtime supports subagents, dispatch independent reviewers with minimal task-local context. Do not leak the intended answer.

Reviewer prompt must ask for:
- score or verdict;
- top gap;
- top risk;
- evidence checked;
- blocker vs non-blocker distinction.

## §4. Aggregate

| Audit | Score | Verdict | Top gap | Top risk |
|---|---:|---|---|---|
| reviewer-1 | ... | APPROVED / NEEDS_REVISION | ... | ... |

Consensus rules:
- all approved -> overall `APPROVED`;
- any blocking issue -> `NEEDS_REVISION`;
- split verdicts -> present both views and recommend a decision.

## §5. Plan-Review Iteration

For plan-review, if verdict is `NEEDS_REVISION`:
1. Update the plan with accepted suggestions and reasons for rejected suggestions.
2. Re-dispatch review only if the user asked for iterative review or the mode explicitly requires it.
3. Stop after 3 cycles or when approved.

Record review summary in the plan when a plan file exists.

## Output Contract

Output MUST include:
- artifact/claim audited;
- backend/mode used or unavailable;
- per-audit verdict table;
- consensus verdict;
- unique useful insight from each reviewer;
- blockers and next action.

## FORBIDDEN

- Present a local self-check as independent external audit.
- Invent model outputs or reviewer verdicts.
- Hide backend/script errors.
- Send secrets or sensitive data to external reviewers.
- Run more than 3 reviewers per backend.

## Hard fail

- No audit subject.
- No backend/mode statement.
- Consensus verdict without per-audit evidence.
- External review claimed when no external reviewer ran.
