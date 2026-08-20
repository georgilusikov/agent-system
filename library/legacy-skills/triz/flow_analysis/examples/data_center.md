# Example: Data Center Cooling

## Input
"Our server room overheats despite having powerful AC units."

## Execution Trace
1.  **Flow ID:**
    - Type: **Energy Flow** (Heat).
    - Source: Servers (CPU/GPU).
    - Target: Outdoor Environment.

2.  **Flow Mapping:**
    `[CPU] -> [Heatsink] -> [Rack Air] -> [Room Air] -> [AC Intake] -> [Freon] -> [Outdoor]`

3.  **Pathology Diagnosis:**
    - **Bottleneck:** `[Rack Air] -> [Room Air]`. The hot air from servers mixes with cold room air immediately (Short Circuit).
    - **Vortex:** Hot air recirculates back into server intake because racks are not sealed.
    - **Dead Zone:** Corners of the room where air doesn't move.

4.  **Conservation Check:**
    - Input Heat: 100 kW.
    - AC Removal Capacity: 150 kW.
    - Result: Overheating! Why? Because the flow isn't REACHING the AC effectively.

## Output
## 🌊 Flow Analysis: Server Room Heat

### 1. Flow Map
- **Type:** Thermal Energy (Heat)
- **Route:** `CPU -> Rack Air -> Room Air (Mix) -> AC Unit`

### 2. Identified Pathologies
| Location | Type | Severity | Fix Logic |
|----------|------|----------|-----------|
| **Rack Exhaust** | **Vortex (Recirculation)** | **Critical** | Hot air flows back to intake (Short circuit). |
| **Room Space** | **Mixing (Entropy)** | High | Mixing hot/cold air degrades AC efficiency (Delta-T drops). |

### 3. Solution Logic
Isolate the flow! "Hot Aisle / Cold Aisle" containment.
- Convert "Mixing Chamber" (Room) into "Duct" (Direct path).

## ➡️ Next Step
→ @trimming (Remove "Room Air" link, connect Rack directly to AC duct).
