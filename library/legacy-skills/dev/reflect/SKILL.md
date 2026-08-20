---
skill_id: reflect
skill_name: Self-Reflection
version: 1.0.0
category: dev
triggers:
  - "reflect"
  - "саморефлексия"
  - "gap analysis"
  - "что упустил"
dependencies: ["compound_learning"]
description: "Self-reflection after completing a task. Use when finishing work, encountering repeated failures, or when quality check is needed."
---

# Self-Reflection Protocol

1. **Gap analysis**: expected vs actual output
2. **What was missed?** Edge cases, untested paths
3. **Confidence recalibration**: [before]% → [after]% — [reason]
4. **Record learnings**:
   - Errors → `_agent_shared/error_feedback/errors_YYYY-MM.md`
   - Patterns → `_agent_shared/memory/patterns.md`
