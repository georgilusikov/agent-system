---
skill_id: qa_notes
skill_name: QA Notes
version: 1.0.0
category: dev
triggers:
  - "qa notes"
  - "QA notes"
  - "как тестировать"
  - "передать тестировщику"
  - "handoff"
dependencies: []
---

# 🔧 QA Notes

**Purpose:** Сгенерировать “handoff” для тестирования: что изменилось, как проверить, где риск.

**When to use:**
- Закрыл задачу и нужно передать в QA/продакт/себе в будущем
- Нужна проверяемая инструкция “как убедиться что работает”

**Output:** Markdown “QA Notes” (готово для вставки в Jira/PR/Memory Bank)

**Gate Check:**
- Есть “How to test” с конкретными шагами
- Есть “Risk areas” + “Rollback/mitigation”
