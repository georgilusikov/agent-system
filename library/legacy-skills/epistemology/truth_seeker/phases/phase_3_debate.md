# Phase 3: Adversarial Review + Debate

## Цель
Принудительная проверка качества выводов Phase 2 через двух специализированных агентов (Skeptic и Bias Hunter) и структурированные дебаты между линзами.

> ⚠️ Эта фаза выполняется ТОЛЬКО в режиме `deep`.

## Алгоритм

### Шаг 1: Загрузить инструкции агентов
- Прочитать `agents/skeptic.md`
- Прочитать `agents/bias_hunter.md`

### Шаг 2: Раунд 1 — Атака

**Skeptic (Адвокат Дьявола):**
1. Получает summary-таблицу из Phase 2
2. Для каждого sub-claim с verdict ≠ UNDETERMINED:
   - Ищет **сильнейший контрпример** (web search по запросу "[claim] criticism/debunked/controversy")
   - Проверяет: **есть ли альтернативное объяснение?**
   - Атакует самое **слабое логическое звено** в reasoning
3. Формулирует **Challenge** — конкретный, конструктивный вызов

**Bias Hunter:**
1. Получает summary-таблицу + reasoning от каждой линзы
2. Проверяет:
   - Не повторяется ли **один и тот же вывод** во всех линзах? (→ подозрение на системный bias LLM)
   - Есть ли **confirmation bias** (искали только подтверждения)?
   - Есть ли **authority bias** (полагались на "авторитет" без проверки)?
   - Нет ли **ложной корреляции** в reasoning?
3. Формулирует **Bias Alert** — конкретное указание на искажение

### Шаг 3: Раунд 2 — Ответ линз

Каждая атакованная линза:
1. Видит Challenge от Skeptic и/или Bias Alert
2. **ОТВЕЧАЕТ** на атаку: защищает свою позицию ИЛИ **ОБНОВЛЯЕТ** verdict/confidence
3. Если verdict обновлён — фиксировать: `verdict_v1 → verdict_v2 (причина: [challenge])`

### Шаг 4: Раунд 3 — Финальный (если нужен)

Если после Раунда 2 остаются **критические расхождения** (>0.3 разброс confidence по одному claim):
- Skeptic ищет **дополнительный evidence** через `search_web`
- Финальный арбитраж: линзы дают окончательный verdict

Максимально 3 раунда. Жёсткий лимит.

### Шаг 5: Фиксация протокола

```
Debate Protocol:
  rounds_completed: [1|2|3]
  challenges:
    - challenger: "Skeptic"
      target_lens: "Correspondent"
      target_claim: "SC2"
      challenge: "[текст вызова]"
      response: "[текст ответа]"
      verdict_changed: [true|false]
  bias_alerts:
    - type: "[confirmation_bias|authority_bias|echo_chamber|...]"
      description: "[описание]"
      action_taken: "[что было сделано]"
  agreement_points: [список]
  disagreement_points: [список]
```

## Output
Обновлённая summary-таблица + Debate Protocol → передать в Phase 4.
