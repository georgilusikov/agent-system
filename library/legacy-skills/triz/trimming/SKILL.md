---
skill_id: trimming
name: trimming
skill_name: Trimming (Свертывание)
version: 1.0.0
category: triz
triggers:
  - "свертывание"
  - "trimming"
  - "убрать компонент"
  - "упростить систему"
  - "удалить операцию"
dependencies: ["functional_analysis"]
description: 'Trimming: Radical simplification - remove components/operations while preserving function.'
---

# ✂️ Trimming (Свертывание)

**Purpose:** Radical simplification - remove components/operations while preserving function.

**When to use:**
- After Functional Analysis identified Rank C components
- Need to reduce cost/complexity
- Have parasitic functions to eliminate

**Output:** Trimming plan with delegation rules (6 rules A-F), energy path validation

**Gate Check:**
- MPV/main function anchored
- Components ranked (A/B/C), Rank A protected
- All 6 trimming rules (A-F) checked
- Energy path validated
- Secondary problems (Trimming Conflicts) identified
