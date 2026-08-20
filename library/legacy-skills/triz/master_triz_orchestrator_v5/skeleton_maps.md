# 🗺️ Skeleton Maps (карты с ветвлениями)

> **Источник:** Эти карты извлечены из core_instructions.md (v5 refactoring).
> Вызываются оркестратором при выборе маршрута через Routing Kernel.

---

#### Карта А: Авария/Брак (Investigation)

```
@akts →
  ⛔ GATEWAY: причина известна?
  ├─ НЕТ → @triz_troubleshooter (парадоксы) →
  │    ⛔ GATEWAY: парадоксы найдены?
  │    ├─ ДА → @causal_analysis (верифицировать гипотезу) →
  │    └─ НЕТ → @causal_analysis (классический ПСА) →
  │    ⛔ GATEWAY: тип причины?
  │    ├─ Конфликт параметров → @contradictions → @forty_principles
  │    ├─ Вредное взаимодействие → @oz_ov → @resource_analysis → @vepoli → @standards
  │    ├─ Нужен механизм → @ikr → @effects
  │    └─ Причина ясна + контрмера очевидна → СТОП
  └─ ДА → @oz_ov → @resource_analysis →
       ⛔ GATEWAY: решение очевидно?
       ├─ ДА → СТОП
       └─ НЕТ → Routing Kernel (определить барьер)
→ @microstandards (опц.) → @critic → @akts (повторная сверка) → @final_triz_report
```

#### Карта Б: Дорого/Лишнее (Optimization)

```
@akts → @functional_analysis → @value_analysis →
  ⛔ GATEWAY: что дорого/лишнее?
  ├─ Компоненты с низкой ценностью → @trimming →
  │    ⛔ GATEWAY: возник новый конфликт?
  │    ├─ ДА → @contradictions → @forty_principles
  │    └─ НЕТ → СТОП
  ├─ Нужен идеал → @oz_ov → @resource_analysis → @ikr
  └─ Нужна гибкость → @dynamization
→ @microstandards (опц.) → @critic → @akts (повторная) → @final_triz_report
```

#### Карта В: Тупик/Прорыв (Strategy)

```
@akts → @system_operator → @s_curve →
  ⛔ GATEWAY: стадия на S-кривой?
  ├─ Рост → @zrts → @dynamization
  ├─ Зрелость/Насыщение → @limits_strategy →
  │    ⛔ GATEWAY: источник прорыва?
  │    ├─ Конкуренты лучше → @benchmarking → @oas_transfer
  │    ├─ Нужен аналог из другой области → @fos → @reverse_fos
  │    └─ Нужна новая архитектура → @contradictions → @forty_principles
  └─ Деградация → @inversion → @antisystem
→ @microstandards (опц.) → @critic → @final_triz_report
```

#### Карта Г: Аудит/Риски (Diagnostic)

```
@structural_analysis → @functional_analysis → @akts → @diversion_analysis →
  ⛔ GATEWAY: риск локализован + контрмера ясна?
  ├─ ДА → @critic → @final_triz_report (СТОП)
  └─ НЕТ → @oz_ov → @resource_analysis → @vepoli → @standards
→ @critic → @final_triz_report
```

#### Карта Д: Прогноз/Эволюция (Predictive)

```
@akts → @system_operator → @s_curve → @zrts →
  ⛔ GATEWAY: цель?
  ├─ Найти технологию → @fos → @effects
  ├─ Найти рынки → @reverse_fos
  └─ Повысить гибкость → @dynamization
→ @critic → @final_triz_report
```

#### Карта Е: Тупик/ARIZ (Deep)

```
@causal_analysis → @arip (быстрая попытка) →
  ⛔ GATEWAY: АРИП решил?
  ├─ ДА → @critic → @final_triz_report (СТОП)
  └─ НЕТ → Полный АРИЗ:
       @contradictions (ТП) → @oz_ov → @resource_analysis →
       @ikr → ФП → @mmch (опц.) →
       @vepoli → @standards → @effects (опц.) →
       @ariz (полный алгоритм) →
       ⛔ GATEWAY: решение-парадокс?
       ├─ ДА → @inversion / @antisystem
       └─ НЕТ → СТОП
→ @critic → @final_triz_report
```

#### Карта Ж: Быстрое решение (Express)

```
@causal_analysis → @arip →
  ⛔ GATEWAY: решено?
  ├─ ДА → @critic → @final_triz_report (СТОП)
  └─ НЕТ → @oz_ov → @resource_analysis → @contradictions → @forty_principles
→ @microstandards (опц.) → @critic → @final_triz_report
```

#### Карта Л: Перенос свойств (Feature Transfer)

> **Канон (Редколис):** АКТС → Бенчмаркинг → ОАС → ПСА → Перенос свойств

```
@akts → @benchmarking →
  ⛔ GATEWAY: найден лидер с нужными свойствами?
  ├─ ДА → @oas_transfer → @causal_analysis (проверка совместимости) →
  │    ⛔ GATEWAY: перенос возможен?
  │    ├─ ДА → @critic → @final_triz_report (СТОП)
  │    └─ НЕТ → @contradictions → @forty_principles (устранить конфликт переноса)
  └─ НЕТ → @fos (кросс-доменный поиск) → @oas_transfer
→ @critic → @akts (повторная) → @final_triz_report
```

#### Карта М: Потоковый анализ / Процесс (Process Optimization)

```
@akts → @flow_analysis (ФАП) → @functional_analysis →
  ⛔ GATEWAY: bottleneck найден?
  ├─ Поток избыточен → @trimming
  ├─ Поток конфликтует → @contradictions → @forty_principles
  ├─ Взаимодействие вредное → @oz_ov → @vepoli → @standards
  └─ Причина неясна → @causal_analysis → Routing Kernel
→ @critic → @akts (повторная) → @final_triz_report
```

#### Карта Н: Reliability / FMEA (Failure Prediction)

```
@functional_analysis → @structural_analysis → @afd_failure_predictor →
  ⛔ GATEWAY: отказы локализованы?
  ├─ ДА → @diversion_analysis (проверка уязвимостей) →
  │    ⛔ GATEWAY: диверсия находит новые риски?
  │    ├─ ДА → @oz_ov → @resource_analysis → решение по барьеру
  │    └─ НЕТ → СТОП
  └─ НЕТ → @causal_analysis → повтор на другом системном уровне
→ @critic → @final_triz_report
```

#### Карта З: Химия/Материалы (Specialized)

```
@functional_analysis → @oz_ov → @resource_analysis →
  ⛔ GATEWAY: тип задачи?
  ├─ Взаимодействие веществ → @vepoli → @standards → @effects
  ├─ Конфликт свойств → @contradictions → @forty_principles → @effects
  └─ Экология → @pn_eco_innovation
→ @critic → @final_triz_report
```

#### Карта И: Патент/Изобретение (IP)

```
@patent_claims (парсинг) → @akts → @functional_analysis →
  ⛔ GATEWAY: стратегия обхода?
  ├─ Тримминг → @trimming → @morphological_analysis
  ├─ Кросс-домен → @fos → @oas_transfer
  └─ Противоречие → @oz_ov → @contradictions → @vepoli → @standards
→ @patent_claims (проверка claim-distance) → @critic → @final_triz_report
```

#### Карта К: Обучение/РТВ (Education)

```
@socratic → @dnd (разогрев) → @system_operator → @rvs →
  ⛔ GATEWAY: выбери 1-2 упражнения:
  ├─ @goldfish
  ├─ @robinson
  ├─ @mmch
  └─ @antisystem / @inversion
→ @rtv (итог) → @case_logger → @final_triz_report
```
