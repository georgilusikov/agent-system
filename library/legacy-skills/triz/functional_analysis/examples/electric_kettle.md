# Example: Electric Kettle Analysis

## Input
"Electric Kettle (heating water)."

## Execution Trace
1.  **Decomposition:**
    - Product: Water.
    - System: Kettle Body, Handle, Lid, Heating Element (Coil), Switch.
    - Environment: Table, Air, Electricity, User.

2.  **Function Modeling (Triplets):**
    - Coil -> Thermal Field -> Body (Heats body = Harmful/Waste).
    - Coil -> Thermal Field -> Water (Heats water = Useful/Main).
    - Water -> Chemical Field -> Coil (Scale formation = Harmful).
    - Body -> Mechanical Field -> Water (Holds water = Useful).
    - Switch -> Electric Field -> Coil (Controls current = Useful).
    - Steam -> Thermal Field -> Switch (Triggers auto-off = Useful).

3.  **Ranking:**
    - **Rank A (Core):** Coil (does the heating), Body (holds water).
    - **Rank B (Support):** Switch, Lid.
    - **Rank C (Aux):** Handle? (Does it need to be a separate part, or can the body be cool?).

## Output
## 🔬 Functional Analysis: Electric Kettle

### 1. Component Map
- **Target:** Water
- **System:** Coil, Body, Switch
- **Supersystem:** Table, Air, 220V

### 2. Interaction Triplets
| Subj | Field | Obj | Type | Note |
|------|-------|-----|------|------|
| **Coil** | **Thermal** | **Water** | **(+)** | Main Function |
| Coil | Thermal | Body | (-) | Energy Loss |
| **Water** | **Chemical** | **Coil** | **(-)** | Scale (Corrosion) |
| Steam | Thermal | Switch | (+) | Auto-off Mechanism |
| Switch | Electric | Coil | (+-) | Sometimes fails (Insufficient) |

### 3. Problem Identification
- **Conflict 1:** Coil heats Body (Waste of energy + Burn risk).
- **Conflict 2:** Water attacks Coil (Scale).
- **Trimming Candidate:** Switch (Can we use the steam directly to disconnect the circuit without a mechanical switch?).

## ➡️ Next Step
→ @contradictions ("Coil must be hot for water, but cold for scale").
