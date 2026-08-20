# Карта А: Авария/Брак (Investigation)

> **Триггер:** «Почему сломалось?», «Где причина?», «Брак / отказ / авария»

```
@akts →
  ⛔ GATEWAY: причина известна?
  ├─ НЕТ → @causal_analysis →
  │    ⛔ GATEWAY: тип причины?
  │    ├─ Конфликт параметров → @contradictions → @forty_principles
  │    ├─ Вредное взаимодействие → @oz_ov → @resource_analysis → @vepoli → @standards
  │    ├─ Нужен механизм → @ikr → @effects
  │    └─ Причина ясна + контрмера очевидна → СТОП
  └─ ДА → @oz_ov → @resource_analysis →
       ⛔ GATEWAY: решение очевидно?
       ├─ ДА → СТОП
       └─ НЕТ → определи барьер → выбери путь по Gateway Protocol
→ @critic → @akts (повторная сверка) → @final_triz_report
```
