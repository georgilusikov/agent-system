---
skill_id: triz_memory_capture
skill_name: TRIZ Memory Capture
version: 1.0.0
category: workflow
triggers:
  - "TRIZ"
  - "трез"
  - "сохрани триз"
  - "сохрани результат"
dependencies: []
---

# 🔧 TRIZ Memory Capture

**Purpose:** Зафиксировать цепочку TRIZ‑прогона и результаты в Memory Bank.

**When to use:**
- После связки skills (ФА → противоречия → IKR → решения)
- Когда задача большая и нужно продолжать в новом чате

**Output:** Обновление `triz_session.md` + `activeContext.md` + `progress.md`

**Gate Check:**
- Есть problem statement
- Есть применённая цепочка skills и результаты
