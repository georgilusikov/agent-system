---
skill_id: bas_memory_capture
skill_name: BAS Memory Capture
version: 1.0.0
category: workflow
triggers:
  - "BAS"
  - "Business Architect System"
  - "сохрани анализ"
  - "memory capture"
dependencies: []
---

# 🔧 BAS Memory Capture

**Purpose:** Упаковать результат анализа в Memory Bank так, чтобы новый чат стартовал “с места”.

**When to use:**
- Закончил анализ/идею в BAS
- Нужно кратко зафиксировать: input → гипотезы → выводы → что дальше

**Output:** Обновления для `bas_notes.md`, `activeContext.md`, `progress.md`

**Gate Check:**
- Есть входные данные и выводы
- Есть следующие шаги (actionable)
