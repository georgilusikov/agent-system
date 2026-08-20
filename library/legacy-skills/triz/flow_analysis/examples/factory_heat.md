# Example: Flow Analysis - Factory Heat Loss

## Input
"A factory gets its heat from a central boiler room. Energy costs are rising, but the production floor is still cold. We need to analyze the heat flow."

## Execution Trace

### 1. Flow Mapping
- **Source:** Central Boiler.
- **Carrier:** Steam/Hot Water.
- **Pipe Network:** 500 meters of steel piping.
- **Consumer:** Production Hall radiators.

### 2. Pathologies Detected
- **Leakage (Utyechka):** Pipes are poorly insulated. Infra-red scan shows 30% energy loss into the empty backyard air before reaching the hall.
- **Bottleneck (Zator):** The main valve at the hall entrance is for a 2-inch pipe, while the main feed is 4-inch. Flow is restricted.
- **Gray Zone (Stagnation):** Radiators are located only on one side. Heat stays near the walls; the center of the hall remains cold (no convection flow).

### 3. Proposed Actions
- **Isolation:** Insulate the pipes (Fix leakage).
- **Component Change:** Replace the valve to match pipe diameter (Fix bottleneck).
- **Dynamization:** Add ceiling fans to circulate the air (Fix gray zones).

## Output
- **Primary Pathology:** 30% Leakage + Entrance Bottleneck.
- **Result:** Energy usage reduced by 20% after fixing the flow.
