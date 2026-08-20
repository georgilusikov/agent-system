---
skill_id: avf
name: avf
skill_name: AVF (Environment Analysis)
version: 1.0.0
category: diagnostics
triggers:
  - "АВФ"
  - "черный ящик"
  - "входы выходы"
  - "среда"
  - "внешние факторы"
dependencies: ["flow_analysis", "diversion_analysis"]
description: 'AVF: Analyze ''Black Box'' from outside - inputs, outputs, disturbances.'
---

# 🌍 AVF (Environment Analysis)

**Purpose:** Analyze "Black Box" from outside - inputs, outputs, disturbances.

**When to use:**
- Problems at system boundary
- Looking for free resources in environment
- Checking system isolation

**Output:** I/O map, disturbances, constraints, resource opportunities

**Gate Check:**
- All inputs classified (Substance/Energy/Info)
- All outputs classified (Product/Waste/Loss)
- Disturbances and constraints identified
