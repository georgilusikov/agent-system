---
name: goal-plan
description: 'Use when a goal needs a Goal Contract and gates BEFORE multi-wave or delegated work: цель, состояние, ограничения, критерии завершения сведены в один проверяемый контракт. Triggers: "goal plan", "гоал план", "собери контракт цели", "гейты перед волнами агентов", "работа на несколько волн — что зафиксировать". NOT for: пошаговый TDD-план реализации по готовой спеке (/writing-plans), стратегический роадмап по релизам (/roadmap-planning), исполнение волн до цели (/goal-king), прямая задача в одну сессию (/go).'
---

# Goal Plan

Turn an objective into a compact, evidence-backed Goal Contract and plan.
Optimize for correctness, scope control, minimality, and token economy. The
default output is a plan, not implementation; execute only when explicitly
asked or the mode clearly requires it.

**Shared canon.** This one file is the single source of truth for Claude Code
and Codex (`~/.claude/skills/goal-plan/` is the real directory; the Codex path
is a symlink to it). Platform-specific mappings are marked inline as
*Claude Code primitives* / *Codex primitives* — everything else applies to both.
For plan step format use `writing-plans`; for parallel execution
`agent-orchestrator-standard`; for delegation prompts `delegate`.

## Core Rule

Compile the goal before planning it. "Read the objective file", "launch a
worker", "apply a patch", "enable a config" are not completion. Completion =
the real objective met and verified through the same consumer path the work
is meant to affect.

**State-change gate.** Before finalizing a plan, mentally remove every test,
check, report, review, critic, worker launch, and verification step. If the
real objective is not already true and no remaining action changes the real
consumer state, the plan is invalid. Add the single cheapest state-changing
action, then restore only the minimum proof needed.

## 0. Execution-mode decision

Choose the cheapest sufficient mode before writing the plan:

1. **Direct single-agent `/goal`** — default for 1–2 files or work under 1h **(Recommended)**.
2. **Mode C `decompose-fire-accept`** — 2–3 provably independent lanes.
3. **`goal-king`** — only multi-wave work, provider spend, or unknown seams.

Use Direct single-agent by default. Do not ask the owner to choose a mode unless
the choice materially changes `B`, scope, authority, cost, or elapsed time; if
it does, raise it as a plan-changing question (section 9).

## 1. Freshness Gate

Identify: newest user request; active goal/objective file; workspace root and
dirty state when relevant; project-local instructions (`CLAUDE.md`, `AGENTS.md`,
roadmap, task ledger, authoritative state/config); live/paid/destructive/write
permissions and explicit prohibitions. Check memory preflight per global
`CLAUDE.md`.

If the newest request, active goal, and authoritative state conflict — stop
and write a short reconciliation note before planning. A newer free-form note
does not silently override a machine-readable gate.

Before launch, read `.goal-king/capabilities.md` when present. If acceptance
depends on an unverified or dead capability, re-scope the goal or ask the
owner first; do not launch a partial goal on an unverified seam.

## 1A. Outcome framing of the request

Restate the goal as an end state before compiling it:

```
When {situation / trigger}, I want {change of state}; I do NOT want {negative outcome}.
```

An imperative verb in the request — "make", "build", "show" — flags task substitution:
it buys an artifact, not a result. "Build a landing page" is closed by a landing page;
"get sales" is closed by sales. Artifact shipped ≠ metric moved. The "do NOT want" line
is the checklist of what the plan must not forget and the earliest scope-creep cut
available. This is the owner-language form of `A → B` in section 2: same referent, one
stated as a sentence, one as a transition.

## 2. Real Objective

Separate wrapper goals ("read the objective file", "continue from this
handoff", "wake and check status") from the real objective. A wrapper is a
startup step only; never mark the goal complete after the wrapper is done.

Compile the transition internally before choosing actions:

1. `A`: current real consumer state.
2. `B`: smallest owner-useful observable state.
3. `change`: cheapest action that makes `B` true; tests and reviews do not
   substitute for this action unless the test/review artifact is itself B.
4. `proof`: cheapest observation that distinguishes `A` from `B` through the
   intended consumer.

For runtime incidents, `B` is corrected runtime behavior, not a passing test,
guardrail, alert, or documented contract. Those are proof or protection.
For requests shaped as "add tests/docs/checks so that X", `X` is `B`; the
requested artifact is proof or protection and cannot fill `change`.

Keep this internal when obvious. State `target B`, strongest verifiable
`this-run B`, and the remaining gap only when target B cannot be reached or
verified under current authority or time.

## 3. Ponytail Gate → FAST PATH

Run the ladder, take the FIRST rung that holds:

1. One-step local action is enough — no plan needed.
2. Needed context already in the thread/state file — short plan, no subagents.
3. One critic replaces several scouts.
4. One bounded scout answers the only missing fact.
5. Verification = one production-shaped command or artifact check.

**FAST PATH:** if rung 1–2 holds and no plan-changing question is open, output
only: real objective (1 line), forbidden actions/write scope (1 line), 3–7
plan steps, verification command/artifact, completion criterion, and
`Final gates: PASS; Goal questions: none.` Skip the full contract and
delegation map. Most goals should take this path.

## 4. Delegation Decision

Delegation-eligible shapes:

- 2+ independent lanes with non-overlapping files (parallel wall-clock win);
- long reads: mapping many files/consumers/tests to extract a few facts;
- mass repeatable checks: lint/test sweeps, grep-backed audits;
- research across docs, code history, or external sources;
- flake/debug loops needing many cheap repeated runs;
- independent critique/verification of an orchestrator-produced artifact.

These shapes still must pass the cost gate: delegate only when parallelism,
independent critique, or bounded fact-finding saves more than prompt + review
and integration cost. Otherwise state why delegation beats prompt + review +
integration cost.

Budget by scope: tiny → 0 workers; small-but-risky → 1 critic; unclear-but-
bounded → 1 scout; medium → 1 scout + 1 critic; large/high-risk → 2–3 scouts
+ 1 critic + optional verifier. **Max 2 attempts per lane**, then switch
route or escalate to the user — no silent retry loops.

Route by capability tier and effort class, never by hardcoded model name
(models change):

- `T0 low scout`: search, summaries, mechanical checks, evidence maps;
- `T1 medium implementer/verifier`: bounded patches, failing tests, verifier
  passes;
- `T2 strong specialist`: architecture, ambiguous root cause, disputed
  synthesis — only after cheaper lanes produced compact evidence.

Numeric routing scores (price/speed/quality/reliability per transport, incl.
codex/cursor/agy/gemini + verified launch flags):
`~/.codex/skills/cost-aware-delegation/references/capability-registry.md`
— read it before choosing an external transport; update the scores after any
dispatch with an unexpected result. Keep planning, state management, final
acceptance, and owner/live/paid decisions in the orchestrator. Choose transport
separately from model; a cheap model tier is not a transport.

**Claude Code primitives** (tier → agent, never hardcode model names):

- T0 scout → `Explore` agent, or `model: haiku`;
- T1 implementer/verifier → `general-purpose`, `model: sonnet`;
- T2 specialist → `model: opus`/default — only after cheaper lanes produced
  compact evidence;
- plan drafting → `Plan` agent.

Worker output ≠ fact: reread files/diffs/tests before accepting (multi-agent
audit rules in `CLAUDE.md`).

## 5. Context Pack (only when delegating)

Per worker: one question, one context slice, one output schema, explicit stop
conditions. Pass paths + short summaries, never full logs/diffs/backlogs.
Prompt ≤ 4000 chars; worker output capped by schema (verdict + ≤10 bullets +
evidence as paths). Exact prompt contracts, external-agent lane rules, and
AGY/transport acceptance: `references/worker-contracts.md`.

**Sealed critic.** For an independent critic, pass only the original objective,
final plan, and source/evidence paths. Omit planner rationale and other critics'
findings unless the task is explicitly a synthesis pass.

## 5A. Mode C — decompose-fire-accept

Use only after the owner explicitly selects Mode C or the final goal questions
resolve a material mode trade-off in its favor.

1. **Scout (T0)** maps seams, consumers, tests, and exclusive file ownership
   before slicing. Decomposition without scout evidence is forbidden.
2. **Decompose (T2 judgment)** writes `backlog-<lane>.md` for every worker with
   the task, exclusive file ownership, mechanical acceptance commands (pytest
   set, ruff, and grep markers), and the stop file `BLOCKED-<lane>.md`. Never
   expose credential locations or values in worker prompts.
3. **Fire once; controller ends the turn.** In-turn monitoring and timed
   polling are forbidden.
4. **Scheduled wake:** every 30–60 minutes, pass compact context containing
   only the contract and delta; never pass full history. Read `BLOCKED-*` files
   only; if none exist, sleep again.
5. **Final acceptance (orchestrator; T2 judgment when required):** run one
   mechanical batch per lane and one integration gate. Worker self-reports are
   never verification.

## 6. Goal Contract

**Lite** (default — no delegation, no external agents):

- `real_objective`, `current_state`, `state_change`, `forbidden_actions`,
  `allowed_write_scope`, `verification_path`, `completion_criteria`.

**Full** (only when delegating or using external agents, add):

- `freshest_request`, `authoritative_sources`, `delegation_map`,
  `delegation_budget` (incl. max attempts), `worker_contracts`,
  `external_agent_lanes` + `transport_acceptance_rules`,
  `critic_attack_angles`, `stop_conditions`, `residual_risks`.

Omit fields that do not apply; never fill a field with ceremony.

Delegation map entry: unit, route (tier + effort class + transport), why (saved
reading/risk/wall-clock), allowed_paths, edits_allowed, expected_artifact,
validation, acceptance (what the orchestrator must reread or run), fallback
with an observed trigger. Never "always launch" — "eligible by cached registry"
with a fallback.

Every plan starts with this structural slot, then ordered phases with purpose,
actions, evidence expected, validation, and stop/fallback condition:

```text
STATE TRANSITION
- A: <current consumer state>
- B: <owner-useful observable state>
- Change: <cheapest non-proof action that makes B true>
- Proof: <cheapest consumer observation distinguishing A from B>
```

`Change` must also appear as an action in the plan. A test, report, review,
critic, worker launch, alert, or gate cannot fill it unless that artifact is
the requested product.

**Persist (Goal/GoalKing launch prep):** when preparing a Goal or GoalKing
run, write the contract to `.goal-king/contract.md` (project root; ensure
`.goal-king/` is gitignored) and return the file path + a 3-line launch
prompt referencing it. Never paste the full contract into the launch prompt
or into continuations — path + decision deltas only. goal-plan produces the
contract; it does not execute the work.

## 7. Acceptance Gate

A plan is acceptable only if: it answers the real objective, not the wrapper;
facts and assumptions are separated; write/live/paid/destructive boundaries
are explicit; the Ponytail gate names the cheapest sufficient path;
delegation is justified and owner/final-acceptance work stays local; worker
prompts are bounded with non-overlapping scopes; every important claim has a
source or is marked a hypothesis; verification checks the runtime consumer or
final artifact; completion criteria are stronger than "command succeeded" or
"worker said OK"; residual risk is explicit.

Before finalizing a non-trivial plan, scan `references/failure-modes.md`
(also the critic's default attack checklist).

End every non-FAST-PATH draft with this compact gate summary; do not create a
separate artifact:

```text
FINAL GATES
- Point B coverage: PASS|FAIL — draft names an owner-visible observable state
- State-change coverage: PASS|FAIL — draft includes a non-proof action making B true, or B is already true
- Minimality: PASS|FAIL — no action can be removed without losing change, proof, or safety
- Proof coverage: PASS|FAIL — draft includes consumer-path evidence distinguishing A from B
- Authority: PASS|FAIL — write/live/paid/destructive boundaries are respected
- Goal clarity: PASS|WAITING — no open plan-changing question, or questions follow
```

Any `FAIL` requires revision before presentation. `WAITING` allows a draft but
forbids execution, dispatch, or a completion claim until the answers are
incorporated.

**Outcome verify (optional final step, large goals):** after N days a
scheduled task or reminder checks whether the result is actually used. Not
used → open a new bead/task with a hypothesis why.

## 8. Plan Challenge (anti-bias + pre-mortem)

Before presenting a non-trivial plan (skip on FAST PATH):

1. Anti-bias on the chosen approach: name 1-2 rejected alternatives and the
   one-line reason each lost. No alternatives considered = red flag, go back.
2. Pre-mortem: list the top-3 assumptions the plan dies without; for each,
   the cheapest probe that would falsify it BEFORE heavy work starts.
   An assumption with no probe goes into residual_risks.

## 8A. Plan Critic Gate

Before presenting a non-FAST-PATH plan, run the `plan-critic` subagent (sealed
input per section 5: objective + draft plan + evidence paths only). It attacks
five lines — task substitution, unobservable step criteria, irreversible steps
without rollback, the first step that will fail, contradictions with accepted
decisions — and returns `## Возражения критика` + a verdict.

- `ADVISORY` — attach the objections section to the plan verbatim and present it.
- `BLOCK` (critical only: goal substituted / irreversible step without rollback /
  contradicts an owner decision or `ACCEPTED:` line) — revise the plan and rerun
  the critic. **Max 2 cycles**, then escalate to the owner with both positions.

**Hard fail:** a non-FAST-PATH plan presented without a plan-critic run is invalid.

## 9. Goal Questions

Ask 1–5 independent questions only when their answers can change `B`, scope,
done criterion, hard constraints, non-goals, or a priority trade-off. Execution
mode — one agent does the scoped work itself vs orchestrates/delegates — is
ALWAYS plan-changing when not explicit in the request: ask it, with your
recommendation. Already answered → don't re-ask. Nothing plan-changing → state
`GOAL QUESTIONS: no open questions — B and done criterion are explicit.`
Never ask for approval of the plan or invent ceremonial choices. Each question
carries your recommended answer.

```text
N. <question>
   Recommendation: <answer> (recommended)
   Plan impact: <what changes if the owner chooses differently>
```

**WHEN to ask — platform-dependent, because the mechanism differs:**

- *Claude Code primitives:* ask via the **AskUserQuestion tool, BEFORE** writing
  the contract, plan, or any worker prompt (after gates and scouting). The tool
  is interactive and visible; questions buried as text under an already-written
  plan do not get answered and the plan then silently rests on assumptions. The
  recommended answer is the FIRST option, marked "(Recommended)".
  **Hard fail:** any contract/plan/prompt text produced before the questions
  block (or an explicit "no open questions" line) on a non-FAST-PATH run.
- *Codex primitives (and any channel without an interactive ask tool):* put a
  visible `GOAL QUESTIONS` section **LAST**, after the draft and `FINAL GATES`,
  so the owner assesses the questions against a concrete draft.

Both ways: a draft with open questions labels `Goal clarity: WAITING` and is
**not** an execution authorization. Do not emit worker prompts, execute, or
dispatch until answers are incorporated. In a headless run, output the draft,
gates, and questions, then stop; owner silence is not consent.

## Output Style

FAST PATH goals: the 6-line block from section 3, nothing else.

Normal goals: 1. Goal Contract (lite or full); 2. Delegation Decision; 3. Draft
Plan; 4. Verification and stop conditions; 5. `FINAL GATES`; 6. `GOAL
QUESTIONS` (placement per section 9). If questions are open, stop. After answers
are incorporated, emit worker prompts if warranted (≤4000 chars each). If asked
to run subagents, spawn only the minimal bounded set and inspect outputs before
changing the plan.
