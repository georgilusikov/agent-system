---
skill_id: value_analysis
name: value-analysis
skill_name: Value Analysis (FSA)
version: 1.0.0
category: diagnostics
triggers:
  - "ФСА"
  - "стоимостный анализ"
  - "value engineering"
  - "дорогой узел"
dependencies: ["functional_analysis", "trimming"]
description: 'Value Analysis: Find cost/value disproportion for trimming targets.'
---

# 💰 Value Analysis (ФСА)

**Purpose:** Find cost/value disproportion for trimming targets.

**When to use:**
- Need to reduce costs without losing quality
- Looking for "golden toilets" (expensive low-value parts)
- Before trimming to identify targets

**Output:** FSA index table, problem zones, trimming recommendations

**Gate Check:**
- Functions ranked by consumer value
- Costs allocated to functions (not just parts)
- FSA index calculated (Cost/Value)
