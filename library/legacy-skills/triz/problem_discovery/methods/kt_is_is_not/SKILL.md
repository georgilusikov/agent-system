---
skill_id: kt_is_is_not
name: kt-is-is-not
description: Kepner-Tregoe IS/IS NOT analysis for isolating the cause of deviations from normal operation
version: 1.0.0
category: analysis
triggers:
  - "сломалось"
  - "перестало работать"
  - "отклонение"
  - "раньше работало"
  - "дефект"
  - "причина неизвестна"
  - "investigation"
dependencies: []
---

# 🔍 Kepner-Tregoe IS/IS NOT Analysis

> Transitional reference only. The executable top-level runtime skill now lives at `triz/kt_is_is_not/`.

**Purpose:** Systematically isolate the most probable cause of a deviation from normal operation by comparing where the problem IS versus where it IS NOT.

**Origin:** Charles Kepner & Benjamin Tregoe (1958). Used by Ford (8D), VDA (automotive), IATF 16949.

**When to use:**
- Something broke/failed/degraded and the cause is unknown
- System worked before and now doesn't (deviation from norm)
- Need to distinguish symptoms from root cause
- Multiple possible causes and need to narrow down quickly

**When NOT to use:**
- Innovation tasks (no "norm" to deviate from)
- Optimization/cost reduction (use ARIZ or Value Analysis)
- Vague user complaints without observable symptoms (use Empathy Probe)

## Instructions

### Step 1: Problem Statement

Write a clear deviation statement:

```text
[OBJECT] has [DEVIATION] since [TIME/EVENT].
Expected: [normal behavior]
Actual: [observed behavior]
```

**Rule:** The statement must describe a CHANGE. If the system never worked correctly, KT is the wrong method.

### Step 2: IS/IS NOT Matrix

Build the contrast matrix across 4 dimensions:

| Dimension | IS (problem present) | IS NOT (problem absent) | Distinction |
|-----------|---------------------|------------------------|-------------|
| **WHAT** — What object has the defect? | [affected objects] | [similar objects WITHOUT defect] | [what's unique about affected?] |
| **WHERE** — Where on the object? Where geographically? | [locations with defect] | [locations WITHOUT defect] | [what's unique about those locations?] |
| **WHEN** — When first observed? When in cycle/process? | [times when defect occurs] | [times when defect does NOT occur] | [what changed at that time?] |
| **EXTENT** — How many? How much? Trend? | [scope/quantity/trend] | [expected scope if worse] | [why this extent and not more?] |

### Step 3: Distinction Analysis

For each row, identify the DISTINCTION — what is unique about the IS column compared to IS NOT.

**Key question:** "What is different, unique, or peculiar about the IS compared to the IS NOT?"

### Step 4: Change Analysis

For each distinction, ask: "What CHANGED in, on, around, or about this distinction?"

List all changes that correlate with the timing of the deviation.

### Step 5: Most Probable Cause

Test each possible cause against ALL IS/IS NOT data:

```text
IF [proposed cause] is true:
  ✅ Does it explain WHY the problem IS in [IS column]?
  ✅ Does it explain WHY the problem IS NOT in [IS NOT column]?
  ✅ Does it explain the EXTENT?
  ✅ Does it explain the TIMING?
```

**Rule:** A cause must explain BOTH the IS AND the IS NOT. If it only explains IS but not IS NOT → reject it.

### Step 6: Handoff to ARIZ

Once the most probable cause is identified, translate it to TRIZ language:

```text
CAUSE FOUND: [specific cause]
→ OBJECT (Изделие): [what is affected]
→ TOOL (Инструмент): [what causes the effect — the cause itself]
→ Suggested TP: IF [cause is present], THEN [harmful effect], BUT [useful function it also serves]
```

Pass this to `@problem_formulator` for full ARIZ-85B formulation.

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Skip IS NOT column | IS NOT is where the insight lives |
| Accept first plausible cause | Test against ALL four dimensions |
| Use for innovation tasks | KT works only for deviations from an existing norm |
| Mix symptoms with causes | Symptoms go in WHAT IS, causes come from analysis |
| Rush to the fix | Complete the full matrix before proposing causes |

## Output Format

```markdown
## 🔍 KT IS/IS NOT Report

### Problem Statement
[OBJECT] has [DEVIATION] since [TIME].

### IS/IS NOT Matrix
| Dimension | IS | IS NOT | Distinction | Change |
|-----------|----|----|-------------|--------|
| WHAT | ... | ... | ... | ... |
| WHERE | ... | ... | ... | ... |
| WHEN | ... | ... | ... | ... |
| EXTENT | ... | ... | ... | ... |

### Tested Causes
| # | Proposed Cause | Explains IS? | Explains IS NOT? | Verdict |
|---|---------------|-------------|-----------------|---------|
| 1 | ... | ✅/❌ | ✅/❌ | Accept/Reject |

### Most Probable Cause
[cause] → confidence: [High/Medium/Low]

### TRIZ Translation
- Object: [...]
- Tool: [...]
- Suggested TP: [...]
→ Handoff: @problem_formulator
```

## Gate Check

| Criterion | Required | Pass? |
|-----------|----------|-------|
| Deviation statement describes a CHANGE | Yes | ✅/❌ |
| All 4 dimensions filled (WHAT/WHERE/WHEN/EXTENT) | Yes | ✅/❌ |
| IS NOT column is not empty | Yes | ✅/❌ |
| At least one distinction identified | Yes | ✅/❌ |
| Proposed cause tested against IS AND IS NOT | Yes | ✅/❌ |
| TRIZ translation provided for handoff | Yes | ✅/❌ |

## Next Step / Handoff

1. Cause found → `@problem_formulator` (formulate TP around the cause)
2. Cause unclear after matrix → `@causal_analysis` (deeper RCA+)
3. Multiple equally probable causes → `@experiment_designer` (design test to discriminate)
