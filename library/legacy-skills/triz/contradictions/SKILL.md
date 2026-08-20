---
skill_id: contradictions
name: contradictions
skill_name: Contradictions (ТП/ФП)
version: 1.0.0
category: triz
triggers:
  - "противоречие"
  - "ТП"
  - "ФП"
  - "конфликт параметров"
  - "компромисс"
dependencies: ["functional_analysis", "akts", "forty_principles", "effects", "socratic"]
description: 'Contradictions: Formulate and resolve Technical (ТП) and Physical (ФП) contradictions.'
---

# ⚖️ Contradictions (ТП/ФП)

**Purpose:** Formulate and resolve Technical (ТП) and Physical (ФП) contradictions.

**When to use:**
- System has conflicting requirements
- Need to improve parameter without worsening another
- Breaking out of compromise thinking

**Output:** ТП-1/ТП-2 pair, ФП formulation, resolution strategy

**Gate Check:**
- ТП formulated as "If [Action], then [Benefit], but [Harm]"
- ФП formulated as "Element must be [X] and [NOT X]"
- ≥4 separation strategies checked (time/space/structure/conditions), best chosen with concept
