# Финальный отчёт: аудит 100 AI-скиллов (2026-10-02)

Репозиторий: `https://github.com/georgilusikov/agent-system` (локально `~/workspace/audit-skillov/repo` — только чтение на протяжении всех эвалов; коммитов/пушей по итогам аудита нет).

Вопрос аудита: даёт ли скилл измеримую добавленную ценность против базового агента без скилла — на слепых A/B-задачах с подставными дефектами. Меряется дельта, не красота инструкции.

## Сводка вердиктов (100/100)

| Вердикт | N | Что означает |
|---|---|---|
| keep | 5 | Чистая положительная дельта, скилл оставить как есть |
| change | 32 | Дельты нет или отрицательная — скилл переписать/усилить |
| replace | 1 | Скилл заменить настоящим инструментом |
| merged | 2 | Поглощён другим скиллом (по слову Георгия, 2026-10-01) |
| archive | 1 | Архивировать (по слову Георгия, 2026-10-01) |
| insufficient-data | 59 | Измерить не удалось: потолок/пол задач, слабый сигнал при n=1, задачи недискриминативны |

Действий по вердиктам (правки SKILL.md, слияния, архивация, замена) **не выполнялось** — только записи в реестр. Всё ниже ждёт слова Георгия.

## Вердикты по волнам

| Волна | Модель под тестом | Скиллов | keep | change | replace | merged | archive | insufficient-data |
|---|---|---|---|---|---|---|---|---|
| 1 (+раунд 2) | gemini-3.6-flash-medium | 15 | 0 | 0 | 0 | 2 | 1 | 12 |
| 2 батч 1 | muse-spark-subagent | 15 | 1 | 12 | 0 | 0 | 0 | 2 |
| 2 батч 2 | muse-spark-subagent | 35 | 3 | 11 | 0 | 0 | 0 | 21 |
| 3 | muse-spark-subagent | 32 | 1 | 9 | 0 | 0 | 0 | 22 |
| Особые (без эвала) | n/a | 3 | 0 | 1* | 0 | 0 | 0 | 2* |
| **Итого** | | **100** | **5** | **32** | **1** | **2** | **1** | **59** |

\* frontend-ui-dark-ts — change по инспекции (не эвал); pdf и codex-advisor — insufficient-data без эвала.

**Положительные дельты (keep):** leverage, domain-modeling, codebase-design (волна 2 батч 2), playwright (волна 2 батч 1), reframing-problems (волна 3).
**Отрицательные дельты (скилл вредит):** principles-review, writing-plans (батч 2), bouncer, jobs-to-be-done, jtbd-scenarium-create, rules-and-hooks-maintenance (батч 1), system-value-architect (−2, волна 3).
**Замена инструментом:** graphify → настоящий PyPI-пакет `graphifyy`.

## Методология стенда

- Слепые прогоны: исполнитель не знает вариант (noskill/v-skill), транскрипты без имён вариантов — проверяется `verify-blind` (PASS везде, где применимо).
- Судейство двухуровневое: **программный оракул авторитетен**, LLM-грейдер (agy/Gemini) вторичен — он систематически мягче (см. «LLM vs oracle»).
- Задачи: planted-дефекты, ловушки на ложные срабатывания, t3-контрольные без дефектов. Сначала baseline-пилот (проверка дискриминативности задачи), недискриминативные усиливаются один раз, затем перепилот.
- n=1 на ячейку: дельты ±1 трактуются как шум → insufficient-data («нужен ретест»), а не keep/change.
- Волна 1 гонялась на другой модели (gemini-3.6-flash-medium, прогоны через agy); волны 2–3 — субагенты Muse Spark. Вердикты волн читать раздельно.

## Стоимость

| Этап | Прогоны | Стоимость |
|---|---|---|
| Волна 1 (пилот 54 + 100) | 154 | ~$3.64 (прогоны) + $0.067 (грейдер) |
| Раунд 2 | 24 | ~$0.96 |
| Волна 2 батч 1 (75 + 11 рестейдж) | 86 | Spark $0 (подписка) + agy ~$0.2 |
| Волна 2 батч 2 (пилоты 105 + 105) | 210 | Spark $0 + agy ~$0.07 |
| Волна 3 (пилоты 96 + перепилоты 52 + батч 192) | 340 | Spark $0 + agy llm-grade ~$0.07 (ориентир волны 2; точный лог стоимости не писался) |
| **Итого** | **~814** | **~$4.9 agy + подписка Spark** |

## Качество и ограничения стенда (честно)

1. **n=1 на ячейку.** Одиночные прогоны шумят; все слабые дельты ±1 — insufficient-data.
2. **Потолок/пол модели.** 59 insufficient-data — в основном задачи, которые muse-spark-subagent либо всегда решает, либо никогда: измеряется калибровка задач, а не скилл.
3. **Переформулированные промпты (батч 1).** 11 ячеек получены на изменённых промптах после safety-отказов — строгое A/B с раундом 1 невозможно; вердикты помечены.
4. **Утечки слепоты.** Исполнители читали запрещённый `.run-info.json` и вписывали имена вариантов в логи (волна 3: 27/32 сравнений на первом проходе) — вылечено маскированием blind-копий; знание варианта могло повлиять на поведение, эффект неизмерим постфактум.
5. **Ремонт bookkeeping.** Часть исполнителей не следовала схеме файлов (answer.md вместо result.json и т.п.) — метаданные реконструированы, оригиналы сохранены.
6. **Фантомные FAIL (батч 1).** Сборка 2026-10-01 записала 65 FAIL-артефактов по неисполненным ячейкам — вычищены, манифесты пересобраны.
7. **LLM-грейдер мягче оракула** — вердикты стоят на оракуле (детали ниже).

## LLM vs oracle (волна 3, 192 ячейки)

llm-grade (agy/Gemini): 192 вызова, оценки в 190 ячейках (2 ошибки грейдинга: code-review-03, оба варианта).
- Совпадение с программным оракулом: 118/190 (62.1%).
- Мягкость грейдера: 66/190 (34.7%) — оракул FAIL, грейдер correctness=1.0 (мягкость в 26 из 32 скиллов).
- Строгость: 6/190 (3.2%) — оракул PASS, грейдер <1.0.
- Распределение correctness: 1.0 — 180/190 (94.7%).

Паттерн волн 1–2 подтверждён количественно: грейдер систематически мягче оракула. Все вердикты стоят на программном оракуле.

## Лицензионные флаги (из upstream-check)

1. `pdf` — upstream заявляет Proprietary, локально приложен текст Apache 2.0. Расхождение проверить отдельно.
2. `user-story-mapping` — upstream CC BY-NC-SA 4.0 (non-commercial, share-alike); локально лицензия не заявлена.
3. `critical-chain-design` — upstream CC BY 4.0 с обязательной атрибуцией; локально атрибуции нет.
4. Пять скиллов Matt Pocock (`code-review`, `to-spec`, `to-tickets`, `triage`, `wayfinder`) — upstream MIT, локальной атрибуции нет. Рекомендация: единый NOTICE-файл.
5. `executing-plans`, `finishing-a-development-branch` (obra/superpowers, MIT), `frontend-ui-dark-ts` (microsoft/skills, MIT) — локально поле license не заявлено.

## Самые спорные вердикты

- **system-value-architect (change, −2):** v-skill не выдал вердикт там, где baseline PASS — редкий случай измеримого вреда; но n=1, нужен ретест перед действиями.
- **graphify (replace):** единственный replace; инструмент выиграл 1/3, скилл 0/3 — тонкая грань, но направление однозначное.
- **playwright (keep):** скилл обыграл и baseline, и настоящий CLI — проверить, не артефакт ли это localhost-фикстур.
- **59 insufficient-data:** не «скиллы плохие», а «измерить не удалось». Для ceiling-скиллов нужны задачи другого класса.

## Открытые решения (ждут слова Георгия)

1. Пуш коммита `3c3c447` (слияния anti-bias→check, systematic-debugging→debug).
2. 18 правок `origin_detail` в реестре.
3. Слияние implement/executing-plans (паритет 9/9 измерен).
4. Любые действия по вердиктам change/replace/archive.
5. Отключение крона `skill-audit-night-shift` после приёмки отчёта.

---

## Приложение: все 100 скиллов

| Скилл | Вердикт | Волна | Модель | Основание |
|---|---|---|---|---|
| agent-orchestrator-standard | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-goalking-vs-aos; субшкалы раздельно): исполнено 3/3 ячеек — полный паритет с b |
| algorithmic-art | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-algorithmic-art; модель muse-spark-subagent): смешанный сигнал (t2 чинен, t1 сломан); |
| anti-bias | merged | 1 | gemini-3.6-flash-medium | Раунд 2 (round2-antibias-vs-check): 12 прогонов, программный оракул 8/12 PASS (noskill 4/4, v-antibi |
| attentional-blindness-analyzer | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-attentional-blindness-analyzer; модель muse-spark-subagent): пол 0/6 — зада |
| audit-fanout | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-audit-fanout; модель muse-spark-subagent): паритет — 1/3 по оракулу, 2/3 по |
| blueprinter | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-blueprinter; модель muse-spark-subagent): слабый −1 (t2 сломан, chartjunk пропущен);  |
| bottleneck-identifier | archive | 1 | gemini-3.6-flash-medium | Эвал волны 1 (wave1-bottleneck-identifier): 6 прогонов, программный оракул 6/6 PASS у всех вариантов |
| bouncer | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-bouncer): T2 — регресс (noskill PASS, v-bouncer FAIL), T1 — общий FAIL, T3 — п |
| canvas-design | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-canvas-design; модель muse-spark-subagent): потолок PPP/PPP даже на усиленных задачах |
| caveman | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-caveman; модель muse-spark-subagent): смешанный сигнал +1/−1 (t1,t3 чинены; t2 сломан |
| check | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| claude-skills | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-claude-skills; модель muse-spark-subagent): пол FFF/FFF — строгая нейтрализация Claud |
| code-review | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-code-review; модель muse-spark-subagent): потолок PPP/PPP — задачи недискриминативны. |
| codebase-design | keep | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-codebase-design; модель muse-spark-subagent): программный оракул v 2/3 vs n |
| codex-advisor | insufficient-data | 3 | n/a (no eval) | Отложен (wave-3-plan §1): требует живого Codex-моста (codex exec) — на стенде субагентов неизмерим;  |
| corridor-tester | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-corridor-tester; модель muse-spark-subagent): слабый +1; n=3 — недостаточно |
| cost-aware-delegation | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-cost-aware-delegation; модель muse-spark-subagent): пол 0/6 — калибровка за |
| critical-chain-design | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-critical-chain-design; модель muse-spark-subagent): паритет по сути (oracle |
| debug | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| delegate | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-delegate; модель muse-spark-subagent): слабый +1; n=3 — недостаточно для ke |
| design-communication-analyzer | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-design-communication-analyzer; модель muse-spark-subagent): слабый −1 (t2); нужен рет |
| dispatching-parallel-agents | change | 3 | muse-spark-subagent | Волна 3 (wave3-dispatching-parallel-agents; модель muse-spark-subagent): паритет PPF/PPF на дискрими |
| doc-coauthoring | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-doc-coauthoring; модель muse-spark-subagent): паритет 4/6 (t2 не решена ник |
| domain-modeling | keep | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-domain-modeling; модель muse-spark-subagent): программный оракул v 3/3 vs n |
| executing-plans | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-implement-vs-executing-plans) + перестейдж 2026-10-02 (модель muse-spark-subag |
| falsify | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-falsify) + перестейдж 2026-10-02 (модель muse-spark-subagent, переформулирован |
| feynman | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-feynman; модель muse-spark-subagent): почти пол (1/6); слабый сигнал +1 нер |
| find-skills | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| finishing-a-development-branch | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-finishing-a-development-branch; модель muse-spark-subagent): слабый −1 (t2); нужен ре |
| frontend-design | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-frontend-design; модель muse-spark-subagent): потолок 6/6. verify-blind PAS |
| frontend-ui-dark-ts | change | 3 | n/a (no eval) | Инспекция (волна 3, без эвала): boilerplate UI-кит (React+Tailwind+Framer Motion, дизайн-токены, gla |
| get-linked-context | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-get-linked-context; модель muse-spark-subagent): слабый −1 (t3); нужен ретест. verify |
| go | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-go; модель muse-spark-subagent): слабый +1 (t1 чинен); n=1 на ячейку — шум, нужен рет |
| goal-king | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-goalking-vs-aos) + перестейдж 2026-10-02 (модель muse-spark-subagent, переформ |
| goal-plan | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-goal-plan; модель muse-spark-subagent): пол 0/6 — калибровка задач, не изме |
| graphify | replace | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-graphify-vs-graphifypypi): v-graphify-skill 0/3 (провалы провенанса анализа ко |
| grilling | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| handoff | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-handoff; модель muse-spark-subagent): потолок 6/6. verify-blind PASS. |
| how-to-write-skills | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-how-to-write-skills; модель muse-spark-subagent): слабый −1 (t3); нужен ретест. verif |
| hypothesis-eval-loop | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| implement | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-implement-vs-executing-plans) + перестейдж 2026-10-02 (модель muse-spark-subag |
| improve-codebase-architecture | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-improve-codebase-architecture; модель muse-spark-subagent): паритет; реальн |
| init-project | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-init-project; модель muse-spark-subagent): потолок 6/6. verify-blind PASS. |
| interior-design-expert | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-interior-design-expert; модель muse-spark-subagent): слабый −1 (t2); нужен ретест. ve |
| internal-comms | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-internal-comms; модель muse-spark-subagent): паритет по сути (oracle-FAIL — |
| jobs-to-be-done | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-jtbd-vs-jtbd-scenarium) + перестейдж 2026-10-02 (модель muse-spark-subagent, п |
| jtbd-scenarium-create | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-jtbd-vs-jtbd-scenarium): T1 и T3 — паритет с baseline, на усиленной T2 v-jtbds |
| known-symptom-fixes | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-known-symptom-fixes; модель muse-spark-subagent): сравнение недискриминатив |
| landing-page-optimizer | change | 3 | muse-spark-subagent | Волна 3 (wave3-landing-page-optimizer; модель muse-spark-subagent): паритет PPF/PPF; побед нет. veri |
| leverage | keep | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-leverage; модель muse-spark-subagent): программный оракул v 2/3 vs noskill  |
| manage-nodeterm-canvas | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-manage-nodeterm-canvas; модель muse-spark-subagent): потолок PPP/PPP — задачи недискр |
| meta | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-meta; модель muse-spark-subagent): слабый +1 на одной дискриминативной зада |
| moai-domain-uiux | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-moai-domain-uiux; модель muse-spark-subagent): паритет по сути (oracle-FAIL |
| mood-board-builder | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-moodboard-vs-themefactory): исполнено 9/9, полный паритет с baseline и theme-f |
| multimodal-video-retakes-editor | change | 3 | muse-spark-subagent | Волна 3 (wave3-multimodal-video-retakes-editor; модель muse-spark-subagent): паритет FPF/FPF; побед  |
| onboarding-optimizer | change | 3 | muse-spark-subagent | Волна 3 (wave3-onboarding-optimizer; модель muse-spark-subagent): паритет FPP/FPP; побед нет. verify |
| pdf | insufficient-data | 3 | n/a (no eval) | Вопрос лицензионный, не эвальный (wave-3-plan §1): локально приложен текст Apache-2.0 (LICENSE.txt), |
| performance-profiling | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| pinokio | change | 3 | muse-spark-subagent | Волна 3 (wave3-pinokio; модель muse-spark-subagent): паритет PFF/PFF; побед нет. verify-blind PASS. |
| pizdej | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-pizdej) + перестейдж 2026-10-02 (модель muse-spark-subagent, переформулированн |
| playwright | keep | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-playwright-vs-playwrightcli) + перестейдж 2026-10-02 (модель muse-spark-subage |
| ponytail | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-ponytail; модель muse-spark-subagent): потолок 6/6. verify-blind PASS. |
| principles-review | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-principles-review; модель muse-spark-subagent): v 2/3 vs noskill 3/3 — слаб |
| prioritize | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-prioritize; модель muse-spark-subagent): паритет 4/6 (t3 не решена никем —  |
| prototype | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-prototype; модель muse-spark-subagent): 5/6 ячеек — prototype-01/noskill не |
| receiving-code-review | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-receiving-code-review; модель muse-spark-subagent): смешанный сигнал (t2 чинен, t3 сл |
| reframing-problems | keep | 3 | muse-spark-subagent | Волна 3 (wave3-reframing-problems; модель muse-spark-subagent): программный оракул v 3/3 vs noskill  |
| requesting-code-review | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-requesting-code-review; модель muse-spark-subagent): слабый +1 (t3 чинен); нужен рете |
| research | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-research; модель muse-spark-subagent): потолок 6/6 даже после усиления — за |
| resolving-merge-conflicts | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-resolving-merge-conflicts; модель muse-spark-subagent): паритет по сути (ед |
| retro | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-retro; модель muse-spark-subagent): смешанный сигнал (t2 чинен, t3 сломан); нужен рет |
| roadmap-planning | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-roadmap-planning; модель muse-spark-subagent): потолок PPP/PPP — задачи недискриминат |
| rules-and-hooks-maintenance | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-rules-and-hooks-maintenance) + перестейдж 2026-10-02 (модель muse-spark-subage |
| security-best-practices | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| sensory-writing-coach | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-sensory-writing-coach; модель muse-spark-subagent): слабый +1 (t2 чинен); нужен ретес |
| subagent-driven-development | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-subagent-driven-development; модель muse-spark-subagent): смешанный сигнал (t3 чинен, |
| sus | change | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-sus): полный паритет с baseline по всем трём задачам, включая общий FAIL на ус |
| system-value-architect | change | 3 | muse-spark-subagent | Волна 3 (wave3-system-value-architect; модель muse-spark-subagent): −2 системно — v-skill не выдал в |
| systematic-debugging | merged | 1 | gemini-3.6-flash-medium | Раунд 2 (round2-debug-vs-systematic): 12 прогонов, программный оракул 11/12 PASS (все варианты нашли |
| teach | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-teach; модель muse-spark-subagent): потолок PPP/PPP — задачи недискриминативны. verif |
| test-driven-development | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| theme-factory | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 1 (wave2-moodboard-vs-themefactory): исполнено 9/9, полный паритет с baseline и mood-bo |
| theory-of-constraints | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-theory-of-constraints; модель muse-spark-subagent): слабый −1 (t2); нужен ретест. ver |
| thinking-theory-of-constraints | change | 3 | muse-spark-subagent | Волна 3 (wave3-thinking-theory-of-constraints; модель muse-spark-subagent): паритет PPF/PPF; побед н |
| to-spec | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-to-spec; модель muse-spark-subagent): потолок 6/6. verify-blind PASS. |
| to-tickets | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-to-tickets; модель muse-spark-subagent): потолок 6/6. verify-blind PASS. |
| tool-scout | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-tool-scout; модель muse-spark-subagent): потолок 6/6 — задачи недискриминат |
| tremor-design-system | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-tremor-design-system; модель muse-spark-subagent): потолок 6/6. verify-blin |
| triage | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| triz | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| truth-seeker | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| user-story-mapping | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-user-story-mapping; модель muse-spark-subagent): слабый +1 (t2 недискримина |
| using-git-worktrees | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-using-git-worktrees; модель muse-spark-subagent): потолок 6/6; «цена без де |
| verification-before-completion | change | 3 | muse-spark-subagent | Волна 3 (wave3-verification-before-completion; модель muse-spark-subagent): паритет PFP/PFP; побед н |
| visual-explainer | insufficient-data | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-visual-explainer; модель muse-spark-subagent): почти пол (1/6) — судить о с |
| wayfinder | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-wayfinder; модель muse-spark-subagent): паритет 2/3 на дискриминативных зад |
| web-artifacts-builder | change | 3 | muse-spark-subagent | Волна 3 (wave3-web-artifacts-builder; модель muse-spark-subagent): паритет PFP/PFP; побед нет. verif |
| webapp-testing | insufficient-data | 1 | gemini-3.6-flash-medium | Волна 1 (модель gemini-3.6-flash-medium): «различий не выявлено» — паритет на 3 задачах; по методоло |
| write-a-skill | insufficient-data | 3 | muse-spark-subagent | Волна 3 (wave3-write-a-skill; модель muse-spark-subagent): слабый +1 (t3 чинен); нужен ретест. verif |
| writing-plans | change | 2 | muse-spark-subagent | Волна 2 батч 2 (wave2-b2-writing-plans; модель muse-spark-subagent): v 1/3 vs noskill 2/3 — слабо от |