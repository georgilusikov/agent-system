---
skill_id: master_triz_orchestrator
name: master-triz-orchestrator
skill_name: TRIZ General HQ
version: 4.2.0  # Step-by-step routing + skeleton_maps/ lazy loading + Redkolis rules + Adaptive Critic
category: orchestration
triggers: ["TRIZ", "ТРИЗ", "solve problem", "/triz"]
dependencies: ["final_triz_report"]
routing_targets:
  # === Аналитические (диагностика) ===
  - akts
  - causal_analysis
  - flow_analysis
  - diversion_analysis
  - functional_analysis
  - value_analysis
  - structural_analysis
  - informational_flow_analysis
  - avf
  - afd_failure_predictor
  - inconsistent_parameters
  - principle_comparison
  - socratic
  # === Моделирование ===
  - oz_ov
  - ikr
  - vepoli
  - mmch
  - system_operator
  - rtv
  - rvs
  - goldfish
  # === Решение противоречий ===
  - contradictions
  - ariz
  - arip
  - forty_principles
  - inversion
  - antisystem
  - dnd
  # === Синтез (решения) ===
  - trimming
  - fos
  - reverse_fos
  - ofop
  - benchmarking
  - standards
  - effects
  - chemical_triz
  - pn_eco_innovation
  - oas_transfer
  - patent_claims
  - morphological_analysis
  - dynamization
  # === Стратегия/эволюция ===
  - s_curve
  - zrts
  - limits_strategy
  - robinson
  # === Верификация ===
  - critic
  - reflection_gate
  - experiment_designer
  # === Утилитарные ===
  - case_logger
  - final_triz_report
description: 'TRIZ TRIZ General HQ — use for triggers in SKILL.md: triggers: [''TRIZ'', ''ТРИЗ'', ''solve problem'', ''/triz''], ''final_triz_report''.'
---
# 🎖️ TRIZ General HQ
**Role:** Центральный роутер TRIZ.
**Description:** Классифицирует запрос, выбирает цепочку скиллов, проверяет их валидаторы, не симулирует ответы. При запросе на "отчет/результат" запускает сборку финального человеко‑читаемого отчёта через `@final_triz_report`.
**Output:** Диспетч (маршрут + проверки) + финальный отчёт (если это нужно пользователю).
**Quality:** Русский текст; выводы с маркером/порогом/проверкой или `[ASSUME]+тест`; для стратегии — ищем хотя бы 1 перенос тренда.
**Gate Check:** См. `core_instructions.md` — строгий роутинг, без self‑simulation, с проверкой `validators/gate_check.md` выбранного скилла.
**Writer Framework:** При генерации классического TRIZ-отчёта — **обязательно** прочитай и следуй `classic_report_writer.mdc` (содержит все фазы: Phase 0–6, Feasibility Gate, Anti-Patterns, Gate Check). Шаблон выхода: `templates/classic_triz_report.md`.
