# Example: Contradictions - Airplane Wing (Honeycomb Structure)

## Input
"The airplane wing must be STRONG (to not break during flight) and LIGHT (to take off and save fuel). These requirements seem mutually exclusive."

## Execution Trace (TC/PC Protocol)

### Phase 1: Localization
- **OZ (Zone):** Wing structure (load-bearing sections).
- **OT (Time):** During flight (constant load).
- **Conflict Element:** Wing Material/Structure.
- **Parameters:** Strength vs Weight.

### Phase 2: Technical Contradictions
- **TC-1:** If we add metal -> Strength (+), Weight (-).
- **TC-2:** If we remove metal -> Weight (+), Strength (-).
- **Selection:** TC-1, because wing failure is fatal (blocking main function).

### Phase 3: Physical Contradiction (The Core)
**"Wing material must be HEAVY (lots of substance for strength) AND LIGHT (little substance for weight)."**

### Phase 4: Resolution Strategy
| Principle | Applicability | Hypothesis |
|-----------|---------------|------------|
| **Space** | Yes | Material present WHERE load is, absent WHERE no load. |
| Time | No | Load is constant during flight. |
| **Structure** | Yes | Macro = Strong, Micro = Empty (Honeycomb). |

### Phase 5: Selected Solution
**Strategy:** Separation in Space / Structure.
**Concept:** Use a **honeycomb structure** or porous materials.
- Material IS present at load-bearing paths (ribs, skins).
- Material IS NOT present in empty cells (voids).
- Result: Maximum strength-to-weight ratio.

## Output Summary
- **Physical Contradiction:** The wing must be both heavy and light.
- **Resolution:** Separation in Structure (Honeycomb = Strong Macro, Empty Micro).
- **TRIZ Principle:** #31 (Porous Materials).
