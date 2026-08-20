---
name: agent-orchestrator-standard
description: 'Use when coordinating delegated lanes, worktrees, integration, or long-run monitoring; not for direct one-session work. Triggers: "оркеструй работу", "разложи задачи по worktree", "запусти волну агентов и следи", "orchestrate lanes", "monitor the workers and integrate". NOT for: выбор канала/тира модели и цена делегирования (/cost-aware-delegation), один исполнитель с брифом и приёмкой (/delegate), автономное закрытие цели волнами по контракту (/goal-king), прямая правка в этой же сессии (/go).'
---

# Agent Orchestrator Standard

Use this skill when the user wants Codex to coordinate work, not merely implement a single change. Treat Codex as the control plane: discover state, split work, launch agents, verify results, integrate, and keep the user informed with compact checkpoints.

## Project Intake

Before launching work, establish project facts from disk:

1. Identify roots:
   ```bash
   pwd
   git rev-parse --show-toplevel
   git status --short --branch
   git log --oneline -8
   ```
2. List worktrees:
   ```bash
   git worktree list --porcelain
   ```
3. Check active agents/sessions when herdr is available:
   ```bash
   herdr agent list
   ```
4. Locate backlog/issue sources:
   ```bash
   rg -n "backlog|todo|roadmap|issue|status|priority" docs .github README* -S
   ```
5. Locate validation commands:
   ```bash
   ls
   rg -n "pytest|ruff|eslint|vitest|jest|cargo test|go test|pnpm|npm test|make test|pre-commit" pyproject.toml package.json Makefile Cargo.toml go.mod .github -S
   ```

Report a short state checkpoint: branch, dirty files, active agents, likely backlog source, validation commands, and proposed next action.

## Operating Principles

- Prefer delegated worker lanes for implementation when there are multiple independent tasks.
- Use Codex for orchestration, prompt design, diff review, local verification, integration, and final reporting.
- Create worker lanes yourself when useful. Do not wait for the user to create Cursor/Claude/AntiGravity sessions if local tools exist and the requested work benefits from delegation. Treat `cmd` (Command Code) with any model tier as an internal Codex worker lane, not an external agent.
- Select worker/model by expected value, not habit: choose the cheapest option
  likely to produce verified evidence, and escalate only when ambiguity, risk,
  or expected rework cost justifies it.
- Ask the user only before live/paid/destructive work, protected remote pushes, or ambiguous product decisions. Agent/worktree creation is normal orchestration work.
- Do not trust memory or prior summaries; verify current files and git state.
- Do not give two agents the same files unless explicitly coordinating a handoff.
- Use isolated worktrees for implementation waves.
- Keep scopes larger when independent and well bounded; keep scopes narrow when files or behavior overlap.
- Do not run costly/live/destructive operations unless the user explicitly allowed them.
- A missing process environment variable means `not_loaded`, not `missing`.
  When the current task authorizes credential inspection, check configured
  sources without printing values and classify the state as `not_loaded`,
  `missing`, `invalid`, or `quota_exhausted` before declaring a blocker.
- Do not declare done until code, tests, and backlog/issue state agree, or blockers are explicitly listed.
- When a repository provides a project-local orchestration or goal-prompt
  standard, treat this skill as the universal base and load the project-local
  standard for domain-specific paths, budgets, gates, and output files.

## Worktree Standard

Create a separate worktree for each implementation wave:

```bash
git worktree add <absolute-worktree-path> -b <branch-name> <base-branch>
```

Use branch names that encode the wave:

```text
feat/<area>-<ticket-or-wave>
fix/<area>-<bug>
sync/<area>-backlog-trim
analysis/<area>-audit
```

After a wave is merged/integrated and the worktree is clean:

```bash
git worktree remove <absolute-worktree-path>
```

Never remove a dirty worktree without inspecting the changes and confirming they are merged or disposable scratch.

## Agent Launching

The orchestrator may create and close herdr agents, create isolated worktrees,
and hand work to internal Command Code/Codex workers, OpenCode, or
Cursor/Claude/AntiGravity without further confirmation when the requested work
benefits from delegation. Ask only before live/paid/destructive actions,
protected pushes, or ambiguous product decisions.

Delegation is not automatically cheaper than direct work. Use it when
parallelism, independent review, isolation, or risk reduction beats prompt and
acceptance overhead. Prefer one coherent lane over many tiny prompts.
Prefer Herdr launch for Cursor and interactive AGY so the session has inspectable
status, output, and a pane that can be closed after acceptance or blocker capture.

Bound every worker:

- exact worktree/repo path and scope;
- exemplar of the expected output built on 1 real input (few-shot; brief order:
  exemplar -> prohibitions -> task -> acceptance). Cannot build the exemplar =
  do not delegate yet;
- forbidden actions;
- expected output file or compact final;
- validation commands;
- pizdezh/evidence check before final;
- no full logs, broad diffs, or repo-wide dumps unless blocked.

## Cost-Aware Routing

Use the cheapest capable lane that can leave inspectable evidence. Escalate only
when ambiguity, risk, conflict, or expected rework cost justifies it.
Choose transport first, model tier second: `cmd` for bounded reports/patches,
OpenCode for free/Go provider lanes, Cursor for narrow implementation, AGY for
verification, and Claude/Codex Goal workers for coherent high-ownership phases.
Route by capability tier (T0 scout / T1 implementer / T2 specialist), never by
hardcoded model name; the current tier→model mapping lives in
`cost-aware-delegation/references/capability-registry.md`.

Default routing:

- Direct Codex work: tiny edits, short answers, local commands, obvious 1-2
  file changes, or anything where delegation overhead exceeds the task.
- Low/cheap scout: repo search, long reading, log/report summarization,
  consumer mapping, test discovery, issue triage, low-risk audits, repeated
  mechanical checks, and evidence maps.
- Medium implementer/verifier: bounded multi-file patches, known failing tests,
  narrow production wiring, ordinary feature/fix lanes with clear validation,
  and independent verifier passes.
- High specialist/orchestrator: architecture decisions, conflicting findings,
  ambiguous root cause, shared-contract changes, security/release/provider risk,
  long-context synthesis, final integration, and acceptance responsibility.

For large or unclear work, prefer scout-before-implementer: send a cheap/medium
worker to produce a compact map of files, consumers, tests, likely fixes, and
evidence before spending high-model tokens on decisions. Do not split into many
tiny scouts; one coherent bounded lane is usually cheaper than several prompts
plus several acceptance passes.

Before launching, hold a quick budget check:

- direct_cost: can the orchestrator finish in 10-15 minutes with small context?
- delegation_overhead: prompt, context transfer, wait, review, integration;
- risk_cost: cost of accepting a wrong cheap answer or needing rework.

Delegate only when expected saved high-model work exceeds overhead and risk.
Record detailed evidence in result files or worker finals; keep chat compact.

## Chat Budget

Do not turn delegation into a chat transcript. The user wants decisions and
blockers, not worker prompts, logs, or routine polling.

Default chat limits:

- launch/progress: no partial results; only the host-mandated lifecycle signal,
  a blocker, or a plan change, in English and max 2 lines per batch;
- unblock request: max 5 lines with exact blocker and next action;
- owner final: Russian unless requested otherwise; max 12 lines for done/partial,
  max 20 lines if blocked;
- never paste full prompts, worker transcripts, diffs, or test logs unless the
  user explicitly asks.

Write detail to result files, task ledgers, or `/tmp` logs. In chat, report only
agent name, scope, status, evidence path, blocker, and next decision.
Set the smallest practical output cap; keep long waits in a separate monitor task.
Filter command output before it enters model context: scoped `rg`, `jq`
projection, targeted tails, and bounded tool output; widen only when blocked.

## Agent Reference Cards

Load exactly the card needed for the transport you are about to use:

- `references/agent-cursor.md`: Cursor Composer/Agent implementation lanes.
- `references/agent-claude-code.md`: Claude Code Goal Mode/lane manager.
- `references/agent-command-code.md`: `cmd` / Command Code workers and model routing.
- `references/agent-opencode.md`: OpenCode workers and provider/model routing.
- `references/agent-antigravity.md`: AGY/Gemini verification and backlog analysis.
- `references/agent-codex-goal-worker.md`: Codex Goal Mode worker prompts.

For project-specific repositories, apply the local project overlay after the
universal card. Example: Nikita uses its own skill for state files, provider
gates, backlog semantics, and known failure modes.

## Monitor Cadence

Use event-driven handoff, not timed polling loops:

1. Dispatch the lane and prove its state is `working` once.
2. End the controller turn; do not monitor in-turn.
3. On a scheduled wake, read only the compact contract delta and
   `BLOCKED-*` files; no blocker means sleep again.
4. If a blocker exists, inspect the bounded artifact, send one narrow unblock
   prompt, or switch route. If done, inspect the final diff and run acceptance.

`sleep 300; herdr agent list` and all timed polling loops are forbidden.
Prefer durable result files over logs; print only their path and compact status.

## Validation Matrix

Infer project commands from local files. Examples:

Python:

```bash
git diff --check
python3 -m pytest <targeted-tests> -q
ruff check <changed-python-files>
python3 -m json.tool <changed-json-file> >/dev/null
```

Node:

```bash
git diff --check
npm test -- <targeted-tests>
npm run lint -- <changed-files>
npm run typecheck
```

Rust:

```bash
git diff --check
cargo test <targeted-tests>
cargo fmt --check
cargo clippy -- -D warnings
```

Go:

```bash
git diff --check
go test ./...
gofmt -w <changed-go-files>
```

Structured files:

- JSON: `python3 -m json.tool file.json >/dev/null`
- YAML: use the project parser if present, or a local validation command.
- Markdown tables/backlogs: run the project sync/validation script if present.

Do not run language linters on file types they do not support.

Run full test suites at integration checkpoints or before reporting a broad wave as stable. Prefer targeted tests for per-wave acceptance.

For a check whose measured runtime exceeds two minutes, make the first launch
durable: write stdout/stderr to a named log and persist the exit code beside it.
Before any retry, inspect the PID, log progress, and exit marker. Never launch a
second copy while the first is alive. Run targeted tests after each patch and
the full suite once after the integrated wave, not once per micro-fix.

## Backlog / Issue Rules

First verify, then update status.

Mark done only when:

- the production path is wired, not just helper code;
- tests cover the behavior or a credible manual artifact proves it;
- backlog/issue text accurately describes residual risk;
- remaining work is truly live/paid/owner-gated, not missing implementation.

Keep open/partial when:

- the acceptance condition requires live proof not yet run;
- only one side of a producer/consumer contract exists;
- a feature is opt-in but no production path exercises it;
- local seams for named consumers are missing;
- tests prove only a narrower claim than the ticket makes.

When syncing backlog, add concise evidence such as commit, test file, command, and residual. Avoid rewriting unrelated backlog entries.

## Integration Procedure

After an agent finishes:

1. Read final report.
2. Inspect `git diff`.
3. Run targeted verification locally.
4. Run independent verifier for risky or user-visible changes.
5. Fix or send unblock prompt if verifier finds real issues.
6. Commit in the wave worktree if accepted.
7. Rebase on integration/base if needed.
8. Fast-forward merge when possible:
   ```bash
   git -C <integration-worktree> merge --ff-only <wave-branch>
   ```
9. Re-run targeted integration checks.
10. Remove clean worktree and close panes.

Do not push/merge to protected remotes unless the user explicitly asked.
If a worker is done or blocked and its report is already captured in files or no
report is needed, close the Herdr pane after inspecting the final output. Do not
leave completed Cursor/AGY panes around as pseudo-active blockers.

## Known Failure Modes

- Pasted agent prompts may sit at the shell/agent prompt without Enter.
- Claimed model names may not be available in local Claude Code.
- Verifiers can create scratch files.
- Green tests can mask wrong path layout; test realistic directories.
- A helper can be implemented but inert if no production caller reaches it.
- A backlog ticket can overclaim coverage; verify every named adapter/consumer.
- A full suite run by a worker lane can waste time; request targeted tests unless full suite is needed.
- Worktree collisions are easy when multiple agents share a repo; separate files and branches.
- Docs/backlog mirrors often drift; validate with project scripts before trusting either side.

## Cycle Report

After each cycle, report:

1. Agent/session status
2. Test/eval state
3. Integration changes
4. Backlog/issue delta
5. Next action: wait / unblock / launch / ask owner / stop

Keep it short and decision-oriented: default <=8 lines.
