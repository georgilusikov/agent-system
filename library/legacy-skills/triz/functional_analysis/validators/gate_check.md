# Gate Check for Functional Analysis (ФА / ФСА)

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| Компонентная модель построена? | Да | ___ | ✅/❌ |
| Функции записаны в строгом синтаксисе Subject → Action → Object? | Да | ___ | ✅/❌ |
| Для функций указан Field/MATHEM? | Да | ___ | ✅/❌ |
| Есть классификация Useful/Harmful/Insufficient/Excessive? | Да | ___ | ✅/❌ |
| Выделены corrective functions? | Да | ___ | ✅/❌ |
| Есть FSA/Significance логика (functional vs problem vs cost)? | Да | ___ | ✅/❌ |
| Есть кандидат на trimming / handoff rationale? | Да | ___ | ✅/❌ |
| Выбрана Топ-1 проблема (остальные "припаркованы")? | Да | ___ | ✅/❌ |

## Block Conditions
If any of these are true, **STOP and escalate**:
- [ ] Нет строгого синтаксиса функций → сначала исправить модель
- [ ] Нет corrective functions при наличии ручных/буферных компенсаций → анализ поверхностный
- [ ] Нет FSA/Significance логики в задаче "дорого/сложно" → ФА неполный, углубить в ФСА
- [ ] Нет Топ-1 проблемы → уточнить MPV через @akts или @socratic

## Confidence Adjustment
- All checks pass: Confidence += 10%
- 1 check fails: Confidence -= 20%
- 2+ checks fail: Confidence = 50% max
- Нет strict syntax: Confidence = 30%
- Нет FSA/Trim candidate в cost-optimization задаче: Confidence = 35%
