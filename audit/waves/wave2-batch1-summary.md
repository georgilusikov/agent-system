# Волна 2, батч 1 — сводка (2026-10-01)

_Обновлено 2026-10-02: перестейдж 11 ячеек с переформулированными промптами,
покрытие 86/86, вердикты пересмотрены (см. «Покрытие исполнения»)._

Схема: прогоны — субагенты (модель под тестом: `muse-spark-subagent`), судейство —
agy/Gemini (`grade.py llm-grade`), программный оракул (`oracle-full-<cmp>.py`)
авторитетен, LLM-оценки вторичны. Объём: 11 сравнений, 15 скиллов, 34 задачи,
86 запланированных прогонов.

## Покрытие исполнения: 86/86

Исполнено и проградуировано 86 прогонов. 11 ячеек, не исполненных в батче
2026-10-01 (safety-отказы исполнителей при чтении `prompt.txt` —
falsify-03/noskill, goalking-vs-aos-02/v-goalking, implement-01/noskill,
implement-01/v-executing-plans, implement-02/v-implement,
implement-03/v-executing-plans, jtbd-01/v-jtbd, pizdej-02/v-pizdej,
playwright-01/noskill, playwright-02/v-playwright-cli,
rules-and-hooks-maintenance-01/v-full), закрыты перестейджем 2026-10-02:
промпты переформулированы (разрешение Георгия 2026-10-02 ~07:55 WEST),
семантика заданий, фикстуры и формат финального ответа сохранены, модель
прогонов та же (`muse-spark-subagent`), судейство — agy/Gemini. Конвейер по
каждому перестейдж-рану: assemble-restage → blind → oracle → oracle-full →
llm-grade → verify-blind (PASS) → aggregate; детали — `wave2-<cmp>/eval-report.md`,
§10 каждого отчёта.

**Оговорка сравнимости (важно).** 11 ячеек получены переформулированными
промптами; строгое A/B с ячейками раунда 1 невозможно. Дельты ниже читаются
качественно: программный оракул — по-прежнему авторитетная метрика,
LLM-оценки — вторичные. Вердиктов insufficient-data «по причине не исполненных
ячеек» больше нет (0); остались 2 по другой причине — mood-board-builder и
theme-factory (задачи не дискриминировали).

`verify-blind`: PASS во всех 11 сравнениях. Конвейер по каждому сравнению:
assemble → blind → oracle → oracle-full → llm-grade → verify-blind → aggregate;
отчёты — `wave2-<cmp>/eval-report.md`, детали — `wave2-<cmp>/programmatic/*.json`.

**Чистка фантомных артефактов (2026-10-02, координатор досборки).** Сборка
2026-10-01 21:51–21:56 записала в 7 основных директорий сравнений артефакты по
11 не исполненным тогда ячейкам: пустые `blind/<label>/transcript.md` (в 2
случаях — лог safety-блокированной попытки), `oracle/` и `programmatic/` с
FAIL «по отсутствию данных», `grades/` — оценки пустых транскриптов, и
соответствующие FAIL-строки в `results*.csv`. Эти данные противоречили
методологии («неисполненная ячейка — отсутствие прогона, не FAIL») и
маскировали бы реальные результаты рестейджа. Все 65 фантомных файлов/строк
удалены из основных директорий (манифесты и CSV пересобраны только из
реальных замеров раунда 1; verify-blind после чистки — PASS везде);
оригиналы сохранены в recoverable `/tmp/w2b1-phantom-trash/`. Реальные данные
рестейджа — только в `wave2-<cmp>-restage/`, сводный вид — в §10 отчётов.

## Результаты по сравнениям (программный оракул, только исполненные ячейки)

| Сравнение | Baseline (noskill) | Скилловые варианты | Дельта |
|---|---|---|---|
| bouncer | T1 FAIL, T2 PASS, T3 PASS | v-bouncer: T1 FAIL, T2 FAIL, T3 PASS | **отрицательная** (регресс на T2) |
| falsify | T1 PASS, T2 PASS, T3 FAIL* | v-falsify: T1 PASS, T2 PASS, T3 FAIL | паритет, положительной нет |
| goalking-vs-aos | T1 FAIL, T2 FAIL, T3 PASS** | v-goalking: T1 FAIL, T2 FAIL*, T3 PASS**; v-aos: FAIL/FAIL/PASS** | не доказана (полный паритет) |
| graphify-vs-graphifypypi | 0/3 | v-graphify-skill 0/3; v-graphify-pypi 1/3 (T2) | **инструмент > скилл** |
| implement-vs-executing-plans | T1 PASS*, T2 PASS, T3 PASS | v-implement: 3/3 PASS (T2*); v-executing-plans: 3/3 PASS (T1*, T3*) | полный паритет 9/9, гипотеза поглощения измерена |
| jtbd-vs-jtbd-scenarium | T1 PASS, T2 PASS, T3 PASS | v-jtbd: T1 FAIL*, T2 FAIL, T3 PASS; v-jtbdscen: T1 PASS, T2 FAIL, T3 PASS | **отрицательная** (v-jtbd — T1* и T2; v-jtbdscen — T2) |
| moodboard-vs-themefactory | T1 FAIL, T2 PASS, T3 PASS | оба варианта — идентично baseline | не измерена (потолок+пол задач) |
| pizdej | T1 PASS, T2 PASS, T3 FAIL | v-pizdej: T1 PASS, T2 PASS*, T3 FAIL | полный паритет |
| playwright-vs-playwrightcli | T1 PASS*, T2 PASS, T3 FAIL | v-playwright-skill 3/3 PASS; v-playwright-cli: T1 FAIL, T3 PASS, T2 PASS* | **положительная у скилла** |
| rules-and-hooks-maintenance | infra: T1 PASS, T2 PASS; content: 2/2 | v-full: infra T1 FAIL*, T2 PASS; content 2/2 | **отрицательная на T1 (infra)** |
| sus | T1 PASS, T2 FAIL, T3 PASS | v-sus — идентично | нет |

\* ячейка перестейджа 2026-10-02 (переформулированный промпт — риск сравнимости).
\** goalking T3 — слабый PASS по порогу оракула: cycle 0.4 у всех вариантов;
mechanics: noskill 0.2222, v-goalking 0.3333, v-aos 0.2222. Субшкалы
cycle/mechanics (goalking) и infra/content (rules-and-hooks-maintenance) нигде
не усреднялись.

## Вердикты по 15 скиллам (записаны в `registry/skills-registry.yaml` с основаниями)

| Скилл | Вердикт | Основание одной строкой |
|---|---|---|
| playwright | **keep** | 3/3 PASS; единственная положительная дельта батча |
| graphify | **replace** | скилл 0/3; PyPI-инструмент выиграл единственную решённую задачу T2 |
| jobs-to-be-done | change | FAIL на T1* и ловушке T2 при PASS baseline (отрицательная дельта); wired |
| jtbd-scenarium-create | change | FAIL на T2 при PASS baseline; wired |
| bouncer | change | регресс на T2 (baseline PASS, скилл FAIL); wired |
| falsify | **change** | паритет на T1/T2; T3 — общий провал (v-falsify и baseline FAIL); положительной дельты нет; wired ×13 |
| agent-orchestrator-standard | change | полный паритет с baseline на 3/3 ячейках, побед нет |
| sus | change | полный паритет, включая общий FAIL на дискриминативной T2 |
| implement | **change** | полный паритет 9/9 со всеми вариантами (4 ячейки — переформулированные промпты); гипотеза поглощения измерена, слияние — предложение Георгию (см. ниже) |
| executing-plans | **change** | то же; в caller-map вызывающих нет |
| goal-king | **change** | дискриминативная T2 измерена*: v-goalking FAIL, паритет со всеми; положительной дельты нет |
| mood-board-builder | insufficient-data | паритет при непродискриминировавших задачах (потолок T2/T3, пол T1) |
| theme-factory | insufficient-data | то же |
| pizdej | **change** | полный паритет: T1/T2 PASS у обоих, T3 FAIL у обоих |
| rules-and-hooks-maintenance | **change** | T1 (infra): v-full FAIL* при PASS baseline — отрицательная дельта; T2–T4 паритет |

\* переформулированный промпт — риск сравнимости.

**Слияние implement/executing-plans — предложение Георгию (не действие).**
Полный паритет 9/9 на программном оракуле; сверка с `registry/caller-map.md`:
у `executing-plans` вызывающих нет, `implement` вызывается из
`rules/operational/skill-routing.md`. Решение о слиянии и любые правки
`repo/` — только по его слову.

Действия по вердиктам (правки SKILL.md, слияния, архивация, замена) — только по
слову Георгия; репозиторий скиллов в этом батче не трогался.

## Замечания по стенду и методу

1. **Баг фикстур исправлен**: `subagent_runner.py stage` не копировал фикстуры
   (нормализованный конфиг `run.py` терял `fixtures_src`/`forbidden_bins`/
   `preflight`); фикс — `_merge_raw_extras` в subagent_runner.py (run.py,
   grade.py, aggregate.py не трогались).
2. **LLM-грейдер мягок и шумит**: agy ставил 1.0 многим транскриптам, заваленным
   оракулом (сильнее всего в graphify — 8 расхождений: судья не видит требований
   провенанса tool calls). Вердикты стоят на программном оракуле — как в волне 1.
3. **Отказы исполнителей на чтении prompt.txt** — главный операционный риск
   схемы: доля росла от ~21% (пилоты) до ~37% (волны полного батча). В батче 1
   11 ячеек закрыты перестейджем с переформулированными промптами (разрешение
   Георгия 2026-10-02 ~07:55 WEST; отказов безопасности на переформулировках
   не было). Цена — оговорка сравнимости (см. «Покрытие исполнения»).
4. **n=1 на ячейку**: одиночные прогоны шумят (baseline RHM T3: FAIL в перепилоте,
   PASS в батче). Вердикты change/insufficient-data учитывают это; для keep/replace
   картина согласована по нескольким задачам.
5. **graphify T1/T3 — возможный перегиб усиления**: 0/9 у всех вариантов; пороги
   провенанса (tool-calls-prove-code-analysis) не прошёл никто, включая вариант с
   настоящим инструментом на T1/T3. Перед батчем 2 пороги стоит перепроверить.
6. **goalking T3 — слабый порог PASS оракула** (оба субскора > 0): PASS при
   cycle 0.4 / mechanics 0.22 трактовать как слабый проход, не успех.
7. pytest на машине не установлен — проверки оракулов гоняются через
   `python3 <script>` (файлы pytest-совместимы). Внешние сайты из Chromium в
   песочнице недоступны — playwright-задачи только на localhost-фикстурах.
8. Стоимость батча долларами не считается: исполнители — Spark по подписке
   (86 прогонов), судейство agy ≈ $0.2 за батч.
