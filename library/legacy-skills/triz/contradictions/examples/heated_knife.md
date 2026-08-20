# Example: Hot/Cold Knife

## Input
"I want a knife that cuts frozen butter easily (needs to be hot) but doesn't melt the butter structurally or burn the user (needs to be cold)."

## Execution Trace
1.  **Localization:**
    - Zone: The Blade surface.
    - Time: During cutting.
    - Element: **The Blade**.

2.  **TC Formulation:**
    - TC-1: If Blade is HOT -> Cuts fast (+), but Melts butter/User risk (-).
    - TC-2: If Blade is COLD -> Safe (+), but Cuts hard (-).
    - Selection: TC-1 (We need cutting speed).

3.  **Physical Contradiction:**
    - "**The Blade** must be **HOT** to cut easily, AND must be **COLD** to preserve butter shape/safety."

4.  **Resolution Strategies:**
    - *Space:* Edge is hot, handle/spine is cold? (Partial solution).
    - *Time:* Hot only at the moment of entry? (Induction heating? Complex).
    - *structure:* Micro-saw? (Mechanical solution, avoids heat).
    - *Condition (Logic of FOS):* Maybe the *butter* should be soft? No, butter is given.

5.  **Refined PC (Parametric):** "The *contact interface* must be Liquid (hot) and Solid (cold)."

6.  **Separation:**
    - **Separation in Space:** The very edge is a heated wire (Hot), the rest of the blade is removed or insulated (Cold).
    - **Separation in Structure:** The blade vibrates (Ultrasonic). Friction heat is generated ONLY at the contact point (Micro-Space), while the blade remains macro-cold.

## Output
## ⚔️ Contradiction Analysis: Frozen Butter Knife

### 1. Localization
- **Zone:** Blade Edge / Butter Interface.
- **Element:** Knife Blade.

### 2. Physical Contradiction
"The **Blade Edge** must be **HOT** (to melt path through butter) AND must be **COLD** (to keep butter structure and user safety)."

### 3. Resolution Strategy
| Principle | Concept |
|-----------|---------|
| **Space** | Heated edge only (Wire cutter). |
| **Structure** | **Ultrasonic Vibration.** |

### 4. Selected Solution
**Strategy:** Separation in Structure (System effect).
**Concept:** **Ultrasonic Knife**.
- The vibration creates friction heat strictly at the *micro-point* of contact (Operational Zone).
- Macroscopically, the blade remains cold to the touch.
- Conflict resolved: Hot locally, Cold globally.

## Why This Works
Correctly identifies that "Hot" is needed only for *function* (cutting), not as a state of the object. Ultrasonic creates "Heat on Demand" at the exact spot.
