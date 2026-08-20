# Example: Aircraft Wing Optimization

## Input
"We need to make the aircraft wing lighter to increase range, but making it thinner or using less material reduces its structural strength and durability."

## Execution Trace
1. **Identify Parameters:**
   - Improving: Lighter Wing -> **Weight of moving object (#1)**
   - Worsening: Less Strength -> **Strength (#14)**
2. **Matrix Lookup:**
   - Command: `python3 _agent_shared/scripts/triz_matrix_lookup.py --improving 1 --worsening 14`
   - Result: [28, 27, 18, 40]
3. **Concept Generation:**
   - Principle #1 (28 Mechanics Substitution / Mechanical System Substitution): Use pneumatic structures? Flexible?
   - Principle #2 (27 Cheap Short-Living Objects): Disposable wings? No.
   - Principle #3 (18 Mechanical Vibration): Not clear.
   - Principle #4 (40 Composite Materials): Carbon fiber!
   - Principle #1 (28) Re-interpreted: Replace mechanical stiffeners with air pressure (inflatable) or fields?

## Output
## 💡 TRIZ Principles Solution: Aircraft Wing Weight

### 1. Conflict Parameters (Matrix Input)
- **Improving:** [1] Вес подвижного объекта
- **Worsening:** [14] Прочность
*(Found using scripts/triz_matrix_lookup.py)*

### 2. Matrix Result
**Identified Principles:** #28, #27, #18, #40
*(Found via Altshuller Matrix v1.0)*

### 3. Concept Generation
#### Concept 1: Composite Materials (Principle #40)
- **Mechanism:** Replace aluminum alloys with carbon fiber reinforced polymers (CFRP).
- **Why it works:** Composites provide higher strength-to-weight ratio than metals.

#### Concept 2: Active Pneumatic Structure (Principle #28 - Substitution of Mechanics)
- **Mechanism:** Use internal pressure to maintain rigidity (like a balloon) rather than heavy ribs.
- **Physics:** Pneumatic structures (See `@effects`).

#### Concept 3: Honeycomb Structure (Principle #1 Segmentation/Structure?)
- *Note:* While #1 was not in the top 4, #27 (Cheap copies) might inspire using many small cells (honeycomb) instead of one big spar?
- *Strict Adherence:* Using Principle #27: Use "Cheap" materials? Maybe "Disposable" layers? (Less likely).
- *Re-visiting Principle #18 (Vibration):* Use resonance testing to find exact weak points and reinforce ONLY them (Optimization).

### 4. Recommendation
- **Best Shot:** Concept 1 (Composite Materials) is the standard industry solution derived from Principle #40.

## Why This Works
The AI identified exact parameters and matched them to Principle 40 (Composites), which is the textbook solution for Weight vs Strength in aviation.
