# Agent State Contract Standard

**Класс:** method
**Название:** State + Task/Result Contracts for Cursor Agent Work
**Дата создания:** 2026-06-19

## Фундаментальное правило

For long-running or multi-agent work, keep orchestration state in files, not in
chat memory. The agent may use prose for explanation, but allowed actions,
blockers, tasks, and worker results must be machine-readable and reviewable.

## Problem This Solves

- The user rewrites a large prompt every run.
- Agents re-read stale context and overclaim progress.
- Workers receive long prompt dumps instead of bounded tasks.
- "Done" is reported from agent confidence instead of evidence.
- Expensive reasoning modes run always-on instead of by trigger.

## Minimal File Layout

Use this layout in any large project:

```text
agent/
  state.yaml
  tasks/
    README.md
    <task-id>.yaml
    <task-id>-result.yaml
    templates/
      task.yaml
      result.yaml
```

For small projects, use only `agent/state.yaml` and one task/result pair.

Canonical copyable templates:
`_agent_shared/templates/agent-state-contract/`.

## `state.yaml` Contract

`state.yaml` answers: "what is true enough to route work right now?"

Required fields:

```yaml
version: project.agent_state.v1
updated_at: "YYYY-MM-DD"
phase: current_phase

source_of_truth:
  project_rules: ./AGENTS.md
  task_contracts_dir: ./agent/tasks

allowed_actions:
  - read_source
  - run_local_test
  - write_task_contract
  - update_state

blocked_actions:
  - id: no_publish_without_review
    actions: [publish_claim, live_deploy]
    until: owner_review_recorded
    evidence: ./agent/state.yaml

active_task_contracts:
  - ./agent/tasks/example-task.yaml
```

Rules:

- `allowed_actions` and `blocked_actions` are gates, not suggestions.
- State can route or block work, but never proves acceptance by itself.
- Every blocker needs `until` and `evidence`.
- Keep counts and status summaries compact; link detailed reports.

## Task Contract

`tasks/<id>.yaml` answers: "what exactly should one worker do?"

Required fields:

```yaml
version: project.task_contract.v1
id: example-task
status: ready
created_at: "YYYY-MM-DD"
goal: "One bounded outcome."
recommended_worker: cursor_agent
worktree: /absolute/or/project/path

source_of_truth:
  - ./AGENTS.md
  - ./agent/state.yaml
  - ./relevant/report/or/spec.md

scope:
  intent: implement_or_verify
  may_modify_files: true
  files_to_read: []
  files_to_modify: []
  commands_to_consider: []

forbidden_actions:
  - commit
  - push
  - destructive_git
  - live_external_call

acceptance:
  - "Exact evidence required before PASS."

result_schema: ./agent/tasks/templates/result.yaml
```

Rules:

- One task contract = one bounded outcome.
- Give paths, commands, acceptance, and forbidden actions.
- Do not paste full logs, full backlogs, or full diffs into the prompt.
- If the worker may edit files, list the allowed area.
- If the task is verifier-only, set `may_modify_files: false`.

## Result Contract

`tasks/<id>-result.yaml` answers: "what happened, and what evidence supports it?"

Required fields:

```yaml
version: project.task_result.v1
task_id: example-task
status: pass_or_fail_or_partial_or_blocked
completed_at: "YYYY-MM-DDTHH:MM:SSZ"
worker: cursor_agent
summary: "One concise sentence."
changed_files: []
tests:
  - command: "exact command"
    result: pass_or_fail_or_not_run
    evidence: "short output or artifact path"
verified_findings: []
attempted_falsification: []
artifacts: []
residual_blockers: []
state_updates_recommended: []
next_action: accept_or_retry_or_block_or_launch_next_task
```

Rules:

- Transport success is not evidence.
- A worker verdict is not final until the orchestrator spot-checks risk-scaled
  evidence: files, commands, artifacts, reports, or tests.
- Missing evidence becomes `partial` or `blocked`, not `pass`.

## Triggered Reasoning Modes

Do not run heavy reasoning always-on. Put triggers in the task or state:

```yaml
thinking_gates:
  before_acceptance: [falsify]
  before_architecture_change: [fusion_review]
  after_repeated_failure: [root_cause, circuit_breaker]
```

Use:

- `falsify` before accepting claims, readiness, publish, or worker PASS.
- `fusion_review` for architecture choices with 2+ viable options.
- `root_cause` after repeated failures or contradictory evidence.
- `circuit_breaker` when the same fix attempt fails 3 times.

## Cursor Prompt Pattern

For the orchestrator:

```text
Read project rules, then ./agent/state.yaml.
Execute active task contracts from state.yaml.
Use task/result files for workers.
Do not perform blocked actions.
Spot-check evidence before updating state or claiming done.
```

For a worker:

```text
Read and execute this task contract:
./agent/tasks/<task-id>.yaml

Write the result YAML requested by the contract.
Do not perform forbidden actions.
```

## Adoption Guide

1. Add `agent/state.yaml` with only current phase, gates, and active tasks.
2. Copy templates from `_agent_shared/templates/agent-state-contract/`.
3. Convert the next real unit of work into one `tasks/<id>.yaml`.
4. Run one worker against the contract.
5. Review its result, spot-check evidence, and update state.
6. Only then scale to multiple workers or projects.

## Anti-Patterns

- A huge daily prompt that mixes identity, state, tasks, and blockers.
- A lead agent that only relays text between orchestrator and worker.
- Worker prompts that include full backlog/log/diff dumps.
- Accepting `done` without tests, artifacts, or falsification.
- Moving every small project to this system without long-running state.

## Cross-References

- `_agent_shared/rules/agent-state-contracts.mdc`
- `_agent_shared/rules/core-plan.mdc`
- `_agent_shared/rules/core-check.mdc`
- `_agent_shared/rules/circuit-breaker.mdc`
- `_agent_shared/standards/root-cause-analysis-standard.md`

## История изменений

| Дата | Изменение | Причина |
|------|-----------|---------|
| 2026-06-19 | Создание стандарта | Promote Nikita state/task/result contract pattern into Cursor shared rules. |
