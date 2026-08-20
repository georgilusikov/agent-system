---
skill_id: fos
name: fos
skill_name: FOS (Function-Oriented Search)
version: 1.0.1
category: synthesis
triggers:
  - "FOS"
  - "поиск аналогов"
  - "биомиметика"
  - "как в природе"
  - "другие отрасли"
dependencies: ["contradictions", "benchmarking", "forty_principles", "resource_analysis", "trimming", "limits_strategy"]
description: 'FOS: Найти лидеров по функции (другие отрасли/бионика) и оформить проверяемые гипотезы переноса с огранич.'
---

# 🔭 FOS (Function-Oriented Search)

**Purpose:** Найти лидеров по функции (другие отрасли/бионика) и оформить проверяемые гипотезы переноса с ограничениями и тестами.

**Inputs:** Функция L1/L2/L3, среда/режимы, hard constraints.

**Outputs:** Доноры (почему лидер, механизм), перенос тренда (было→стало→следующий шаг), гипотезы переноса (ограничения/тесты), handoff.

**Seed Donors:** Перед открытым поиском проверьте Bank of Evolutionary Alternatives:
`_agent_shared/skills/forecasting/boris_v5/reference/bank_of_evolutionary_alternatives.md` —
каталог 13+ реальных DE-кейсов по отраслям и S-Curve стадиям (Злотин). Если аналогичный переход уже задокументирован — используйте как стартовую точку.

**Gate Check:** см. `_agent_shared/skills/triz/fos/validators/gate_check.md`
- L1/L2/L3 функция, доноры ≥5 из ≥2 отраслей.
- ≥1 перенос тренда.
- Гипотезы ≥3 с ограничениями + маркер/фальсификация/тест.
