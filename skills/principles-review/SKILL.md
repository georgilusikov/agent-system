---
name: principles-review
description: 'Периодический аудит СИСТЕМЫ правил и скиллов против META_PRINCIPLES: violated principles, recurring patterns, drift check, verdict (контракт — в теле). Triggers: "principles review", "meta review", "проверь систему правил", "system health", "system drift". NOT for: внешний второй взгляд на один готовый артефакт (/bouncer), аудит маршрутизации и конфликтов триггеров скиллов (/sus), верификация конкретного результата (/check), ретроспектива одной сессии (/retro).'
---

# Principles Review — периодический аудит системы против META_PRINCIPLES

## Назначение

Периодический аудит состояния AI-системы (не личных задач). Проверяет соответствие `~/.claude/META_PRINCIPLES.md` по данным из `~/.claude/memory/ai.incidents.jsonl`.

Ловит:
- Violation принципов (fabricated evidence, no expected state, ritual without function)
- Recurring patterns → candidates для design injection
- Ritual drift (rules которые не проходят §17 4-function test)

Источник: META_PRINCIPLES §22 (runnable tests) + §24 (dogfood) + §25 (manual baseline).

**Не путать с `/jedi-review`** — тот про личные задачи Дорофеев, этот про системное здоровье.

---

## Claim forms (когда активировать)

Skill активируется когда user утверждает:
- `"Проверь систему"` / `"Как дела с принципами?"` / `"Аудит моего setup"`
- `"Что-то система стала шуметь"` — подозрение на drift
- `"Перед новой фичей проверь что не сломал"` — pre-change audit
- `"Воскресенье, пора обзор делать"` — weekly ritual

---

## When NOT to Use

- Обзор личных задач / бэклога → `/jedi-review`
- Процессная рефлексия после задачи → `/pizdej`
- External audit конкретного артефакта → `/bouncer`
- Верификация одного файла → `/check`
- Фальсификация claim → `/falsify`

---

## Input Checklist

- [ ] `~/.claude/META_PRINCIPLES.md` существует
- [ ] `~/.claude/memory/ai.incidents.jsonl` существует и содержит ≥3 entries
- [ ] Задан scan period (default: 7 дней; при `<3 incidents за 7 дней` расширить до 14)
- [ ] Понятен scope audit: только `~/.claude/**` или включая workspace

---

## Definition of Done

- [ ] Incidents за period собраны и classified
- [ ] Violated principles table с count ≥0 для каждой группы
- [ ] Recurring patterns flagged (≥3 повторений = pattern)
- [ ] ≥1 design injection предложен OR явно написано "no actionable drift found"
- [ ] Verdict HEALTHY/DRIFT/CRITICAL с обоснованием

---

## §1. Scan period

**Команды:**
```bash
PERIOD_DAYS=${PERIOD_DAYS:-7}
CUTOFF=$(date -u -v-${PERIOD_DAYS}d +%Y-%m-%dT%H:%M:%SZ)

jq -c "select(.occurred_at >= \"$CUTOFF\")" \
  ~/.claude/memory/ai.incidents.jsonl \
  | tee /tmp/principles-review-incidents.jsonl \
  | wc -l
```

**PASS criterion:** ≥3 entries за period. Если `<3` → extend period до 14 дней; если всё ещё `<3` → baseline too small, verdict=INSUFFICIENT_DATA.

**§1b. KPI-триплет (снять 3 числа, 2 минуты, до анализа):**
```bash
rtk gain | tail -3                                  # tokens/задачу
tail -5 ~/.claude/memory/kpi.tsv                    # исправления владельца/сессию (пишет /retro)
jq -r .dedup_key ~/.claude/memory/ai.incidents.jsonl | sort | uniq -d | wc -l   # повторные ошибки
```
Тренд вниз = правила работают. Тренд вверх при растущем объёме правил = ритуал, смотри §5/§5b. Числа — в output review, история — в `~/.claude/SYSTEM.md` §Журнал.

---

## §2. Violated principles table

**Mapping incident kind → principle:**

| Incident kind / pattern | Principle violated |
|---|---|
| `skill-gap` + fabricated/precedent/scan/evidence | §6 No fabricated evidence |
| `skill-gap` + self-test/field/mapping/schema | §22 Runnable tests |
| `skill-gap` + missing handoff/routing/protocol | §10 Incident → RCA |
| `verification-gap` | §22 Runnable tests / §23 A/B testing |
| `script-gap` | §22 Runnable tests |
| `process-failure` + memory/preflight/skipped | §12 Markdown = external hippocampus |
| `falsify` + self-test/system-claim | §24 Dogfood self-falsification |
| `fabricated-evidence`, `invented-command`, `synthetic-output` | §6 No fabricated evidence |
| `missing-expected-state`, `post-hoc-check` | §3 Expected State FIRST |
| `no-precedent-scan`, `duplicate-solution` | §13 Precedent scan before design injection |
| `shared-file-overwrite`, `parallel-overwrite` | §19 Read перед Edit |
| `_fixed / _final / _FINAL postfix created` | §18 Edit existing |
| `confidence-without-verification` | §5 Confidence gate |
| `memory-skipped` | §12 Markdown = external hippocampus |
| `auto-patch-shared-standard` | §11 Scope-based rewrite |
| `ritual-bloat` (no 4-function) | §17 4-function rule |
| `skipped-RCA` | §10 Incident → RCA |

**Output table:**

```
| Principle | Count | Top affected skill | Severity median | Last occurrence |
|---|---|---|---|---|
| §6 No fabricated evidence | 5 | /triage | medium | 2026-04-23 |
| §17 4-function rule | 3 | standards/hooks-safety | low | 2026-04-22 |
```

**Rule:** если count ≥ 3 для одного principle → candidate для design injection (§4).

---

## §3. Recurring patterns

Grep дубликаты через `dedup_key` или `summary_hash`:

```bash
jq -r '.dedup_key' /tmp/principles-review-incidents.jsonl \
  | sort | uniq -c | sort -rn | awk '$1 >= 3'
```

**Output:** pattern ID + count + первая/последняя occurrence + affected files.

Если ≥1 pattern с ≥3 повторениями — **это design injection candidate** (§13 precedent scan: похожий паттерн был, значит system не научилась).

---

## §4. Design injection proposals

Для каждого top-3 violated principle или recurring pattern:

```
Design Injection #N:
  File: <absolute path>
  Section: §N — <section name>
  Text to inject: |
    <concrete markdown>
  Rationale: closes principle §<X> violation count <N>
  Effort (0-100): <X>
  Actor: agent / owner / both
```

**FORBIDDEN здесь:** abstract proposals ("улучшить систему"). Только concrete file:section:text per META_PRINCIPLES §12 (Design injection ≤50 chars format в actual Krasinsky skill-construction R12).

**Auto-apply rule (per §11 Scope-based rewrite):**
- Target file в `~/.claude/**` → allowed auto-patch after user approval
- Target file в `_agent_shared/**` или `workspace shared` → gate required, НЕ auto-patch

---

## §5. Drift check (§17 4-function rule application)

Для каждого standard/rule изменённого за period:
- git diff за period
- для каждой добавленной строки спросить: `prevent incident / reduce effort / increase P / observe error`?
- если ни одна функция не выполняется → flag для удаления

**Output:**
```
Files modified in period: N
Lines reviewed: M
Lines flagged as bloat: K (показать examples)
```

Если `K ≥ 5` → предложить cleanup PR/commit.

**Skills cross-runtime drift:** запусти `~/.claude/bin/skills-drift-check.sh` —
пары канон↔адаптация (Claude↔Codex↔workspace, 19 пар). DRIFT → перенеси дельту
смысла в адаптацию руками (НЕ зеркаль текст: адаптации несут runtime-специфику),
затем `--ack`. Контекст пар: `курсор/_agent_shared/reports/skills_dedup_matrix_2026-07-09.md`.

---

## §5b. Rule TTL — selection pressure (monthly, с period=30)

Правила без selection только копятся и разбавляют живые. Раз в месяц:

1. Возраст каждого правила/файла: `git -C ~/.claude log --diff-filter=A --format=%as -- rules/<f>.md` (то же для `~/.codex/rules/`).
2. Срабатывания за 90 дней: grep имени правила / его ключевых слов в `ai.incidents.jsonl` + memory/incidents + retro-записях.
3. **Правило старше 90 дней с 0 зафиксированных срабатываний → кандидат на удаление.** Показать владельцу списком (правило | возраст | срабатываний | причина рождения из git log). Не удалять без OK.
4. Гейт от ложного удаления: правило могло сработать превентивно (инцидентов нет ПОТОМУ ЧТО оно работает). Для guard-правил (backup, git add явными путями, pkill) — пометка `preventive`, TTL не применяется; удалять только по решению владельца.

**Output:** таблица кандидатов + счётчик «родилось за период / умерло за период». Здоровая система: смертность > 0.

---

## §6. Verdict

| Verdict | Criterion |
|---|---|
| **HEALTHY** | <3 violations any principle, no critical severity, no recurring pattern, drift K<3 |
| **DRIFT** | 3-10 total violations OR ≥1 medium severity OR 1-2 recurring pattern OR drift K=3-5 |
| **CRITICAL** | ≥1 high/critical severity OR ≥3 recurring patterns OR ≥10 violations OR drift K≥6 |

Verdict должен включать:
- Main reason (которая метрика tipped)
- Top-3 next actions (priority + file + effort)
- Re-audit period (DRIFT — 3 дня, CRITICAL — immediately после fix)

---

## §7. Калибровка уверенности

**Уверенность: [до]% → [после]% — [причина]**

Пороги:
- <70% → `verdict = NEEDS_MORE_DATA`, попросить baseline extension
- 70-84% → verdict даётся с caveats
- ≥85% → verdict готов к actions

Если `incidents count < 5` за period → уверенность понижается на −30% (small sample).

---

## FORBIDDEN

- Auto-patch shared standards без user approval (нарушение §11)
- Синтезировать incidents которых нет в JSONL (нарушение §6)
- Verdict без violation count (нарушение §22 runnable tests)
- Design injection в абстрактной форме ("улучшить систему") — только concrete file:section:text
- Дублировать работу `/jedi-review` (это про личные задачи, не системные принципы)
- Вносить patches без explicit user confirmation для scope >personal

## Hard fail

- `~/.claude/META_PRINCIPLES.md` отсутствует → skill невалиден
- `ai.incidents.jsonl` отсутствует или размером 0 → невалидно
- Verdict без §2 violation table → output не засчитан
- §4 design injection без concrete file:section:text → output не засчитан
- Нарушение §11 (auto-patch в shared scope) → incident required

---

## Known failure modes

- **Small sample noise:** <5 incidents = выводы шаткие, явно пометить
- **Self-dogfooding gap:** skill ревьюит принципы, но сам нарушает §17 — ревьюить `principles-review` саму через /falsify
- **Map gaps:** новые kind incidents не мапятся на principles — нужен periodic update mapping table в §2
- **Multi-project confusion:** incidents из разных проектов мешаются; по умолчанию scope=`~/.claude/**`, workspace отдельной командой

---

## Handoff

- Verdict CRITICAL → `/falsify` на claim "система healthy" для полного pipeline
- Design injection proposed → `/check` после apply чтобы verify
- Ritual bloat found → `/clean` на конкретные файлы
- Recurring pattern на одной причине → `/debug` Mode L с fact-basis
- Recurring pattern на ≥3 причинах → `/debug` Mode H
- Новый incident обнаружен при скане → `log-incident.sh`

---

## Usage examples

```bash
# Default: weekly review ~/.claude/**
/principles-review

# Extended period
/principles-review period=14

# Scope ограничение
/principles-review scope=personal   # default
/principles-review scope=all        # include _agent_shared + workspace

# After large change
/principles-review since=commit:503aa2a
```

---

## Когда запускать (рекомендация)

| Trigger | Когда |
|---|---|
| **Weekly ritual** | Воскресенье вечер, отдельно от `/jedi-review` |
| **Pre-feature** | Перед крупным изменением в `~/.claude/` |
| **Post-incident spike** | ≥3 incidents за день |
| **Pre-automation** | Перед включением UserPromptSubmit / Schedule |
| **Session review** | После длинной multi-skill session |
| **Monthly deep audit** | Раз в месяц с `period=30` |

---

## Self-check

После каждого запуска принципов review:
1. Проверить что сам skill не нарушает принципы (§17 4-function на каждую свою секцию)
2. Если нарушает — log-incident self-referential, design injection на этот же файл
3. Раз в квартал: `/falsify` на claim "principles-review корректно ловит все documented violation types"
