# Example: Trimming the Smartphone Bezel

## Input
"Smartphone Bezel (Frame around screen)."

## Execution Trace
1.  **Target ID:**
    - Component: Bezel.
    - Function: Holds the screen, Protects edge, Hides connectors.
    - Rank: C (We want full screen).

2.  **Rules Application:**
    - **A (Useless):** Can we remove protection? No, glass breaks.
    - **B (Self-service):** Can the Screen hold itself? Yes, if glass is structural (Gorilla Glass).
    - **C (Tool):** Can the Body hold it? Yes.
    - **E (Component):** Can the Glue hold it? Yes.
    - **F (Physics):** Can we bend the light (Optical Effect) to hide the bezel? (2.5D Glass).

3.  **Concept:** "Waterfall Display" (Curved Glass).
    - The screen (Rank A) *becomes* the edge.
    - Bezel is trimmed physically from the front view.

4.  **Energy Path / Physics:**
    - Structural integrity provided by the Glass itself (Self-service).
    - Touch rejection needed (Software fix).

5.  **Secondary Problem:**
    - "Screen at the edge breaks easily."
    - Contradiction: Glass must be at the edge (for design) AND not at the edge (for safety).

## Output
## ✂️ Trimming Analysis: Smartphone Bezel

### 1. Trimming Target
- **Component:** Bezel (Frame)
- **Function:** Structural Support
- **Goal:** Remove it (100% Screen-to-body ratio)

### 2. Applied Rules
| Rule | Idea | Result |
|------|------|--------|
| **B (Self)** | **Screen is the structure** | **Selected** |
| **F (Physics)** | Optical Illusion (Bend light) | Selected (Combined) |

### 3. Selected Concept
**Concept:** "Waterfall / Edgeless Display".
- The physical frame is removed from sight.
- The glass curves around the side.

### 4. Secondary Problems
- **Conflict:** Accidental touches on the side.
- **Handoff:** -> @contradictions ("Screen must be sensitive for fingers, but insensitive for grip").

## ➡️ Next Step
→ @contradictions
