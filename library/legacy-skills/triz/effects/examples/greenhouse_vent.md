# Example: Effects - Self-Opening Greenhouse Vent

## Input
"A greenhouse vent must open when it gets too hot (to let air in) and close when it cools down (to protect plants). We want a solution that requires NO electricity and NO complex sensors."

## Execution Trace (Physical Effects Selection)

### 1. Desired Function
Convert temperature change (Thermal Field) into movement (Mechanical Field).

### 2. Candidate Effects
- **Effect A: Thermal Expansion (Solids).** Bi-metallic strip.
    - *Pros:* Simple.
    - *Cons:* Small movement range; too weak for large vents.
- **Effect B: Phase Transition (Liquid to Gas/Solid to Liquid).**
    - *Pros:* Huge volume change.
    - *Cons:* Needs a container.
- **Effect C: Shape Memory Alloy (SMA).**
    - *Pros:* High force.
    - *Cons:* Expensive.

### 3. Selection
**Solution:** Wax Cylinder Actuator (Phase Transition).
- **Mechanism:** Solid wax inside a cylinder melts at a specific temperature (Stage 1 -> Stage 2).
- **Physics:** Volume expands by ~15% when melting, pushing a piston.
- **Result:** Piston opens the vent. When it cools, wax solidifies and a spring closes it.

## Output
- **Effect used:** Phase Transition (Solid-Liquid expansion).
- **Result:** Fully autonomous, zero-energy cooling for greenhouses.
