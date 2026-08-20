# Gate Check for Inconsistent Parameters

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| Параметр с противоречивыми требованиями выделен? | Да | ___ | ✅/❌ |
| Обосновано требование значения А? | Да | ___ | ✅/❌ |
| Обосновано требование значения не-А (или B)? | Да | ___ | ✅/❌ |
| Использован физический вывод (разделение в пространстве/времени/структуре)? | Да | ___ | ✅/❌ |

## Block Conditions
If any of these are true, **STOP and escalate**:
- [ ] Требования можно удовлетворить компромиссом (нет острого конфликта) → переформулировать
- [ ] Значения А и не-А не относятся к одному параметру → выбрать один параметр

## Confidence Adjustment
- All checks pass: Confidence += 10%
- 1 check fails: Confidence -= 20%
- 2+ checks fail: Confidence = 50% max
