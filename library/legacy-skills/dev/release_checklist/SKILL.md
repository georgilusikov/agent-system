---
skill_id: release_checklist
skill_name: Release Checklist
version: 1.0.0
category: dev
triggers:
  - "release"
  - "релиз"
  - "готово к прод"
  - "готово к выкладке"
dependencies: []
---

# 🔧 Release Checklist

**Purpose:** Сформировать чеклист перед выкладкой/демо/мерджем.

**When to use:**
- Перед релизом или “готово к ревью”
- Перед большим мерджем в main

**Output:** Чеклист + “blockers” (что обязательно исправить)

**Gate Check:**
- Есть проверка запуска/тестов
- Есть проверка конфигов/секретов
