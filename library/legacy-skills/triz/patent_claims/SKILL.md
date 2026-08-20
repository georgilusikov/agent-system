---
skill_id: patent_claims
name: patent-claims
skill_name: Patent Claims (Draft/Refine)
version: 1.0.0
category: synthesis
triggers:
  - "patent claim"
  - "патентная формула"
  - "claims"
  - "патентовать"
dependencies: []
description: 'Patent Claims: Сформировать черновик патентной формулы (независимый + зависимые) из TRIZ‑решения, убрать стоп‑терми.'
---

# 🧾 Patent Claims (Draft/Refine)
**Purpose:** Сформировать черновик патентной формулы (независимый + зависимые) из TRIZ‑решения, убрать стоп‑термины и отметить риски (overbreadth/indefiniteness).
**Inputs:** Узлы/признаки решения, PoA, отличия от прототипа; страна (RU/EPO/US); тип (устройство/способ/ПО).
**Outputs:** Независимый пункт + 2–3 зависимых; таблица рисков и что вынести в зависимые.
**Gate Check:** см. `validators/gate_check.md`
- Существенные признаки перечислены; есть отличие от прототипа.
- Независимый пункт без стоп‑слов и “голых” функциональных терминов.
- Зависимые уточняют материалы/режимы/варианты; риски рассмотрены.
