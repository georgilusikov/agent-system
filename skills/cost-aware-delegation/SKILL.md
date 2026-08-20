---
name: cost-aware-delegation
description: 'Use before substantial work when delegation, transport, model tier, or token cost may change the outcome. Triggers: "какой моделью это делать", "стоит ли звать субагента", "дорого ли делегировать", "выбери канал и тир", "which model tier for this task". NOT for: написание брифа уже выбранному исполнителю и приёмка (/delegate), механика worktree-волн, мониторинга lanes и запуска нескольких агентов (/agent-orchestrator-standard).'
---

# Cost-Aware Delegation

Use this skill before substantial work where delegation or model choice could
change total cost, latency, or quality. The goal is not "delegate more"; it is
"spend expensive reasoning only where it changes the outcome."

## Quick Decision

Before launching subagents, estimate:

- `direct_cost`: can the main model finish in 10-15 minutes with small context?
- `delegation_overhead`: prompt + context transfer + wait + review + integration.
- `risk_cost`: how expensive is a wrong cheap answer or rework?
- `saved_high_tokens`: how much expensive-model reading/checking will be avoided?

Delegate only when `saved_high_tokens` is clearly larger than
`delegation_overhead + risk_cost`.

## Transport First, Model Second

Pick the work shape before picking a model:
- Built-in subagent: the platform selects the model; use it only when exact tier
  is irrelevant. Give it a bounded evidence task, normally with no inherited
  turns, and keep judgment/acceptance in the parent.
- Explicit tier required: use a verified Codex thread or CLI/transport exposing
  model selection; resolve the model through the capability registry first.
- `cmd` / Command Code: cheapest default for bounded scouts, short reports,
  patch proposals, and targeted implementation with durable result files.
- OpenCode: use when OpenCode free/Go models are the best price fit, or `cmd`
  is busy; avoid OpenRouter-backed models unless explicitly allowed.
- Cursor: narrow implementation with clear file scope and local validation.
- AGY/Antigravity: verifier, skeptic, artifact review, backlog falsification.
- Claude Code / Codex Goal worker: coherent phases, shared-core debugging,
  architecture-heavy implementation, or long unattended ownership.

## Default Tier Routing

Route by capability tier, never by hardcoded model name — models change and
cheaper ones appear. Tier→model mapping lives ONLY in
`references/capability-registry.md`; update that file, not skill text.

- Main model directly: short answers, obvious 1-2 file edits, local commands,
  tiny bug fixes, small config/docs edits, and tasks with high handoff overhead.
- `T0 low scout`: grep/search, summaries, simple audits, formatting,
  mechanical checks, and evidence maps.
- `T1 medium scout/implementer`: bounded multi-file patches, known failing
  tests, ordinary coding, consumer mapping, and verifier passes.
- `T2 strong/high specialist`: ambiguous root cause, architecture,
  long-context synthesis, conflicting findings, shared contracts,
  security/release/provider risk, and final acceptance.

Model choice and responsibility are separate: an auto-routed built-in worker may
collect evidence, but it never owns a judgment seam (root cause, contract/schema,
architecture, conflicting evidence, security/release/provider, worker acceptance,
or final verdict). The parent or an explicitly routed T2 lane owns that decision.

Do not use a T2 model for routine fact gathering, formatting, simple patching,
or one-pass checks when a T0/T1 lane can leave evidence. Before hard-coding a
launch command, resolve the tier through the registry; refresh it per its
protocol (`cmd --list-models`, `opencode models`, `agy models`).

## Delegation Shapes And Stops

Good shapes: scout-before-implementer, parallel independent lanes, verifier
lanes, and long-run monitors that write durable reports.

Do not delegate when:

- The task is smaller than the prompt needed to explain it.
- The worker would need the whole conversation or broad repo context.
- Multiple workers would read/edit the same files without a handoff protocol.
- The result would be uninspectable prose instead of files, tests, logs, or
  artifacts.
- The main risk is product judgment, security judgment, or acceptance quality.

## Canon And Representative-Example Gate

Before briefing a worker, read the smallest real source-of-truth seam: the
schema or contract, validator, producer and consumer, plus one minimal fixture.
One file is partial canon, not enough evidence for a cross-system change.

For judgment-heavy or repeated work, inspect or run one representative real
example before scaling. If a real sample is unavailable, label the brief as a
hypothesis and make the worker's first deliverable a bounded sample plus
verification evidence. Do not dispatch a full batch from an imagined example.

## Prompt Contract

Every delegated worker gets:

```text
Scope: exact repo/worktree and files or subsystem.
Task: bounded goal.
Forbidden: no destructive git, no live/paid providers, no unrelated files.
Output: result file or compact final with status/evidence/commands/risks.
Verification: exact commands or artifacts to inspect.
Budget: do not print full logs, diffs, prompts, or long reasoning.
```

Prefer one coherent bounded prompt over many tiny prompts.

## Acceptance

Worker output is not fact. Accept only after checking:

- current files or diff;
- targeted tests, logs, or artifacts;
- whether the production consumer reads the changed path;
- whether residual risk is stated accurately.

If evidence is missing, mark the lane `attempted_no_evidence` and do not use it
as support for a done claim.

Keep chat cheap: one compact launch line per batch, progress only when blocked
or changing plan, and finals limited to status, paths, evidence, and risks. Put
details in result files, task ledgers, or local reports.
