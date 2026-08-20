---
skill_id: commit_style
skill_name: Commit Style
version: 1.0.0
category: dev
triggers:
  - "commit"
  - "коммит"
  - "commit message"
  - "сообщение коммита"
dependencies: []
---

# 🔧 Commit Style

**Purpose:** Сформировать осмысленное сообщение коммита (summary + optional body).

**When to use:**
- Перед `git commit`
- При наведении порядка в истории (squash/rebase)

**Output:** 1–3 варианта commit message + краткое обоснование выбора

**Gate Check:**
- Summary в повелительном наклонении (“Add”, “Fix”, “Refactor”)
- Есть “why”, если изменение не очевидно
