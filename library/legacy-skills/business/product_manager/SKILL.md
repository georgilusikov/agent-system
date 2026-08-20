---
skill_id: product_manager
skill_name: Product Manager Toolkit
version: 1.0.0
category: business
triggers:
  - "product manager"
  - "cjm"
  - "customer journey map"
  - "user interview"
  - "interview protocol"
dependencies: ["jtbd/job_graph"]
description: "Product Manager templates: Customer Journey Map generator + user-interview protocol. Use when converting JTBD/research into As-Is vs To-Be maps, or planning 30-min user interviews."
---

# Product Manager Toolkit

**Purpose:** шаблоны для типовых задач продакт-менеджера на стыке JTBD и продуктовой дискавери.

**Содержание:**
- `cjm_template.md` — Customer Journey Map generator (As-Is vs To-Be). Использует Job Stories + user research на входе.
- `interview_protocol.md` — протокол user-interview.

**When to use:**
- Есть Job Stories / JTBD выход → нужно CJM для дизайна / стейкхолдеров.
- Планирование user interview, нужен короткий протокол.
- Переход от discovery к product delivery.

**Flow:**
1. JTBD discovery (см. `_agent_shared/skills/jtbd/job_graph/`).
2. Этот скилл: CJM generator или interview protocol.
3. Landing/GTM (`_agent_shared/skills/jtbd/landing_jtbd/`, `product_launch/`).
