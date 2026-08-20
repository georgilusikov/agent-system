---
skill_id: afd_failure_predictor
name: afd-failure-predictor
skill_name: AFD Failure Predictor
version: 1.0.0
category: analysis
triggers: ["найди риски", "предскажи отказ", "скрытые дефекты", "как это сломается", "уязвимости системы", "find risks", "predict failure", "vulnerability"]
dependencies: []
description: Specialized Anticipatory Failure Determination (AFD) skill using Pevzner's hidden defect classification to proactively invent system failures.
---

# Anticipatory Failure Determination (AFD)

Use this skill when tasked with finding risks, vulnerabilities, or preventing failures in a system (mechanical, software, or business).

Instead of standard risk analysis, this skill uses inverted thinking: it acts as a "saboteur" trying to intentionally break the system using available resources and time. It systematically explores three hidden defect categories:
1. Delayed Defects
2. Time-dependent Defects (Degradation)
3. Special Condition Defects

Follow exactly the guidelines provided in `core_instructions.md` when tasked with an AFD analysis.
