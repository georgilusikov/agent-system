# Gate Check for AFD Failure Predictor

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| Система определена? | Да | ___ | ✅/❌ |
| Доступные ресурсы перечислены? | Да | ___ | ✅/❌ |
| Скрытые дефекты определены (3 категории Певзнера)? | Да | ___ | ✅/❌ |
| Предложены диверсионные гипотезы? | Да | ___ | ✅/❌ |

## Block Conditions
If any of these are true, **STOP and escalate**:
- [ ] Система не описана → запросить детали
- [ ] Только очевидные дефекты (не использована методология Певзнера) → пересмотреть подход
- [ ] Гипотезы невозможно протестировать → уточнить

## Confidence Adjustment
- All checks pass: Confidence += 10%
- 1 check fails: Confidence -= 20%
- 2+ checks fail: Confidence = 50% max
