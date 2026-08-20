---
skill_id: truth_seeker
skill_name: "Truth Seeker — Multi-Lens Epistemic Analysis Protocol"
version: 1.0.0
category: epistemology
triggers:
  - "истина"
  - "правда ли"
  - "проверь миф"
  - "фактчекинг"
  - "проверить утверждение"
  - "/istina"
dependencies:
  # Epistemology skills
  - epistemological_audit
  - source_reliability_scorer
  - propaganda_resistance
  - truth_worldview_audit
  - manipulation_detector
  # Baumeister agents
  - correspondence_verifier
  - coherence_analyst
  - hermeneutic_spiral
  - thought_experiments
  - facts_vs_assertions
  - opinion_vs_knowledge
  # Baumeister skills
  - cognitive_biases
  - dialectics
  - conceptualization
---

# 🏛️ Truth Seeker — Multi-Lens Epistemic Analysis Protocol

> **Миссия:** Глубокая проверка утверждений через 7 теорий истины, мульти-агентные дебаты, генеалогию заблуждений и самокритику. Не даём один "магический" ответ — раскладываем тему на проверяемые утверждения и анализируем каждое через разные эпистемологические линзы.

---

## 🚀 QUICK START

```text
User: "/istina Гомеопатия лечит" или "Правда ли что X?"
      ↓
Truth Seeker: Intake → Decomposition → 7 Lenses → Debate → Genealogy → Pizdej → Report
      ↓
Output: Truth Matrix + Verdict + Debate Highlights + Contradiction Graph + Genealogy + Sources
```

---

## 📋 ВХОДНЫЕ ДАННЫЕ

| Параметр | Обязательность | Описание |
|----------|----------------|----------|
| `claim_text` | ✅ Required | Утверждение для проверки |
| `mode` | ⚪ Optional | `quick` (3 линзы, ~5 мин) / `deep` (7 линз + дебаты, ~20 мин). Default: `deep` |
| `domain_hint` | ⚪ Optional | `science`, `finance`, `tech`, `social`, `medical`, `legal`, `auto` |
| `time_scope` | ⚪ Optional | As-of date. Default: текущая дата |
| `location_scope` | ⚪ Optional | Географический контекст, если важен |

---

## 🎛️ РЕЖИМЫ

| Mode | Линзы | Фазы | Время |
|------|-------|------|-------|
| **quick** | Correspondent + Coherentist + Pragmatist | 0→1→2→5→6 | ~3-5 мин |
| **deep** | Все 7 линз + Skeptic + Bias Hunter | 0→1→2→3→4→5→6 | ~15-30 мин |

---

## 🧭 ПОТОК РАБОТЫ

0. **Intake** — зафиксировать Claim Object (text, domain, time_scope, risk_level)
1. **Decomposition** — разбить на 3-12 атомарных sub-claims, классифицировать тип
2. **Multi-Lens Tribunal** — 7 линз анализируют каждый sub-claim, выдают VerdictCell
3. **Adversarial Review + Debate** — Skeptic атакует, Bias Hunter ловит искажения, линзы отвечают (2-3 раунда)
4. **Genealogy of Delusion** — откуда заблуждение, механизм распространения, cognitive biases
5. **Pizdej Self-Check** — что не учли, blast radius, bias check, калибровка
6. **Synthesis Report** — Truth Matrix + Verdict + Debate + Contradiction Graph + Sources + Quality Metrics

### Обязательные артефакты
- **Claim Object** с domain/time_scope/risk_level
- **Sub-claims** с типами [EMPIRICAL/LOGICAL/NORMATIVE/DEFINITIONAL]
- **VerdictCell** от каждой линзы (verdict + confidence + evidence + counterexamples)
- **Truth Matrix** (sub-claim × теория × verdict × confidence)
- **Contradiction Graph** (нерешённые конфликты)
- **Quality Metrics** (5 осей)

---

## 📚 7 ЛИНЗ (Теории Истины)

| # | Линза | Файл | Вопрос | Режим |
|---|-------|------|--------|-------|
| 1 | 🔵 Correspondent | `lenses/correspondent.md` | Соответствует ли фактам? | quick + deep |
| 2 | 🟢 Coherentist | `lenses/coherentist.md` | Непротиворечиво ли? | quick + deep |
| 3 | 🟡 Pragmatist | `lenses/pragmatist.md` | Работает ли на практике? | quick + deep |
| 4 | 🟠 Consensus | `lenses/consensus.md` | Что говорит экспертный консенсус? | deep |
| 5 | 🔵 Hermeneutic | `lenses/hermeneutic.md` | Контекст, интерпретации, сдвиги? | deep |
| 6 | 🔴 Deflationist | `lenses/deflationist.md` | Не тавтология ли? Не подмена понятий? | deep |
| 7 | 🟣 Aletheia | `lenses/aletheia.md` | Что скрыто в утверждении? | deep |

## 🗡️ СПЕЦИАЛЬНЫЕ АГЕНТЫ (Phase 3)

| Агент | Файл | Роль |
|-------|------|------|
| ⚔️ Skeptic | `agents/skeptic.md` | Адвокат Дьявола — атакует все выводы, ищет контрпримеры |
| 🔍 Bias Hunter | `agents/bias_hunter.md` | Ловит когнитивные искажения и манипулятивные нарративы |

---

## 📊 SOURCE POLICY (Приоритет источников)

| Приоритет | Тип |
|-----------|-----|
| 1 (высший) | Стандарты, регуляторные документы |
| 2 | Peer-reviewed статьи, мета-анализы |
| 3 | Патенты, техническая документация |
| 4 | Качественная прикладная аналитика |
| 5 (низший) | Форумы и UGC (только слой мнений) |

Правила: 1) минимум 2 типа источников на claim; 2) искать и ЗА, и ПРОТИВ; 3) фиксировать даты.

---

## ⚠️ КРИТИЧЕСКИЕ ПРАВИЛА

- **Единица анализа: Claim** — не мнение, не вопрос, а конкретное проверяемое утверждение.
- **Факт ≠ Интерпретация** — никогда не объединять в одну формулировку (из `facts_vs_assertions`).
- **Evidence Tags** обязательны: `[FACT]`, `[SOURCE]`, `[LOGIC]`, `[CONSENSUS]`, `[DISPUTED]`, `[ASSUME]`.
- **"Не знаю" допустим** — если evidence недостаточно, verdict = `UNDETERMINED`. Не маскировать неопределённость.
- **High-Risk Mode** — автоматически для finance/medical/legal: усиленная проверка + дисклеймер.
- **Confidence Downgrade** — автоматическое снижение при односторонних источниках, отсутствии контрпримеров, устаревших данных.
- **Core-Pizdej** — Phase 5 обязателен. Если обнаружена серьёзная дыра → RETURN TO Phase 2 (макс 1 возврат).
- **Context Management** — между фазами передаётся только summary, не полный лог.
- **Лимит времени** — deep ≤ 30 мин; quick ≤ 5 мин.
