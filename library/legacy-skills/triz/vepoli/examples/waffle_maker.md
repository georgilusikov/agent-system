# Example: Vepoli - Waffle Maker Overheat

## Input
"Plastic latch (S1) on a waffle maker melts because it touches the hot metal casing (S2) heated by the coil (F_heat)."

## Execution Trace

### 1. Vepol Diagnosis
- **S1 (Object):** Plastic Latch.
- **S2 (Tool):** Hot Casing.
- **F (Field):** Thermal Field (Heat).
- **Type:** **Harmful Vepol** (S2 heats S1, causing damage).

### 2. Standard Solutions (Class 1)
- **Std 1.2.1 (Remove coupling):** Move S1 away from S2. (Design change).
- **Std 1.2.2 (Add S3):** Introduce a blocker between S1 and S2.
    - *Idea:* Thermal insulation gasket (S3).
- **Std 1.2.4 (Field F2):** Counter-field.
    - *Idea:* Cooling fan (F_cool). (Too expensive).

### 3. Advanced Synthesis (Smart S3)
- Use a **Bi-metallic strip** (S3) instead of simple plastic.
- When F_heat rises, S3 bends and disconnects the circuit (Self-Regulation).

## Output
- **Model:** Harmful Vepol S1-S2 (Heat).
- **Solution:** Introduce S3 (Insulator) or Change S1 to Heat-Resistant Material.
