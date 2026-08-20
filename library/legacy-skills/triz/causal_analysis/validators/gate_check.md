# Gate Check for Causal Analysis (RCA+)

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| НУЭ (Нежелательный Эффект) описан конкретно? | Да | ___ | ✅/❌ |
| Есть Observed Event / наблюдаемое событие? | Да | ___ | ✅/❌ |
| Цепочка "Почему?" логически непрерывна? | Да | ___ | ✅/❌ |
| Достигнуто стоп-условие (Физический/Управленческий/Средовой предел)? | Да | ___ | ✅/❌ |
| Zone of Control / Sphere of Influence зафиксированы? | Да | ___ | ✅/❌ |
| Проверены порочные круги (Vicious Circles)? | Да | ___ | ✅/❌ |
| Key Deficiency отделён от симптома? | Да | ___ | ✅/❌ |
| Установлена связь с противоречием (для передачи в @contradictions)? | Да | ___ | ✅/❌ |
| Есть action set / break points? | Да | ___ | ✅/❌ |

## Block Conditions
If any of these are true, **STOP and escalate**:
- [ ] Менее 3 уровней "Почему?" → анализ поверхностный, углубить
- [ ] Нет стоп-условия → причинная цепочка "висит в воздухе", искать физический/управленческий предел
- [ ] Нет Observed Event → сначала уточнить факт/маркер НЭ
- [ ] Нет зоны контроля → дерево не готово к действию
- [ ] НУЭ описан абстрактно ("всё плохо") → @socratic для уточнения

## Confidence Adjustment
- All checks pass: Confidence += 10%
- 1 check fails: Confidence -= 20%
- 2+ checks fail: Confidence = 50% max
- Менее 3 уровней "Почему?": Confidence = 30% max
- Нет Key Deficiency / Action Set: Confidence = 35% max
