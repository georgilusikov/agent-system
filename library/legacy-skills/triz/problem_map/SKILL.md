---
name: problem-map
description: Convert a tangled situation into a compact engineering problem map before formal TRIZ problem formulation
skill_id: problem_map
skill_name: Problem Map
version: 1.0.0
category: analysis
triggers:
  - "клубок задач"
  - "расплывчатая ситуация"
  - "много симптомов"
  - "непонятно что решать"
  - "multiple problems"
  - "problem map"
dependencies: []
---

# Problem Map

**Purpose:** Превратить сырое описание и диагностические ответы в компактную карту проблем: симптомы, владелец боли, ущерб, ограничения, метрика и candidate problem statements.

**When to use:**
- После `@socratic`, когда ситуация сузилась, но ещё не выбрана главная проблема
- Когда в описании несколько симптомов и неясно, что формулировать в TRIZ первую очередь
- Когда нужно выбрать один primary problem statement перед `@problem_formulator`

**When NOT to use:**
- Задача уже оформлена как TP / FP / clear contradiction
- Уже есть один выбранный problem statement и нужен ARIZ-style formalization
- Нужно расследовать конкретную причину отклонения, а не сегментировать problem space

**Output:** symptom clusters, owner of pain, current harm, constraints, metric, 2-4 candidate problem statements, recommended primary problem statement, handoff recommendation.
