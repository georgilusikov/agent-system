# Meta v3 — design (не зоопарк)

**Дата:** 2026-08-03
**Вход:** ревизия всех owner skills + диалог про JTBD/ODI/Голдратт/TRIZ/графы + A/B B2/B2+
**Цель:** один вход «как думать», который **связывает** домены, а не перечисляет 60 SKILL.md.

---

## 1. Что не так было в B2 / B2+

| Ошибка | Почему |
|--------|--------|
| Плоский список skills | Meta = каталог, не модель системы |
| `goal-plan` в карте | Это **контракт делегирования волн**, не линза мышления о проблеме/продукте |
| TRIZ-листья в meta | Уже есть `/triz` (роутер + C1–C11 + problem_discovery) — дубль |
| Нет JTBD / outcome | «Кто и зачем» выпало; остались только «как чинить систему» |
| Graphify = «ещё skill» | Graph — **язык связей**, не конкурент JTBD/TRIZ |
| Нет behavioral gate | Ценность может быть выдумана (выбор/платёж/повтор не проверены) |

---

## 2. Ядро (из твоего разбора + канона на диске)

Пять вопросов → пять ролей. Не пять «библиотек на выбор», а **слои одной модели**:

| # | Вопрос | Слой | Что делает | Инструменты у тебя |
|---|--------|------|------------|-------------------|
| Q1 | **Кто / зачем** | JTBD + outcome | Роль, работа, прогресс, атомарный outcome | `outcome-designer`, `jtbd-scenarium-create`, `_agent_shared/skills/jtbd/*`, `akts` (MPV) |
| Q2 | **Как связано** | Graph | Узлы/рёбра/веса/потоки; не mind map | `/graphify` (код/корпус), job graph / causal maps (TRIZ `causal_*`, `structural_analysis`, `flow_analysis`) |
| Q3 | **Где узкое место** | Goldratt / ToC | Constraint, critical chain, CRT/FRT-мышление | `1-critical-chain-design`, `/leverage`, `theory-of-constraints`, `thinking-theory-of-constraints`, TRIZ `flow_analysis` |
| Q4 | **Как менять систему** | TRIZ | Функции, свертывание, противоречия, ИКР | **`/triz` только** (не листья в meta) — FA, trimming, contradictions, ikr, C1–C11… |
| Q5 | **Ценность не выдумана?** | Behavioral / claim gate | Выбор, платёж, повтор, evidence claims | `experiment_designer`, `/falsify`, `/check`, **`/pizdej`**, anti-bias (на выборе) |

**ODI** (outcome importance × satisfaction) — пока **нет отдельного skill** на диске. Не выдумывать skill. Пока: outcomes из JTBD/outcome-designer + веса вручную / через anti-bias при приоритизации. Если понадобится — отдельный thin skill, не раздувать meta.

**Kano / Lean / Cynefin / Wardley** — **не** в ядре, пока нет конкретной дыры (как в твоём разборе).

---

## 3. Архитектура: meta = диспетчер слоёв, не энциклопедия

```
                    ┌──────────── meta v3 ────────────┐
                    │ 1. Класс запроса (A–F)           │
                    │ 2. Режим: single | pipeline | dual│
                    │ 3. Делегирование в DOMAIN router  │
                    │ 4. Behavioral / pizdej gate       │
                    └──────────────┬───────────────────┘
           ┌───────────┬───────────┼───────────┬────────────┐
           ▼           ▼           ▼           ▼            ▼
      outcome/JTBD   graphify    Goldratt    /triz      pizdej/falsify
      scenarium      (structure) leverage    C1–C11     check/anti-bias
                     job graph   crit-chain  problem_
                     causal…                 discovery
```

### Режимы

| Mode | Когда | Поведение |
|------|--------|-----------|
| **single** | Один явный вопрос | Один domain skill/router |
| **pipeline** | Нужна цепочка «кто→связь→constraint→change» | Фиксированный каркас CORE-P (ниже), без зоопарка |
| **dual** | High-stakes / «проверь себя» | Producer path + adversarial (`pizdej` / `falsify` / `anti-bias`) |
| **heavy** | Полный TRIZ-конвейер / forecast | `master_triz_orchestrator_v5` **или** Elena/Boris MCP — **не** default |

### CORE-P (pipeline по умолчанию для продукта/системы)

Не invent-as-you-go. Жёсткий скелет:

1. **Frame** — `outcome-designer` *или* `problem_map`/`socratic` (если ещё нет задачи)
2. **Structure** — если «что на что влияет / много связей» → graphify *или* FA/structural (через `/triz`)
3. **Constraint** — critical-chain *или* leverage (одно)
4. **Change** — `/triz` с **одной** цепочкой C-N (часто C1 FA→VA→trimming, C3 contradictions, C9 ikr…)
5. **Gate** — behavioral: что должно случиться (выбор/платёж/повтор/метрика) + при отчёте `/pizdej` Mode A

Шаги 2–3 можно skip, если вопрос узкий (только «сверни», только «outcome»).

---

## 4. Что **внутри** meta (карта делегирования)

Meta **не** копирует 62 TRIZ skill. Meta знает **домены и входы**.

### IN — framing / who-why

| Симптом | Куда |
|---------|------|
| «сформулируй задачу / outcome / 5 so what / что получу» | **outcome-designer** (agent) |
| «JTBD сценариум / когда-хочу-чтобы» | **jtbd-scenarium-create** |
| JTBD ↔ TRIZ мост | **jtbd_triz_bridge** |
| Клубок / непонятно что решать | **`/triz` → C8 или problem_discovery** (не дублировать в meta) |

### STRUCTURE — graph

| Симптом | Куда |
|---------|------|
| Код/корпус: «что вызывает / поток / как устроен проект» | **`/graphify`** |
| Система функций/потоков/причин (продукт/процесс) | **`/triz`**: FA, flow, structural, causal_loop, system_operator |
| Job graph / иерархия джоб | JTBD job_graph + bridge B3/B4 |

Граф **не** заменяет JTBD/TRIZ: он отвечает «как связано».
Mind map ≠ graph (как в твоём тексте).

### CONSTRAINT — Goldratt

| Симптом | Куда |
|---------|------|
| План >2 шагов, цепочка от конца | **1-critical-chain-design** |
| Узкое место системы / что тормозит | **leverage** (+ ToC skills) |
| Поток / КПД | **`/triz` C6** (FA → flow_analysis) |

### CHANGE — TRIZ (только через роутер)

| Симптом | Куда |
|---------|------|
| Любой TRIZ-симптом | **`/triz`** (карта + C1–C11) |
| Явно: упростить / свернуть / ФА | `/triz` **C1/C2** → functional_analysis → (value) → **trimming** |
| Противоречие | `/triz` **C3** |
| ИКР | `/triz` **C9** |
| Pre-mortem | `/triz` **C5** diversion… |

**В meta не перечислять** forty_principles, ariz, vepoli… — иначе dual maintenance с `/triz`.

### GATE — honesty / behavior

| Симптом | Куда |
|---------|------|
| После сложной работы / «что упустил» | **`/pizdej`** |
| «Можно ли релизить / опровергни claim» | **`/falsify`** |
| Expected State vs результат | **`/check`** |
| Выбор между альтернативами, bias | **anti-bias** |
| Дешёвый тест концепции | experiment_designer (через `/triz` или skill) |

### OUT — явно **НЕ** meta

| Skill | Почему не meta |
|-------|----------------|
| **goal-plan** | Контракт волн/гейтов делегирования — другой lifecycle |
| goal-king, implement, writing-plans, delegate | Исполнение / оркестрация кода |
| debug | RCA бага — `/debug` |
| bouncer, code-review | Аудит артефакта |
| fusion | Multi-model panel |
| Clear Thought / sequential MCP | Не ядро; sequential не бьёт baseline |

---

## 5. Elena / Boris MCP

**Есть:** `elena-boris-mcp` — tools: `elena_run/preview`, `boris_run/preview`, `validate_artifact`, `run_route_benchmark`.
Это **runtime конвейера** (providers, recipes, envelope), не thin «линза».

| Когда | Действие |
|-------|----------|
| Нужен полный Elena/Boris run, forecast, pinned methods | **heavy mode** → MCP/CLI, не skill-роутер |
| Обычное «подумай / упрости / JTBD» | **не** звать Boris |
| Meta default | **off** — иначе latency, ключи, зависимость от providers |

Статус: **опциональный backend для heavy**, не узел ядра Q1–Q5.

---

## 6. Субагенты

| Паттерн | Когда |
|---------|--------|
| Default | **нет** субагентов — sequential pipeline в одном агенте |
| dual | producer + `pizdej`/`falsify` (второй взгляд) |
| parallel lenses | только owner-запрос «сравни 2 линзы» + merge-rubric |
| heavy | Elena/Boris сам оркестрирует методы |

---

## 7. Связь с твоим текстом (JTBD + graph + Goldratt + TRIZ)

| Слой текста | Реализация |
|-------------|------------|
| Кто — узлы | JTBD roles / outcome-designer |
| JTBD — связи user↔jobs | scenarium + job_graph |
| ODI — веса | пока вручную / prioritize+anti-bias; skill ODI later |
| Голдратт — bottleneck | leverage + critical-chain + flow |
| TRIZ — изменить структуру | `/triz` FA/trimming/contradictions/ikr |
| Graph — «как связано» | graphify (code) + TRIZ structure/flow/causal (system) |
| Behavioral gate | pizdej + falsify + experiment |

**jtbd_triz_bridge** — уже готовый **клей** B1–B7; meta должна на него ссылаться, не копировать таблицу.

---

## 8. Решение по артефактам

| Файл | Роль |
|------|------|
| `meta_v3/SKILL.md` | Рабочий thin router (single/pipeline/dual) |
| `meta_b2plus/SKILL.md` | Legacy eval; не развивать |
| `/triz` | Единственный TRIZ-вход |
| Elena MCP | heavy only, config отдельно |

---

## 9. DoD этой ревизии

- [x] goal-plan убран из meta
- [x] pizdej, outcome-designer, FA/trimming (via /triz), graphify, Goldratt в модели
- [x] полный зоопарк skills **не** вставлен в meta
- [x] Boris = heavy optional
- [x] graph = язык связей, не mind map

**Confidence design: ~85%** — ядро совпадает с твоим текстом и с файлами на диске; ODI skill отсутствует (явный gap).
