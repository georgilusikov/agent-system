# 📋 Стандарты для всех проектов

## 🎯 Концепция стандартов

**Стандарт** — это документ, который фиксирует воспроизводимое правило, метод или контракт,
чтобы агенты не повторяли ошибку и работали единообразно. Чаще всего рождается **после ошибки**.

Стандарты хранятся здесь и используются всеми проектами через ссылки в правилах агента
(`_agent_shared/rules/*.mdc`) и в скиллах.

## 🧬 Три класса стандартов

Не каждый стандарт — микро-чек-лист. Класс определяет лимит и форму (детали — `STRUCTURE_RULES.md`):

| Класс | Лимит | Что это | Эталон |
| :--- | :--- | :--- | :--- |
| **micro** | ≤ 100 строк | Рождён из ошибки, структура по `TEMPLATE.md` | `safe-deletion-standard.md` |
| **method** | ≤ 400 строк | Воспроизводимый пайплайн: стадии + hard-гейты + artifacts | `triz-gap-closure-audit-standard.md` |
| **contract** | ~150 строк | Контракт инструмента: инварианты + CLI surface + verification matrix | `agent_loops/ralph_loop.md` |

## 📂 Структура

```bash
_agent_shared/standards/
├── README.md                          # Этот файл — индекс канона
├── STRUCTURE_RULES.md                 # Правила структурирования (3 класса)
├── TEMPLATE.md                        # Шаблон micro-класса
│
├── research-data-standard.md          # micro
├── root-cause-analysis-standard.md    # micro
├── safe-deletion-standard.md          # micro
├── rules-validation-standard.md       # micro
├── verification-methods-standard.md   # micro
├── ui-component-matrix-standard.md    # micro
├── report-preflight-standard.md       # micro
├── triz-gap-closure-audit-standard.md # method
├── universal-matrix-standard.md       # method
├── rat-framework-standard.md          # method
├── competitor-analysis-standard.md    # method
│
├── agent_loops/                       # contract-стандарты для tools/agent_loops/
│   ├── ralph_loop.md
│   ├── dev_swarm.md
│   ├── architect_loop.md
│   ├── extraction_protocol.md
│   ├── parallel_worktree_swarm.md
│   └── skill_improvement_ab_loop.md
├── multi_agent/
│   └── model_adapter_contract.md      # contract (база для agent_loops)
└── process/
    └── rule_dialects.md               # contract (диалекты правил)
```

## 📋 Канон стандартов (все 20)

### Топ-уровень (micro + method)

| Стандарт | Класс | Описание | Используется в |
| :--- | :--- | :--- | :--- |
| `research-data-standard.md` | micro | Работа с данными в research: проверка структуры/схемы и тегов источника [O/I/S/A] перед выводами | `core-master.mdc` |
| `root-cause-analysis-standard.md` | micro | Root Cause Analysis: симптом → 5 Whys с доказательствами → корневая причина → точечный фикс | `core-why.mdc`, `anti-freeze.mdc`, `core-master.mdc`, `/why` |
| `safe-deletion-standard.md` | micro | Безопасное удаление: корзина вместо `rm`, бэкап, подтверждение владельца | `core-clean.mdc`, `core-auto.mdc` |
| `rules-validation-standard.md` | micro | Валидация **правил агента** перед коммитом (бэкап, тест изменённого правила, валидные пути, change-log) | `core-master.mdc`, `process/rule_dialects.md` |
| `verification-methods-standard.md` | micro | Generic-методы верификации: 3-method cross-check, test-by-change-type, when-tests-fail (процесс — в `/check`) | `/check`, `rules-validation-standard.md` |
| `ui-component-matrix-standard.md` | micro | UI-компонентная матрица (промоут `atomic_hub/ui_matrix_protocol.md`): протокол построения матрицы UI-компонентов | `atomic_hub`, UX-задачи |
| `report-preflight-standard.md` | micro | Preflight-чеклист отчёта перед публикацией (промоут BAS `preflight_checklist.md`) | `BAS/03_HEAVY_MODE.md` |
| `triz-gap-closure-audit-standard.md` | method | Feature-discovery аудит: джобы → непокрытые → ТРИЗ-генераторы (ресурсы/тренды/ИКР/ФА) → бэклог фич с привязкой к коду. Триггеры: «найди отсутствующие фичи», «feature gap audit» | `skills/jtbd/jtbd_triz_bridge`, `/jobs-to-be-done`, `/prioritize`, `/why`, `/triage` |
| `universal-matrix-standard.md` | method | Универсальная матрица доноров-кандидатов: что строить с нуля (промоут Nikita `UNIVERSAL_MATRIX_STANDARD.md`). Пара к `triz-gap-closure` (gap-аудит построенного) | `triz-gap-closure-audit-standard.md`, Nikita engineering |
| `rat-framework-standard.md` | method | RAT (Riskiest Assumption Test): выявление и проверка самого рискованного допущения (промоут VANECHKA `rat-framework.md`) | VANECHKA, продуктовые гипотезы |
| `competitor-analysis-standard.md` | method | Пайплайн анализа конкурентов: рамка через джобу → intel → value/feature teardown → Desire-Delivery gap → скоринг доноров → позиционные разрывы + бэклог. Триггеры: «анализ конкурентов», «competitor teardown», «разбери конкурента» | `projects/xerox`, BAS workflows, `triz-gap-closure`, `/jobs-to-be-done`, `/prioritize` |
| `change-receipts-standard.md` | contract | Metadata-only append-only JSONL receipts: связывают state, tasks, hooks, deployments и projections с runtime evidence без содержимого разговоров или tool payloads | state/task writers, hooks, deployment/projection writers, runtime adapters |

### `agent_loops/` — контракты agent-loop инструментов

| Стандарт | Класс | Описание | Используется в |
| :--- | :--- | :--- | :--- |
| `agent_loops/ralph_loop.md` | contract | Persistent autonomous plan loop: один таск за итерацию, exact-match completion-маркер, без `git add .`/auto-commit. **Эталон contract-класса** | `tools/agent_loops/` |
| `agent_loops/dev_swarm.md` | contract | Иерархическая мульти-модельная оркестрация: manager → 3 generator ∥ → 1 critic → synthesizer, всё через VibeProxy; cost/confidence — явные поля | `CLAUDE.md` (`dev_swarm.py`) |
| `agent_loops/architect_loop.md` | contract | Стратегический планинг PRD → Critique → Tasks → Execute, фаза = файл, провайдер-агностично | `workspace-output-standard.mdc` |
| `agent_loops/extraction_protocol.md` | contract | Протокол выноса root-скриптов в standards+tools: стандарт ПЕРВЫМ, owner-approval, потом рефактор по model-adapter contract | мета-контракт остальных `agent_loops/` |
| `agent_loops/parallel_worktree_swarm.md` | contract | N кодеров в N изолированных `git worktree`, сбор патчей, единый reviewer перед apply; кодер не пишет вне своего worktree | `tools/agent_loops/` |
| `agent_loops/skill_improvement_ab_loop.md` | contract | A/B-цикл улучшения скилла: baseline (A) vs candidate (B) под staging, одинаковый eval, явный owner-gate перед промоутом в канон | `tools/agent_loops/` |

### `multi_agent/`

| Стандарт | Класс | Описание | Используется в |
| :--- | :--- | :--- | :--- |
| `multi_agent/model_adapter_contract.md` | contract | Базовый контракт переиспользуемых tools: executor-абстракция, output-dir, max-iterations, dry-run, `--no-commit` по умолчанию; провайдер — в адаптере, не в tool | база для всех `agent_loops/` контрактов |

### `process/`

| Стандарт | Класс | Описание | Используется в |
| :--- | :--- | :--- | :--- |
| `process/rule_dialects.md` | contract | Source-of-truth диалектов правил: канон `.mdc`, все адаптеры компилит `compile_rules.py`, скомпилированные выходы не править | `skills/REGISTRY.md`, `compile_rules.py` |

## 🌐 Методологии вне канона

Часть методологий и протоколов **намеренно оставлена на месте** в проектах (завязаны на
проектный пайплайн или кодовую базу) — в канон стандартов не промоутятся, здесь только указатели:

| Методология | Где живёт | Почему вне канона |
| :--- | :--- | :--- |
| BAS workflows (LIGHT/MEDIUM/HEAVY, synthesis, boris_oracle, system_modeling, triz_surgery) | `projects/Business_Architect_System/docs/workflows/` | Проектный пайплайн BAS |
| UX specs (BLUEPRINT_PATCH, CLARITY_SCORE, FEATURE_INTAKE, FRAMEWORK_ROUTER, USABILITY_RUNTIME, VERSIONING_AND_GATES) | `projects/UX_Architect_Lab/` | Завязаны на кодовую базу UX-лаба |
| napoleon SPEC + execution_pilot | `projects/napoleon/` | Проектная спецификация |
| Nikita STYLE_GUIDE, author_input_protocol, feedback_protocol | `projects/Nikita/` | **Уезжают с Nikita-сиблингом** при её выносе |
| productheroes design_communication_framework, typography_hierarchy | `projects/course_productheroes/` | **Promote отложен** (решение владельца) |
| Ops_Center README_PROTOCOLS | `projects/Ops_Center/` | Проектные оперативные протоколы |
| architect-templates | `shared/plans/architect-templates/` | Шаблоны планирования, не стандарт |

> Промоутнуто в канон на этапе консолидации (Фаза 3): `universal-matrix-standard.md`,
> `ui-component-matrix-standard.md`, `rat-framework-standard.md`, `report-preflight-standard.md`
> (standards); JTBD domain-knowledge VANECHKA + `simulated_interview` → `skills/jtbd/resources/`;
> `krasinsky_unit_economics` → `skills/business/`.

## 🔗 Как использовать

### В правилах агента:

```markdown
**ОБЯЗАТЕЛЬНО:** Find and read: `_agent_shared/standards/research-data-standard.md`
```

### Создание нового стандарта:
1. Допустил ошибку / описываешь метод / фиксируешь контракт инструмента → определи **класс**.
2. **Прочитал `STRUCTURE_RULES.md`** — правила структурирования и выбор класса.
3. Взял образец класса: micro → `TEMPLATE.md`; method → `triz-gap-closure-audit-standard.md`;
   contract → `agent_loops/ralph_loop.md`.
4. Создал стандарт в `_agent_shared/standards/` (в пределах лимита класса).
5. Добавил ссылку в соответствующее правило в `_agent_shared/rules/` или скилл.
6. Обновил этот README (таблица + дерево).

## ⚠️ Важно

- Лимит зависит от класса: **micro ≤100 / method ≤400 / contract ~150** строк.
- Стандарт содержит **фундаментальные правила / стадии / контракт**, а не детали конкретных случаев.
- Дубли не плодить — только cross-ref на другой стандарт/скилл/правило.
- Используй `TEMPLATE.md` (micro) и `STRUCTURE_RULES.md` (классы и правила).
- Регулярно пересматривай стандарты и удаляй устаревшие части.
