---
skill_id: benchmarking
name: benchmarking
skill_name: Functional Benchmarking
version: 1.0.1
category: diagnostics
triggers:
  - "бенчмаркинг"
  - "сравнение функций"
  - "лучший в классе"
  - "best in class"
dependencies: ["fos"]
description: 'Functional Benchmarking: Сравнить лидеров по функции (не бренды) и сформулировать гипотезы переноса с ограничениями/тестами.'
---

# 📊 Functional Benchmarking

**Purpose:** Сравнить лидеров по функции (не бренды) и сформулировать гипотезы переноса с ограничениями/тестами.

**Inputs:** Функция L1/L2/L3, контекст/ограничения.

**Outputs:** Лидеры по функции, “дуэль” по параметрам, гипотезы переноса + перенос тренда.

**Gate Check:** см. `_agent_shared/skills/triz/benchmarking/validators/gate_check.md`
- Функция L1/L2/L3, лидеры ≥5 (≥1 из другой отрасли).
- ≥3 параметра сравнения.
- Гипотезы ≥2 с маркером/фальсификацией/тестом.
- Перенос тренда или аргументированный отказ.
