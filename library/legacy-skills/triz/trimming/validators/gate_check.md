# Gate Check for Trimming (Свёртывание)

## Minimum Criteria
| Check | Required | Actual | Pass? |
|-------|----------|--------|-------|
| MPV/главная функция зафиксирована? | Да | ___ | ✅/❌ |
| Компоненты ранжированы (Rank A/B/C)? | Да | ___ | ✅/❌ |
| Выбрана "жертва" (Rank C или B)? | Да | ___ | ✅/❌ |
| Rank A НЕ удаляется? | Да | ___ | ✅/❌ |
| Проверены все 6 правил свёртывания (A-F)? | 6/6 | ___ | ✅/❌ |
| Энергетический путь проверен (Energy Path Check)? | Да | ___ | ✅/❌ |
| Вторичные проблемы (Trimming Conflict) идентифицированы? | Да | ___ | ✅/❌ |
| Главная функция сохранена после свёртывания? | Да | ___ | ✅/❌ |

## Block Conditions
If any of these are true, **STOP and escalate**:
- [ ] Удаляется Rank A (Изделие) → ЗАПРЕЩЕНО, пересмотреть выбор жертвы
- [ ] Энергетический путь разорван → решение может не работать, нужна перекомпоновка
- [ ] Нет функциональной модели → сначала @functional_analysis

## Confidence Adjustment
- All checks pass: Confidence += 10%
- 1 check fails: Confidence -= 20%
- 2+ checks fail: Confidence = 50% max
- Rank A удалён: Confidence = 0% (FATAL)
