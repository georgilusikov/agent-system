---
name: goal-king
description: 'Use for autonomous multi-wave completion of a roadmap or large goal. Triggers: "goal king", "гол кинг", "закрой roadmap", "доведи до конца", "работай автономно до цели". NOT for: один бриф одному исполнителю (/delegate), только план и гейты без исполнения (/goal-plan), механика lanes/worktree/мониторинга внутри одной волны (/agent-orchestrator-standard).'
disable-model-invocation: true
---

# Goal King — автономный цикл волн до закрытия цели

Дирижёр поверх существующих скиллов: `/goal-plan` (гейты до старта) →
волны → `/delegate` (бриф каждого lane) → verify → merge → следующая волна.
Ничего из них не дублирует — добавляет ЦИКЛ, anti-stall политику и контроль
отклонения траектории. Один вызов = движение до completion criteria или
до жёсткого блокера, без «Should I continue?» между волнами.

**Shared canon.** Этот файл — единственный источник правды для Claude Code и
Codex (`~/.claude/skills/goal-king/` — реальная папка, путь в `~/.codex/skills/`
— симлинк на неё). Никаких ручных синхронизаций «EN-адаптации» больше нет.

## Назначение

Skill нужен когда уже прозвучало:
- `агент останавливается на каждом баге / при росте scope`
- `хочу поставить и уйти, а он сам тестирует и чинит`
- `roadmap большой, задач много, до конца никто не доходит`
- `он крутился долго, но сделал не то` (пост-фактум)

и надо дойти до цели с минимальным отклонением траектории: не стоять,
но и не делать лишнего.

## When to Use

- `закрой этот roadmap / бэклог`
- `goal king: <большая цель>`
- `доведи проект до <состояния> автономно`
- задача > 3 независимых подзадач И нужна делегация

## When NOT to Use

- Одна задача / один исполнитель → `/delegate`
- Есть детальный линейный план, исполнители = Claude-субагенты →
  `/subagent-driven-development`
- Цель ещё не ясна, нужен только план → `/goal-plan`
- Long unattended wait/monitoring → separate task or automation, not the working session

## Input checklist

- [ ] Есть цель ИЛИ roadmap-файл (если цель размыта — сначала §1 контракт)
- [ ] Репозиторий git, рабочее дерево чистое (`git status`)
- [ ] Известен бюджет: сколько волн/часов пользователь готов дать сессии
- [ ] Для media/signal-проектов: есть 1 реальный образец контента для canary

## §1. Expected State (контракт + state-файлы)

Прогони гейты `/goal-plan` (Freshness → Real Objective → Ponytail →
**Clarifying Questions**: до 5 план-меняющих вопросов через AskUserQuestion
ДО фиксации contract.md и ДО первого брифа — не хвостом после готового
плана; после старта волн вопросы только destructive/платное/👤).
Результат зафиксируй в файлах — контекст сессии не переживает compaction,
файлы переживают:

```
.goal-king/
├── contract.md   # real_objective, forbidden, write_scope,
│                 # completion_criteria (проверяемые командой!), бюджет волн
├── ledger.md     # ## Wave N: lanes → исполнитель → verdict → commit
└── backlog.md    # найденное по пути, но НЕ в контракте (не делаем сейчас)
```

**Пиши contract.md по `references/contract-template.md`** — шаблон снят с
прогона, давшего ноль дрейфа (`backlog.md` = «none yet»), и там же разбор
против прогона, где контракт переписывался трижды. Главное правило шаблона:
каждое поле — число, имя файла/теста или команда. Прилагательное в контракте
= открытая степень свободы = пустая волна.

Обязательные поля contract.md сверх целей:
- **baseline_fails:** точный список тестов, красных ДО старта — их не
  чинить и не считать регрессией; «green» волны = ровно этот baseline.
- **known_blockers:** импорт из прошлых RCA/аудитов проекта (битые ассеты,
  ненадёжные каналы); перед дорогим шагом (rerender, батч, деплой) —
  сверка со списком, не переоткрывать опытом.
- **owner_queue:** марки задач — ☁️ воркер / 🔁 код воркер + proof
  владельцу / 🏠 машина-ключи владельца / 👤 продукт-решение.
  🏠 и 👤 НЕ диспатчатся: копятся в очередь, отдаются отчётом волны.
- **capability_cache:** статус провайдера/канала + evidence пиши в
  `contract.md`; мёртвые каналы (Google quota=0, AGY audio unavailable,
  известная поломанная форма запуска) кэшируй на 24ч. Внутри TTL канал НЕ
  перепробовать — сброс только явным решением владельца.

**Авторизация владельца держится на весь активный контракт.** Прежде чем
спросить ещё раз — перечитай `contract.md` и ledger. Обратимый внутренний выбор
внутри авторизованного scope (тест, хелпер, продюсер, алгоритм, локальный ассет)
— решение оркестратора, а не гейт владельца: реши и залогируй.

**Каждая завершённая волна дописывает одну строку только из наблюдённого**
(неизвестное — `n/a`, не догадка):

```text
Efficiency: wall_sec=... model_rounds=... tool_calls=... input=... cached=...
output=... workers=... retries=... owner_corrections=... acceptance_failures=...
```

Единица оптимизации — принятый milestone, не тред и не отдельный вызов.
**Отчитывайся только переходами:** старт/конец волны, блокер, гейт владельца.
Не пересказывай раунды модели, проценты сьюта и прогресс воркеров.

Добавь `.goal-king/` в `.gitignore`. Completion criteria сильнее чем
«команда прошла»: именованный артефакт + acceptance-команда на него.
**Red-test критериев:** прогони completion criteria на текущем состоянии
ДО работ — обязаны FAIL. Зелёные до старта = ничего не измеряют, перепиши.
То же для acceptance каждого lane при нарезке волны.

## §2. Нарезка волны

Из roadmap выбери следующую волну: только задачи БЕЗ cross-зависимостей
между собой, сгруппированные по file ownership (два lane не трогают один
файл — rules/parallel-agents.md). Каждый lane = бриф по `/delegate`
(эталон → запреты → задача → ACCEPTANCE) со схемой секций
CONTEXT / TASK / CONSTRAINTS / DONE WHEN / VERIFY / OWNED FILES.
DONE WHEN и VERIFY обязательны — их отсутствие = главная причина стопов
исполнителя («не знает, когда хватит») и расползания scope.

**Максимизируй ширину волны:** не бери первую группировку — активно ищи,
можно ли разрезать крупный lane на 2+ независимых (по файлам/модулям).
Guard: режь только если куски НЕ делят файлы и каждый крупнее стоимости
своего брифа (1 файл / 15 минут → не отдельный lane).

**Effort scaling** (калибруй вниз, не только вверх): простая подзадача =
1 lane; сравнение/средняя = 2-4; максимум 5. Волна из 5 lanes на простую
цель = сожжённые токены, не скорость.

**Интерфейсы решает оркестратор, не воркеры:** file ownership защищает от
конфликтов записи, но не решений — два lane примут разные неявные
допущения (формат, сигнатура, стиль), оба зелёные по отдельности, вместе
несовместимы. Всё cross-lane (схемы, сигнатуры, форматы файлов) зафиксируй
В брифах до dispatch; воркер не выбирает то, что видит другой lane.

**Батчи по дорогому потребителю, не по симптому:** перед полным сьютом,
рендером, батчем, деплоем или media-ревью собери ВСЕ подтверждённые фиксы
корневых причин, которые бьют в один и тот же финальный артефакт/потребитель и
совместимы по записям. Красные тесты и вердикты держи раздельно по причинам, но
за дорогой гейт плати один раз. Непроверенная гипотеза в батч не попадает.

**Rerender queue gate:** перед мутацией финального артефакта пересмотри контракт,
ledger и текущую очередь RCA на известные фиксы, которые всё равно инвалидируют
тот же хеш. Впервые найденный пост-рендерный дефект — следующая волна; известный
пред-рендерный дефект не оправдывает ещё один избежимый рендер.

Волна ≤5 write-lanes. Больше пяти → раздели на две волны; НЕ вводи слой
«менеджеров» — суб-оркестратор спавнится только если волна физически
не влезает (отдельный субагент на изолированный кусок roadmap).

## §3. Dispatch (Meta-rules — applies to ANY agent: internal, AGY, Grok, Codex, etc.)

**Core meta-rule (never violate):** Orchestrator is ONLY a brief-writer + dispatcher + verifier. It NEVER implements, NEVER writes production code, NEVER does deep manual analysis that can be delegated.

### 3.1 Strict role separation (with cheap subagent bias)
- Orchestrator writes briefs, launches dispatch, runs acceptance commands from the brief, reads evidence files, and makes high-judgment decisions.
- **All other work** → delegated lanes. This includes: verification, counting, table building, simple analysis, cross-checks, log grepping, evidence gathering, report drafting.
- **Mini-first policy (critical for speed):** For any read-only, low-judgment, or preparation task use the cheapest capable model first (GPT-54 mini / Spark / equivalent). Reserve heavy models (Opus, Grok Build, etc.) only for real write-work or complex judgment.
- All complex work (analysis, code, root-cause, reports) → delegated lanes.
- If every available channel fails for a task → stop or ask owner. Do **not** do the work yourself.

### 3.2 Parallel bias (default)
- When decomposing a phase, first try to split into independent lanes by file ownership / run / concern.
- Launch all independent lanes in one step when possible.
- Use separate worktrees or output files for write-lanes.

### 3.3 Ledger-first, minimal re-work
- Before any re-check or re-read: consult the ledger + key artifact files first.
- State lives in files (`.goal-king/ledger.md`, reports/, /tmp/evidence/), not in conversation history.
- Re-exploration only when ledger explicitly says "data may be stale".

### 3.4 Bounded briefs for every agent (meta template + cheap delegation)
Every brief must contain:
- Scope (exact files/runs only)
- Ethalon / Expected output (on 1 real example)
- Constraints / Forbidden (no src edits, no live spend, etc.)
- Task + steps
- **Explicit mini-delegation**: "For all read-only verification, counting, table building, simple cross-checks — use cheapest mini model (GPT-54 mini / Spark). Do not use heavy model for this."
- ACCEPTANCE commands (what orchestrator will run to verify)
- Owned files / output location

When writing a brief, always carve out cheap sub-tasks for mini agents in parallel.

### 3.5 External / any-agent channel hygiene (general, not Grok-only)
For any external CLI or subagent:
- Never paste previous logs, history, or large context into the prompt.
- Always prepare prompt in a file first (`/tmp/<lane>-brief.md`), then `cat` it.
- Cap tool output; write long stdout/logs to `/tmp`, return only a summary + path.
- Use appropriate `--max-turns` (higher for multi-step).
- Ask for durable output (write to specific file + short status only).
- Test task (preflight) before any real lane on a new/fragile channel.
- After 2 transport/execution failures on the same channel for the same symptom → automatic fallback + record pattern. Do not retry the broken pattern.

### 3.6 Fallback & channel failure
- Define fallback order per task type in the wave plan.
- On repeated failure of a channel: switch, do not keep feeding it the same bad context.

- **Write-lane** → свой worktree + своя ветка, один исполнитель
  (rules/parallel-agents.md). Первый Edit — verify маркером, что правка
  легла в worktree-путь, не в main checkout.
- **Read-lane** (ревью, разведка, аудит) → параллель без worktree безопасна.
- Исполнители и модели НЕ хардкодить — роутинг по
  `~/.codex/skills/cost-aware-delegation/references/capability-registry.md`
  (цена/скорость/качество/надёжность + verified launch-флаги).
- Claude-субагенты → Agent tool, `run_in_background`. Внешние CLI
  (codex/cursor-agent/agy) → Bash + watchdog
  (`perl -e 'alarm shift; exec @ARGV' <sec> …` — на macOS нет `timeout`).
  Workflow/Agent-тул shell-out НЕ умеет — внешние CLI только через Bash.
- Новый канал → одна тестовая задача до пакета (`/delegate` §4 preflight).
- Крупный многошаговый lane на транспорте с нативным goal/thread-созданием →
  диспатч lane КАК Goal-сессии: бриф lane = контракт этого воркера
  (objective, DONE WHEN, VERIFY, owned files). Мелкие ограниченные lanes —
  one-shot exec. Acceptance всегда у оркестратора.
- Между dispatch и результатами оркестратор СПИТ: фоновые воркеры сами
  будят его по завершении. Не поллить статусы впустую; watchdog покрывает
  зависших.

## §4. Verify — реальные тесты, не self-report

- Verdict исполнителя («done», зелёный статус) = claim. Оркестратор САМ
  гонит acceptance-команду каждого lane: `ls` / `grep` / `pytest` / diff.
- Wave-end: полный тест-сьют (против `baseline_fails`), не только targeted
  наборы lane'ов — integration-регрессии всплывают только на сочетании веток
  (rules/merge-queue-checkpoints.md). Исключение: хеш интегрированного дерева
  совпал с деревом, уже записанным как полностью протестированное → полный
  сьют не гоняй, прогони acceptance изменённого шва.
- Media/signal-проекты (рендер, аудио, кодеки): canary на РЕАЛЬНОМ
  контенте обязателен — синтетические фикстуры маскируют content-баги.
  Ревью визуального выхода — отдельный read-lane (модель для видео — по
  capability-registry).
- Review-lane (второй агент) ДОПОЛНЯЕТ acceptance, не заменяет: вердикты
  LLM-агентов коррелированы (2 подтверждения ≠ 2× уверенность), команда —
  единственный не-claim. Второй агент — только для суждений, которые
  команда не измеряет (качество видео/кода).
- Найден баг → сначала probe/тест, воспроизводящий его, потом фикс-lane.
- Test-critic lane (бесплатный verifier, напр. AGY): диспатчит ОРКЕСТРАТОР
  на RED, параллельно реализации, неблокирующе. Находки до интеграции →
  fix-lane; после → backlog. Рискованный шов (shared producer/consumer,
  деньги, provider, media, прошлая регрессия) → интеграция ЖДЁТ вердикт.
  Воркер НЕ вызывает критика сам: воркер гоняет команды (pytest/lint/
  mutation), LLM-суждения диспатчит оркестратор; пересказанный воркером
  вердикт критика = self-report.

## §5. Anti-stall — движение без остановок

- Lane упал → quarantine: structured reason в ledger (permission gate?
  timeout? неверный бриф? конфликт файлов?) → почини БРИФ → re-dispatch.
  Максимум 2 попытки на lane, затем смени исполнителя/модель.
- 2 смены не помогли → lane паркуется в backlog.md с причиной, волна
  ПРОДОЛЖАЕТСЯ по остальным lane'ам. Один lane не блокирует волну.
- **Consensus-эскалация — смена ВОПРОСА, не канала.** Смена исполнителя лечит
  «канал плохой»; она бессильна, когда неверен сам вопрос. Эскалируй в
  `/fusion`, если верно хоть одно: два прогона упали на ОДНОМ корневом
  вопросе · уверенность в следующем шаге < 0.65 И неопределённость меняет путь
  реализации · шаг irreversible (прод, деньги, миграция, публикация,
  удаление данных) · при нарезке волны развилка из нескольких правдоподобных
  архитектур с большим blast radius.
  НЕ эскалировать: форматирование, косметика, оценки трудоёмкости, ещё один
  раунд с ТЕМ ЖЕ контекстом. Новых данных нет — сначала spike/probe, он же
  всегда идёт ПЕРЕД эскалацией, если отвечает на вопрос дешевле.
  Бюджет: ≤1 эскалация на lane (сброс только при новом блокере, меняющем
  материальный вопрос) и ≤1 финальная на волну. Решение + отвергнутые
  альтернативы — строкой в ledger, иначе следующая волна переоткроет спор.
- **Волна FAIL:** ≥50% lanes запаркованы → СТОП цикла, отчёт пользователю.
  Массовый park = системная причина (протухшие флаги, битый канал, кривой
  контракт), а не 5 разных случайностей — следующая волна повторит то же.
- Формальный FAIL runner'а (timeout) ≠ реальный FAIL — верифицируй по
  файлам перед quarantine.
- Вопрос пользователю только: destructive-действие, платное/внешнее,
  реальное изменение scope контракта. Всё остальное — решай и логируй
  решение в ledger.
- **Перед остановкой или пометкой «заблокировано» докажи, что КАЖДЫЙ
  оставшийся lane контракта упёрся в жёсткий гейт.** Повторить владельцу тот же
  вопрос — не работа: запаркуй этот lane и двигай другой. Перекат контекста
  (compaction) — это `partial/active`, никогда не `blocked`.

## §6. Anti-drift — минимальное отклонение траектории

- Начало КАЖДОЙ волны: перечитай `contract.md`. Каждый lane волны обязан
  мапиться на пункт roadmap/контракта — не мапится → не диспатчится.
- Найдено по пути «хорошо бы ещё X» → строка в `backlog.md`, НЕ lane.
  Расширение scope без явного решения пользователя запрещено.
- **Контракт неизменяем после первой волны.** Запрет на lane вне контракта
  бесполезен, если можно переписать сам контракт — это обход, а не
  соблюдение. Критерии, бюджет, политика диспатча, промты исполнителей
  после старта не редактируются: криво сформулировано → OWNER_QUEUE,
  бюджета мало → STOP + отчёт, не новое число в файле. Прошлый контракт
  при новом прогоне не перезаписывается (`Prior run of record: … NOT
  overwritten`), новый прогон — новый файл с датой.
- **Волна с `Cost: 0 dispatches`, продукт которой — новая версия контракта,
  промта или политики, считается пустой.** Одна = предупреждение в ledger,
  две подряд = цикл встал, СТОП и отчёт владельцу. Мета-работа над
  собственными правилами не является прогрессом по цели.
- Ledger = decision log: решение → причина, одной строкой. Перед
  разворотом решения — сверься с ledger (flip-flop gate).
- После compaction: ledger + `git log` главнее собственной памяти —
  завершённые волны не передиспатчивать.

## §7. Цикл и завершение

```
while (completion_criteria не PASS && бюджет волн не исчерпан):
    §6 перечитай контракт → §2 нарезка → §3 dispatch →
    §4 verify → merge lanes (verify-merge при конфликтных файлах) →
    cleanup: worktrees remove + ветки волны delete →
    отметь волну в ledger + чекбоксы roadmap
```

Resume после смерти сессии: сначала `git worktree list` — осиротевшие
worktrees незавершённой волны убрать или переиспользовать осознанно,
не диспатчить новые поверх.

**Один ход = одна связная волна или реальный жёсткий гейт.** Не заканчивай ход
после безопасного микрошага, когда следующее действие в scope известно —
ставь commentary-чекпоинты и продолжай в том же ходе. На жёстком лимите
контекста: доведи безопасный milestone → обнови компактный ledger → дай
compaction произойти → перечитай компактное состояние и текущий diff →
продолжай в ТОЙ ЖЕ задаче. Новый тред/сессия — только по явной просьбе
владельца или при доказанном отказе платформы.

**Cost circuit breaker:** мульти-агентный прогон ≈ 15× токенов чата —
оправдан только на high-value целях. В ledger после каждой волны — строка
расхода (число dispatches × канал, хотя бы грубо). Бюджет из contract.md
(волны / время / $) пробит → СТОП + отчёт, независимо от прогресса.

Roadmap закрыт → финальный broad review (внешний аудит — `/bouncer`) →
прогон completion criteria → отчёт: волны, parked lanes из backlog.md,
остаточные риски. Бюджет исчерпан, цель не закрыта → отчёт «где
остановился + что дальше», НЕ тихое продолжение.

## Definition of Done

- [ ] `contract.md` создан ДО первой волны, completion criteria — командой
- [ ] Каждый write-lane: свой worktree, бриф с DONE WHEN + ACCEPTANCE
- [ ] Каждый lane verified оркестратором (команда + результат в ledger)
- [ ] Wave-end полный тест-сьют после каждой волны — вердикт в ledger
- [ ] backlog.md существует (пустой = тоже результат: дрейфа не было)
- [ ] Runnable test:
      `test -f .goal-king/contract.md && grep -q "^## Wave" .goal-king/ledger.md`

## Известные грабли

- **«Агент в goal-режиме ничего не сделал»** — permission gate, не тупость
  → защита: write-флаги канала из capability-registry + тестовая задача.
- **Edit ушёл в main checkout вместо worktree** (NVP 2026-06-12) →
  защита: §3, первый Edit verify маркером/`wc -l`.
- **Три волны подряд с нулём диспатчей** (nikita/video-engine 2026-07-09,
  Wave 3.5/3.6/3.7): агент упёрся в задачу и вместо работы выпустил
  contract v3, PROMPT v2→v3, criteria_check v3, правку capability-registry
  и поднял бюджет 6→8. Следующая волна — BLOCKED, 5 внешних диспатчей
  впустую. Ledger вырос до 218 KB / 92 заголовка, backlog набрал P0 вне
  контракта → защита: §6 неизменяемость контракта + шаблон
  `references/contract-template.md`.
- **Оркестратор сам полез кодить** и сжёг контекст (2026-07-07) → защита:
  роль оркестратора = бриф→dispatch→verify→merge; диагностика корня —
  можно, имплементация — lane.
- **Полу-волна принята по self-report**, регрессия всплыла через волну →
  защита: §4, acceptance своими руками + wave-end full suite.
- **agy виснет на крупной multi-file генерации** → защита: bounded-задачи
  для agy, крупный build — codex/cursor (см. capability-registry).
- **Канал завис тихо**: процесс жив, лог пуст после init, квота не
  тратится (кейс codex 2026-07-07) → kill -9 + переброс lane на надёжный
  канал; НЕ жди и не перезапускай тем же вызовом.
- **pytest в Antigravity-терминале диспатчит live-промпты себе же**
  (self-loop) → защита: тесты AgentNet-workspace — только с отключённым
  bridge discovery.
- **Grok (и другие контекст-чувствительные внешние CLI):** bundle limit + сильная деградация от размера промпта.
  Пример падения (2026-07-09): в `-p` вставили весь предыдущий краш-лог → bundle > 52MB + max-turns 20.
  Защита:
  - Всегда пиши lane-brief в отдельный файл + `cat /tmp/brief.md`.
  - `--max-turns 60+` для не-тривиальных lane.
  - Чистый self-contained промпт (никакой истории предыдущих попыток).
  - Обязательный крошечный preflight перед большой задачей (см. `headless-agent-dispatch-cheatsheet.md` + `/delegate` + `delegate/references/grok-dispatch.md`).

## Связанные скиллы

- `agent-orchestrator-standard` (codex-side) — механика dispatch: intake,
  worktrees, запуск, мониторинг, интеграция. Этот скилл её не дублирует
- `/goal-plan` — гейты и контракт (§1 использует его, не дублирует)
- `/delegate` — бриф и preflight каждого lane
- `/subagent-driven-development` — если план линейный и исполнители Claude
- `/bouncer` — финальный внешний аудит
- rules/parallel-agents.md, rules/merge-queue-checkpoints.md — дисциплина
  worktree и merge

## Worker Prompt Prefix (вставляется в начало КАЖДОГО брифа)

Единственная каноническая версия (EN — работает для любой модели/канала):

```
SUB-AGENT RULES:
- Do ONLY the task in this brief. No scope creep.
- Use the lightest sufficient approach; minimize output tokens.
- Work and communicate in English; return compact evidence, not progress prose.
- Never weaken, skip, or delete tests/gates to make them pass. Any test
  change must be justified in your report.
- Output ONLY to the specified location, exact format requested.
- Unclear or blocked → finish with status BLOCKED + one short question
  in your final output. Never guess. (Headless channels have no
  mid-task backchannel — do not wait for answers.)
- Never paste chat history or prior logs anywhere.
- Finish with: deliverables + 1-sentence summary.
```

После префикса — бриф строго по схеме §2 (CONTEXT / TASK / CONSTRAINTS /
DONE WHEN / VERIFY / OWNED FILES, эталон по `/delegate`). Других шаблонов
брифа в этом скилле нет.

**Mini-first роутинг:** non-core работа (чтение, подсчёт, таблицы,
разведка, cross-check) → самый лёгкий канал из capability-registry;
тяжёлые модели — только имплементация и суждения. Роль оркестратора —
бриф→dispatch→verify→merge: диагностика корня допустима (дешевле точного
брифа), имплементация — всегда lane.

## FORBIDDEN

- Dispatch lane без DONE WHEN + ACCEPTANCE в брифе
- Принимать self-report исполнителя как верификацию; выдумывать вывод
  acceptance-команды (`~/.claude/standards/no-fabricated-evidence.md`)
- Новый lane вне контракта без записи решения (расширение scope молча)
- Править `contract.md`, критерии, бюджет или промты исполнителей после
  старта волн — вместо OWNER_QUEUE / STOP (обход anti-drift через ТЗ)
- Два write-lane в одном worktree / одном файле
- Останавливать волну из-за одного упавшего lane (кроме destructive/scope)
- Оркестратору писать код руками вместо fix-lane
- Хардкод имён моделей/агентов в брифах — только capability-registry
- Вставлять историю/логи предыдущих запусков в любой промпт агенту
- Выполнять работу lane самому при фейле каналов — только смена
  канала/park по §5 (owner — лишь destructive/scope)
- Re-exploration файлов без предварительной проверки ledger

## Hard fail

- Первая волна задиспатчена без `contract.md` → траектория неконтролируема
- Completion criteria зелёные ДО начала работ (red-test пропущен) →
  критерии ничего не измеряют, «done» недоказуем
- Бюджет волн не зафиксирован в contract.md → цикл без стоп-условия
- Бюджет пробит и поднят правкой контракта вместо СТОПа → стоп-условия нет
- Две волны подряд без диспатчей, продукт которых — свои же
  контракт/промт/политика → цикл встал, работа подменена мета-работой
- «Готово» при непройденных completion criteria из контракта → false done
- Ledger не вёлся → после compaction сессия передиспатчит сделанное
- Wave-end suite пропущен, волны merge'нуты → integration-регрессии слепые
- Начат новый тред/сессия-продолжение для активного Goal без явной просьбы
  владельца или доказанного отказа платформы → false handoff
- Оркестратор пишет продакшн-код или тесты руками вместо fix-lane
