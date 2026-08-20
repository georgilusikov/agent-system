# Example: Light Bulb Factory

## Input
"How to remove air from the glass bulb to prevent filament oxidation?"

## Execution Trace (Resource Hunt)
1.  **Scope:**
    - Zone: Inside the Bulb.
    - Time: During manufacturing.

2.  **V-Resources (Substances):**
    - V1 (Product): **Glass Bulb** (Transparent, Rigid), **Filament** (Tungsten).
    - V2 (Tool): **Pump** (External).
    - V3 (Env/Waste): **Air** (Oxygen = Enemy), **Burned Tungsten** (Waste).
    - V-Zero: **Vacuum** (The absence of air).

3.  **P-Resources (Fields):**
    - P_therm: Heat from the filament itself (High T!).
    - P_mech: Atmospheric pressure pressing outside.
    - P_chem: Oxidation reaction (Harmful).

4.  **Transformation check:**
    - Can we use P_therm (Heat) to interact with Air?
    - Idea: Put a chemical "Getter" (V-Aux) that reacts with Air when heated by Filament (P_therm).
    - Result: Air is consumed by the reaction triggered by the bulb's own heat.

## Output
## 💎 Resource Analysis: Vacuum in Bulb

### 1. Substance Registry
| Code | Name | Role | Note |
|------|------|------|------|
| **V1** | Filament | Product | Source of Heat (P_therm) |
| **V3** | Oxygen | Environment | The target to remove |
| **V-Aux**| Getter | Additive | Absorbs Oxygen |

### 2. Field Registry
| Type | Source | Usability |
|------|--------|-----------|
| **P_therm** | Filament heating | **Perfect (Ready)** |

### 3. Top Idea
**"Chemical Vacuum"**: Use the Filament's own heat (P_therm) to activate a getter (V-Aux) that eats the Oxygen (V3).
**Cost:** Minimal (speck of chemical). Pump is removed/simplified.

## ➡️ Next Step
→ @vepoli (Model: V_air + V_getter + P_therm -> Solid_Oxide).
