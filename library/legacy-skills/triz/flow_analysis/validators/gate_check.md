# Gate Check for Flow Analysis (Потоковый Анализ)

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| Карта построена от Источника до Потребителя? | Да | ___ | ✅/❌ |
| Найден главный Bottleneck с количественной метрикой? | Да | ___ | ✅/❌ |
| Проведён баланс Входа/Выхода? | Да | ___ | ✅/❌ |
| **Primary Lever с Intervention?** | Да | ___ | ✅/❌ |
| **Fast Experiment (1–3 дня)?** | Да | ___ | ✅/❌ |
| **No-go / предел применимости?** | Да | ___ | ✅/❌ |

## Block Conditions
- **BLOCK** если карта не полная (нет начала или конца потока)
- **BLOCK** если bottleneck не определён — результат бесполезен
- **BLOCK** если нет Primary Lever — анализ не дошёл до действия

## Confidence Adjustment
- Все ✅ → confidence ≥ 85%
- 4-5 чеков → confidence 70%
- 3 чека → confidence 60%
- < 3 → BLOCK
