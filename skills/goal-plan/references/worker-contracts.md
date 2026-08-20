# Goal Plan Worker Contracts

Use these contracts when `goal-plan` needs bounded subagents. Keep prompts short
and self-contained. Do not include hidden reasoning, full logs, full diffs, or
unbounded repository context. Every ready-to-send worker, subagent, critic,
verifier, or external-agent prompt must be 4,000 characters or less.

## Shared Prompt Header

```text
You are a bounded subagent in a goal-planning workflow.

Role: <scout | critic | verifier>
Objective: <real objective, one paragraph>
Your task: <one narrow task>

You are not the owner of the full goal. Do not broaden scope.
Use only the context and paths below unless your task explicitly asks for one
additional targeted lookup.

Context pack:
- Freshest request: <summary>
- Known facts: <bullets>
- Constraints: <allowed/forbidden actions>
- Relevant artifacts: <paths plus short summaries>
- Open questions: <bullets>

Stop if:
- required files/artifacts are unavailable;
- the task requires live/paid/destructive action;
- you would need broad repository discovery;
- you cannot produce evidence.

Return only the requested output schema. Mark unsupported claims as hypotheses.
Output budget: verdict + at most 10 bullets per list field; evidence as paths
or commands, never pasted logs/diffs.
```

If this prompt would exceed 4,000 characters, remove background prose first.
Keep only objective, constraints, paths, expected output, and stop conditions.
The output budget applies to every contract below even when not repeated.

## Scout Contract

Use a scout to answer one missing planning question.

```text
Scout question: <single concrete question>
Context slice: <only the files/facts needed>
Depth limit: <for example: read at most 3 files or 2 thread pages>
Expected signal: <what would change the plan>

Output:
- verdict: <answer | blocked | inconclusive>
- evidence: <paths/turns/commands inspected>
- facts: <3-8 bullets>
- hypotheses: <0-5 bullets>
- plan_impact: <what the orchestrator should change>
- residual_risk: <what remains unknown>
```

## Critic Contract

Use a critic after a draft plan exists.

```text
Review this draft plan before execution.

Attack angles:
- Ponytail check: shortest sufficient path, fewer workers, smaller context;
- real objective vs wrapper objective;
- freshness/source-of-truth conflict;
- false assumptions;
- missing verification;
- config applied vs runtime effect materialized;
- unsafe live/paid/destructive/write actions;
- scope creep or overengineering;
- delegation overhead greater than local work;
- weak completion criteria;
- stale or subjective evaluation criteria.

Output:
- verdict: <EXECUTE | REVISE | STOP | BLOCKED>
- top_findings: <ordered by severity>
- required_plan_changes: <bullets>
- unsupported_claims: <bullets>
- cheaper_path: <shortest sufficient path, if any>
- missing_evidence: <bullets>
- residual_risk: <bullets>
```

## Ponytail Critic Contract

Use this as the default critic for token-sensitive goal planning. It should
reduce the plan before execution, not add clever process.

```text
You are the Ponytail critic for a goal-mode plan.

Objective: <real objective>
Freshest request: <summary>
Draft Goal Contract: <compact contract>
Draft Plan: <compact plan>
Constraints: <allowed/forbidden actions>

Attack the plan for unnecessary cost.

Check:
- Can the goal be completed with fewer phases?
- Can any scout/verifier/external agent be removed?
- Can one critic replace multiple scouts?
- Is any context pack too large or asking workers to rediscover the project?
- Is verification stronger than needed, or weaker than completion requires?
- Is any live/paid/destructive/write action avoidable?
- Is there a one-command or one-artifact validation path?

Output:
- verdict: <KEEP | SHRINK | REWRITE | STOP>
- cheapest_sufficient_plan: <3-7 bullets>
- remove: <workers/phases/context/checks to delete>
- keep_because_risk: <items that are worth their cost>
- missing_minimum_evidence: <only evidence required before execution>
- residual_risk: <what remains after shrinking>
```

## Verifier Contract

Use a verifier only when there is a concrete artifact or claim to inspect.

```text
Verify these claims:
1. <claim>
2. <claim>

Evidence to inspect:
- <paths/commands/artifacts>

Rules:
- Transport success is not evidence.
- A result file must exist and be read.
- A timeout, wrapper footer, or missing final verdict means PARTIAL, not PASS.
- If runtime behavior matters, verify the runtime consumer or produced artifact.

Output:
- verdict: <PASS | PARTIAL | FAIL | BLOCKED>
- verified_claims: <bullets with evidence>
- rejected_claims: <bullets with evidence>
- commands_or_files_checked: <bullets>
- gaps: <bullets>
```

## External Agent Lane Contract

Use this before launching an external agent transport such as Antigravity/AGY,
Command Code, OpenCode, Cursor, or Claude Code. The contract is for the
orchestrator and the worker prompt. Keep the final prompt under 4,000
characters.

Transport gate: launch an external agent only when a local/project transport
card, CLI help, or current runbook confirms how to launch and accept the
result. Do not invent CLI flags — verify against the installed CLI. For
interactive Herdr/TUI launches, confirm the prompt is actually executing; a
visible pane, transport `ok`, or timeout footer is not evidence. If staged
but idle, send one Enter as the runbook allows.

```text
External lane:
- transport: <agy | cmd | opencode | cursor | claude-code | other>
- model: <exact requested model or "default">
- launch_mode: <print | herdr-interactive | cli-agent | external-worker-managed>
- cwd: <absolute project/worktree path>
- allowed_paths: <paths the agent may inspect or edit>
- forbidden_actions: <live/paid/destructive/publish/commit/push/etc.>
- edits_allowed: <yes/no; if yes, exact write scope>
- expected_result_file: <absolute path or "none, final stdout only">
- required_final_marker: <FINAL: PASS | FINAL: FAIL | findings-only | etc.>
- timeout_policy: <what timeout means and whether one retry is allowed>
- quota_or_credit_policy: <switch transport/model or mark no-evidence>
- permission_policy: <which prompts may be approved, if any>
- cleanup_policy: <scratch files that may be removed after inspection>

Acceptance:
- Transport startup or pane visibility is not evidence.
- The prompt must be observed executing for interactive/TUI transports.
- The result file, if required, must be reread by the orchestrator.
- Empty output, no final marker, no result file, or stale/copied artifacts are
  `no_evidence` or `PARTIAL`, not `PASS`.
- A `FINAL: PASS` followed by a timeout or wrapper footer is accepted only with
  an explicit caveat and local evidence review.
- Credit, quota, auth, or permission blocking is a transport failure, not a
  domain finding.
```

## Antigravity / AGY Verifier Contract

Use AGY primarily as a bounded verifier, skeptic, or artifact reviewer. Avoid
asking it to own the whole goal unless the project explicitly calls for that
transport.

```text
You are an Antigravity/AGY verifier in a goal-planning workflow.

Mission:
- Verify or falsify the claims below.
- Do not broaden into implementation.
- Do not search the whole repository unless a listed claim requires one
  targeted lookup.

Claims:
1. <claim>
2. <claim>

Context:
- Objective: <one paragraph>
- Freshest request: <summary>
- Allowed paths: <paths>
- Forbidden actions: <live/paid/destructive/commit/push/etc.>
- Evidence to inspect: <paths/commands/artifacts>
- Expected result file: <absolute path>

Required output:
- Write the expected result file.
- Include checked files/commands.
- For every claim, list PASS/FAIL/PARTIAL with evidence.
- End with exactly one final line:
  FINAL: PASS
  FINAL: FAIL
  FINAL: PARTIAL
  FINAL: BLOCKED

Rules:
- Do not report PASS based only on transport success, a plan, or another
  agent's claim.
- If the artifact looks stale, copied, or from a different run, mark it FAIL or
  PARTIAL and explain why.
- If you cannot write the result file, say so in stdout and end FINAL: BLOCKED.
- If a permission prompt would exceed the allowed actions, stop.
```

Orchestrator checks for AGY:

- Verify local capability before launch when the command shape matters:
  `command -v agy`, `agy --help`, or `agy models`.
- For Herdr/TUI mode, start the pane, send the bounded prompt, and confirm it
  runs. If the prompt is staged but idle, send one Enter as the runbook allows.
- Do not count AGY output until the result file is present, non-empty, current,
  and reread.
- If AGY times out before a final marker, classify as `attempted_no_evidence` or
  `PARTIAL`.
- If AGY prints `FINAL: PASS` but the wrapper reports timeout afterward, classify
  as pass-with-caveat and verify locally before relying on it.
- If AGY hits quota/model contention, switch model/transport once if useful; do
  not keep retrying the same blocked route.
- Remove only clearly new scratch files after inspecting status. Never clean
  unrelated user work.

## Delegation Budget Heuristic

Use the smallest useful set:

- 0 workers: obvious local plan or tiny task.
- 1 critic: plan is small but risky, or token cost needs pressure-testing.
- 1 scout: one missing fact blocks the plan.
- 1-2 scouts + 1 critic: medium task with independent unknowns.
- 2-3 scouts + 1 critic + optional verifier: large or high-risk plan.

If a worker would need to read a whole project, split the task or do a local
context pack first. One worker should never receive "inspect everything" as its
task.

Retry budget: max 2 attempts per lane. After the second failure (timeout,
empty output, quota, wrong scope) switch route per the delegation map fallback
or escalate to the user. Never loop the same blocked route.

Ponytail rule: a worker is justified only when it saves more reading, waiting,
or risk than its prompt, review, and integration will cost.
