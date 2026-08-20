# Gate Check for AVF (Анализ Входов-Выходов / Audit Value Flow)

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| Inputs идентифицированы (S/E/P)? | Да | ___ | ✅/❌ |
| Outputs идентифицированы (S/E/P)? | Да | ___ | ✅/❌ |
| Каждый вход/выход отмечен как Useful/Harmful? | Да | ___ | ✅/❌ |
| Выявлены Harmful Inputs (уязвимости)? | Да/N/A | ___ | ✅/❌ |
| Выявлены Harmful Outputs (потери)? | Да/N/A | ___ | ✅/❌ |
| Сформулирован Diagnosis (главная уязвимость + неэффективность)? | Да | ___ | ✅/❌ |

## Block Conditions
- **BLOCK** если нет классификации Useful/Harmful — без неё диагноз невозможен
- **BLOCK** если нет ни одного Harmful элемента — анализ поверхностный

## Confidence Adjustment
- Все 6 ✅ → confidence ≥ 85%
- 4-5 → confidence 65-80%
- < 4 → BLOCK
