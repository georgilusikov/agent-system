---
skill_id: functional_analysis
name: functional-analysis
skill_name: Functional Analysis
version: 2.2.0
category: triz
triggers:
  - "функциональный анализ"
  - "паразитные функции"
  - "анализ компонентов"
  - "ФА"
  - "ФАП"
  - "Muda"
  - "First Principles Audit"
  - "False Productive"
dependencies: []
changelog:
  - version: 2.2.0
    date: 2026-01-21
    changes:
      - "Added [P/S/C/T/M/L] Process Tagging (from BAS)"
      - "Added First Principles Audit (The 'Why?' Hammer)"
      - "Added 'False Productive' concept and anti-pattern"
      - "Added Efficiency and Ideality formulas"
  - version: 2.1.0
    date: 2025-XX-XX
    changes:
      - "Added MPV Guard and top-1 problem selection"
  - version: 1.0.0
    date: 2025-XX-XX
    changes:
      - "Initial release with MATHEM fields"
description: 'Functional Analysis: Build functional model of system, identify useful/harmful/parasitic functions. Prepare for trimming.'
---

# 🔧 Functional Analysis (ФА + ФАП + Process Tagging)

**Purpose:** Build functional model of system, identify useful/harmful/parasitic functions. Prepare for trimming. Advanced: detect "False Productive" operations.

**When to use:**
- Cost optimization (убрать лишние компоненты)
- Process simplification (убрать лишние операции, особенно [C/T/M])
- Finding "parasites" for trimming
- Business process analysis (с [P/S/C/T/M/L] теггингом)
- First Principles check (Are we solving the right problem?)

**Output:**
- Component/operation table with function tags (physical: Useful/Harmful/Insufficient; process: [P/S/C/T/M/L])
- Efficiency (E) and Ideality (I) scores
- "False Productive" candidates (operations not physically required)
- Rank C candidates for trimming

**Gate Check:**
- Minimum 5 components/operations identified
- At least 2 parasites marked
- For processes: Efficiency E calculated
- Top-1 problem selected (rest parked)

## Output Contract (for BAS Integration)

When used in BAS Phase 2, output **MUST** include:

### Process Map Table (mandatory format)
```markdown
| # | Операция | Тег | Объект | Результат | Время | Комментарий |
|---|---------|-----|--------|-----------|-------|-------------|
| 1 | _action_ | [P] | _target_ | _outcome_ | _min_ | _why needed_ |
```

Tags: `[P]` Productive, `[S]` Supporting, `[C]` Corrective, `[T]` Transport, `[M]` Monitoring, `[L]` Loss

### Efficiency Formula
```
E = P_count / Total_count × 100%
```

### Requirements for BAS HEAVY mode
- **≥3 separate process maps** (Status Quo + 2 competitors)
- **Efficiency comparison table** across all mapped solutions
- All [P] tags verified via First Principles — no false-productive steps
- Top-3 parasites identified with severity ranking
