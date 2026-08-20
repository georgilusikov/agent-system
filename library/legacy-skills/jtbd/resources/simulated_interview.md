# Simulated User Interview Protocol (Vanechka Switch)

> **Универсальный JTBD switch-протокол** (канон-ресурс jtbd). Проектная реализация-источник —
> `projects/Business_Architect_System/docs/workflows/tools/simulated_interview.md` (синхронизировано через `cp`).

**Goal:** Simulate a depth interview (JTBD Switch) with a synthetic persona to uncover deep motivations and "Forces of Progress" that pure data mining misses.

## 🎭 The Persona Engine
Before interviewing, generate a **Persona** based on the `Phase 1` Signals (The "Hate Cluster").
*   **Name:** [Name]
*   **Role:** [Role facing the problem]
*   **Context:** Just switched (or tried to switch) from [Current Solution] to [Competitor/Alternative].
*   **Mood:** Frustrated / Anxious / Relieved.

## 🎤 The Interview Script (Switch Protocol)
Agent acts as the **Interviewer**. Synthetic Persona acts as the **Respondent**.

### Step 1: The Switch Event (Point B)
*   **Q:** "Tell me about the moment you finally bought/switched to [New Solution]. When was it?"
*   **Goal:** Anchor in a real (simulated) moment.

### Step 2: The Trigger (Point A)
*   **Q:** "What happened on that day that made you say 'Enough is enough'? What was the specific trigger?"
*   **Goal:** Find the "First Thought".

### Step 3: The Push (The Pain)
*   **Q:** "What specifically about the old way made you so angry/frustrated?"
*   **Goal:** Identify the functional and emotional friction.

### Step 4: The Pull (The Dream)
*   **Q:** "What did you *hope* the new solution would give you?"
*   **Goal:** Identify the Job To Be Done (JTBD).

### Step 5: The Anxiety (The Barrier)
*   **Q:** "What were you worried about before switching? What almost stopped you?"
*   **Goal:** Identify the friction of the new solution.

### Step 6: The Outcome
*   **Q:** "Did it work? Or are you stuck again?"

## 📝 Output Format
After the simulation, output the **Forces of Progress Card**:

```markdown
### 👤 Persona: [Name]
- **Trigger:** [Event]
- **Push (Pain):** [Why they left]
- **Pull (Desire):** [What they wanted]
- **Anxiety (Fears):** [What held them back]
- **Habit (Inertia):** [What they still miss]
- **Jobs To Be Done:** "When [Situation], I want to [Change], so that I can [Outcome]."
```

## Usage
Called by `01_signal_mining.md`.
Use this card to validate if the "Administrative Contradictions" found in search are actually relevant to the user.
