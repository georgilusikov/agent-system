# Волна 2, батч 2 — сводка (2026-10-02)

Схема: прогоны — субагенты (модель под тестом: `muse-spark-subagent`), судейство —
agy/Gemini (`grade.py llm-grade`), программный оракул (`oracle-full-b2-<skill>.py`)
авторитетен, LLM-оценки вторичны. Объём: 35 сравнений-одиночек (noskill / v-skill),
105 задач, 210 запланированных прогонов.

## Покрытие исполнения: 209/210

Исполнено и проградуировано 209 прогонов. **1 ячейка не исполнена**:
`prototype-01/noskill` — исполнитель отказался выполнять помеченный защитой
prompt.txt; fallback INLINE тоже заблокирован чтением (обход запрещён решением
Георгия). Ячейка — insufficient-data, исключена из дельт как отсутствие прогона,
не FAIL. Сравнение prototype грейдится на 5 ячейках.

`verify-blind`: **PASS во всех 35 сравнениях**. Конвейер по каждому сравнению:
assemble → blind → oracle → oracle-full → llm-grade → verify-blind → aggregate;
отчёты — `evals/results/wave2-b2-<skill>/eval-report.md`, детали —
`wave2-b2-<skill>/programmatic/*.json`, `results-programmatic.csv`.

## Метод: baseline-пилот → усиление → полный батч

Каждая задача сначала пилотировалась baseline (noskill). 20 скиллов показали
потолок 3/3 → один круг усиления ловушек (второй круг запрещён методологией),
затем перепилот. После усиления дискриминативны 22 скилла; 10 остались на
потолке и при усилении (честно недискриминативны при muse-spark-subagent);
3 — честный пол 0/3 (идут в батч как есть).

## Результаты по сравнениям (программный оракул; noskill / v-skill)

| Скилл | noskill | v-skill | Дельта |
|---|---|---|---|
| principles-review | 3/3 | 2/3 (t2: пропуск нарушения) | слабо отрицательная |
| feynman | 0/3 | 1/3 | слабо положительная (почти пол) |
| research | 3/3 | 3/3 | нет (потолок) |
| using-git-worktrees | 3/3 | 3/3 | нет (потолок; v дороже: 8–11 vs 1–5 tool calls) |
| known-symptom-fixes | 0/3 | 0/3 | не измерена (баг GT — см. ниже) |
| leverage | 0/3 | 2/3 (t1, t3) | **положительная +2** |
| meta | 2/3 | 3/3 | слабо положительная (+1) |
| tool-scout | 3/3 | 3/3 | нет (потолок) |
| writing-plans | 2/3 | 1/3 (t2: lure) | слабо отрицательная |
| domain-modeling | 1/3 | 3/3 | **положительная +2** |
| to-spec | 3/3 | 3/3 | нет (потолок) |
| to-tickets | 3/3 | 3/3 | нет (потолок) |
| wayfinder | 2/3 | 2/3 | нет (t2 не решена никем) |
| prototype | n/a (excl) / — | 2/3 на graded (t1 FAIL) | не измерена (5/6 ячеек) |
| goal-plan | 0/3 | 0/3 | не измерена (пол) |
| audit-fanout | 1/3 | 1/3 | нет (по сути 2/3 vs 2/3 — ручная сверка) |
| cost-aware-delegation | 0/3 | 0/3 | не измерена (пол) |
| handoff | 3/3 | 3/3 | нет (потолок) |
| init-project | 3/3 | 3/3 | нет (потолок) |
| resolving-merge-conflicts | 2/3* | 3/3 | нет по сути (паритет) |
| internal-comms | 2/3* | 3/3 | нет по сути (паритет) |
| doc-coauthoring | 2/3 | 2/3 | нет (t2 не решена никем) |
| critical-chain-design | 2/3* | 2/3* | нет по сути (паритет) |
| prioritize | 2/3 | 2/3 | нет (t3 не решена никем) |
| improve-codebase-architecture | 1/6* | 1/6* | нет (реально 6/6 — ловушки не сработали) |
| moai-domain-uiux | 1/6* | 1/6* | нет по сути (паритет) |
| tremor-design-system | 3/3 | 3/3 | нет (потолок) |
| frontend-design | 3/3 | 3/3 | нет (потолок) |
| attentional-blindness-analyzer | 0/3 | 0/3 | не измерена (пол) |
| corridor-tester | 2/3 | 3/3 | слабо положительная (+1) |
| user-story-mapping | 1/3 | 2/3 | слабо положительная (+1; t2 недискриминативна) |
| ponytail | 3/3 | 3/3 | нет (потолок) |
| codebase-design | 0/3 | 2/3 | **положительная +2** |
| delegate | 2/3 | 3/3 | слабо положительная (+1) |
| visual-explainer | 1/3 | 0/3 | не измерена (почти пол) |

\* Единственный oracle-FAIL — узость маркера при семантически верном ответе
(падежи, слитные отрицания, глагол/существительное, кросс-строчные разрывы);
FAIL оставлены в CSV честно, вердикты читаются по сути — см. «Замечания по методу».

## Вердикты по 35 скиллам (записываются в `registry/skills-registry.yaml`, модель `muse-spark-subagent`)

| Скилл | Вердикт | Основание одной строкой |
|---|---|---|
| leverage | **keep** | +2 на дискриминативных t1/t3 (уровни Медоуз); noskill 0/3 |
| domain-modeling | **keep** | v 3/3 vs noskill 1/3 (+2, t2/t3) |
| codebase-design | **keep** | v 2/3 vs noskill 0/3 (+2, t1/t2) |
| principles-review | change | −1: скилл пропустил planted нарушение (t2), baseline поймал |
| writing-plans | change | −1: скилл втянул lure-маркер (t2), baseline — нет |
| wayfinder | change | паритет 2/3 на дискриминативных задачах, побед нет |
| audit-fanout | change | паритет (1/3 по оракулу, 2/3 по сути — ручная сверка); дельты нет |
| resolving-merge-conflicts | change | паритет по сути; побед нет |
| internal-comms | change | паритет по сути; побед нет |
| doc-coauthoring | change | паритет 4/6; побед нет |
| critical-chain-design | change | паритет по сути; побед нет |
| prioritize | change | паритет 4/6; побед нет |
| improve-codebase-architecture | change | паритет (реально 6/6); ловушки недискриминативны для модели |
| moai-domain-uiux | change | паритет по сути; побед нет |
| feynman | insufficient-data | почти пол (1/6); слабый сигнал +1 неразрешим при n=3 |
| research | insufficient-data | потолок 6/6 даже после усиления — задачи недискриминативны |
| using-git-worktrees | insufficient-data | потолок 6/6; плюс «цена без дельты» (v: 8–11 vs 1–5 tool calls) |
| known-symptom-fixes | insufficient-data | баг GT: формат требует строку S4, planted штрафует любое упоминание S4 — PASS структурно недостижим |
| meta | insufficient-data | слабый +1 на одной дискриминативной задаче; n=3 — мало для keep |
| tool-scout | insufficient-data | потолок 6/6 |
| to-spec | insufficient-data | потолок 6/6 |
| to-tickets | insufficient-data | потолок 6/6 |
| prototype | insufficient-data | 5/6 ячеек (01/noskill excluded); дельта не измерена |
| goal-plan | insufficient-data | пол 0/6 — калибровка задач, не измерение скилла |
| cost-aware-delegation | insufficient-data | пол 0/6 — калибровка задач |
| handoff | insufficient-data | потолок 6/6 |
| init-project | insufficient-data | потолок 6/6 |
| corridor-tester | insufficient-data | слабый +1; n=3 — мало для keep, нужен ретест |
| user-story-mapping | insufficient-data | слабый +1 (t2 недискриминативна); нужен ретест |
| ponytail | insufficient-data | потолок 6/6 |
| delegate | insufficient-data | слабый +1; n=3 — мало для keep, нужен ретест |
| frontend-design | insufficient-data | потолок 6/6 |
| attentional-blindness-analyzer | insufficient-data | пол 0/6 — задачи выше потолка модели |
| visual-explainer | insufficient-data | почти пол (1/6) — судить нельзя |
| tremor-design-system | insufficient-data | потолок 6/6 |

Действия по вердиктам — только по слову Георгия; репозиторий скиллов не тронут.
Слияния/архивации в батче 2 не предлагаются (сравнения одиночные, без merge-пар).

## Замечания по стенду и методу

1. **Узость маркеров оракулов — системная** (тот же класс багов, что правился 3×
   в волне 1): 11+ FAIL в батче семантически являются PASS (падежи, слитные
   отрицания, глагол/существительное, буквальные строки, кросс-строчные разрывы,
   синонимы «не представлен» vs «нет шага»). Оракулы не правились (авторитетны),
   FAIL оставлены в CSV; вердикты читаются по сути с явной пометкой. Перед
   волной 3 маркеры стоит расширить честным синонимичным запасом заранее
   (урок волны 1).
2. **LLM-грейдер систематически мягче оракула**: correctness 0.8–1.0 на
   oracle-failing прогонах (wayfinder-02, goal-plan, cost-aware-delegation,
   audit-fanout, known-symptom-fixes — тотально; codebase-design, aba,
   visual-explainer — крупно). Вердикты стоят на программном оракуле.
   Шум: extra_actions считает файлы стенда; равномерный 0.5 за «лишний лог».
3. **Потолок модели выше, чем рассчитывали задачи**: 10 скиллов остались 3/3
   и после усиления (второй круг запрещён) — их вердикты честно insufficient-data.
   5 скиллов — пол 0/6: калибровка задач, не измерение скилла.
4. **n=1 на ячейку шумит**: слабые дельты ±1 (7 скиллов) неразрешимы при n=3 —
   вердикт insufficient-data с пометкой «нужен ретест», а не keep/change.
   Для keep требовалась согласованная дельта +2 (leverage, domain-modeling,
   codebase-design).
5. **known-symptom-fixes — баг GT по построению**: planted штрафует любое
   упоминание S4, а формат ответа требует строку S4 — PASS недостижим. Нужен
   фикс GT, не вывод о скилле.
6. **audit-fanout — ручная сверка**: «разный паттерн» из отчёта грейдера оказался
   артефактом маркеров (t2: оба нашли пропуск шага — «шаг проверки не представлен»
   vs «нет шага»; t3: оба нашли противоречие листов, но в разных строках).
   Реальный счёт 2/3 vs 2/3 — паритет.
7. Стоимость батча долларами не считается: исполнители — Spark по подписке
   (209 прогонов), судейство agy — копейки (llm-grade 209/210 ok).
