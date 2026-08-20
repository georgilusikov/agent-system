---
skill_id: standards
name: standards
skill_name: "18 Key TRIZ Standards (из 76)"
version: 1.0.0
category: synthesis
triggers:
  - "стандарты ТРИЗ"
  - "76 стандартов"
  - "шаблон решения"
dependencies: ["vepoli"]
description: '18 Key TRIZ Standards: Apply 18 most frequent standards (из 76 Альтшуллера), covering ~80% of typical vepol tasks. MPV-anch.'
---

# 📚 18 Key TRIZ Standards (из 76)

**Purpose:** Apply 18 most frequent standards (из 76 Альтшуллера), covering ~80% of typical vepol tasks. MPV-anchored.

**When to use:**
- Have a vepol model from `@vepoli`
- Need quick proven solution pattern
- Vepol is Incomplete / Harmful / Insufficient / Measurement

**Output:** Vepol diagnosis, selected standard with code, transformation logic (before→after), No-Go conditions, Reflection Gate

**Gate Check:**
- Vepol type correctly classified
- Standard from correct Class (1-5)
- Concrete resource from `@resource_analysis` used
- MPV/metric anchored (or explicit `[ASSUME]` + test)
- Reflection Gate (CRITICAL + BLIND SPOT) filled
