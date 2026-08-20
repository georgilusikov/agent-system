# Gate Check for Reflection Gate

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| Выявлены ли слепые зоны (blind spots)? | Да | ___ | ✅/❌ |
| Проведена ли переоценка уверенности (Confidence)? | Да | ___ | ✅/❌ |
| Сформулированы ли критические вопросы к самому себе? | Да | ___ | ✅/❌ |
| Есть ли альтернативные интерпретации данных? | Да | ___ | ✅/❌ |

## Block Conditions
If any of these are true, **STOP and escalate**:
- [ ] Оценка Confidence осталась 100% без сомнений → формальная рефлексия, повторить
- [ ] Не найдено ни одной новой гипотезы → недостаточная глубина рефлексии

## Confidence Adjustment
- All checks pass: Confidence += 10%
- 1 check fails: Confidence -= 20%
- 2+ checks fail: Confidence = 50% max
