# Функциональная кластеризация 100 AI-скиллов agent-system

Дата: 2026-10-01. Синтез четырёх воркеров (источники в `registry/worker-out/`):
- w1-graph.md — граф slash-ссылок (218 уникальных рёбер), конвейеры, висячие ссылки, степени;
- w2-thin-overloaded.md — перепроверка thin/overloaded по чтению всех 100 SKILL.md;
- w3-merge-split.md — merge/split-кандидаты вне пилота, wired-цены посчитаны скриптом по caller-map;
- w4-coverage.md — карта 56 функций: перепокрытие / одиночки / дыры.

Опорные документы: `skills-registry.yaml` (100 скиллов, 12 типов), `dupe-clusters.md`,
`caller-map.md` (46 wired / 54 без), `pilot-candidates.md` (6 пар пилота — здесь не дублируются, только ссылки).

Методологическая рамка (из dupe-clusters §7, w3): пересечение механики ≠ избыточность;
каждый вердикт «объединить/разбить/архивировать» — гипотеза для волнового аудита
с held-out тестами, не приговор. Паритет = «различий не выявлено».

---

## 1. Кластеры: 10 функциональных доменов, 56 функций

Группировка по функции («что получает пользователь»), глубже 12 формальных типов.
Легенда: **[W]** — есть wired-вызывающие; **[thin]** — подтверждённый thin; **[ovl]** — overloaded; **[pd]** — possible-dupe.

| Домен | Функций | Скиллов | Сильное/умеренное перепокрытие | Хрупкие одиночки |
|---|---|---|---|---|
| D. Диагностика и исследования | 5 | 11 | D2 (TOC/рычаги — 4 скилла, confirmed-dupe + пустой шаблон), D1 (RCA — 3 скилла, один вопрос «почему упало») | D3 truth-seeker (единственный фактчекер), D5 attentional-blindness-analyzer |
| V. Верификация | 7 | 14 | V1 (предзаверочная: check / VBC / grilling — неясно, какой звать) | V4 corridor-tester, V5 hypothesis-eval-loop (единственный количественный eval «стало ли лучше») |
| O. Оркестрация агентов | 8 | 10 | — | O4 codex-advisor (единственный мост Antigravity↔Codex) |
| P. Планирование и проектирование | 7 | 16 | P5 (спека→тикеты→план: upstream без wired), P1 (3 ответа на «чего добиваемся»), P4 (3 входа в «как спроектировать») | P3 wayfinder (вход в Matt Pocock pipeline висит на ручном вызове) |
| I. Реализация | 3 | 3 | — | I1 implement **[thin]** — ядро цикла на 14 строках |
| Q. Ревью качества кода | 4 | 5 | — (Q1 — overlap, не дубль) | Q2 receiving-code-review (асимметрия: запросить зовут, принимать некому напомнить), Q4 ponytail |
| G. Доменный дизайн | 8 | 17 | G2 (Frontend/UI — 5 скиллов на один триггер «построй UI»), G3 (UX-аудит — 3 скилла, общий JTBD-каркас) | G4 interior-design-expert, G5 mood-board-builder **[thin]**, G6 theme-factory, G7 multimodal-video-retakes-editor |
| C. Контент и текст | 6 | 7 | — | C2 doc-coauthoring, C3 internal-comms, C4 sensory-writing-coach, C6 pdf (единственный документный инструмент) |
| M. Методики мышления | 1 | 3 | — (M1 — слоистая архитектура by design: meta→triz→reframing) | — |
| T. Мета-тулинг | 7 | 14 | T2 (4 точки входа «напиши/найди скилл») | T6 playwright |

**Топливо для merge-аудита** (сильное + умеренное перепокрытие, 9 функций): G2, D2, T2, D1,
V1, P1, P4, P5, G3. Особо: D2 (confirmed-dupe + пустой шаблон), G2 (4 скилла на один
триггер), V1 (пользователь не знает, какой из трёх звать перед сдачей), P5 (pipeline,
у которого upstream не вызывается экосистемой — висит на ручном вызове).

---

## 2. Граф конвейеров

### 2.1. Подтверждённые (w1, с точными ссылками)

**P1. wayfinder → to-spec → to-tickets → (метка ready-for-agent).**
Все звенья — тип «граница» (NOT for), прямых вызовов нет. Уточнения w1:
`ready-for-agent` — не скилл, а метка триажа (такого скилла в репо нет);
звено to-tickets → implement существует только в копии `go/workflows/to-tickets/SKILL.md:107`,
топ-уровневый to-tickets ни на что не ссылается как на следующий шаг.

**P2. writing-plans → executing-plans | subagent-driven-development → finishing-a-development-branch.**
Сильнейший: REQUIRED SUB-SKILL в обе стороны (`writing-plans/SKILL.md:78,189,194,198`;
`executing-plans/SKILL.md:35-36,70`; `sdd/SKILL.md:66,81`). Развилка inline/subagent
задокументирована в самом writing-plans. Все ссылки — со старым префиксом `superpowers:`
(устаревшее имя пакета). В ветке sdd между исполнением и финишем вставлен шаг ревью
(`requesting-code-review/code-reviewer.md`).

**P3. to-tickets → implement → code-review.**
`implement/SKILL.md:12` — «Once done, use /code-review to review the work.»
(та же строка в go-копии). См. нюанс P1 про to-tickets → implement.

### 2.2. Новые цепочки (w1 N1–N8 + w3 §E, дедуплицированы)

1. **go → goal-plan → goal-king → delegate** (→ bouncer как альтернативный финал).
   Автономная ветка: роутер → контракт с гейтами → цикл волн → бриф lane → внешний аудит.
2. **known-symptom-fixes → debug → check | falsify → anti-bias.** Верификационная ветка
   дебага: префикс-чеклист «известный симптом?» → RCA → верификация (high-stakes → falsify)
   → debias ожиданий (check и falsify оба роутит в /anti-bias как preprocessing).
3. **Веер в to-spec через grilling:** wayfinder → grilling → to-spec;
   triage → grilling → to-spec; improve-codebase-architecture → grilling → to-spec;
   wayfinder → domain-modeling → to-spec. **grilling — хаб**: 3 входящих цепочки.
4. **audit-fanout → bouncer** — внутренний multi-axis read-only аудит, затем внешний
   аудит чужой моделью (взаимные NOT-границы уже есть).
5. **research → truth-seeker** — фоновый сбор первоисточников, затем эпистемическая проверка.
6. **find-skills → claude-skills** — поиск+установка скилла, затем его запуск изнутри Codex.
7. **user-story-mapping → to-spec / to-tickets** — карта историй → спека/тикеты.
8. **requesting-code-review ↔ receiving-code-review** — комплементарная пара «запрос ↔ приём», не дубль.
9. **roadmap-planning → prioritize** — приоритизация как подшаг роадмапа.
10. **handoff + retro** — конец сессии: перенос контекста + извлечение уроков (параллельные).
11. **meta → reframing-problems → triz** — слоистая архитектура выбора линзы.

### 2.3. Хабы графа (w1, 218 рёбер)

- **Утилиты-терминалы** (высокий in-degree, низкий out): debug (20), check (15),
  bouncer (13), pizdej (11), falsify (10), code-review (10) — их зовут, они не зовут.
- **Роутеры** (высокий out-degree): go (21), how-to-write-skills (15), meta (12).
- **Двусторонние**: debug (20/7), anti-bias (8/5), delegate (6/6), goal-plan (8/6).
- 19 скиллов без исходящих slash-ссылок, 19 — без входящих (по slash-методу;
  вызовы из rules//standards//docs/ учтены отдельно в caller-map).

**Вывод для вердиктов:** конвейеры §2.1–2.2 — не дубли, слияние звеньев разрушает
пайплайны. Позвоночник верификации: debug → check/falsify → anti-bias (+ bouncer
как внешний контур). Слабое место: upstream Matt Pocock (wayfinder, to-spec, to-tickets)
без wired — весь P1/P3 висит на ручном вызове.

---

## 3. Таблица merge/split-кандидатов

Цена слияния: «общих N / различных M» wired-вызывающих из caller-map (w3, посчитано скриптом).
Пилотные 6 пар + резерв — см. `pilot-candidates.md`, здесь одной строкой для сводки.

### 3.1. Пилотные пары (ссылка, не дубль разбора)

| Пара | Ожидаемый вердикт (пилот) |
|---|---|
| check / falsify | объединить (слои одного протокола), если held-out не докажет различий |
| verification-before-completion / check | оставить оба с NOT-границей |
| code-review (+requesting) / reviewdog, PR-Agent | изменить (развести триггеры) |
| implement / go-маршрут / Aider, OpenHands | изменить/оставить (граница исполнитель vs роутер) |
| executing-plans / subagent-driven-development | объединить (executing-plans → fallback sdd) |
| theory-of-constraints / thinking-theory-of-constraints | объединить (канон = theory-of-constraints) |
| (резерв) anti-bias / check | изменить (общий debias-блок в канон) |

### 3.2. Новые merge-кандидаты (w3)

| Пара | Тип связи | Сила | Цена слияния (wired общ./разл.) | Вердикт |
|---|---|---|---|---|
| debug / systematic-debugging | дубль | сильная | 0 / 4 (все у debug; systematic 0 wired) | **объединить**: systematic → режим внутри debug; уникальное (3+ фейла → вопрос архитектуре, root-cause-tracing.md, defense-in-depth.md) перенести как § |
| goal-king / agent-orchestrator-standard | пересечение | сильная | 1 / 0 (общий skill-routing) | оставить с границей: goal-king = цикл, AOS = механика; слияние = переписывание двух зрелых тел, не раньше волнового эвала |
| jobs-to-be-done / jtbd-scenarium-create | пересечение | средняя | 0 / 5 (два несвязанных кластера: доменные стандарты vs оркестрация) | оставить с границей — цена слияния **разрушительная** |
| design-communication-analyzer / attentional-blindness-analyzer | пересечение | средняя | 0 / 0 | оставить оба; общий блок «когнитивная нагрузка/подсчёт объектов» → shared-фрагмент |
| tool-scout / find-skills | пересечение | слабая-средняя | 0 / 2 | оставить с границей (критерии качества инструмента ≠ критерии качества скилла); discovery-каркас — опциональный shared-фрагмент |
| system-value-architect / jobs-to-be-done | пересечение | слабая-средняя | 0 / 3 | оставить с границей (разные школы: формула мотивации vs JTBD) |

### 3.3. Split-кандидат (w2+w3, сошлись независимо)

**rules-and-hooks-maintenance → 2 скилла.** Шов «инфра vs контент»: §1 (контракт хуков:
5 условий, фикстуры, fail-open) + §2 (приёмка правок правил от внешнего агента) —
связная тема «защита канона»; §3 (обновление скиллов DS-курса: скрипт на Mac Mini,
привязка к `~/Documents/GOGOS`) — чужеродный персональный конвейер. Цена разбиения
дешёвая: 1 wired (skill-routing). Бонус-находка w2: в файле `EXPIRES: 2026-10-30` —
срок истекает через месяц. Не подтверждают overloaded: security-best-practices
(одна функция, три режима), subagent-driven-development (418 строк — подмеханики
одного workflow), graphify (20 сабкоманд — фазы одного жизненного цикла).

### 3.4. Поглощения тонких скиллов (w2)

| Thin-скилл | Поглотить в | Обоснование |
|---|---|---|
| bottleneck-identifier (73 строки, ноль механики) | performance-profiling (§5 «Common Bottlenecks: By Symptom» уже реализует функцию) | пустой шаблон → архивировать после переноса 2 строк роутинга; 0 wired |
| jobs-to-be-done (55, памфлет без протокола) | jtbd-scenarium-create (как §0 «рамка JTBD» в 5 строках) | теория без механики; но 3 wired в доменных стандартах — поглощение требует правок там |
| mood-board-builder (31, банальности без критериев) | theme-factory (как шаг «собери референсы перед выбором темы») | ранний этап того же пайплайна стилизации |
| implement (14, стаб-оркестратор) | executing-plans | та же функция «исполнение плана»; но implement — пилот №4, решение после эвала |
| resolving-merge-conflicts (14, но функционален — флаг thin снят) | finishing-a-development-branch (как раздел «если конфликт») | только после триггер-аудита; триггер чёткий, вреда от тонкости нет |

Снятые флаги реестра (w2, чтение всех SKILL.md): grilling — реальный протокол,
не thin; resolving-merge-conflicts — 5 шагов с критериями; security-best-practices,
subagent-driven-development — не overloaded.

### 3.5. Рассмотрены — не кандидаты (оставить с границей / shared-фрагмент)

critical-chain-design / theory-of-constraints (общее-частное); delegate /
dispatching-parallel-agents (dpa — кандидат на перенос в references/, не скилл);
truth-seeker / research (конвейер, не дубль); how-to-write-skills / write-a-skill
(false-positive: канон+дельта by design); meta / triz / reframing-problems (слоистая
архитектура); triz / leverage (пересечение by design); canvas-design / algorithmic-art
(общий манифест-каркас, разные медиумы); landing-page-optimizer / onboarding-optimizer
(структурные близнецы, разные домены); frontend-ui-dark-ts / tremor-design-system
(не слияние: dark-ts → templates, триггер сузить); codebase-design / domain-modeling
(взаимные NOT); goal-plan / writing-plans / roadmap-planning (три артефакта);
prioritize / roadmap-planning; handoff / retro; playwright / webapp-testing;
caveman / feynman (противоположные цели); grilling / pizdej (NOT-граница, pizdej
с ~10 wired не трогать).

---

## 4. Дыры: функции, которых нет (w4)

Критерий: функция логически требуется конвейерами и соседями, отсутствие бьёт
по замкнутости циклов.

- **Д1. Замкнутый remediation-loop.** bouncer/falsify выдают вердикты, audit-fanout —
  «план фиксов», но владельца «доведи до зелёного и перепроверь» нет: цикл
  верификация → исправление → повторная верификация не замкнут.
- **Д2. Гейт приёмки тикета / DoD-контроль.** Между to-tickets и implement нет
  формального «тикет готов к исполнению».
- **Д3. Мост triage(внешний) → to-tickets.** Два контура не соединены: оттриаженный
  issue не конвертируется в execution-тикет (подтверждено dupe-clusters §4).
- **Д4. Метрология самих скиллов.** 54/100 без wired — некому отличить «полезен
  вручную» от «мёртв». Частично закрывается текущим аудитом, но как функции нет.
- **Д5. Сторож долгих автономных волн.** goal-king крутит волны без внешней
  наблюдаемости/аварийного стопа.
- **Д6 (слабая). Протокол отката при провале гейтов.** Что делать, когда check/falsify
  сказали «нет» — ad hoc.

**personal-productivity (0 скиллов): вердикт — тип лишний, не дыра.** Единственный след —
secondary-type у prioritize; предметная область системы — работа агента, не жизнь
пользователя. Пустой тип вводит в заблуждение при роутинге (`go` может маршрутизировать
в пустоту). Рекомендация: убрать из таксономии.

---

## 5. Висячие ссылки: 9 (w1, все с файл:строка)

| Имя | Кто ссылается |
|---|---|
| thinking-systems | thinking-theory-of-constraints (SKILL.md:29) |
| web-design-expert | interior-design-expert (SKILL.md:5, 42) |
| color-theory-palette-harmony-expert | interior-design-expert (SKILL.md:5) — новая, в dupe-аудите не отмечена |
| setup-matt-pocock-skills | code-review, to-spec, wayfinder (+ go-копии) — 5 файлов |
| jedi-review | principles-review (SKILL.md:19, 35, 232, 288) |
| clean | how-to-write-skills, principles-review |
| deep-research | research (внешний путь `~/.claude/skills/deep-research/`), how-to-write-skills |
| brain-dump | how-to-write-skills |
| task-format | how-to-write-skills/references |

Пограничные (не висячие): `/tdd` (алиас к test-driven-development без явной связи),
`/goal` (команда агента, не скилл). Ложные срабатывания отфильтрованы w1
(скрипты, локальные .md, HTML-теги, пути, упоминания языка Go).

---

## 6. Сводка вердиктов для волн

| Вердикт | Кандидаты | Источник |
|---|---|---|
| Объединить | debug+systematic-debugging; 6 пилотных пар (см. pilot-candidates.md) | w3, пилот |
| Разбить | rules-and-hooks-maintenance → инфра-скилл + DS-курс-микроскилл | w2+w3 |
| Поглотить/архивировать | bottleneck-identifier → performance-profiling; mood-board-builder → theme-factory; jobs-to-be-done → jtbd-scenarium-create (§0); frontend-ui-dark-ts → templates | w2, пилот |
| Оставить с границей / shared-фрагмент | §3.5 (16 пар), A2–A6 | w3 |
| Конвейеры — не трогать как дубли | 11 цепочек §2.1–2.2 | w1+w3 |
| Закрыть дыры (новые скиллы/механики) | Д1–Д6 | w4 |
| Починить висячие ссылки | 9 имён §5 | w1 |
| Убрать из таксономии | personal-productivity (пустой тип) | w4 |

Репозиторий не изменялся (только чтение) на всех этапах.
