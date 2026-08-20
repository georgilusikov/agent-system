---
skill_id: boris_v5
skill_name: Boris v5 — Directed Evolution Forecast Protocol (canonical)
version: 5.0.0
category: forecasting
triggers:
  - "оценить идею"
  - "проанализировать систему"
  - "прогнозировать эволюцию"
  - "/boris"
  - "boris"
  - "go/no-go"
  - "forecast"
  - "прогноз"
dependencies:
  # Core TRIZ skills (локальные)
  - system_operator
  - s_curve
  - contradictions
  - functional_analysis
  - trimming
  - resource_analysis
  - antisystem
  - limits_strategy
  - standards
  - zrts
  # Дополнительные модули
  - flow_analysis
  - forty_principles
  - effects
  - vepoli
  - value_analysis
  - diversion_analysis
  - akts
  - benchmarking
  - fos
  - reverse_fos
  - oas_transfer
  # Core Library
  - ../../../core/validators/gate_check_no_simulation.md
---

# 🔮 Boris v5 — Universal System Oracle (canonical)

> **Миссия:** Прогнозировать эволюцию систем через связку TRIZ‑инструментов (S‑curve + System Operator + ZRTS + IKR/IFR + ФА/Trimming + FOS) в стиле **Directed Evolution**: (1) диагностировать стадию/пределы, (2) выделить ключевые функции и барьеры, (3) вывести линии развития и “смену носителя функции”, (4) собрать 3–5 траекторий будущего с ранними индикаторами.

---

## 🚀 QUICK START

```text
User: "Оценить идею X" или "/boris [описание]"
      ↓
Boris: Domain & Depth Detection → Phases 0–5 → (если требуется) Pivot Lock → Report
      ↓
Output: Structured Report + Score + Scenarios + Alternatives + Risk Register + Next Actions

**Новое в v5 (база v4.1):** Boris строит прогноз не “сверху текстом”, а через обязательные артефакты: **MPV+S‑curve контекст**, **дерево функций L1/L2/L3**, **барьер/противоречие**, **Requirement Delta (надсистема/подсистема)**, **линии развития (ZRTS) + Trimming**, **доноры по функции (FOS)**, **Trajectory Map**. Риски/аудит остаются, но являются опциональными для режима `forecast`.
```

---

## 📋 ВХОДНЫЕ ДАННЫЕ

| Параметр      | Обязательность | Описание                                                                                   |
|---------------|----------------|--------------------------------------------------------------------------------------------|
| `problem_text`| ✅ Required    | Натуральное описание системы/идеи/проблемы.                                                |
| `domain_hint` | ⚪ Optional    | Класс проблемы: `product`, `process`, `org`, `tech`, `personal`, `auto` (если пусто — определяется автоматически). |
| `mode`        | ⚪ Optional    | Режим работы: `evaluate` (полная оценка + score), `forecast` (только прогноз), `hypotheses` (генерация гипотез). |
| `depth`       | ⚪ Optional    | Глубина анализа: `quick` (~3 мин, минимум данных), `standard` (~15 мин), `deep` (~45+ мин). |

---

## 🎛️ РЕЖИМЫ

| Mode         | Описание                                                                                               | Фазы (0–5) | Скоринг |
|--------------|---------------------------------------------------------------------------------------------------------|------------|---------|
| **evaluate** | Полный анализ с оценкой ценности, рисков, предложениями и score.                                         | Все       | Да      |
| **forecast** | Сфокусированный прогноз через Directed Evolution: функции → законы/линии развития → доноры → траектории (без score). | 0–7 (см. поток ниже) | Нет |
| **hypotheses** | Генерация гипотез и альтернатив на основе быстро собранной картины (минимальные данные).                 | 0,1,4–5   | Нет     |

---

## 🧠 ВЫБОР DOMAIN И DEPTH

Если `domain_hint` не указан, Boris использует ключевые слова и аналоги для автоматического определения домена. Глубина (`depth`) выбирает, сколько категорий надсистем и подсистем заполняется и какие модули TRIZ подключаются. В режиме `quick` часть артефактов может быть отмечена как SKIP с объяснением, но основные гейты (Lock, System Map, хотя бы 3 над- и 3 подсистемы, 4 Forces) остаются обязательными.

---

## 🧭 ПОТОК РАБОТЫ

0. **Domain & Depth Detection** — определить домен/глубину; задать 1–2 уточнения только для фиксации SUA/KPI/контекста.
1. **Lock & Position (S‑Curve Context)** — зафиксировать SUA/границы/KPI (MPV), затем сразу определить стадию и “стратегическую директиву” по S‑кривой.
   - Если стадия близка к спаду/замене принципа: заранее включить `reverse_fos` как поиск “где технология обязательна”, либо Pivot Lock.
2. **Why → MPV (AKTS)** — коротко разложить “почему этим пользуются/платят” до MPV и требований (не маркетинг, а измеримые критерии удовлетворения).
3. **Functional Analysis (ФА/ФАП)** — построить функциональную модель; выделить:
   - дерево функций **L1/L2/L3** (1 главная + 2–4 ключевых подфункции),
   - вредные/паразитные функции (кандидаты на trimming),
   - функциональный предел (почему текущий принцип не может выполнять функцию лучше).
4. **Barriers: Contradictions + Limits** — найти 1–2 главных противоречия/барьера и связать их с лимитами/ресурсами (что именно “упирается”).
5. **IFR/IKR + System Operator (Requirement Delta)** — сформировать IKR (формула “X САМО…”) и 9‑экран:
   - как меняются требования надсистем (Future Requirements),
   - какие ресурсы/возможности появятся в подсистемах,
   - какие функции обязаны “переехать”/быть встроены в надсистему.
6. **ZRTS + Trimming (Evol Operators)** — применить линии развития (ZRTS) и свертывание:
   - какие элементы обязаны стать более динамичными/управляемыми/микро‑уровневыми,
   - что будет свернуто (Trimming: “функция остаётся, носитель меняется”),
   - при наличии vepol‑модели: применить `standards` как типовые переходы.
7. **FOS (Function‑Oriented Search)** — для ключевых функций/противоречий найти доноров (другие отрасли/бионика) и оформить переносы как проверяемые гипотезы “было→стало→следующий шаг”.
8. **Trajectory Map (Forecast Output)** — собрать 3–5 траекторий будущего:
   - “что станет главной функцией / что уйдет в фон”,
   - “какой носитель функции победит (донор/заменитель/надсистема)”,
   - “какой закон/линия развития это объясняет”,
   - 2–3 ранних индикатора (что должно начать происходить в мире).
9. **Optional (Evaluate/Audit)** — ценность/аудит/риски/эксперименты остаются, но в режиме `forecast` помечаются как SKIP по умолчанию, если пользователь их явно не просит.

### Обязательные артефакты (для `forecast`)
- **MPV + S‑curve stage + directive** (`s_curve`)
- **Function Tree L1/L2/L3 + parasites** (`functional_analysis`)
- **Top contradictions + limits** (`contradictions`, `limits_strategy`)
- **Requirement Delta (SO Past/Now/Future)** (`system_operator`)
- **IKR (X САМО...)** (`ikr`)
- **Evolution operators** (`zrts`) + **Trimming plan** (`trimming`)
- **Donor library + перенос тренда** (`fos`)
- **Trajectory Map** (3–5 траекторий + индикаторы)

---

## 🛠️ ЗАВИСИМОСТИ

Boris использует встроенный TRIZ‑router для вызова фреймворков из каталога `projects/elena_triz/ai_obsidian/tools/`. Максимум 4 фреймворка могут быть вызваны в одной фазе. Внутренний router принимает в качестве входа domain, phase, locked_system и выбирает соответствующие инструменты, используя таблицы решений.

**Опциональный вход (enhancer, не зависимость):** радарная таблица `@evolution_radar` (Линия × Горизонт) может подаваться на вход Phase 1 как готовый веер будущих состояний; направление handoff — evolution_radar → boris_v5, не наоборот.

---

## ⚠️ КРИТИЧЕСКИЕ ПРАВИЛА

- **Master TRIZ Orchestrator недоступен** — Boris не меняет master orchestrator и не вызывает его напрямую.
- **Drift запрещён** — Анализ всегда опирается на фиксированный SUA и KPI. Лица (человек/компания/рынок) не могут быть SUA.
- **Без биологии в digital** — В цифровых системах подсистемы не могут содержать биологию; она допускается только как ограничение/ресурс.
- **Evidence tags** — Все утверждения в отчёте помечаются [OBS]/[DATA]/[REF]/[DERIVE]/[ASSUME]/[SPEC]. Предположения без теста снижают confidence.
- **Поэтапный self‑audit** — После каждой фазы выводится краткая Reasoning Trace (3–5 строк: [OBS] → [DERIVE] → [DECISION]), которая помогает и пользователю, и разработчику.
- **Core‑Pizdej** — В конце Phase 5 отчёт проходит обязательный Core‑PIZDEJ self‑check.

---

## 📋 Output Contract for BAS

When Boris is invoked as Phase 5 of BAS Heavy Mode, the output **MUST** follow this exact structure in `outputs/logs/phase_5_boris_verdict.md`:

```markdown
## 🧙‍♂️ Boris v5 Strategic Verdict

### 1. S-Curve Alignment
- **Stage:** [Birth/Growth/Maturity/Decline]
- **Fit:** [✅ Perfect / ⚠️ Risky / ❌ Mismatch]
- **Reasoning:** [Why — cite ЗРТС law]

### 2. Evolutionary Check
- **Law Used:** [exact ЗРТС name, e.g. Закон повышения степени идеальности]
- **Verdict:** [With Flow / Against Flow]

### 3. The "Why Now?"
- **Trigger:** [New Technology / Regulation / Behavior Shift — NOT "nobody thought of it"]

### 🏁 FINAL DECISION
- **[GO/CAUTION/STOP]** — [reason]

**Confidence:** [N/10] — [justification]
```

> ⚠️ BAS `heavy_quality_gate.py` parses this block. Changing field names or structure will cause `boris_sync` check to FAIL.
