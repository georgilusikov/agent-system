# Example: ARIZ-85C - The "Fragile Bulb" Problem

## Input
"We need to test glass light bulbs for micro-cracks by pressurizing them. But putting them in a chamber and pressurizing takes too long (pressurize/depressurize cycle). If we pressurize fast, they break from shock. If we keep the chamber pressurized, how do we get bulbs in/out without losing pressure?"

## Execution Trace (ARIZ Protocol)

### PART 1: Model
- **Target:** Light Bulb (Glass).
- **Tool:** Pressure Chamber (Air).
- **Conflict:**
    - TC-1: If Chamber is OPEN -> Bulbs move fast (+), Pressure is lost (-).
    - TC-2: If Chamber is SEALED -> Pressure kept (+), Bulbs cannot enter (-).
- **X-Component:** Something at the entrance.

### PART 2: Resources
- **OZ:** Entrance of the chamber.
- **OT:** Moment of entry.
- **Resources:**
    - Zones: Entrance, Inside, Outside.
    - Substances: Air, Bulb, Glass, **Water** (if used for cooling elsewhere?), **Mercury** (liquid seal?).
    - Fields: Gravity, Atmospheric Pressure.

### PART 3: IFR and PC
- **IFR-1:** The *Entrance Itself* allows the bulb to pass but stops the air.
- **Physical Contradiction:** The Entrance must be **OPEN** (for Bulb) and **CLOSED** (for Air).

### PART 4: Mobilization (MMCH)
- Imagine "Little Men" at the door.
- When Bulb comes, they step aside (Open).
- When Air tries to pass, they lock arms (Closed).
- **Concept:** What acts like these Little Men?
    - A **Liquid Trap (U-shaped water seal)**?
    - But pressure is high, water will blow out.
    - We need a "Heavy Liquid". -> **Mercury** or **Ferrofluid** held by a magnet.

### PART 5: Solution w/ Effects
- Use a **Ferrofluid Seal**.
- Magnetic field holds the liquid (Closed for Air).
- Glass bulb passes through liquid easily (Open for Object).

## Output
## 💎 ARIZ-85C Analysis: Pressure Chamber Seal

### PART 1: The Model
- **Mini-Problem:** Allow bulbs to enter high-pressure zone without losing pressure.

### PART 2: Resources
- **Zone:** Chamber Entrance.
- **Resources:** Air, Magnetic Field (if available), Liquid (Seal).

### PART 3: The Contradiction
**Physical Contradiction:** The "Door" must be **Hole** (for Bulb) and **Solid Wall** (for Air).

### PART 4: Solution Concept
**Concept:** **Magnetic Liquid Seal (Ferrofluid).**
**Logic:** A magnetic liquid held by a ring magnet forms a "Liquid Wall".
- For Air (`P_air < P_magnetic`): It is a WALL.
- For Bulb (Solid object): It is a LIQUID (permeable).
- **Result:** Continuous testing without depressurization.

### PART 5: Validation
- Does it use resources? Yes (Field + Substance).
- Complexity: Medium (Need magnets).
- Efficiency: Extremely High (Continuous flow).
