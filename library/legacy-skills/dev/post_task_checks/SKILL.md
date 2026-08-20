---
skill_id: post_task_checks
skill_name: Post-Task Checks
version: 1.0.0
category: dev
triggers:
  - "проверки"
  - "checks"
  - "после изменений"
  - "после задачи"
  - "post task"
dependencies: []
---

# 🔧 Post-Task Checks

**Purpose:** Прогнать минимальные проверки после правок (tests/build), не превращая это в “релиз”.

**When to use:**
- После внесения изменений агентом
- Перед тем как сказать “готово”

**Output:** Команды проверки + интерпретация результата/что чинить первым

**Gate Check:**
- Указаны конкретные команды под проект
- Есть “если упало — что делать”
