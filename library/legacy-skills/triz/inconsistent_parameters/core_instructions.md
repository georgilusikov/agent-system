# Core Instructions: Inconsistent Parameters Method

## 1. Context and Purpose
The "Method for identifying inconsistent parameters" (Метод определения несогласованных параметров) enhances classical TRIZ Functional Modeling. It is used when a system fails or performs poorly, but the exact chain of causation is obscured by complex interactions.

## 2. Step 1: Extended Functional Modeling
Build a standard Functional Model (Component A -> Function -> Component B).
**New requirement:** Add a fourth column called "Parameter Object" (Параметр объекта).
For every function, explicitly state:
- What is the expected parameter of Component B (e.g., Temperature = 100C)?
- What is the actual parameter delivered by Component A (e.g., Temperature = 85C)?

Identify the exact **inconsistency** (несогласованность) between the required parameter and the delivered parameter.

## 3. Step 2: The Inverse Graph (Инверсный Граф)
Normally, models map components as nodes and functions as edges.
In this method, **invert the graph**:
- **Nodes** become the Functions.
- **Edges** become the Components that transfer states between functions.

By tracing the Inverse Graph backward from the ultimate Harmful Function (or inadequate Useful Function), you will reveal the "Chain of Inadequate Execution" (Цепочка неадекватного выполнения).

## 4. Step 3: Resolving the Mismatch
Once the root inconsistent parameter is identified at the start of the chain:
1. Formulate a Technical Contradiction (TC) or Physical Contradiction (PC) specifically about that parameter.
2. Apply standard TRIZ resolution tools (`Forty Principles`, `Separation Principles`) to align the parameter without introducing new harm.

## 5. Output Format
When executing this method, you must output:
1. **Parameter Mismatch Table**: A list of the top 3 functions where the required parameter of the target object does NOT match the delivered parameter of the tool object.
2. **Inverse Graph tracing**: A text-based trace (Function C <- Component 2 <- Function B <- Component 1 <- Function A) showing how the initial mismatch caused the final failure.
3. **Contradiction Definition**: The exact contradiction formulated from the root mismatch.
