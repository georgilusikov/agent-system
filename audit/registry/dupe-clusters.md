# Дублетные кластеры — черновик

Статус: завершён 2026-10-01. Три разведчика отчитались; ключевые пары перепроверены лично
чтением SKILL.md; сверка с caller-map выполнена для всех кластеров.

Метод: чтение обоих SKILL.md пары, различение «одинаковая функция / пересечение / false-positive».
Сверка с caller-map: `~/workspace/audit-skillov/registry/caller-map.md`.

## 1. Вердикты по 6 парам инвентаризации

| Пара | Вердикт | Обоснование |
|---|---|---|
| frontend-ui-dark-ts / frontend-design | overlap | Общий триггер «сделай UI», разные механизмы: готовая тёмная React-система с конфигами vs арт-дирекшн-методология против «AI slop» |
| how-to-write-skills / write-a-skill | false-positive | Канон + дельта по дизайну; «This file is delta-only; canon content is not duplicated here» |
| jobs-to-be-done / jtbd-scenarium-create | overlap | Общий JTBD-домен и триггеры; разные выходы: объяснение методологии/дискавери vs генерация документа по 9-частному канону Красинского |
| thinking-theory-of-constraints / theory-of-constraints | overlap сильный | Одна модель (5 шагов Голдратта); узкая перф-линза vs широкий диагностический ранбук (decision trees, queries/, config.json). Гипотеза на слияние |
| leverage / bottleneck-identifier | false-positive | Настоящий discovery-протокол (TOC-скан, лестница Медоуз, blind-spot scan) vs пустой плейсхолдер («Execute bottleneck identifier operations», ноль механики). bottleneck-identifier — кандидат на архивацию как thin |
| landing-page-optimizer / onboarding-optimizer | overlap структурный | Общий JTBD-каркас аудита, разные домены/шаги/выходы (квиз+офер vs раскадровка+learning tax). Не дубли |

## 2. Кластер code-review-quality (проверен лично, 5 скиллов)

Состав: code-review, requesting-code-review, receiving-code-review, pizdej, ponytail.

- **requesting-code-review / receiving-code-review** — complement, не дубль: инициатор (диспатч ревьюера-субагента с git SHAs + шаблон) vs реципиент (верификация перед имплементацией, no performative agreement, pushback-протокол). Две стороны одного взаимодействия.
- **code-review / requesting-code-review** — overlap: оба в итоге гонят субагента ревьюить дифф, но разные триггеры и функции: code-review — двухоосевое ревью диффа (Standards/Spec, два параллельных субагента, методология Matt Pocock) vs requesting-code-review — протокол «когда и как запросить ревью» с workflow-интеграцией. Не дубль.
- **pizdej** — false-positive относительно ревью: самокритика собственной работы постфактум (Mode A: claim integrity перед отчётом; Mode B: процесс-рефлексия), явно НЕ ревью диффа («NOT for: … ревью диффа (/code-review)»). Тип — verification, но другой объект.
- **ponytail** — false-positive относительно ревью: персистентный режим «ленивого сеньора» (YAGNI, минимальные решения) на ЛЮБУЮ кодовую задачу; стиль/режим, не протокол ревью.

Wired-пересечения: code-review (agents/plan-critic.md, skill-routing.md) и pizdej (skill-routing.md + ~10 стандартов) — оба активны, удаление любого — разрыв; requesting/receiving/ponytail — без wired-вызывающих.

**Вывод по кластеру: 0 подтверждённых дублей, 1 overlap (code-review/requesting-code-review), 2 false-positive (pizdej, ponytail), 1 complement-пара.**

## 3. Кластер верификации (отчёт субагента, лично перепроверены ключевые пары)

Состав: check, bouncer, falsify, principles-review, verification-before-completion,
grilling, hypothesis-eval-loop, corridor-tester, performance-profiling,
security-best-practices, webapp-testing, anti-bias, sus.

### Вердикты по парам (лично перепроверены)

| Пара | Вердикт | Обоснование |
|---|---|---|
| check vs falsify | **overlap сильный** | Общие ~60–70% механики: E-ID до фактов (anti-postdiction), gap-таблица, content-depth gate 3–5 значений, калибровка уверенности, hard fail на invented evidence. Falsify сам: «orchestrator: joins /check + /debug into a single artifact ending in a Verdict». Дифференциация осознанна и записана: «ordinary artifact verification → /check is enough», stakes-gate (§0), precedent scan, runtime gate, RCA, обязательный Design Injection, вердикт PASS/PARTIAL/FAIL + новая гипотеза. Кандидат на слияние «с флагом stakes», но это изменение дизайна, не исправление ошибки |
| check vs verification-before-completion | **overlap** | VBC = Iron Law «NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE», микро-гейт момента заявления (IDENTIFY→RUN→READ→VERIFY→claim), без Expected State и gap-таблиц; check = полный протокол. Гипотеза «check lite», но VBC работает как триггер-напоминание «всегда перед любым claim», check — как протокол. Не дубль |
| anti-bias vs check | **overlap (вложенность)** | check требует anti-bias как препроцессинг («Сначала применяй /anti-bias к своим выводам»); challenge-шаг check («3 способа доказать что ты неправ») дублирует Counter-Evidence / Confirmation bias чеклист anti-bias. Гипотеза: общий debias-канон, на который ссылаются оба. Разные функции (debias vs evidence-верификация) |
| hypothesis-eval-loop vs falsify | overlap по механике, **false-positive по функции** | Сам скилл: «falsify опровергает один claim о готовом артефакте; eval-loop измеряет эффект изменения количественно на повторе одной и той же задачи». Разные объекты (claim vs изменение), объединение нецелесообразно |
| check vs bouncer | **false-positive** | Взаимные NOT-границы; bouncer: «/check всё равно обязателен». Комплементарность: свой evidence-пайплайн vs чужая модель смотрит |
| bouncer vs falsify | **false-positive** | Взаимные NOT-ссылки; мнение второй модели vs структурированное опровержение |
| grilling vs falsify | **false-positive** | Интервью пользователя (диалог, «The decisions, though, are mine») vs опровержение claim таблицами |
| principles-review vs sus | **false-positive** | Аудит соответствия META_PRINCIPLES (violation table, HEALTHY/DRIFT/CRITICAL) vs аудит роутинга и триггер-конфликтов скиллов (trigger_collisions.py). Явная NOT-граница |
| corridor-tester / performance-profiling / security-best-practices / webapp-testing | **false-positive** | Домены (UX-макеты людьми; Core Web Vitals; OWASP-гайдлайны) и инструмент (Playwright-тулкит, не протокол). webapp-testing комплементарен falsify §2.3 (добывает runtime-evidence) |

### Сверка с caller-map (лично)

- check ← 20+ стандартов/agents (outcome-designer, plan-critic, skill-routing, dev_swarm, rules-validation, verification-methods, response-clarity-golden, no-fabricated-evidence, README). Самый вызываемый скилл кластера.
- falsify ← 13+ (outcome-designer, skill-routing, agent-orchestration, hooks-safety, incident-logging, mac-mini-deploy, output-format, scope-rewrite-policy).
- anti-bias ← 8 стандартов; bouncer ← plan-critic, skill-routing, README; principles-review ← acceptance-lock, incident-parking, skill-routing; sus ← skill-routing; security-best-practices ← skill-routing.
- Без wired-вызывающих: verification-before-completion, grilling, hypothesis-eval-loop, corridor-tester, performance-profiling, webapp-testing.
- **Важно для гипотезы слияния check+falsify:** множества вызывающих частично различаются (check уникален для dev_swarm, rules-validation, verification-methods, agy-video-rca; falsify — для hooks-safety). Слияние порвёт эти ссылки — стоимость мерджа выше, чем кажется по SKILL.md.

## 4. Кластер implementation + Matt Pocock pipeline (отчёт субагента, сверен с frontmatter лично)

### Карта pipeline (подтверждена цитатами)

```
wayfinder ──(destination = «a spec to hand off»)──▶ to-spec ──▶ to-tickets ──▶ ready-for-agent (ЛЕЙБЛ, не скилл)
writing-plans ──▶ subagent-driven-development ──▶ finishing-a-development-branch
              └─▶ executing-plans ───────────────▶ finishing-a-development-branch
to-tickets ──▶ implement ──▶ code-review
test-driven-development — кросс-каттинг методология (implement: «Use /tdd where possible»;
  sdd: «Subagents should use: superpowers:test-driven-development»; user-invocable: false)
prototype — спайк-инлайн (wayfinder prototype-tickets; TDD-исключение «Throwaway prototypes»)
triage — ОТДЕЛЬНЫЙ контур: входящие внешние issues/PRs → state machine → agent brief
```

Ключевое уточнение: третье «звено» цепочки to-spec→to-tickets — это лейбл `ready-for-agent`
(«Apply the ready-for-agent triage label — no need for additional triage»), а не скилл triage.
Скилл triage обслуживает входящие внешние issues/PRs и отграничен NOT в обе стороны.

### Вердикты по парам

| Пара | Вердикт | Обоснование |
|---|---|---|
| implement / executing-plans / subagent-driven-development | overlap, не дубли | Три разные механики с явным роутингом: sdd decision-graph («stay in session? yes→sdd / no→executing-plans»); executing-plans сам уступает sdd при наличии субагентов; implement — тонкий исполнитель без оркестрации (14 строк, коммитит сам). Взаимные NOT в implement |
| to-spec / to-tickets / triage | confirmed pipeline (с уточнением) | Поток артефактов подтверждён; скилл triage — другой контур |
| wayfinder / to-tickets | false-positive | Decision tickets (вопросы, Plan-don't-do) vs execution tickets (tracer-bullet срезы) |
| wayfinder / to-spec | pipeline-предшественник | Туман→карта; destination может быть спекой для to-spec |
| test-driven-development / implement | false-positive | TDD — подключаемый кросс-каттинг слой, не режим implement |
| prototype / implement | false-positive | Взаимные NOT; throwaway-спайк без тестов vs боевая реализация |
| code-review / triage (PR-ветка) | overlap частичный | Triage верифицирует claim входящего PR сам, не вызывая code-review; входы разные |
| writing-plans → исполнители → finishing | confirmed pipeline | REQUIRED SUB-SKILL в обе стороны; finishing — терминальный хук |

### Сверка с caller-map (лично)

Wired: code-review (plan-critic, skill-routing), implement (skill-routing), prototype (skill-routing),
triage (7 стандартов), writing-plans (skill-routing).
**Без wired-вызывающих: executing-plans, subagent-driven-development, test-driven-development,
finishing-a-development-branch, to-spec, to-tickets, wayfinder** — весь Matt Pocock upstream
и оба исполнителя-оркестратора никем из экосистемы не вызываются напрямую.

### Открытый вопрос (не вердикт)

executing-plans почти полностью покрывается subagent-driven-development, и сам executing-plans
это признаёт. Оба без wired-вызывающих — держать оба или свернуть executing-plans в fallback-режим
решит волновой аудит с held-out тестами, не кабинетный вердикт.

## 5. Кластер дизайна + методик мышления (отчёт субагента, ключевые пары перепроверены лично)

### Вердикты по парам

| Пара | Вердикт | Обоснование |
|---|---|---|
| thinking-theory-of-constraints / theory-of-constraints | **confirmed-dupe (по модели и триггерам)** | Одна модель (5 шагов Голдратта), одна фирменная цитата дословно в обоих («An hour saved at a non-bottleneck is a mirage»), пересечение триггеров («speed this up», «why is this slow», «bottleneck»). Разница — упаковка: измерительный ранбук (decision trees, queries/*.sh, config.json, gotchas.md) vs когнитивная линза с worked examples. Оба полноразмерные. Ни один нельзя удалить без потери функции → **рекомендация слияние, не удаление**. Бонус: thinking-* ссылается на несуществующий `thinking-systems` (проверено — в репо нет); interior-design-expert ссылается на несуществующий `web-design-expert` — дыры роутинга |
| frontend-design / frontend-ui-dark-ts | overlap | Триггеры пересекаются («построй React-интерфейс/дашборд»), но dark-ts — зафиксированный boilerplate (Tailwind+стек+тёмная тема, `source: community`, `risk: unknown`), а не методология; прямо нарушает эстетические запреты frontend-design (Segoe UI, glassmorphism). Гипотеза: не скилл, а template |
| frontend-ui-dark-ts / tremor-design-system | overlap (доменный) | Один домен («dashboards, admin panels, data-rich UIs»), разный стек; триггер «построй дашборд» неоднозначен |
| frontend-design / web-artifacts-builder | overlap (комплементарны) | Дублируются anti-slop гайдлайны; но тулчейн (init/bundle скрипты под claude.ai HTML-артефакты) vs арт-дирекшн — складываются |
| canvas-design / algorithmic-art | overlap каркаса, не дубли | Общий манифест-шаблон («философия 4–6 абзацев → выражение», «Name the movement»); разные медиумы: статичный .png/.pdf vs генеративный p5.js-код. Два скилла оправданы; гипотеза — общий shared-фрагмент каркаса |
| landing-page-optimizer / onboarding-optimizer | false-positive (структурные близнецы) | Общий JTBD-аудит-каркас и концепт «налогов», но разные предмет/вход/шаги/метрики — не параметризуется без потери сути |
| landing-page-optimizer / design-communication-analyzer | overlap | DCA-линза (сообщение/когнитивная нагрузка) неявно внутри LPO-аудита; OO/REFERENCE.md уже ссылается на DCA |
| triz / meta / reframing-problems | overlap (слоистая архитектура) | meta явно делегирует («Не дублируй /triz»); лестница meta-диспетчер → reframing-выбор задачи → triz-роутер канона. Зону «vague problem» (triz-C8 vs reframing) стоит развести в обоих файлах |
| leverage / ToC-скиллы | overlap (by design) | leverage включает TOC-скан как §3 из 6; triz роутит «поиск горлышка без противоречия» в /leverage; шире (Медоуз + blind spots) vs глубже (5 шагов) |
| frontend-design / moai-domain-uiux | false-positive | Креатив+код vs инженерия дизайн-систем (явный NOT на кодинг) |
| frontend-design / tremor-design-system | false-positive | Tremor явно «не для general frontend» |
| leverage / bottleneck-identifier | false-positive | Discovery-протокол vs пустой сгенерированный шаблон («Execute bottleneck identifier operations») |
| interior-design-expert / кластер | false-positive | Физические интерьеры, явный NOT на web/UI |
| mood-board-builder / арт-скиллы | false-positive | Коллаж референсов (исследование) vs генерация артефактов |
| theme-factory / дизайн-скиллы | distinct | Только стилизация готового артефакта (10 пресетов); ни с чем не пересекается |

### Не скиллы, а шаблоны/библиотеки (гипотезы разведчика, поддержаны лично)

- **bottleneck-identifier** — сгенерированный SEO-шаблон без механики; кандидат на архивацию как thin (совпадает с вердиктом пары №5 из §1).
- **frontend-ui-dark-ts** — стартовый boilerplate; кандидат в templates.
- **theme-factory** — asset-библиотека с тонкой обёрткой; пограничный случай.
- **tremor-design-system** — легитимная skill-обёртка над внешней библиотекой, но хрупкая (зависит от внешнего API Tremor).

### Сверка с caller-map (лично)

Wired: leverage, meta, moai-domain-uiux, pizdej, tremor-design-system, triz (AGENTS.md, decision-alternatives-standard и др.).
**Без wired-вызывающих: ОБА ToC-скилла** (слияние дёшево — править ссылки не в чем),
frontend-design, frontend-ui-dark-ts, canvas-design, algorithmic-art, landing-page-optimizer,
onboarding-optimizer, interior-design-expert, theme-factory, web-artifacts-builder,
design-communication-analyzer, mood-board-builder, reframing-problems, bottleneck-identifier.

## 6. Аналоги на кластер (внешние, проверены)

- **code-review-quality**: reviewdog (MIT) — автоматический code review: гоняет линтеры/анализаторы и постит инлайн-комменты в PR; не LLM-ревью по Standards/Spec, но покрывает «ревью диффа автоматически» механикой, а не промптом. Прямого LLM-аналога двухоосевому ревью (Standards+Spec через субагентов) в open source не найдено.
- **verification**: promptfoo (MIT, теперь в составе OpenAI, остаётся open source) — CLI для LLM-evals и red-teaming: декларативные YAML-конфиги, матрица prompts×providers×cases, deterministic + LLM-as-judge assertions, CI-интеграция, веб-вьювер. Внешний аналог культуры hypothesis-eval-loop / регрессионного тестирования скиллов; есть готовый community SKILL.md (vezril/claude-toolkit, MIT) «regression-testing the Claude Code skills you build». Для связки check+falsify (машинные квитанции §7.5, обязательный рендер таблиц скриптом) прямого OSS-аналога не найдено — это собственная разработка экосистемы.
- **implementation / Matt Pocock pipeline**: Aider (Apache 2.0, 45K+ звёзд) — терминальный AI pair programmer: правит код в git-репо, автокоммиты с осмысленными сообщениями, repo-map, lint/test/repair loop, BYO-LLM (Anthropic/OpenAI/Gemini/Ollama). Внешний аналог связки implement+code-review на уровне инструмента, а не промпта. Сам Matt Pocock pipeline (wayfinder→to-spec→to-tickets→ready-for-agent) — third-party импорт: локальное свидетельство — зависимость от `/setup-matt-pocock-skills` и конфига `docs/agents/issue-tracker.md`, флаги `disable-model-invocation: true`.
- **design**: shadcn/ui (MIT) — не библиотека, а дистрибуция компонентов: CLI копирует исходники (Radix UI + Tailwind) в проект, код принадлежит владельцу. Прямой внешний аналог стека web-artifacts-builder (React 18 + TS + Vite + Tailwind + shadcn) и естественный ответ на вопрос «зачем свой boilerplate» для frontend-ui-dark-ts / tremor-design-system: вместо своих шаблонов — чужой зрелый CLI.
- **методики мышления**: ToC-скиллы цитируют «Цель» Голдратта (книга, не инструмент); triz — роутер над открытым корпусом TRIZ. Прямых продуктовых аналогов-«убийц» нет: это методологические промпты, их проверяет волновой аудит, а не замена инструментом.
- (раздел закрыт)

Проверенные факты:
- reviewdog — MIT, https://github.com/reviewdog/reviewdog — «🐶 Automated code review tool integrated with any code analysis tools regardless of programming language»
- promptfoo — MIT, остаётся open source после вхождения в OpenAI; CLI для LLM-evals и red-teaming, декларативные YAML-конфиги, assertions, CI-интеграция
- Aider — Apache 2.0, терминальный AI pair programmer с git-интеграцией (автокоммиты), BYO-LLM
- shadcn/ui — MIT, не библиотека а дистрибуция компонентов (copy-paste в проект), Radix UI + Tailwind CSS

## 7. Итоговые вердикты и рекомендации к следующему шагу

### Подтверждённые дубли (1)

1. **thinking-theory-of-constraints / theory-of-constraints — confirmed-dupe по модели и триггерам.**
   Одна модель, одна цитата, пересекающиеся триггеры; разная упаковка (измерительный ранбук
   vs когнитивная линза). Рекомендация: **слияние** — theory-of-constraints как каноническое тело,
   thinking-* как entry-линза/режим с явной ссылкой; не удаление (оба полноразмерные, функции
   дополняют). Оба без wired-вызывающих → слияние дёшево. Висячая ссылка на `thinking-systems`
   — дополнительный аргумент.

### Кандидаты на архивацию как thin / не-скиллы (2)

2. **bottleneck-identifier** — пустой сгенерированный шаблон, ноль механики, без wired-вызывающих.
   Пересечение с leverage только лексическое. Рекомендация: архивировать.
3. **frontend-ui-dark-ts** — boilerplate, не протокол (`source: community`, `risk: unknown`).
   Рекомендация: перенести в templates, триггер сузить до «инициализация тёмного дашборда»;
   триггер «построй дашборд» сейчас неоднозначен с tremor-design-system.

### Сильнейшие overlap — кандидаты на слияние/общий фрагмент (5)

4. **check / falsify** — ~60–70% общей механики; falsify = check+debug+вердикт для high-stakes.
   Гипотеза: слои одного протокола с флагом stakes. Риски: дифференциация осознанна
   («ordinary verification → /check is enough»); множества wired-вызывающих частично различаются —
   слияние порвёт ссылки. Решение — только после волновых тестов.
5. **check / verification-before-completion** — VBC как «check lite» для мелких шагов.
   Риск: VBC работает как триггер-напоминание, check как протокол; слияние может убить простоту вызова.
6. **anti-bias / check** — вынести общий debias-блок в канон, оба ссылаются (challenge-шаг check
   дублирует Counter-Evidence чеклист).
7. **canvas-design / algorithmic-art** — общий манифест-каркас в shared-фрагмент, тела раздельные.
8. **landing-page-optimizer / onboarding-optimizer** — общий JTBD-аудит-каркас в shared-фрагмент;
   скиллы оставить оба (домен-специфика не параметризуется).

### Подтверждённые pipeline (не дубли, документировать как цепочки)

- wayfinder → to-spec → to-tickets → **лейбл** ready-for-agent (не скилл triage); triage — отдельный
  контур входящих issues/PRs.
- writing-plans → subagent-driven-development / executing-plans → finishing-a-development-branch;
  to-tickets → implement → code-review; requesting ↔ receiving code-review — комплементарная пара.

### Открытые вопросы для волнового аудита (не решать кабинетно)

- executing-plans vs subagent-driven-development: держать оба или свернуть executing-plans в fallback?
  Оба без wired-вызывающих; решит held-out тест «исполни план» с грейдингом результата.
- Дыры роутинга: `thinking-systems` (из thinking-theory-of-constraints) и `web-design-expert`
  (из interior-design-expert) отсутствуют в репо — битые ссылки.
- moai-domain-uiux и tremor-design-system ссылаются на отсутствующих соседей семейства
  (moai-domain-frontend, moai-library-shadcn) — маркеры внешнего каталога, проверить полноту импорта.

### Методологическая пометка

Ни один «overlap» выше не доказан как избыточность: пересечение механики ≠ одинаковый результат.
По плану аудита каждый кандидат на слияние/архивацию идёт в волны с held-out наборами и слепым
грейдированием; этот документ — только карта подозрений, не приговор.
