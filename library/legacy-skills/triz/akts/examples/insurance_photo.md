# Example: AKTS - Insurance Photo Case

## Input
"Process of photographing a car for KASKO insurance takes too long and requires driving to the office."

## Execution Trace

### 1. System Definition
- **System:** Car Inspection Process.
- **Goal:** Verify car condition for policy issuance.

### 2. Stakeholder Map
- **Primary:** Client (Driver), Manager (Insurer).
- **Secondary:** Photographer (Agent).
- **Hidden:** **Family** (waiting in the car!), Queue (other clients).

### 3. Satisfaction Analysis (MPV)
- **Parameter:** Waiting Time.
    - **Our System:** Low Satisfaction (30 mins + travel).
    - **Market Best:** High Satisfaction (5 mins app self-service).
    - **Gap:** Huge. This is the **MPV Target**.

### 4. Rudiments Identification
- **Photographer:** Why is he needed? To verify authenticity. Can we trim him?
- **Trip to Office:** Why? To meet the photographer.

## Output
- **Key Insight:** The "Photographer" is a rudiment. The function "Verify Authenticity" can be delegated to the **Client** (via App with geoloc/timestamp) or **AI** (fraud detection).
- **Proposed Change:** Switch to Self-Inspection via Mobile App. Eliminate office trip.
