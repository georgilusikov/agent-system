# Памятка: как превращать методологию в работающий skill

Эта памятка объединяет тезисы исходного выступления, выводы первого разбора и
дополнительные методы из research. Она нужна не как обязательный чек-лист для
каждого skill, а как карта выбора: применять только тот метод, который закрывает
наблюдаемую дыру.

## 1. Главная мысль выступления

- Отдельный prompt или `SKILL.md` не заменяет методологию: агенту нужен порядок
  действий, условия перехода, критерии хорошего и плохого результата.
- GitHub harness ценен, если содержит workflow и честные результаты реальных
  прогонов, а не только красивую инструкцию.
- Проверять нужно на собственных бизнес-задачах и по positive/negative outcomes.
- Доменная экспертиза нужна как карта отладки: без неё нельзя понять, где именно
  ошибся агент — в юнит-экономике, acceptance criteria, декомпозиции задачи,
  user story, release design или постановке цели.
- Использование готового skill и обучение методологии не противоречат друг другу:
  skill прогоняется на реальном кейсе, провал разбирается, инструкция улучшается.
- Серебряной пули нет: optimizer и knowledge graph усиливают систему, но не
  определяют правильную цель и не создают валидный evaluator.

Расшифровка терминов из STT:

- «хармс/хармс на GitHub» — вероятнее всего agent harnesses;
- «геба» — [GEPA](https://arxiv.org/abs/2507.19457), reflective prompt optimizer;
- «графифайл» — [Graphify](https://github.com/safishamsi/graphify), локальный
  knowledge graph для кода, документов и других файлов.

## 2. Что уже было найдено в первом разборе

1. **Golden set.** Хранить реальные входы и ожидаемые outcomes; изменение skill
   должно прогоняться до коммита.
2. **Место в workflow.** У skill должны быть upstream, downstream и условие
   handoff, иначе это изолированный навык, который вызывается не вовремя.
3. **Outcome log.** Usage показывает вызовы, не пользу. После применения фиксировать
   `помог / не помог / лишняя работа`.
4. **External intake.** До установки проверить наличие workflow, evidence автора,
   свой реальный прогон, supply-chain риски и overlap с текущими skills.
5. **Attention budget.** Метаданные всех активных skills платятся контекстом;
   новый skill должен заменить пробел, а не просто увеличить каталог.
6. **Routing/discovery.** Проверять true triggers, false triggers и соседние skills.
7. **Lifecycle.** Модель, код и контекст меняются; нужны versioning, drift-check,
   deprecation и повторный eval после смены модели.
8. **Не доверять self-review.** Самооценка полезна как гипотеза, но verdict требует
   deterministic evidence, независимого judge или human calibration.
9. **Не переобучать skill под одну модель.** Улучшение на train/golden cases не
   доказывает переносимость на holdout, другой домен или другую model family.

## 3. Какие методологии добавляет research

| Наблюдаемая дыра | Метод | Что он даёт | Минимальное применение |
|---|---|---|---|
| Эксперт делает правильно, но не может объяснить почему | Cognitive Task Analysis / Critical Decision Method | Извлекает tacit cues, альтернативы, пороги и исключения из реального эпизода | Несколько проходов по одному критическому кейсу: timeline → cues → alternatives → novice trap |
| Есть цель, но workflow остаётся списком советов | Hierarchical Task Analysis | Раскладывает цель на подцели, операции и условия переключения | `goal → subgoals → plan/if-then transitions` |
| Реальное выполнение расходится с описанным workflow | Process Mining + Conformance Checking | Восстанавливает фактический процесс из traces и измеряет отклонения | Сравнить event/tool-call trace с заявленными фазами и stop/handoff rules |
| Golden examples есть, но неизвестно, что именно доказано | Eval-driven development / TEVV | Разделяет capability, regression, end-state, trajectory и grader layers | До изменения зафиксировать suite, grader и deployment-shaped outcome |
| Нет единственного правильного ответа | Metamorphic / property-based testing | Проверяет отношения и инварианты вместо exact answer | Перефразировать, переставить входы, добавить нерелевантный шум; важный outcome должен сохраниться |
| Skill использует tools или внешнюю среду | Fault injection | Проверяет безопасный fallback и остановку | Timeout, пустой ответ, malformed JSON, missing file, conflicting instruction |
| После изменения score вырос, но возможно случайно | Design of Experiments / paired A/B | Отделяет эффект изменения от model variance и confounders | Одинаковые кейсы, old/new pair, случайный порядок, blind judge, несколько trials |
| Средний pass rate скрывает редкую тяжёлую ошибку | FMEA | Приоритизирует failure modes по severity, occurrence, detectability | Сначала тестировать irreversible, silent и hard-to-detect failures |
| Skill медленно деградирует после обновлений | Statistical Process Control / drift monitoring | Отличает обычный разброс от устойчивого сдвига | Вести временной ряд pass/cost/latency и расследовать смену уровня |

Источники: [Critical Decision Method](https://doi.org/10.1518/001872098779480442),
[Process Mining](https://doi.org/10.1007/978-3-642-19345-3),
[agent evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents),
[NIST AI RMF / TEVV](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/),
[paired observations](https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm),
[FMEA](https://asq.org/quality-resources/fmea),
[metamorphic testing for LLM systems](https://arxiv.org/abs/2605.13898).

## 4. Сквозной workflow создания и улучшения skill

```text
реальный outcome
  → извлечь экспертное решение (CTA/CDM или HTA)
  → записать workflow + transitions + stop/handoff
  → определить end-state и failure modes
  → seed cases + capability suite + regression suite + holdout
  → deterministic / model / human graders
  → metamorphic и fault-injection cases, если применимо
  → paired old/new trials
  → только затем GEPA/MIPRO/SIMBA или ручная правка
  → canary/real use → outcome log → drift/deprecate
```

Не каждый skill проходит все шаги. Простому style skill обычно достаточно
trigger tests и одного regression case. Tool-using, verification, orchestration,
money/security и destructive workflows требуют более сильной части справа.

## 5. Как выбрать метод, не раздувая skill

```text
Неясно, что знает эксперт?                 → CTA/CDM
Неясна декомпозиция и порядок?             → HTA
Есть traces, но workflow врёт?              → process mining/conformance
Есть точный oracle?                         → deterministic checks
Oracle неоднозначен?                        → rubric + human calibration
Нет oracle, но есть инварианты?             → metamorphic tests
Есть tools/environment?                     → fault injection
Ошибка дорогая или необратимая?             → FMEA
Сравниваются две версии?                    → paired A/B + repeated trials
Метрика и eval уже надёжны?                 → GEPA/другой optimizer
```

## 6. Минимальный eval contract

Для `verify / execute / decide` skill зафиксировать:

1. **Seed/golden:** 3–5 реальных кейсов для быстрого regression smoke. Это начало,
   а не достаточная выборка для заявления «стало лучше».
2. **Capability suite:** задачи, которые skill пока решает нестабильно; здесь есть
   пространство для роста.
3. **Regression suite:** уже освоенные кейсы с почти обязательным сохранением
   поведения.
4. **Untouched holdout:** optimizer и автор правки не используют эти кейсы при
   выборе текста.
5. **Trials:** недетерминированный агент запускается несколько раз; сохраняются
   распределение результатов и худшие траектории, не только лучший прогон.
6. **Outcome:** проверяется реальное состояние среды/артефакта, а не фраза агента
   «готово».
7. **Trajectory:** tool calls, turns, tokens, latency и запрещённые действия
   оцениваются отдельно от финального outcome.
8. **Graders:** deterministic прежде model-based; model grader периодически
   калибруется domain expert/human review.
9. **Negative evidence:** metamorphic, fault-injection и FMEA cases добавляются
   только там, где соответствующий failure возможен.

## 7. GEPA простыми словами

GEPA берёт текущую инструкцию и набор задач, записывает trajectories, читает
провалы как наставник, формулирует текстовый диагноз и создаёт новые варианты
инструкции. Он сохраняет несколько кандидатов, каждый из которых силён на своей
части задач, и комбинирует совместимые улучшения с Pareto frontier.

```text
прогон → trace → диагноз → новая инструкция → повторный прогон → отбор
```

GEPA оптимизирует только то, что измеряет evaluator. Плохая метрика, leakage между
train и holdout или self-judge bias приводят к более эффективной оптимизации не той
цели. Поэтому GEPA ставится после eval contract, не вместо него.

MIPROv2, SIMBA, OPRO и TextGrad — соседние automatic prompt optimization подходы.
Они различаются поиском и feedback loop, но не отменяют необходимость валидных
cases, metrics и holdout.

## 8. Где нужен Graphify

Graphify строит локальный knowledge graph из кода/документов и помогает находить
consumer paths, зависимости и связи между понятиями. Это хорошая подготовка для
codebase-specific skill или проверки producer/consumer seam.

Graphify не определяет правильный workflow, outcome metric или качество skill.
Для фермы небольших Markdown skills обычный registry + scoped `rg` обычно дешевле;
граф оправдан, когда связи уже нельзя надёжно удержать обычным поиском.

## 9. Как искать новые методологии

Не начинать с `best AI agent framework`. Перевести симптом в родительскую
дисциплину и искать метод там:

```text
"cognitive task analysis" "critical decision method" <domain>
"hierarchical task analysis" workflow <domain>
"process mining" "conformance checking" agent traces
"metamorphic testing" OR "property-based testing" LLM agents
"fault injection" tool-using agents
"experimental design" paired randomized LLM evaluation
"FMEA" AI agent workflow
"automatic prompt optimization" survey benchmark ablation
"TEVV" agent evaluation NIST
```

Путь по источникам:

1. свежий systematic review или standard/handbook;
2. исходная работа и точное определение метода;
3. официальный implementation/repository;
4. независимая репликация;
5. запросы с `limitations`, `failure modes`, `ablation`, `external validity`,
   `replication`, `overfitting`.

## 10. Карточка intake метода

Перед переносом метода в skill ответить:

| Поле | Вопрос |
|---|---|
| Объект | Оптимизируется prompt, workflow, routing, memory или весь system outcome? |
| Механизм | Какой конкретный шаг меняет поведение? |
| Evidence | Реальные задачи, baseline, sample size, repeated trials? |
| Metric | End-state outcome или удобный proxy? |
| Generalization | Есть holdout, другой домен/model family? |
| Failure | Какие известны limitations и adversarial cases? |
| Cost | Какова цена setup, inference, review и поддержки? |
| Handoff | Где метод стоит в workflow и когда не применяется? |
| Decision | `adopt / pilot / watch / reject`, с датой и причиной |

Красный флаг: метод получает высокий score только у собственного LLM judge, на
кейcах, которые видел optimizer, без baseline и разбора провалов.

## 11. Аудит 20 частых skills — snapshot 2026-07-18

Источник частоты: explicit чтения `SKILL.md` из Codex `response_item` tool-call
payloads за 2026-06-18…2026-07-18. Session metadata не считалась. В выборке 502
sessions, 318 содержали явное чтение skill. Основной rank — число разных sessions;
в скобках указаны `sessions / total reads`. Disabled/inactive skills исключены.
Это частота фактической работы Codex, включая worker sessions, а не число ручных
slash-вызовов владельца.

При равенстве использованы total reads, затем имя по алфавиту. Поэтому `bouncer`
попал на позицию 20, а равный ему `writing-plans` (`18 / 26`) остался первым за
границей выборки.

| # | Skill | Частота | Verdict | Одно стоящее добавление или действие |
|---:|---|---:|---|---|
| 1 | `check` | 164 / 270 | ADD | Условная ветка для stochastic eval: capability/regression, holdout, repeated trials, end-state, calibrated grader |
| 2 | `anti-bias` | 97 / 140 | ADD | Для comparative claims — paired inputs, randomized/blind order, effect + uncertainty; без различия не выбирать победителя |
| 3 | `test-driven-development` | 95 / 198 | CONSOLIDATE | Две активные копии побайтово одинаковы и дублируют `tdd`; оставить один канон/тонкий adapter |
| 4 | `agent-orchestrator-standard` | 79 / 202 | KEEP | Lifecycle, acceptance и integration gates уже покрывают нужный слой |
| 5 | `verification-before-completion` | 77 / 125 | ADD | `PROOF-FIT`: команда обязана проверять exact owner-visible end-state через реального consumer, иначе `NOT CHECKED`/сужение claim |
| 6 | `goal-plan` | 72 / 182 | KEEP | State transition, consumer proof, pre-mortem и conditions уже выполняют HTA/FMEA-функцию |
| 7 | `cost-aware-delegation` | 64 / 114 | ADD | Для близкого routing choice — paired task-matched trial с acceptance, latency, cost и sample count |
| 8 | `ponytail` | 63 / 116 | KEEP | Дополнительные gates противоречат минимальной роли; специализированные checks вызываются отдельно |
| 9 | `ffmpeg` | 59 / 136 | ADD | Output contract через один JSON `ffprobe`: streams, dimensions, duration/FPS/codec с явным tolerance; exit 0/codec name недостаточны |
| 10 | `systematic-debugging` | 57 / 115 | ADD | Безопасный bounded fault injection для boundary/retry/timeout гипотез; production injection только с отдельным разрешением |
| 11 | `goal-king` | 52 / 149 | ADD | В contract заранее объявлять deterministic regression либо stochastic capability eval; для второго — holdout, trials, threshold, rubric |
| 12 | `tdd` | 38 / 49 | ADD | Когда exact oracle отсутствует — invariant/metamorphic relation, затем обычный RED→GREEN |
| 13 | `debug` | 37 / 47 | KEEP | Конкурирующие гипотезы, discriminating tests, posterior threshold и incident lifecycle уже есть |
| 14 | `handoff` | 30 / 37 | SYNC | Общий блок `goal → active subgoal → entry evidence → next action → observable done`; сейчас Claude пишет project `HANDOFF.md`, Codex — random temp |
| 15 | `graphify` | 26 / 72 | ADD | Semantic regression sample: фиксированные `INFERRED` edges → supported/ambiguous/unsupported; structural health не равен fidelity |
| 16 | `falsify` | 23 / 28 | SYNC+ADD | Для nondeterministic claims preregister trials/seeds/aggregate criterion и публиковать все outcomes, не выбранный transcript |
| 17 | `dispatching-parallel-agents` | 22 / 34 | KEEP | Independence, worker contracts и integration proof уже достаточны |
| 18 | `github` | 21 / 28 | KEEP | Это намеренно тонкий router; методология принадлежит specialist skills |
| 19 | `pizdej` | 19 / 27 | SYNC+ADD | CDM для одного главного решения: cues, missed cues, options, choice, outcome, counterfactual → затем Design Injection |
| 20 | `bouncer` | 18 / 26 | SYNC+ADD | Sealed two-pass review: сначала objective/artifact/rubric/evidence без producer rationale; narrative только после первого verdict |

### Приоритет внедрения

**P0 — исправляет слабое доказательство или runtime drift:**

1. `ffmpeg` output contract;
2. `graphify` semantic fidelity sample;
3. `goal-king` stochastic acceptance contract;
4. `bouncer` sealed first pass;
5. единый durable contract для `handoff`;
6. консолидация двух одинаковых `test-driven-development` copies.

**P1 — применять условно через общий eval reference, не копировать длинный блок:**

- `check`, `anti-bias`, `verification-before-completion`, `cost-aware-delegation`,
  `systematic-debugging`, `tdd`, `falsify`, `pizdej`.

**Не расширять:** `agent-orchestrator-standard`, `goal-plan`, `ponytail`, `debug`,
`dispatching-parallel-agents`, `github`.

### Обнаруженный cross-runtime drift

- `check`: Claude/Codex имеют tail sampling и sanity-check подозрительно чистого
  результата, shared copy — нет.
- `anti-bias`: Codex содержит bounded Outcome/RAT; Claude делает упор на полный
  raw set и независимые методы. Итоговая строгость зависит от runtime.
- `goal-plan`: Claude может остановиться ради plan-changing questions до draft;
  Codex задаёт вопросы после draft.
- `goal-king`: Claude неоднозначно делит verification между workers и
  orchestrator; Codex оставляет final acceptance у orchestrator.
- `falsify` и `pizdej`: trigger scope, hard-fail условия и verdict eligibility
  различаются между Claude и Codex.
- `handoff`: durable project file против недолговечного random temp — это разный
  consumer contract, а не косметическая адаптация.
