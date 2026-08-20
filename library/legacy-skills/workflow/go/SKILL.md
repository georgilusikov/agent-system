---
skill_id: go
skill_name: Go — Workflow Router
version: 1.0.0
category: workflow
triggers:
  - "go"
  - "/go"
  - "workflow router"
  - "new feature"
  - "bugfix"
  - "refactor"
  - "qa"
dependencies:
  - "check"
  - "triage"
  - "why_analysis"
  - "spec_flow"
  - "tdd"
  - "prd_to_issues"
description: "Workflow router for choosing the right canonical skill chain. Use when the user invokes /go, asks to start a feature, bugfix, refactor, QA session, TDD implementation, or quality exit and the next workflow is not obvious. Output MUST include chosen intent, route, loaded skills/references, step summary, and next action."
---

# Go — Workflow Router

Route the user's request to the smallest effective workflow. Do not load every referenced skill; load only the selected route.

## Input Checklist

- [ ] User goal is present.
- [ ] Intent is one of feature, bugfix, refactor, QA, TDD, quality exit, or unknown.
- [ ] Relevant project context has been read from `WORKSPACE_ROUTER.md` / `WORKSPACE_INDEX.md` when codebase scope matters.
- [ ] If intent is unknown, ask one clarifying question.

## §1. Route Table

| Intent | Signals | Route |
|---|---|---|
| Feature / idea | feature, фича, хочу сделать, идея, план | `spec_flow` -> PRD/plan work -> `tdd` |
| Bug / clear error | bug, ошибка, traceback, не работает | `why_analysis`; if 3+ causes, `triage` first |
| Multi-cause debug | flaky, race, inconsistent, timezone, cache, network, several causes | `triage` -> `why_analysis` -> `check` |
| QA session | qa, тестирую, found bugs, баги | `check` for verification ledger; `qa_notes` if notes are needed |
| Refactor | refactor, переписать, почистить architecture | `spec_flow` -> `tdd` -> `check` |
| TDD implementation | tdd, tests first, red green, реализуй с тестами | `tdd` |
| Quality exit | готово, проверь, validate, done, release readiness | `check`; `bouncer` if independent review requested |

## §2. Route Rules

1. If intent is clear, state route and load only the needed canonical skill.
2. If intent is unclear, ask one question: "Это новая фича, баг, рефакторинг, QA или quality check?"
3. If a route reaches implementation, prefer `tdd` unless the user explicitly requests a non-code-only planning step.
4. If a route reaches final verification, use `check`.
5. If the user requests independent audit, second opinion, score, or dual review, use `bouncer`.

## §3. Quality Exits

| Signal | Route | Pass forward |
|---|---|---|
| Ready artifact / "готово, проверь" | `check` | goal, files, claimed outcome, known risks |
| One clear error / traceback | `why_analysis` | command, output, expected behavior |
| 3+ causes / flaky / race | `triage` | symptoms, candidate causes, logs/tests seen |
| Stuck / timeout / repeated attempts | `why_analysis` or `triage` | last known state, failed attempts, one new probe |
| Prod readiness / high-stakes plan | `bouncer` after local `check` | claim, source-of-truth files, release risk |

## §4. Step Summary

After each major workflow step, emit:

```text
Goal: ...
Did: ...
Result: OK/FAIL (...)
Next: ...
```

## Output Contract

Output MUST include:
- chosen intent;
- chosen route;
- skill(s) loaded or to load;
- one-step summary;
- next action or one clarifying question.

## FORBIDDEN

- Load every possible workflow.
- Continue with an unclear route when one question would resolve it.
- Skip `triage` when 3+ competing causes are visible.
- Claim completion without routing to `check`.

## Hard fail

- No route selected.
- More than one clarifying question before starting.
- A multi-cause debug case is treated as a single confirmed cause without evidence.
