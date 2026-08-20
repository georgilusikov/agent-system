# Gate Check for IKR (Идеальный Конечный Результат)

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| Функция (Что делать?) и Объект (S1) известны? | Да | ___ | ✅/❌ |
| Ресурсы из @resource_analysis доступны? | Да | ___ | ✅/❌ |
| Использован Resource ID (Rxx) из реестра? | Да | ___ | ✅/❌ |
| В формуле ИКР присутствует слово "САМ"? | Да | ___ | ✅/❌ |
| Обоснована "даровость" решения (Cost = 0 или Transformable)? | Да | ___ | ✅/❌ |
| Сформулировано ФП (если ИКР невозможен)? | Да (если нужно) | ___ | ✅/❌ |

## Block Conditions
If any of these are true, **STOP and escalate**:
- [ ] Нет реестра ресурсов → сначала @resource_analysis
- [ ] В ИКР предлагается НОВОЕ устройство (не из ресурсов) → переформулировать через "САМ"
- [ ] Resource ID отсутствует (ресурс "из головы") → привязать к реестру

## Confidence Adjustment
- All checks pass: Confidence += 10%
- 1 check fails: Confidence -= 20%
- 2+ checks fail: Confidence = 50% max
- Нет слова "САМ" в ИКР: Confidence -= 30%
