---
skill_id: flow_analysis
name: flow-analysis
skill_name: Flow Analysis
version: 1.0.0
category: diagnostics
triggers:
  - "потоки"
  - "узкое место"
  - "bottleneck"
  - "утечка"
  - "КПД"
dependencies: ["trimming", "contradictions"]
description: 'Flow Analysis: Optimize movement of Substance, Energy, Information flows.'
---

# 🌊 Flow Analysis (Потоковый Анализ)

**Purpose:** Optimize movement of Substance, Energy, Information flows.

**When to use:**
- System has low efficiency (KPD < 100%)
- Looking for bottlenecks and leaks
- Need to speed up process

**Output:** Flow map, pathology list (leaks/bottlenecks), recommendations

**Gate Check:**
- Flow type identified (Substance/Energy/Info)
- Source → Path → Consumer mapped
- Pathologies found and classified
