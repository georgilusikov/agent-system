# Gate Check for Microstandards Lookup

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| Запрос переформулирован из модели | Да | ___ | ✅/❌ |
| Поиск выполнен (CLI или LLM) | Да | ___ | ✅/❌ |
| Результат с score >= 6 найден | ≥1 | ___ | ✅/❌ |
| Аналогия объяснена (не "похоже") | Да | ___ | ✅/❌ |
| Адаптация к текущей задаче дана | Да | ___ | ✅/❌ |

## Block Conditions
If any of these are true, **STOP and report "no matches"**:
- [ ] Все результаты score < 6 → микростандартов не найдено, продолжить без них
- [ ] Запрос не переформулирован → вернуть на переформулировку

## Confidence Adjustment
- 3+ matches score >= 7: Confidence += 10%
- 1-2 matches score 6-7: Confidence += 5%
- No matches: Confidence unchanged (tool just didn't help, not a failure)
