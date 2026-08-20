# Gate Check for Chemical TRIZ

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| Химическое противоречие сформулировано? | Да | ___ | ✅/❌ |
| Использован алгоритм Маркосова? | Да | ___ | ✅/❌ |
| Рассмотрена модификация прекурсора (Метод 1A)? | Да | ___ | ✅/❌ |
| Рассмотрены маскирующие агенты (Метод 1B)? | Да | ___ | ✅/❌ |

## Block Conditions
If any of these are true, **STOP and escalate**:
- [ ] Противоречие не химическое → перенаправить на другой скилл
- [ ] Нет конкретных химических агентов, только абстракции → углубить химический анализ

## Confidence Adjustment
- All checks pass: Confidence += 10%
- 1 check fails: Confidence -= 20%
- 2+ checks fail: Confidence = 50% max
