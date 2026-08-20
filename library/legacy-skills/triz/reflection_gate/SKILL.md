---
skill_id: reflection_gate
name: reflection-gate
skill_name: Reflection Gate (Self-Check)
version: 1.0.0
category: triz
triggers:
  - "reflection"
  - "самокритика"
  - "слабое звено"
  - "blind spot"
  - "я не проверил"
dependencies: []
description: 'Reflection Gate: Обязательный финальный self-check перед выдачей результата любого TRIZ-скилла. Находит самое слабое .'
---

# 🔍 Reflection Gate (Self-Check)

**Purpose:** Обязательный финальный self-check перед выдачей результата любого TRIZ-скилла. Находит самое слабое звено анализа и пропущенную область.

**When to use:**
- Встроен в Output Format каждого TRIZ-скилла (inline)
- Вызывается отдельно при сомнениях в качестве анализа
- Перед финализацией `@final_triz_report`

**Output:** 2 строки (CRITICAL + BLIND SPOT), контекстуализированые для инструмента

**Gate Check:**
- CRITICAL назван конкретно (не «всё может быть неправильно»)
- BLIND SPOT привязан к инструментам данного скилла
- Если CRITICAL или BLIND SPOT фатален — дано указание каким skill вернуться
