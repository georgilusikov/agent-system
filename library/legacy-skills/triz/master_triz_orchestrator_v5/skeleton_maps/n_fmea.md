# Карта Н: Reliability / FMEA (Failure Prediction)

> **Триггер:** «Надёжность», «FMEA», «Предсказать отказ», «Где сломается?»

```
@functional_analysis → @structural_analysis → @afd_failure_predictor →
  ⛔ GATEWAY: отказы локализованы?
  ├─ ДА → @diversion_analysis (проверка уязвимостей) →
  │    ⛔ GATEWAY: диверсия находит новые риски?
  │    ├─ ДА → @oz_ov → @resource_analysis → определить барьер → решение
  │    └─ НЕТ → СТОП
  └─ НЕТ → @causal_analysis → повтор на другом системном уровне
→ @critic → @final_triz_report
```

> **Disambiguation:** `@afd_failure_predictor` предсказывает **КАК** система может отказать (FMEA). `@diversion_analysis` ищет **КТО/ЧТО** может навредить (диверсия Злотина). AFD = reliability, Diversion = vulnerability.
