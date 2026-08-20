---
name: problem-discovery
description: Sub-orchestrator that classifies situations into 6 scenarios and routes to chains of existing TRIZ skills for problem-finding before the main pipeline
skill_id: problem_discovery
skill_name: Problem Discovery Sub-Orchestrator
version: 2.0.0
category: orchestration
triggers:
  - "расплывчатая ситуация"
  - "непонятно что решать"
  - "много проблем"
  - "клубок задач"
  - "что сломалось"
  - "где проблема"
  - "какие риски"
  - "стоит ли развивать"
dependencies: []
---

# 🔍 Problem Discovery Sub-Orchestrator

**Purpose:** Классифицировать вход пользователя в один из 6 сценариев и направить на цепочку существующих TRIZ-скилов для **поиска проблемы** (Phase 0), прежде чем переходить к решению.

**When to use:**
- Пользователь описывает ситуацию, а не задачу
- Проблема расплывчатая или их несколько
- Непонятно какой TRIZ-инструмент применить первым

**When NOT to use:**
- Задача уже сформулирована (есть ТП/ФП) → прямо в main triage
- Пользователь явно запрашивает конкретный скил (`@ariz`, `@trimming`)

## Архитектура

```text
User Input
    ↓
┌──────────────────────────────────────────────────────┐
│  Problem Discovery Router (discovery_router.py)       │
│  1 LLM-вызов → классификация в S1..S6               │
│                                                       │
│  S6 (FORMULATED) → bypass ──────────────────────────→ │
│  S1..S5 → цепочка существующих скилов               │
└──────────────────────────────────────────────────────┘
    ↓ (сформулированная задача)
    Main TRIZ Orchestrator v5 (triage → skeleton map → solution)
```

## 6 сценариев маршрутизации

### S1: Расплывчатая ситуация (`VAGUE_SITUATION`)

**Признаки:** «Плохо работает», «что-то не так», много проблем, нет явного противоречия.

**Основная цепочка:**

| Шаг | Скил | Что делает |
| --- | --- | --- |
| 1 | `@socratic` | Диагностические вопросы → сужение ОЗ/ОВ |
| 2 | `@problem_map` | Карта симптомов → владелец боли → метрика → candidate problem statements |
| 3 | `@problem_formulator` | АРИЗ-85В Часть 1 → ТП-1/ТП-2 + модель задачи |

**Альтернативы:** `@system_operator` (расширить обзор через 9 экранов), `@avf` (анализ среды)

---

### S2: Расследование отказа (`INVESTIGATION`)

**Признаки:** «Сломалось», «раньше работало — теперь нет», дефект, причина неизвестна.

**Основная цепочка:**

| Шаг | Скил | Что делает |
| --- | --- | --- |
| 1 | `@kt_is_is_not` | Матрица IS/IS NOT → изоляция вероятной причины |
| 2 | `@causal_analysis` | RCA+ (5+ уровней «Что является причиной?») |

**Альтернативы:** `@triz_troubleshooter` (метод парадоксов Фаера), `@inconsistent_parameters` (инверсные графы)

---

### S3: Проактивный поиск рисков (`RISK_PROACTIVE`)

**Признаки:** «Как может сломаться?», «какие уязвимости?», pre-mortem, надёжность.

**Default цепочка:**

| Шаг | Скил | Что делает |
| --- | --- | --- |
| 1 | `@diversion_analysis` | Мышление диверсанта → сценарии поломки |
| 2 | `@afd_failure_predictor` | Скрытые дефекты (отложенные, деградационные, специальные) |

**Primary path при control-loop signals:** `@stpa_analysis → @problem_formulator`

Использовать как primary path, если во входе есть:
- controller / operator / PLC / software safety
- feedback / sensor / actuator / interlock
- unsafe control action / timing / wrong command sequence

Если же риск описан как sabotage / weaponization / misuse of existing resources /
latent defect injection, router должен оставлять default path через
`@diversion_analysis → @afd_failure_predictor`.

**Альтернативы:** `@stpa_analysis` (control loops, software, operator hazards, safety logic)

---

### S4: Неэффективность процесса (`INEFFICIENCY`)

**Признаки:** «Медленно», «дорого», «низкий КПД», bottleneck, потери, Muda.

**Default цепочка:**

| Шаг | Скил | Что делает |
| --- | --- | --- |
| 1 | `@functional_analysis` | Паразитные/вредные функции + False Productive |
| 2 | `@flow_analysis` | Узкие места в потоках В/Э/И |

**Primary path при recurring-loop signals:** `@causal_loop_diagram → @problem_formulator`

Использовать как primary path, если во входе есть:
- recurring backlog / rework / firefighting
- oscillation / rebound / delay / policy resistance
- local fixes do not hold / проблема возвращается

**Альтернативы:** `@informational_flow_analysis` (Демукрон, seq→parallel), `@structural_analysis` (жёсткие связи), `@trimming` (радикальное упрощение), `@causal_loop_diagram` (повторяющиеся петли, задержки, policy feedback)

---

### S5: Стратегический анализ (`STRATEGIC`)

**Признаки:** «Стоит ли развивать?», «устарело?», «на каком этапе?», «предел?», инвестировать или заменить.

**Основная цепочка:**

| Шаг | Скил | Что делает |
| --- | --- | --- |
| 1 | `@s_curve` | Определение стадии S-кривой через MPV→MFPV→FPV |
| 2 | `@limits_strategy` | Количественный предел развития, резерв |
| 3 | `@system_operator` | 9 экранов → скрытые ресурсы в надсистеме/подсистеме |

**Альтернативы:** `@resource_analysis` (ВПР — скрытые ресурсы для бесплатного решения)

---

### S6: Задача сформулирована (`FORMULATED`)

**Признаки:** Есть чёткое ТП-1/ТП-2, физическое противоречие, известна конфликтующая пара.

**Действие:** Bypass → прямо в main triage (`triage_agent.py`), скилы не запускаются.

---

## Полная карта скилов

```text
┌─────────────────────────────────────────────────────────────────┐
│  PROBLEM DISCOVERY (Phase 0)                                    │
│                                                                  │
│  S1 ──→ @socratic → @problem_map → @problem_formulator ──→ tri.│
│          alt: @system_operator, @avf                             │
│                                                                  │
│  S2 ──→ @kt_is_is_not → @causal_analysis ──→ main triage       │
│          alt: @triz_troubleshooter, @inconsistent_parameters     │
│                                                                  │
│  S3 ──→ default: @diversion_analysis → @afd_failure_predictor    │
│          primary if control-loop signals:                        │
│          @stpa_analysis → @problem_formulator                    │
│                                                                  │
│  S4 ──→ default: @functional_analysis → @flow_analysis           │
│          primary if recurring-loop signals:                      │
│          @causal_loop_diagram → @problem_formulator              │
│          alt: @informational_flow_analysis, @structural_analysis │
│               @trimming                                           │
│                                                                  │
│  S5 ──→ @s_curve → @limits_strategy → @system_operator ──→ tri. │
│          alt: @resource_analysis                                 │
│                                                                  │
│  S6 ──→ bypass ──────────────────────────────→ main triage      │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

Маршрутизация реализована в `discovery_router.py`:
- 1 LLM-вызов для классификации (промпт ~30 строк)
- `DiscoveryResult` содержит: `category`, `confidence`, `methods` (цепочка), `alternatives`
- Интеграция через `triage_with_discovery()` в `triage_agent.py`
- Active chain валидируется только против реально исполнимых top-level skills
- Для borderline S3/S4 router сначала использует intra-scenario route hint от LLM, затем
  сверяет его с deterministic signal rules (control-loop vs sabotage, recurring loops vs plain bottleneck)
- Если confidence < 0.6 или цепочка невалидна → safe fallback: `@socratic → @problem_map → @problem_formulator`
- Если discovery_router падает — fail-safe через стандартный triage

## Gate Check

| Критерий | Требование |
| --- | --- |
| Сценарий определён | Один из S1–S6 |
| Confidence >= 0.6 | Если ниже → S1 safe fallback |
| Цепочка скилов не пустая | Для S1–S5 минимум 1 скил |
| Скилы существуют | Все skill_id из цепочки существуют как top-level executable skills |
| Bypass корректный | S6 → пустая цепочка |

## Output Format

```json
{
  "scenario": "INVESTIGATION",
  "confidence": 0.9,
  "reasoning": "Пользователь описал отказ насоса, причина неизвестна",
  "skills": ["kt_is_is_not", "causal_analysis"],
  "alternatives": ["triz_troubleshooter", "inconsistent_parameters"],
  "description": "Расследование отказа → контрастная матрица + поиск причин"
}
```
