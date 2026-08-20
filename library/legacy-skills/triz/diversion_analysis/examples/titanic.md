# Example: Diversion Analysis - The Titanic (Unsinkable Ship)

## Input
"A ship is designed with 16 watertight compartments. It can float with any 4 of them flooded. Is it truly unsinkable?"

## Execution Trace (The Saboteur's Mind)

### 1. The Goal
"How can I sink this ship despite its protection?"

### 2. Vulnerability Search
- The ship is safe against vertical punctures (e.g. hitting a mine or torpedo hitting 1-2 compartments).
- **Sabotage Idea:** What if I puncture more than 4? How can I do it with one object?
- **Mechanism:** A **longitudinal cut** (along the side) instead of a round hole.

### 3. Resource Exploitation
- If 5+ compartments are open, the ship tips forward (bow sink).
- **Hidden Vulnerability:** Are the bulkheads (walls) sealed at the top (ceiling)?
- **Discovery:** No, they don't reach the upper deck. Water will "spill" from one compartment to the next like an ice tray.

## Output
- **Scenarios:** A glancing blow from an iceberg or a side-swipe by another ship can create a long enough tear to exceed the safety limit (4 compartments).
- **Result:** The "watertight" protection actually hides a fatal flaw in deck height.
- **Countermeasure:** Seal bulkheads to the ceiling or increase the number of allowed flooded compartments.
