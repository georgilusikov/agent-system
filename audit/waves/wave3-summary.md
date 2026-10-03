# Волна 3 — сводка (2026-10-02)

Схема: прогоны — субагенты (модель под тестом: `muse-spark-subagent`),
судейство — agy/Gemini (`grade.py llm-grade`, вторично), программный оракул
(`oracle-full-w3-<skill>.py`) авторитетен. Объём: 32 сравнения-одиночки
(noskill / v-skill), 96 задач, 192 прогона полного батча (+96 пилотов
и 52 перепилота).

> **О модели исполнения (волна 3).** Прогоны выполнены субагентами (Muse Spark),
> судейство — agy/Gemini. Волна 1 гоняла прогоны через agy на
> gemini-3.6-flash-medium. Прямое сравнение вердиктов волн 1 и 3 некорректно:
> другая модель под тестом, выше потолок возможностей, задачи калиброваны злее.
> Вердикты волн читать раздельно; межволновые сопоставления — только как
> качественные наблюдения, не как A/B.

Метод: baseline-пилот (96 задач, noskill) → калибровка → усиление
недискриминативных задач (один круг) → переилот усиленных (52 прогона,
свежие исполнители) → полный батч (192 прогона: 32 скилла × 3 задачи ×
2 варианта).

## Покрытие исполнения: 192/192

Все 192 ячейки исполнены и проградуированы. Пустых ячеек нет.
`verify-blind`: **PASS во всех 32 сравнениях** (после домаскирования —
см. «Замечания по стенду» п.3). Конвейер по каждому сравнению:
assemble → blind → mask-blind-variants → oracle → oracle-full →
llm-grade → verify-blind; детали — `evals/results/wave3-<skill>/programmatic/*.json`,
`results-programmatic.csv`.

## Дискриминативность задач

- Пилоты (noskill, 96 задач): 17 задач — потолок 3/3 (baseline всё решает).
- Усиление (один круг, правка YAML): 51 задача усилена (S1–S4).
- Перепилоты (52 прогона): 5 скиллов стали дискриминативны
  (algorithmic-art t1, caveman t1, go t3, verification-before-completion t2,
  write-a-skill t2); 12 остались на потолке 3/3 и после усиления.
- Полный батч (усиленные задачи): из 12 «потолочных» 7 показали FAIL
  baseline на усиленных задачах (дискриминативность выросла);
  5 остались на потолке PPP/PPP — честно недискриминативны
  при muse-spark-subagent.

## Результаты по сравнениям (программный оракул; noskill / v-skill)

Формат: P=PASS, F=FAIL по t1t2t3. Дельта: + (v чинит), − (v ломает), = (паритет).

| Скилл | noskill | v-skill | Дельта |
|---|---|---|---|
| reframing-problems | PFF | PPP | **+2 (t2, t3)** |
| go | FPP | PPP | +1 (t1) |
| requesting-code-review | FPF | FPP | +1 (t3) |
| sensory-writing-coach | FFP | FPP | +1 (t2) |
| write-a-skill | PPF | PPP | +1 (t3) |
| caveman | FPF | PFP | +1/−1 (t1,t3 чинены; t2 сломан) |
| algorithmic-art | PFP | FPP | 0 (t2 чинен; t1 сломан) |
| receiving-code-review | PFP | PPF | 0 (t2 чинен; t3 сломан) |
| retro | PFP | PPF | 0 (t2 чинен; t3 сломан) |
| subagent-driven-development | PPF | FPP | 0 (t3 чинен; t1 сломан) |
| blueprinter | FPF | FFF | −1 (t2 сломан) |
| design-communication-analyzer | FPP | FFP | −1 (t2 сломан) |
| finishing-a-development-branch | PPF | PFF | −1 (t2 сломан) |
| get-linked-context | PFP | PFF | −1 (t3 сломан) |
| how-to-write-skills | PPP | PPF | −1 (t3 сломан) |
| interior-design-expert | PPF | PFF | −1 (t2 сломан) |
| theory-of-constraints | PPF | PFF | −1 (t2 сломан) |
| system-value-architect | PPP | FFP | **−2 (t1, t2; v не выдал вердикт)** |
| dispatching-parallel-agents | PPF | PPF | нет (паритет) |
| landing-page-optimizer | PPF | PPF | нет (паритет) |
| multimodal-video-retakes-editor | FPF | FPF | нет (паритет) |
| onboarding-optimizer | FPP | FPP | нет (паритет) |
| pinokio | PFF | PFF | нет (паритет) |
| thinking-theory-of-constraints | PPF | PPF | нет (паритет) |
| verification-before-completion | PFP | PFP | нет (паритет) |
| web-artifacts-builder | PFP | PFP | нет (паритет) |
| canvas-design | PPP | PPP | не измерена (потолок) |
| code-review | PPP | PPP | не измерена (потолок) |
| manage-nodeterm-canvas | PPP | PPP | не измерена (потолок) |
| roadmap-planning | PPP | PPP | не измерена (потолок) |
| teach | PPP | PPP | не измерена (потолок) |
| claude-skills | FFF | FFF | не измерена (пол) |

## Вердикты по 32 скиллам (модель `muse-spark-subagent`)

Планка волны 2: `keep` — только за согласованную чистую дельту +2;
слабые дельты ±1 при n=1 на ячейку — insufficient-data («нужен ретест»);
паритет на дискриминативных задачах — change.

| Скилл | Вердикт | Основание одной строкой |
|---|---|---|
| reframing-problems | **keep** | +2 чистая (t2 конфликт, t3 no-reframe); v 3/3 vs noskill 1/3 |
| system-value-architect | change | −2 системно: v-skill не выдал вердикт на t1/t2, где noskill PASS |
| dispatching-parallel-agents | change | паритет PPF/PPF на дискриминативных задачах; добавленной ценности нет |
| landing-page-optimizer | change | паритет PPF/PPF; побед нет |
| multimodal-video-retakes-editor | change | паритет FPF/FPF; побед нет |
| onboarding-optimizer | change | паритет FPP/FPP; побед нет |
| pinokio | change | паритет PFF/PFF; побед нет |
| thinking-theory-of-constraints | change | паритет PPF/PPF; побед нет |
| verification-before-completion | change | паритет PFP/PFP; побед нет |
| web-artifacts-builder | change | паритет PFP/PFP; побед нет |
| go | insufficient-data | слабый +1 (t1); n=1 на ячейку — нужен ретест |
| requesting-code-review | insufficient-data | слабый +1 (t3); нужен ретест |
| sensory-writing-coach | insufficient-data | слабый +1 (t2); нужен ретест |
| write-a-skill | insufficient-data | слабый +1 (t3); нужен ретест |
| caveman | insufficient-data | смешанный сигнал +1/−1; нужен ретест |
| algorithmic-art | insufficient-data | смешанный сигнал (t2 чинен, t1 сломан); нужен ретест |
| receiving-code-review | insufficient-data | смешанный сигнал; нужен ретест |
| retro | insufficient-data | смешанный сигнал; нужен ретест |
| subagent-driven-development | insufficient-data | смешанный сигнал; нужен ретест |
| blueprinter | insufficient-data | слабый −1 (t2); n=1 — нужен ретест |
| design-communication-analyzer | insufficient-data | слабый −1 (t2); нужен ретест |
| finishing-a-development-branch | insufficient-data | слабый −1 (t2); нужен ретест |
| get-linked-context | insufficient-data | слабый −1 (t3); нужен ретест |
| how-to-write-skills | insufficient-data | слабый −1 (t3); нужен ретест |
| interior-design-expert | insufficient-data | слабый −1 (t2); нужен ретест |
| theory-of-constraints | insufficient-data | слабый −1 (t2); нужен ретест |
| canvas-design | insufficient-data | потолок PPP/PPP — задачи недискриминативны |
| code-review | insufficient-data | потолок PPP/PPP |
| manage-nodeterm-canvas | insufficient-data | потолок PPP/PPP |
| roadmap-planning | insufficient-data | потолок PPP/PPP |
| teach | insufficient-data | потолок PPP/PPP |
| claude-skills | insufficient-data | пол FFF/FFF — задачи выше возможностей модели |

Итого волны 3: keep 1, change 9, insufficient-data 22.

Действия по вердиктам — только по слову Георгия; репозиторий скиллов не тронут
(repo/ — только чтение, коммитов/пушей нет).

## Итог по всем 100 скиллам

- Волна 1 (15 скиллов, gemini-3.6-flash-medium): везде «различий не выявлено»;
  по итогам — 2 слияния (anti-bias→check, systematic-debugging→debug) и
  1 архивация (bottleneck-identifier), всё по слову Георгия.
- Волна 2 батч 1 (15 скиллов, muse-spark-subagent): 18 вердиктов
  (с рестейджем 11 ячеек).
- Волна 2 батч 2 (35 скиллов, muse-spark-subagent): 35 вердиктов.
- Волна 3 (32 эвальных + 3 особых, muse-spark-subagent): keep — 1
  (reframing-problems); change — 9 эвальных; insufficient-data — 22 эвальных.
  Особые случаи: frontend-ui-dark-ts — change (инспекция), pdf —
  insufficient-data (лицензия), codex-advisor — insufficient-data (отложен).
- Покрытие: 100/100 скиллов имеют вердикт в `registry/skills-registry.yaml`
  (15 + 15 + 35 + 32 + 3 особых; merged/archived — внутри волны 1;
  пересечений покрытия между волнами нет — сверено множествами при
  планировании волны 3).

## Стоимость и число прогонов

- Прогоны: 340 (96 пилотов + 52 перепилота + 192 полный батч).
  Исполнители — субагенты Muse Spark по подписке, долларовая стоимость $0.
- Судейство agy (`llm-grade`, 192 вызова): завершено для всех 32
  (190 ячеек с оценками; code-review-03 оба варианта — ошибка грейдинга:
  «не удалось получить валидный JSON метрик»). По волне 2 — копейки
  (~$0.07/волна). Точная цифра — `grader-cost.py` после завершения.
- verify-blind: PASS 32/32 (после домаскирования).

## LLM vs oracle (волна 3, 192 ячейки)

`llm-grade` (agy/Gemini): 192 вызова, оценки есть в 190 ячейках
(2 — ошибки грейдинга: code-review-03, оба варианта). Сравнение
с программным оракулом (авторитет — `oracle-full-w3`, `results-programmatic.csv`):

- Совпадение вердиктов: **118/190 (62.1%)**.
- Мягкость грейдера: **66/190 (34.7%)** — оракул FAIL, грейдер ставит
  correctness=1.0. Распределение correctness: 1.0 — 180/190 (94.7%),
  0.8 — 1, 0.5 — 4, 0 — 5.
- Строгость грейдера: **6/190 (3.2%)** — оракул PASS, грейдер <1.0
  (в т.ч. два нуля: subagent-driven-development-03 v-skill,
  teach-02 noskill).
- Мягкость зафиксирована в 26 из 32 скиллов.

Вывод: паттерн волн 1–2 подтверждён количественно — LLM-грейдер
систематически мягче программного оракула (почти всегда 1.0).
Вердикты стоят на оракуле; грейдер — только вторичный сигнал.

Техническая пометка: колонка `oracle_passed` в `results.csv` пересчитана
из `results-programmatic.csv` — простой oracle внутри `aggregate.py`
падал с `task_missing` на layout задач волны 3 (все 192 ячейки были
`false`). Бэкап исходных CSV — `evals/results/wave3-hidden/`.

## Замечания по стенду и методу

1. **v-вариант получал ПОЛНЫЙ текст SKILL.md** (проверено containment'ом:
   полный SKILL.md — 3–20 КБ — содержится в staged prompt.txt; напр.
   system-value-architect: SKILL.md 3078 Б внутри промпта 6830 Б,
   algorithmic-art: 19770 Б внутри 23570 Б). Тестируется помощь полного
   текста скилла, не дистиллята. Смешанные/отрицательные дельты — эффект
   самого скилла (или его взаимодействия с задачей), не артефакт урезания.
2. **Ремонт bookkeeping-файлов (честный).** 145/192 прогонов не записали
   result.json (писали answer.md/result.md/final.md); 86 tool_calls.json —
   dict-обёртки или JSONL с нестандартными ключами; 13 result.json —
   malformed (ответ задачи вместо метаданных, status ok/declined/blocked).
   Грейдится transcript.md (в порядке); метаданные реконструированы из
   mtime + tool_calls.json, оригиналы в `*.orig-*`, файлы помечены
   `_repaired`. Скрипт: `hidden_files/repair-w3-fullbatch-results.py`.
   Урок: исполнителям нужен полный бриф со схемой всех файлов
   (в перепилотах та же проблема от конденсированного брифа).
3. **Утечки имён вариантов в транскриптах.** Исполнители вписывали
   `(v-<skill>)` / `variant=noskill` в заголовки логов (читали запрещённый
   `.run-info.json` вопреки правилу 4 промпта) — verify-blind падал
   в 27/32 сравнениях на первом проходе конвейера. Фикс:
   `evals/harness/mask-blind-variants.py` маскирует имена вариантов →
   `[variant]` в слепых копиях (оригиналы в `scratch/` не тронуты, маппинг
   не вскрывался) — блайнд восстановлен, финальный verify-blind PASS 32/32.
   Оракул читает маркеры контента, на него маскировка не влияет; грейдинг
   перезапущен на финальных санитизированных данных (лог
   `evals/results/wave3-regrade.log`). Оговорка: знание своего варианта
   могло повлиять на поведение исполнителя — эффект неизмерим постфактум;
   в будущих волнах чтение `.run-info.json` должно отлавливаться
   на assemble (нарушение → error-мета).
4. **Паттерн «ломает t2».** 5 скиллов (blueprinter,
   design-communication-analyzer, finishing-a-development-branch,
   interior-design-expert, theory-of-constraints) — v-skill ломает именно
   t2, где noskill PASS. Возможна системная причина (ловушка в t2,
   которую дистиллят провоцирует). При ретесте — разобрать t2 отдельно.
5. **Потолок модели выше расчёта.** 5 скиллов остались PPP/PPP даже на
   усиленных задачах; 12 «потолочных» пилотов дали 7 дискриминативных
   в полном батче — усиление сработало частично. Для ceiling-скиллов
   нужны задачи другого класса или другая модель-агент.
6. **LLM-грейдер (agy) вторичен.** По волне 3 измерено: совпадение
   с оракулом 62.1%, мягкость (оракул FAIL → грейдер 1.0) — 34.7%,
   строгость — 3.2% (см. раздел «LLM vs oracle»). Вердикты стоят
   на программном оракуле.
7. **n=1 на ячейку.** Все дельты ±1 — в пределах шума; вердикты по ним
   insufficient-data с пометкой «нужен ретест», а не keep/change
   (прецедент волны 2, п.4).
