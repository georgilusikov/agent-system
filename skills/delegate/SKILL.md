---
name: delegate
description: 'Use when briefing ONE external executor and accepting its result (Codex, subagent, NLM). Triggers: "делегируй эту задачу", "делигируй" (частое написание владельца), "делегируй кодексу", "делегируй гроку", "отправь в codex", "поручи субагенту", "напиши бриф исполнителю", "brief an external executor". NOT for: lanes/worktrees/долгий мониторинг воркеров и волны 2+ агентов (/agent-orchestrator-standard), выбор канала и тира модели (/cost-aware-delegation), многоволновая автономия до цели (/goal-king), доделать самому в этой же сессии (/go).'
---

# Delegate — briefing an external executor

Execute protocol. The root cause of most failed delegations is not a stupid executor
but the briefing: partial canon, no reference output, unknown executor constraints, a
permission gate. This skill puts three gates BEFORE dispatch and one AFTER.

## Purpose (claim formats)

Reach for this skill once any of these has been said:
- `просто скинь ему задачу, он разберётся`
- `агент в goal-режиме ничего не сделал` (after the fact)
- `задача простая, бриф не нужен`
- `он же видел этот код раньше`

and the work must be delegated in a way that does not come back to be redone by hand.

## When to Use

- `делегируй X в Codex / agy / субагенту`
- `запусти headless прогон`
- `подготовь бриф для внешней модели`
- batch enqueue of tasks into the agent backlog

## When NOT to Use

- 1 file, 15 minutes of your own work → do it yourself; the briefing costs more than
  the task
- Parallelizing YOURSELF across worktrees → `rules/parallel-agents.md` (one packet =
  one worktree)
- A research question with no artifact → a plain subagent question; the full protocol
  is overkill

## Input checklist

- [ ] The task has a verifiable artifact (file, diff, report) — not "think about"
- [ ] The executor and the channel are known (CLI, MCP, backlog lane, API)
- [ ] There is 1 real input example to build the reference output on

## §0. State the task as an outcome (before Expected State)

Phrase the task to the executor as an **end state**, not as an action:

```
Когда {ситуация / триггер}, хочу {изменение состояния}; НЕ хочу {негативный outcome}.
```

**An imperative verb in the statement flags a substituted task.** "Make", "collect",
"show" buy an artifact, not a result: "make a landing page" is closed by a landing
page, "I want sales" by sales. The agent executes literally, so it will not catch the
substitution. Artifact created ≠ metric moved: there is a gap between output and
outcome, and all the work inside that gap is dead effort.

The `НЕ хочу` line is mandatory. It is both the checklist of what the executor must not
forget and the only thing that cuts scope creep before dispatch.

## §1. Expected State (before dispatch)

Write out 3-5 observable expectations: which files/lines/tests will exist on success,
and which command proves it. Written BEFORE dispatch — otherwise you will accept any
result as "fine".

## §2. Gate 1 — read-before-delegate (domain canon)

Read EVERY canon file of the domain yourself: schema + validator + extractor/scripts +
2-3 samples from the data. One file is partial canon: `SKILL.md` without
`extract.py`/`validators/` is a missed rule, and the executor will break it. Whatever
you did not read will not reach the brief, and the executor will reconstruct the
semantics from ITS training, not yours.

## §3. Gate 2 — expected output FIRST (reference)

Before the call, write the reference result for 1 real example by hand. Include it in
the brief as a few-shot. The brief's structure is strictly:
**reference → prohibitions → task**. If you cannot build the reference yourself, you do
not understand the task and it is too early to delegate.

## §4. Gate 3 — executor constraints (preflight)

| Check | How | Typical failure |
|---|---|---|
| Write/edit permissions | test task or a flag (`--full-auto`, permission mode) | "goal-режим ничего не сделал" = permission gate |
| Workdir / context | where the task actually runs | a backlog lane runs in the agent's own window, not an arbitrary dir |
| Runtime on the target machine | `python3 --version` on target | `X \| None` fails on Python < 3.10 |
| Executor health | probe request before batch dispatch | degraded language server, hung auth |
| Executor's role | what it can actually do | Codex is a reviewer, not a coder: review yes, feature no |

Batch enqueue ONLY after one test task has succeeded through the same channel.

### Channel routing

The canon of channels and models is
`~/.codex/skills/cost-aware-delegation/references/capability-registry.md`
(tiers T0/T1/T2, prices, roles, verified launch flags, nested subagents). Channel
details live in the cards
`~/.codex/skills/agent-orchestrator-standard/references/agent-*.md`
(cursor, antigravity, opencode, claude-code, cmd, codex-goal-worker). Read them BEFORE
picking a lane.

- **External-first (already paid for by subscription):** cursor-agent, grok-build, agy
  (opus/sonnet — bounded code, flash — media/review, NOT codegen), OpenCode.
  The Codex quota (terra/sol/luna) is a fallback only.
- A subagent inside Claude Code = the Agent tool: `Explore` = T0 scout,
  `general-purpose` = T1, model `haiku|sonnet|opus` = T0/T1/T2.
- Model names come ONLY from the registry or the channel's live list (`grok models`,
  `agy models`, `cursor-agent models`). A name from memory is stale by design
  (case 2026-07-09: `gemini -m gemini-2.5-flash` recalled from training — it failed).

## §5. The brief (template)

Section keywords stay in Russian on purpose: the gate below greps them, and briefs
already in flight use them.

```
КОНТЕКСТ: {2-4 строки: система, цель, границы}
ШАГ 0: {команда, которой исполнитель ПЕРВЫМ делом проверяет, что гэп ещё существует
        (дубль не появился, фикс не смержен) — иначе качественная работа над мёртвой задачей}
ЭТАЛОН: {готовый пример результата на 1 реальном входе}
ЗАПРЕТЫ: {3-7 конкретных: форматы, файлы-не-трогать, no _fixed/_final, no новых файлов}
ЗАДАЧА: {императив + список входов + куда положить результат}
ПОТРЕБИТЕЛЬ: {кто/что читает артефакт — программа, гейт, человек. Нет потребителя = отчёт ради отчёта}
ЧЕКПОИНТ: {первый малый артефакт на ~10-15% бюджета (skeleton, 1 пример) — куда положить.
           «Свернул не туда» ловится здесь за копейки, на финальной приёмке — за полную цену}
STOP-ФОРМА: {заблокировался → файл с перечнем ПРОВЕРЕННЫХ мест (для ключей: сначала grep .env),
             не молчаливый обход и не «недоступно»}
ACCEPTANCE: {команда/grep, которой результат будет проверен}
АНОНС ФОРМЫ: {исполнитель ДО первого действия отвечает списком секций/таблиц/файлов,
             которые выдаст — 3-7 строк, без работы}
ФОРМАТ ОТЧЁТА: {таблица-строка на задачу: JTBD | Моя выгода | Статус | Что сделано |
             Доказательство | Следующий шаг}
```

**The executor's report format (six columns, Krasinsky's board).** Two columns carry the
weight. "Моя выгода" — what the owner gets, not what was done (empty, or a restatement
of "what was done", flags an outcome→output substitution). "Доказательство" — a machine
check, not a claim: the command plus its output (detail level, for example:
`Playwright 1600×900: bounds_fail=[], console_errors=0`). "Done" without a command in
the evidence column is NOT CHECKED at acceptance §7.

**Expected output announce (a mandatory line of the brief).** The executor must declare
the expected shape of the result (sections, tables, file paths) BEFORE its first action.
This is a cheap check that the brief was understood, and it costs one round instead of
the whole budget. A final result that diverges from the announcement is a flag for
acceptance §7: if they diverge, find out what the executor understood differently before
accepting the artifact. Pattern source: jtbd-scenarium-tracker + META "Expected State
FIRST".

**Brief ceiling: ≤300 lines, target size 80-160.** Over the ceiling — replace file
contents with paths, command output with a one-line result, and the history of attempts
with a list of "what was rejected and why". A long brief is not more informative:
context-sensitive channels degrade with size (the Grok trap below), and you pay for the
volume on every round.

A deterministic gate BEFORE dispatch — not "try to keep it short":

```bash
[ "$(wc -l < brief.md)" -le 300 ] && grep -q ЭТАЛОН brief.md && grep -q ACCEPTANCE brief.md
```

## §6. Dispatch (the call itself)

A written brief ≠ a delegated task. Make the call and record in the report: the channel,
the exact command, wall-time.

- The command comes from the registry §Verified launch flags or the channel card.
  Do not improvise flags from memory.
- **Observability through herdr (optional; recommended for long, interactive and write
  tasks — you can see what the agent is actually doing):**
  ```bash
  herdr agent start <name> --cwd <worktree> -- <cli + флаги из registry>
  herdr agent read <name> --source recent-unwrapped --lines 80 --format text  # что делает сейчас
  herdr agent wait <name> --status idle --timeout <ms>   # ожидание вместо поллинга
  herdr agent list                                        # все активные агенты
  ```
  Codex standard: cursor-agent and interactive AGY preferably run through herdr (a live
  pane: status, output, closing after acceptance).
- A short one-shot (`gemini -p`, `codex exec` with a bounded brief) can skip herdr;
  send the output to a file, not into the transcript.

## §7. Post-verify (after completion)

- The executor's self-report ("done", "готово", a green runner status) is a claim, not a
  fact. A formal FAIL (timeout) is likewise ≠ a real FAIL. Verify through the files:
  `ls`, `grep`, `pytest`, diff against the §3 reference.
- Run the acceptance command from §5 yourself.
- Walk the fraud checklist `~/.claude/skills/check/references/fraud-table.md`:
  first `git diff -- '*test*'` (weakened asserts / mocked goals are #1 by frequency),
  then false completeness, scope creep, betrayal of the spec.
- A wiring task → read the runtime consumer: does it read EXACTLY the field/artifact that
  was written? Writing to a field the consumer ignores is inert wiring with green tests.
- A divergence from the reference → do NOT fix it silently by hand: fix the brief and
  re-run. A manual fix means the executor learned nothing and the next delegation repeats
  the mistake.
- The acceptance verdict → a row in `references/executor-track-record.md` (executor ×
  task class × whether its claims held). The log calibrates the DEPTH of re-checking:
  a clean track record → spot-check 2-3 claims; a dirty one → full check. The asymmetry
  always holds: negative results are cheap to believe, positive ones must be verified.
- Owner-effort scale 0-100: any click by the owner is at least 50; 0 only when the agent
  does everything itself; +50 if the table needs a legend or glossary; +100 for a trust
  failure.
- Final acceptance digest: `next action | усилие 0-100 | что агент может сделать сам`.

## Definition of Done

- [ ] §1 Expected State written BEFORE dispatch
- [ ] Domain canon read in full (list the files in the brief or in the report)
- [ ] The brief contains a reference built on a real example
- [ ] Preflight §4 passed (for a new channel — a test task)
- [ ] Dispatch §6 done: channel + command (+wall-time) in the report; lane and model
      from the capability registry, not from memory
- [ ] The §5 acceptance command was run AFTER completion, result in the report
- [ ] Brief ≤300 lines (the §5 gate ran BEFORE dispatch)
- [ ] Runnable test: `[ "$(wc -l < brief.md)" -le 300 ] && grep -q "ЭТАЛОН" brief.md && grep -q "ACCEPTANCE" brief.md`

## Known traps

- **Permission gate:** an agent in goal mode "did nothing" — not stupidity but missing
  write permissions → guard: §4 row 1, a test task before the batch
- **One file = partial canon:** delegating from SKILL.md without the validators → the
  executor broke an invisible rule → guard: §2, read schema + validator + samples
- **No reference:** the executor reconstructed the semantics from its own training → a
  foreign format → guard: §3, a reference in every brief
- **Degraded executor:** a hang was written off as "a hard task", models and accounts were
  swapped — the cause was the language server → guard: §4 health probe + restart the
  channel before swapping models
- **Batch ETA from your head:** measure 1-2 tasks through the channel and multiply → the
  §4 test task also gives you the timing
- **Brief without dispatch:** the brief was written, the call never made ("агент не
  вызвался") → guard: §6, dispatch with the command in the report, an item in the DoD
- **Flags/model from memory:** improvising a CLI call from training → a failed call →
  guard: §4 routing + §6, the command only from the registry or the channel card
- **Grok CLI (a context-sensitive external channel):** bundle limit ~52MB plus heavy
  degradation with prompt size.
  - Never paste previous logs or outputs into the prompt.
  - Write the task to a file and `cat /tmp/task.md`.
  - Use `--max-turns 60+` (20 is almost always too few).
  - Mandatory preflight: a tiny test task before the big one.
  - Details and templates:
  - `~/.claude/memory/headless-agent-dispatch-cheatsheet.md` (Grok traps + herdr)
  - `~/.claude/skills/delegate/references/grok-dispatch.md` (full guide + brief examples)

## Related skills

- `/check` — verify the delegated artifact when the result is high-value
- `/prioritize` — WHAT to delegate first
- `rules/parallel-agents.md` — multi-agent parallelism across worktrees
- `~/.codex/skills/cost-aware-delegation/references/capability-registry.md` —
  the CANON of channels/models/flags (single source of truth)
- `~/.codex/skills/agent-orchestrator-standard/references/agent-*.md` — channel cards
- `~/.claude/memory/headless-agent-dispatch-cheatsheet.md` — Grok traps + herdr
  observability only

## FORBIDDEN

- Dispatch without a reference in the brief ("он поймёт по описанию")
- Batch enqueue without one test task through the same channel
- Accepting a self-reported "done" / a green runner status as verification
- Marking a delegation complete without running the acceptance command — and inventing
  its result (see `~/.claude/standards/no-fabricated-evidence.md`)
- Silently patching the result by hand instead of fixing the brief

## Hard fail

- A brief without the ЭТАЛОН and ACCEPTANCE sections → that is a wish, not a delegation
- "Готово" with the acceptance command unrun → false done
- Preflight skipped for a new channel or executor → the result is unpredictable by design
