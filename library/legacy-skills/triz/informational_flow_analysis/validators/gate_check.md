# Gate Check for Informational Flow Analysis

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| Информационные потоки выделены из материальных/энергетических? | Да | ___ | ✅/❌ |
| Определен "источник" и "приемник" информации? | Да | ___ | ✅/❌ |
| Выявлены задержки и рассинхронизации? | Да | ___ | ✅/❌ |
| Использован метод Демукрона (перевод AND в OR)? | Да | ___ | ✅/❌ |

## Block Conditions
If any of these are true, **STOP and escalate**:
- [ ] Описание сводится только к физическому движению → найти управляющий сигнал
- [ ] Не определена причина задержки сигнала → углубить диагностику

## Confidence Adjustment
- All checks pass: Confidence += 10%
- 1 check fails: Confidence -= 20%
- 2+ checks fail: Confidence = 50% max
