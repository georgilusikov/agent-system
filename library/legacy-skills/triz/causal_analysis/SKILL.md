---
skill_id: causal_analysis
name: causal-analysis
skill_name: RCA+ (Causal Analysis)
version: 1.0.0
category: diagnostics
triggers:
  - "RCA"
  - "поиск причин"
  - "почему сломалось"
  - "анализ нежелательного эффекта"
  - "корневая причина"
dependencies: ["contradictions"]
description: 'RCA+: Deep search for root causes of undesirable effects (NUE).'
---

# 🌳 RCA+ (Причинно-Следственный Анализ)

**Purpose:** Deep search for root causes of undesirable effects (NUE).

**When to use:**
- Something is broken or working incorrectly
- Need to find "Primary Sin" in design/process
- To understand deep logic of failure before solving

**Output:** Causal chain/graph, formulated Root Causes, link to contradictions

**Gate Check:**
- Minimum 5 levels of "Why?"
- Stop condition reached (Physical/Control/Env Limit)
- Vicious circles checked
- Root causes clearly identified
