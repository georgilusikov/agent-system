# Gate Check for The Critic

## Minimum Criteria
| Check | Required | Actual | Pass? |
|---|---|---|---|
| Есть `### 💀 Kill Report`? | Да | ___ | ✅/❌ |
| `Status` = `SURVIVED` или `KILLED` | Да | ___ | ✅/❌ |
| `Confidence` в диапазоне 0-100% | Да | ___ | ✅/❌ |
| Есть список `fatal Flaws` (>=2 если KILLED) | Да | ___ | ✅/❌ |
| Есть хотя бы 2 разных типа фаталов (Physics/Economics/Logic) | Да | ___ | ✅/❌ |
| Нет похвалы и нет предложений "как исправить" | Да | ___ | ✅/❌ |
| Есть 1 строка `verdict` | Да | ___ | ✅/❌ |

## Block Conditions (STOP)
- [ ] Есть похвала/одобрение ("классно", "отличная идея") -> переписать
- [ ] Есть советы по улучшению/фиксу -> удалить (критик не чинит)
- [ ] Фаталы слишком общие ("регуляции", "безопасность") без конкретики -> переформулировать

## Confidence Adjustment
- Все checks PASS: Confidence = min(100, Confidence + 10)
- Любой block condition: Confidence = 0 (ответ невалиден)
