# Example: Micro-Dosing System for Medical Device

## Input
"We need to deliver precise micro-amounts of liquid medication to a patient over a long period. Using a mechanical pump is too bulky, expensive, and consumes too much battery."

## Execution Trace
1. **Identify Function:**
   - Goal: Move liquid (specifically small amounts, slowly).
   - Query: "move liquid"
2. **Database Lookup:**
   - Command: `python3 _agent_shared/scripts/effects_lookup.py "move liquid"`
   - Result:
     - **Capillary Effect** (Score 3) - Passive, no energy.
     - **Osmosis** (Score 3) - High pressure potential, slow rate.
     - **Coanda Effect** (Score 0 - not relevant for micro)
     - **Electro-Osmosis** (Score 0? Let's check synonym "pump liquid" next time, but let's stick to initial results).

   *Refinement:* User mentioned "battery is an issue". Passive effects are best.

3. **Concept Generation:**
   - **Concept A (Capillary):** Use a wick system. Like a felt-tip pen.
   - **Concept B (Osmosis):** Use an osmotic pump. A chamber with salt absorbs water through a membrane, expanding and pushing the drug out.

## Output
## ⚡ Physical Effects Solution: Move Liquid (Micro-Dosing)

### 1. Function Query
**Target Function:** "move liquid"

### 2. Identified Effects
| Effect | Principle | Relevance |
|--------|-----------|-----------|
| **Capillary Effect** | Surface tension | High (Passive) |
| **Osmosis** | Osmotic pressure | High (Strong Force) |

### 3. Application Concepts (Top 3)

#### Concept 1: The "Wick" Injector (Capillary Effect)
- **Mechanism:** Use a porous material (wick) to pull medication from the reservoir to the skin contact point.
- **Implementation:** Calibrate the porosity of the wick to define the exact flow rate.
- **Pros:** Zero energy, zero moving parts, extremely cheap.
- **Cons:** Flow rate depends on viscosity/temperature.

#### Concept 2: The Osmotic Push (Osmosis)
- **Mechanism:** "ALZET" style pump. A salt chamber absorbs body water through a semi-permeable membrane. The salt chamber expands and squeezes the flexible sterile drug reservoir.
- **Implementation:** concentric cylinders: [Outer Membrane] -> [Salt Layer] -> [Flexible Bag with Drug] -> [Outlet].
- **Pros:** Constant flow rate, works solely on body water availability (always present), high force.
- **Recommendation:** This is the industry standard for implantable pumps.

### 4. Recommendation
- **Best Choice:** Concept 2 (**Osmosis**) because it provides a more stable flow rate than capillary action against back-pressure from tissues.

## Why This Works
The agent correctly identified that replacing a mechanical pump (System) with a physical phenomenon (Osmosis) solves the Energy vs Performance contradiction.
