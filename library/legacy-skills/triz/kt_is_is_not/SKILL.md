---
name: kt-is-is-not
description: Kepner-Tregoe IS/IS NOT analysis for isolating the cause of a deviation from normal operation
skill_id: kt_is_is_not
skill_name: KT IS/IS NOT (Kepner-Tregoe)
version: 1.0.0
category: analysis
triggers:
  - "сломалось"
  - "перестало работать"
  - "отклонение"
  - "раньше работало"
  - "дефект"
  - "причина неизвестна"
  - "investigation"
dependencies: []
---

# KT IS/IS NOT

**Purpose:** Быстро сузить наиболее вероятную причину отклонения через контраст `IS / IS NOT`, а затем перевести результат в TRIZ-ready handoff.

**When to use:**
- Что-то работало нормально, а потом стало работать хуже или перестало
- Есть отклонение от нормы, но причина ещё неизвестна
- Нужно быстро отсеять ложные причины до глубокой RCA

**When NOT to use:**
- Это не deviation from norm, а новая инновационная задача
- Пользователь описывает расплывчатую жалобу без наблюдаемого симптома
- Задача про оптимизацию стоимости или новую концепцию, а не про неисправность

**Output:** IS/IS NOT matrix, tested causes, most probable cause, TRIZ translation, handoff recommendation.
