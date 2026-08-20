---
skill_id: final_triz_report
name: final-triz-report
skill_name: TRIZ Final Report Writer
version: 1.0.0
category: reporting
triggers:
  - "итоговый отчет"
  - "итоговый отчёт"
  - "собери отчет"
  - "собери отчёт"
  - "финальный отчет"
  - "финальный отчёт"
  - "отчет для клиента"
  - "отчёт для клиента"
  - "презентуй решение"
  - "сделай понятный отчет"
dependencies: ["system_operator", "ikr", "contradictions", "resource_analysis", "causal_analysis"]
description: 'TRIZ Final Report Writer: Превращает промежуточные артефакты ТРИЗ (RCA/ресурсы/противоречия/ИКР/решения) в **понятный человеко.'
---

# 🧾 TRIZ Final Report Writer

**Purpose:** Превращает промежуточные артефакты ТРИЗ (RCA/ресурсы/противоречия/ИКР/решения) в **понятный человеко‑читаемый отчёт**.

**Ключевое требование:** Если в исходных артефактах есть “Next Step / Handoff”, это **не финал** — финал всегда содержит решения с “как работает / конструкция / сценарий”, таблицу выбора и рекомендацию.

**Gate Check:** см. `validators/gate_check.md`.
