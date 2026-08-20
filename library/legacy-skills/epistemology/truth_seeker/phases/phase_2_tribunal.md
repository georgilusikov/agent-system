# Phase 2: Multi-Lens Tribunal

## Цель
Каждая линза (теория истины) анализирует все sub-claims и выдаёт VerdictCell.

## Какие линзы активировать

| Режим | Линзы |
|-------|-------|
| `quick` | Correspondent + Coherentist + Pragmatist (3 линзы) |
| `deep` | Все 7: Correspondent + Coherentist + Pragmatist + Consensus + Hermeneutic + Deflationist + Aletheia |

## Алгоритм

### Шаг 1: Загрузить инструкции линз
Для каждой активной линзы прочитать соответствующий файл из `lenses/`.

### Шаг 2: Последовательный анализ
Для каждой линзы по каждому sub-claim:

1. **Принять роль** линзы (переключить персону)
2. **Анализировать** sub-claim через призму этой теории
3. **Собрать evidence** (web search для Correspondent; логика для Coherentist; и т.д.)
4. **Заполнить VerdictCell**

### Шаг 3: Формат VerdictCell

**Стандартный формат** (Correspondent, Coherentist, Pragmatist, Consensus):

```yaml
VerdictCell:
  lens: "[название линзы]"
  sub_claim_id: "SC1"
  verdict: [TRUE | FALSE | PARTIAL | UNDETERMINED]
  confidence: 0.00-1.00
  evidence:
    - "[текст доказательства]" [FACT/SOURCE/LOGIC/CONSENSUS/DISPUTED/ASSUME]
  counterexamples:
    - "[текст контрпримера]"
  reasoning: "[цепочка рассуждений]"
  limitations: "[что не удалось проверить]"
```

**Hermeneutic** — стандартный VerdictCell + поле ambiguity:

```yaml
  verdict: [TRUE | FALSE | PARTIAL | UNDETERMINED]
  ambiguity_flag: [true | false]   # если true → claim двусмыслен, рекомендуется уточнение
  ambiguity_note: "[какая двусмысленность обнаружена]"
```

> Если `ambiguity_flag = true` и verdict по другим линзам расходятся → пометить в отчёте.

**Deflationist** — альтернативный verdict:

```yaml
  verdict: [MEANINGFUL | TAUTOLOGY | CONCEPT_SUBSTITUTION | N/A]
```

**Aletheia** — InsightCell (не verdict, а анализ скрытого):

```yaml
InsightCell:
  lens: "Aletheia"
  sub_claim_id: "SC1"
  revealed: "[что раскрывается]"
  concealed: "[что скрывается]"
  etymological_insight: "[этимология ключевых понятий]"
  emet: { reliability: "...", stability: "...", fidelity: "..." }
```

### Шаг 4: Проверка Source Policy

Для каждого использованного источника:
- Определить тип (стандарт / peer-review / патент / аналитика / форум)
- Назначить `reliability_score` (0.0-1.0) используя `source_reliability_scorer`
- Проверить дату публикации
- Маркировать `supports` / `refutes` / `neutral`

### Шаг 5: Context Management

После завершения Tribunal — сжать все VerdictCells в summary-таблицу:

```markdown
| Sub-claim | Correspondent | Coherentist | Pragmatist | ... | Общий тренд |
|-----------|:---:|:---:|:---:|:---:|:---:|
| SC1 | TRUE (0.85) | TRUE (0.78) | PARTIAL (0.60) | ... | Скорее TRUE |
```

## Output
Summary-таблица + полные VerdictCells → передать в Phase 3 (deep) или Phase 5 (quick).
