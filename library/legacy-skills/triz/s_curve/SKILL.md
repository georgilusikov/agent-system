---
skill_id: s_curve
name: s-curve
skill_name: S-Curve Analysis
version: 3.0.0
category: triz
triggers: ["S-кривая", "стадия развития", "жизненный цикл", "MPV", "предел развития"]
dependencies: []
description: 'S-Curve Analysis: Определить стадию S-кривой через декомпозицию MPV→MFPV→FPV.'
---

# 📈 S-Curve Analysis
**Purpose:** Определить стадию S-кривой через декомпозицию MPV→MFPV→FPV.
**When to use:** Стратегическое планирование, поиск предела развития.
**Output:** MPV Hierarchy, Limits Matrix, Stage Diagnosis, Strategic Directive.
**Gate Check:**
- [ ] MPV Hierarchy декомпозирована?
- [ ] % от физического предела рассчитан?
- [ ] ≥5 индикаторов подтверждают стадию?
- [ ] Триангуляция выполнена?
- [ ] **Evidence tag:** S-Curve stage MUST have [DATA] or [OBS] evidence. [ASSUME]/[SPEC] is NOT acceptable for S-Curve determination. If no hard data → mark [DERIVE] and explain reasoning chain.
