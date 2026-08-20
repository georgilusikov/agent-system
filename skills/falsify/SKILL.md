---
name: falsify
description: 'Use when trying to DISPROVE a high-stakes readiness claim end-to-end. Triggers: "фальсифицируй", "falsify", "опровергни этот вывод", "prod readiness", "можно ли релизить". NOT for: обычная верификация результата против Expected State (/check), внешний второй взгляд чужой моделью (/bouncer), поиск первопричины конкретного падения (/debug).'
---

# Falsify Protocol — Pipeline Router

This skill is an **orchestrator**: it joins /check + /debug (both modes) into a single artifact ending in a Verdict. Use it when you need the whole picture in one pass rather than separate steps.

**Why it is a separate skill:**
- /check focuses on test cases + the Gap table (verification)
- /debug Mode L — one linear causal chain (5 Whys)
- /debug Mode H — ≥3 parallel hypotheses (Bayes table)
- /falsify assembles all of it into one Verdict for high-stakes decisions

**When NOT to call it:** ordinary artifact verification → `/check` is enough. A single-cause failure → `/debug` is cheaper.

## §0. Input Checklist

- [ ] There is a concrete claim to falsify (not an abstract goal)
- [ ] A source of truth is reachable (files, logs, data, commands) — not the agent's memory
- [ ] You can state ≥3 observable expectations BEFORE gathering facts
- [ ] The stakes are critical (otherwise use /check — cheaper)
- [ ] `~/.claude/memory/incidents/INDEX.md`, or the `~/.claude/memory/incidents/` folder, has been checked (for the §2 precedent scan)

Before falsifying — **run `/anti-bias` over your own expectations**. This is preprocessing: if the expectations are skewed, falsification will confirm the skew.

## §1. Expectations table (E-ID)

Minimum 3, maximum 7 expectations. Filled in **BEFORE** gathering facts (anti-postdiction).

| E-ID — название | Что должно быть истинно | Где подтверждать (SoT) | Next action if unmet | Effort (0-100) |
|---|---|---|---|---|
| E01 — {3-15 слов rus} | {observable, не интерпретация} | {файл/команда/лог} | {конкретный шаг, не «разобраться»} | 0=агент сам / 50+=владелец |
| E02 — ... | ... | ... | ... | ... |
| E03 — ... | ... | ... | ... | ... |

**Filling rules:**
- The ID always carries a label after ` — ` (3-15 words, in Russian). `E01` with no label is invalid
- Every expectation must pass the **camera test**: "could a camera record this?" If not, rephrase it or tag it `[I]/[S]/[A]`
- `Next action if unmet` is written BEFORE the check (anti-postdiction)
- Do not confuse an expectation with a goal. An expectation is an observable fact; a goal is what we want to reach.

## §2. Precedent scan + actual evidence

### §2.1 Precedent scan
```bash
ls ~/.claude/memory/incidents/ 2>/dev/null
test -f ~/.claude/memory/incidents/INDEX.md && sed -n '1,160p' ~/.claude/memory/incidents/INDEX.md
grep -ril "{ключевое слово темы}" ~/.claude/memory/incidents/ 2>/dev/null | head -5
```

Read whatever the scan finds. Similar symptoms are a **strong signal**: the mistake is recurring, so the current rules are weak. Account for that in §6 (strengthen the Design Injection rather than creating a new one).

If incidents are empty or the folder does not exist, say so explicitly: «Precedent scan: не найдено похожих incidents».
If the scan commands were never run, or `INDEX.md` was not read in this session, write `Precedent scan: NOT CHECKED`. Do not write "scan выполнен", "INDEX.md обнаружен", or the names of incidents from memory or guesswork.

### §2.2 Gather actual
For every E-ID from §1 — a **real observation** through Read/Grep/Bash. Not an assumption.

If the file/log/command was not actually read or run in this session:
- Actual = `NOT CHECKED`;
- severity is at least `medium` when the claim is high-stakes;
- confidence cannot exceed `60%`;
- the Verdict cannot be `PASS`.

Inventing logs, line numbers, counts, statuses, command output or file contents is forbidden. With no tool access the honest result is `PARTIAL / NEEDS EVIDENCE`, not a synthetic PASS/FAIL.

Follow `standards/no-fabricated-evidence.md`: user claim, prior memory, or skill template text are not observed evidence.

**Content-depth gate.** Actual must carry concrete values from the source, at least 3-5 per E-ID: test names and what each one checks, ids, hex/rgba, numbers, code quotes, record names. "62 теста прошли", "данные корректны", "конфиг на месте" are `NOT CHECKED`, not observations. A paraphrase cannot be falsified, so no verdict can rest on it.

### §2.3 Runtime Verification Gate (обязателен для claim про сервис, API, UI, pipeline, данные)

When the claim asserts a running service, a reachable API, a populated graph, loaded data, a passing pipeline or a UI that opens — run at least one check FROM RUNTIME **before** the §10 Verdict:

| Проверка | Инструмент |
|---|---|
| Открыть URL и прочитать ответ | Chrome MCP (`navigate` + `get_page_text`) |
| Вызвать endpoint и показать JSON | `curl`, или Chrome MCP `javascript_tool` с `fetch()` |
| Скриншот состояния | computer-use screenshot |
| Запустить скрипт и показать stdout | Bash |
| Перезапустить на изменённых данных и показать diff | любой из выше |

Evidence from a repo, a file or a config is **not enough** for a runtime claim: files being in place ≠ the service answering. If runtime is unreachable, state it in §1 as `Reality: runtime недоступен, причина X`, the verdict lines become FAIL or NEEDS EVIDENCE, and §3 must carry the line `G0N — runtime не проверен: {причина}`.

**Revalidation:** a previous run left artifacts and the current one changed them → checking that the files exist is not enough. Re-run the pipeline on NEW data and show that the result differs (or explain why it is identical). Without the re-run the verdict cannot be PASS.

*(RCA source: 2026-04-05 — the agent assembled the infrastructure, filled the expectations table and issued a verdict without ever opening the service or calling the API.)*

### §2.4 Copy-ready gate (для claim про тикет / ревью / готовый к копированию текст)

A claim of the form "the artifact is now reviewable", "the owner copies it in one click", "delivery is not summary-only" → the evidence must include the **full fenced block** of the target artifact. A screenshot, a paraphrase or a table instead of the block is insufficient proof: raise the expectation `E0N — есть полный fenced-блок` and, if it is missing, the gap `G0N — нет copy-ready блока`.

### §2.5 Склейки данных (identity-stitching)

When the claim involves a join / merge / "склеили сущности по ключам" (userID from clientID, phone_hash, email_hash), the stitch may be WRONG (an anchor attached to someone else's fact, duplicated, inferred from a donor). Run the commutators instead of guessing by hand:

```bash
python3 ~/.claude/skills/falsify/scripts/commutator_check.py --emit-checklist --anchor userID --keys client_id,phone_hash   # план проверок ДО данных
python3 ~/.claude/skills/falsify/scripts/commutator_check.py config.yaml   # прогон по данным (нужен pandas)
```

7 families B/F/P/C/T/R/X; a structural FAIL (B/F/C) means the stitch is broken → severity `critical` in §3.
Paste the table output into §2.2 verbatim as actual evidence; a paraphrase does not count.

## §3. Gap table (G-ID)

Fill in **at least one row** even when gap=none:

| G-ID — название | E-ID ref | Expected | Actual | Gap type | Severity (low/med/high/critical) | Root Cause (1 строка) | Fix | Next action if unmet | Effort |
|---|---|---|---|---|---|---|---|---|---|
| G01 — ... | E01 | ... | ... | knowledge/execution/feedback/integration | ... | ... | ... | ... | ... |

If gap = none, write one row: `G00 — все ожидания met` with the reasoning.

`Gap type` follows Gap Theory: **knowledge** (did not know) · **execution** (knew, did not do) ·
**feedback** (did it, never learned the result) · **integration** (did it, it did not fit the
neighbouring piece). The type determines the class of fix — without it the §8 injection misses.

### §3.1 Gap count (обязательный блок сразу после таблицы)

```text
Gap count
- total: N
- open: N
- partial: N
- closed: N
- highest severity: N/5
```

## §4. 5 Whys для top-1 critical gap

Only for the **top-1** gap by severity (critical > high > medium). The rest go to the §9 backlog.

For deep RCA, hand off to `/debug` (full protocol there, plus Chesterton fence and the multi-cause trigger).

```
1. Почему {top critical gap}? → [факт из {file:line}]
2. Почему {ответ 1}? → [факт]
3. Почему {ответ 2}? → [факт]
4. Почему {ответ 3}? → [факт]
5. Почему {ответ 4}? → [корневая причина — процессная/системная]
```

Every "why" rests on a **fact from a file, log or commit**, never on a guess.

## §5. Alt hypotheses (только если ≥3 параллельных причин)

If §4 lands confidently on a single root cause, skip this step.

If digging surfaced ≥3 competing hypotheses (parallel alternatives, not a chain), hand off to `/debug` for Bayesian processing. Paste only the resulting table back here:

| H-ID — гипотеза | Prior | Evidence за [O] | Evidence против [O] | Discriminating test | Posterior | Verdict |
|---|---|---|---|---|---|---|

From /debug Mode H take the top-1 hypothesis with posterior ≥80% — that is your working hypothesis for §6.

## §6. Causal chain

```
Симптом → Промежуточная причина → Процессный дефект → Корневая причина → Design Injection
{наблюдаемое} → {что вызывает симптом} → {где процесс сломан} → {почему процесс такой} → {что инъектировать}
```

If there is more than one branch, label them explicitly as `primary chain` and `secondary chain`.

## §7. Blast radius

| Зона | Статус (не сломано / требует проверки / сломано) | Что проверить | Кто проверяет |
|---|---|---|---|
| {затронутый компонент} | ... | {команда / файл / тест} | agent / owner |

The point is to stop the fix from inflating in scope. Check that nothing adjacent was touched.

## §8. Design Injection Point

≤50 characters, in the form `файл → секция → что инъектировать`.

```
Where: {абсолютный путь к файлу}
Section: {заголовок секции куда вставить, или "новая секция X"}
Text to inject: {конкретная формулировка правила, 1-3 строки императивом}
Why this prevents recurrence: {как именно эта инъекция блокирует свёрток}
```

Candidates for Where:
- `~/.claude/CLAUDE.md` — a global pattern
- `~/.claude/rules/{name}.md` — a narrow case (create a new one if needed)
- `~/.claude/skills/{skill}/SKILL.md` — a gap in a step of an existing skill
- `~/.claude/standards/{name}.md` — the methodology of an area (if one exists)
- A project `CLAUDE.md` or `.claude/rules/` — when the pattern belongs to one project only

**If the gap is in code, not in instructions** — skip this; §3 Fix already closes it.

**If the gap is in instructions** — this step is **MANDATORY**. Without it you fixed one symptom, and in a week the mistake returns in another shape.

## §9. Next-Action Digest

Top ≤5 actions by priority:

| P-ID — шаг | Closes gaps (G-ID list) | Effort (0-100) | Actor | Зачем первый |
|---|---|---|---|---|
| P01 — ... | G01, G03 | 30 | agent | разблокирует prod release |
| P02 — ... | G02 | 50 | owner | требует ручного решения |

## §10. Verdict

One of three:

- **PASS** = every E-ID met + 0 critical gaps + no Design Injection needed (or it is done)
- **PARTIAL** = ≥50% of E-IDs met + gaps exist but none critical + there is a closure plan
- **FAIL** = <50% of E-IDs met OR ≥1 critical gap left open

**Prohibited:** PASS without the §1 expectations (post-hoc rationalization). PASS without the §3 Gap table (even at gap=none there must be one G00 row).

**Calibration:**

```
Уверенность: [до]% → [после]% — [причина]
```

If confidence is <70%, flag it explicitly and propose how to raise it (extra tests, a second run, /bouncer for external review).

## §10.5 Новая рабочая гипотеза (обязательна при PARTIAL / FAIL)

The original claim did not survive → state the next, narrower one:

| Новая гипотеза | Чем лучше объясняет наблюдённые gaps | Что её опровергнет следующим |
|---|---|---|

The new hypothesis must: explain the maximum number of open gaps · be **narrower** than the
original claim · carry an explicit next falsifying test. "Falsified and walked away" without a
new hypothesis is half the work: the next run starts from zero.

## §11. Handoff

- **PASS** → the task can be closed. Optionally record a positive paragraph in `~/.claude/memory/incidents/` as a success pattern (rarely — only when a non-obvious approach was validated)
- **PARTIAL** → at severity `medium+`, log a JSONL incident + an optional Markdown RCA. Start the §9 P-IDs
- **FAIL** → a JSONL incident is mandatory. If the gap is in instructions, Edit the file from §8. If the gap is in code, hand off to /debug for deep RCA + /check to verify the fix

Command:

```bash
~/.claude/bin/log-incident.sh --kind falsify --severity medium --source /falsify --target "{file/skill/standard}" --summary "Короткий redacted summary"
```

Create a long Markdown RCA only when the JSONL summary would not serve a future precedent scan. Update `~/.claude/memory/incidents/INDEX.md` whenever you create a Markdown RCA.

## Output Shape

```text
FALSIFY
§0 Input Checklist
§1 Expectations table
§2 Precedent scan + actual evidence
§3 Gap table
§4 5 Whys for top gap
§6 Causal chain
§7 Blast radius
§8 Design Injection Point (если gap в инструкциях)
§9 Next-Action Digest
§10 Verdict + confidence calibration
FALSIFY_FINAL: PASS|PARTIAL|FAIL
```

## Machine receipt

The §1 / §3 / §3.1 / §9 / §10 tables are not assembled by hand — `scripts/falsify_render.py`
renders them. The agent prepares YAML/JSON (hypothesis + expectations with `id`, `claim`,
`where`, `expected`, `actual`, `verdict`, `severity`, `gap_type`) and pastes the script's
stdout into the report **verbatim**.

```bash
python3 ~/.claude/skills/falsify/scripts/falsify_render.py input.yaml   # формат: examples/emitter_input_example.yaml
```

The script enforces mechanically: an E-ID without its ` — label` and an invalid enum are errors,
an empty `actual` becomes `NOT CHECKED` and makes PASS impossible, PASS is impossible while a
critical gap is open, and the Gap count and `FALSIFY_FINAL` are computed rather than typed.
Retelling the tables in prose instead of the script's output is a **Hard fail**.

## Guardrails

- **Read-only by default.** Do not fix things during falsification unless explicitly asked.
- Do not go online and do not use live or paid tools without explicit permission.
- Output from AGY/Fusion/an agent does not count until the payload has the required final
  shape and exact evidence.
- Absence of evidence is not evidence: classify it as missing evidence.
- Found a process gap → propose the MINIMAL injection point into the source of truth (§8).

## FORBIDDEN

- A Verdict without the §1 expectations (post-hoc rationalization, even if the guess was right)
- Skipping the §2.1 precedent scan (risks repeating an old mistake, loses context)
- Writing that the precedent scan was done when the commands never ran or `INDEX.md` was never read
- §1 expectations without the camera test (interpretation served as fact)
- A §10 Verdict of PASS while a critical gap stands in §3 (self-deception)
- §8 Design Injection skipped on FAIL/PARTIAL with an instruction gap (the loop is open, the mistake returns)
- Bare intuition in §10 with no §3-§9 evidence
- Marking work done without a JSONL incident on FAIL or a serious PARTIAL
- Inventing actual evidence, logs, counts, line numbers or command results

## Hard fail

- No §1 Expectations table — the output is invalid, there is no basis to falsify against
- No §3 Gap table (not even G00) — the output is invalid
- No §10 Verdict — the output is invalid
- §8 Design Injection missing on FAIL/PARTIAL with an instruction gap → the evolution loop is open → the output is invalid
- Confidence calibration missing — the output is invalid
- Invented evidence, or `PASS` on a `NOT CHECKED` high-stakes claim — the output is invalid
- Precedent scan claimed as done without observed scan evidence — the output is invalid
- A PASS/PARTIAL verdict on a runtime claim with no runtime evidence at all (§2.3) — invalid
- No §3.1 Gap count — the output is invalid
- PARTIAL/FAIL without the §10.5 new working hypothesis — the output is invalid
- The §1/§3/§3.1/§9/§10 tables retold in prose instead of the verbatim output of `scripts/falsify_render.py` — the output is invalid

## Related skills

- `/check` — for light verification without the full pipeline (no Verdict required)
- `/debug` — for deep RCA of one gap (called from §4)
- `/debug` — for Bayesian processing of ≥3 hypotheses (called from §5)
- `/anti-bias` — for preprocessing the §1 expectations
- `/pizdej` — for process reflection AFTER /falsify, not instead of it
- `/bouncer` — for an external Gemini audit of the Verdict when confidence is <70%
