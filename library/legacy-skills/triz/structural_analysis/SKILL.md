---
skill_id: structural_analysis
name: structural-analysis
skill_name: Structural Analysis
version: 1.0.0
category: diagnostics
triggers:
  - "структурный анализ"
  - "связи компонентов"
  - "топология"
  - "граф системы"
dependencies: ["dynamization", "vepoli"]
description: 'Structural Analysis: Analyze and optimize component connections.'
---

# 🏗 Structural Analysis

**Purpose:** Analyze and optimize component connections.

**When to use:**
- Need to understand system architecture
- Looking for rigid connections to replace
- Finding bridges and bottlenecks

**Output:** System graph, connection analysis, dynamization recommendations

**Gate Check:**
- Graph built (nodes = components, edges = connections)
- Connection types classified (Rigid/Flexible/Field)
- Bridges and high-coupling areas identified
