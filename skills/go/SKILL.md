---
name: go
description: 'Use ONLY when the user asks where to start or which workflow fits — маршрутизация, а не сама работа. Роутер разводит feature / bugfix / refactor / QA / TDD по нужному скиллу или workflow-файлу. Triggers: "с чего начать", "не знаю какой скилл нужен", "что дальше делать по этой задаче", "route this task", "куда это отнести". NOT for: задача, где нужный скилл уже назван явно — зови его напрямую (/debug, /check, /delegate); долгая автономная работа до цели (/goal-plan → /goal-king).'
---

# Workflow Router

Определи intent пользователя и загрузи нужный workflow через Read tool.

## Маршруты

| Intent | Ключевые слова | Workflow | Файл |
|--------|---------------|----------|------|
| Новая фича / идея | фича, feature, хочу сделать, идея, план | Feature | `workflows/grill-me.md` → `workflows/to-spec/SKILL.md` → `workflows/to-tickets/SKILL.md` |
| Большой объём работы / эпик | эпик, большая задача, с чего начать, карта работ | Wayfinder | `workflows/wayfinder/SKILL.md` |
| Баг / ошибка | баг, bug, сломалось, не работает, ошибка | Bugfix | `workflows/diagnosing-bugs/SKILL.md` |
| Буксует, проблема не сформулирована | буксует, растём медленно, что-то не так, где узкое место, рычаги | Discovery | Skill `/leverage` |
| Multi-cause debug | flaky, race, то падает то нет, inconsistent, несколько причин, три причины, multi-cause | Triage | Skill `/debug` |
| Рефакторинг | рефакторинг, refactor, переписать, почистить | Refactor | `workflows/to-spec/SKILL.md` (спека) → `workflows/implement/SKILL.md` |
| Реализация с тестами | tdd, тесты, red-green, реализуй | TDD | `workflows/tdd/tdd.md` |
| Quality exit | готово, проверь результат, можно релизить, prod readiness, timeout, stuck | Skill route | `/check`, `/falsify`, `/debug` |
| Внешний аудит | второе мнение, аудит через Gemini/Codex, rate this | External | Skill `/bouncer` |
| Роадмэп / стратегия | roadmap, квартал, стратегия, куда двигаться | Roadmap | Skill `roadmap-planning`, крупные цели → Skill `/goal-plan` |
| Долгая автономная работа | закрой roadmap, работай до цели, автономно | Autonomous | Skill `/goal-plan` → Skill `/goal-king` |
| Делегирование | отправь в codex, поручи агенту, dispatch | Delegate | Skill `/delegate` (стоимость канала — cost-aware-delegation) |
| Оценка сроков | сколько займёт, ETA, успеем | Estimate | замер на 1-2 реальных примерах (CLAUDE.md §Meta-awareness) |
| Приоритизация | что делать первым, ранжируй | Prioritize | Skill `/prioritize` |
| Завершение сессии | хэндоф, handoff, retro, подведи итоги | Wrap | Skill `/handoff` / `/retro` |
| Проблема самой маршрутизации | конфликт скиллов, не тот скилл сработал, скилл не вызвался | Routing | Skill `sus` (codex-side) |
| Механика запуска lanes | worktree, intake, мониторинг воркеров | Orchestration | `agent-orchestrator-standard` (codex-side) + `cost-aware-delegation` (выбор канала) |

Маршрут помечен `codex-side` → скилл живёт в `~/.codex/skills/`; в Claude Code его нет.
Нет подходящего маршрута — скажи об этом прямо, не импровизируй протокол.

## Как маршрутизировать

1. Прочитай сообщение пользователя
2. Если intent ясен — сразу загрузи workflow файл через `Read` и следуй инструкциям
3. Если неясно — задай ОДИН вопрос: "Это новая фича, баг, рефакторинг, или что-то другое?"
4. Для Feature: после grill-me спроси "Оформить в спеку?" → после to-spec спроси "Разбить на тикеты (to-tickets) или реализовать сразу (implement)?"

## Quality exits

Не ломай старую grill-me цепочку. Эти exits добавляются поверх неё:

| Сигнал | Куда | Что передать |
|---|---|---|
| Ready artifact / "готово, проверь" | `/check` | goal, changed files, claimed outcome, known risks. `/check` сам пишет полный Expected State. |
| High-stakes / prod readiness / "можно релизить" | `/falsify` | claim, source-of-truth files, release risk, rollback context. |
| One clear error / traceback | `/debug` | command, exact output, touched files, expected behavior. |
| 3+ causes / flaky / race / timezone / network / inconsistent | `/debug` | symptoms, candidate causes, logs/tests seen. |
| Stuck / timeout / 3 repeated attempts | `/debug` (anti-freeze + режим-роутер внутри) | last known state, failed attempts, one new probe needed. |

## Цепочки

После завершения workflow предложи следующий шаг:

**Feature-цепочка (mattpocock upstream 2026-07-10):**
- grill-me → "Оформить в спеку?" → Read `workflows/to-spec/SKILL.md`
- to-spec → "Разбить на тикеты или реализовать?" → Read `workflows/to-tickets/SKILL.md` или `workflows/implement/SKILL.md`
- to-tickets → если 10+ тикетов: "Приоритизировать через ISRICE?" → Skill `/prioritize`. Затем: "Прогнать сверку spec↔tickets?" → Read `workflows/analyze.md` (рекомендуется при 5+ user stories)
- analyze → если 🔴 GAPS — вернуться к to-spec/to-tickets для фикса. Если 🟡 WARN или ✅ PASS → Read `workflows/implement/SKILL.md`
- очень большая цель, неясно с чего начать → Read `workflows/wayfinder/SKILL.md` (карта research-задач), потом to-spec на первый кусок

**Bug-цепочка:**
- `workflows/diagnosing-bugs/SKILL.md` (первый шаг) — reproduce → minimise → hypothesise
- глубокий RCA → Skill `/debug` (режим-роутер внутри: одна цепочка = Mode L/5 Whys; ≥3 конкурирующих гипотез = Mode H/Bayes-таблица → top-гипотеза → Mode L)
- после RCA → "Починить через TDD?" → Read `workflows/tdd/tdd.md`

**После TDD (любая цепочка):**
- tdd → после GREEN-фазы предложи: "Прогнать `/check` для верификации edge cases и negative space?" → Skill `/check`

**После завершения большой цепочки (опционально):**
- Если задача была сложной или заняла много шагов — предложи: "Прогнать `/pizdej` для саморефлексии?" → Skill `/pizdej`. Не навязывай на каждой мелкой задаче.

## Step Summary между workflow

После каждого крупного шага цепочки (grill-me, PRD, plan, tdd, check) — зафиксируй переход в 4 строки перед загрузкой следующего workflow:

```
Goal: [цель шага]
Did: [что сделал, diff/файлы]
Result: OK/FAIL ([метрика или ссылка на артефакт])
Next: [следующий шаг или вопрос пользователю]
```

Это ловит "агент забыл что решили 5 шагов назад" в длинных цепочках.

## Важно

- Загружай ТОЛЬКО нужный workflow файл, не все сразу
- Для TDD: основной файл `workflows/tdd/tdd.md`, доп. файлы (tests.md, mocking.md, deep-modules.md, interface-design.md, refactoring.md) в той же папке — загружай по необходимости
- Все workflow файлы находятся относительно этого SKILL.md
