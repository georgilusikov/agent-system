---
skill_id: spec_flow
skill_name: Spec Flow Validation
version: 1.0.0
category: dev
triggers:
  - "spec flow"
  - "validate plan"
  - "review plan"
  - "before start"
dependencies: []
disable-model-invocation: true
description: "Validate implementation plan before starting significant work (>3 files or >30 min). Use before complex features or refactoring."
---

# Spec Flow Validation

1. **State the plan**: 3-7 steps, files affected, expected outcome
2. **Multi-persona challenge**:
   - **Architect**: Design sense? YAGNI violations?
   - **QA**: How to test? Edge cases?
   - **Security**: Credentials, injection, access control?
   - **User**: Is this what was actually asked for?
3. **Risk assessment**: What can go wrong? Rollback strategy?
4. **Decision**: Proceed (>80%), modify, or ask user (<50%)
