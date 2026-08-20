# 🔍 Problem Formulator (От ситуации к задаче)

**Purpose:** Transform vague problem descriptions ("inventive situations") into precise TRIZ-ready task formulations following ARIZ-85B Part 1 (Steps 1.1-1.6). Decompose problem clusters, identify the key conflict pair, select TP via MPP, amplify the conflict, and produce the Task Model with X-element.

**When to use:**
- User describes a problem vaguely ("it doesn't work", "too expensive", "breaks often")
- Multiple intertwined problems (problem cluster / "клубок задач")
- Need to select THE key problem before analysis
- Project Phase 0 — Clarification & Problem Definition
- Before any TRIZ tool invocation (this skill is the entry point)

**When NOT to use:**
- Problem already formulated as TP/FP (go directly to `@contradictions`)
- User provides a clear single conflict pair with known cause
- Education/training tasks (use `@socratic` or `@rtv`)

## Instructions

### Upstream Seed Shortcut (если discovery уже локализовал конфликт)

Если вход уже содержит структурированный `Problem Formulator Seed` от `@problem_map`,
`@stpa_analysis` или `@causal_loop_diagram`, не переизобретайте диагностику с нуля.
Сначала извлеките и зафиксируйте:
- primary harmful effect
- object / controlled process / harmed flow
- tool / controller / policy / action source
- useful action to preserve
- operational context / timing
- candidate metric / marker

Затем используйте этот seed как сырьё для TP-1 / TP-2 и Task Model, сохраняя только
одну главную проблему для формализации.

### Step 1: Situation Detoxification (Детерминизация ситуации)

Remove technical jargon. Rewrite every input using simple, non-specialist words.

**Rule (ARIZ-85B):** Technical terms enforce old mental models and amplify psychological inertia. Replace "centrifuge" → "container that spins things"; "capacitor" → "thing that stores electricity".

Parse input for:
- **Type:** Is this a problem / task / idea / question?
- **Cluster check:** Does the description contain >1 independent conflict?
- **Data check:** Are there concrete numbers/metrics or only subjective claims?

If cluster → go to Step 2. If single → go to Step 3.

### Step 2: Cluster Decomposition (Декомпозиция клубка)

Split the fuzzy situation into separate sub-problems. For each sub-problem:
1. Name it in simple words (no jargon)
2. Identify what is the harmful/insufficient effect
3. Rate its impact on the **Main Production Process** (MPP)

**Selection rule:** Choose the sub-problem whose resolution best serves the MPP. Park the rest.

Output: One selected sub-problem → proceed to Step 3 with it.

### Step 3: ARIZ-85B Step 1.1 — Mini-Task Formulation

Record the conditions strictly following this template:

```
ТЕХНИЧЕСКАЯ СИСТЕМА: для [назначение] включает [основные части,
включая природные элементы среды].

ТП-1: Если [состояние инструмента A], то [полезное действие],
но [вредное действие].

ТП-2: Если [состояние инструмента B = NOT A], то [вредное исчезает],
но [полезное тоже исчезает].

НЕОБХОДИМО при минимальных изменениях в системе [требуемый результат].
```

**Critical rules:**
- Include ALL main parts of the system (including environmental elements like air, water, gravity)
- TP-1 and TP-2 must describe TWO opposite states of the SAME element (the "instrument")
- The goal MUST specify "при минимальных изменениях" (this cuts off compromise paths)
- NO technical terms in the formulation

### Step 4: Conflict Pair Identification (Конфликтующая пара)

Extract from Step 3:
- **Изделие (Object):** What is being processed/protected/measured/detected
- **Инструмент (Tool):** What directly interacts with the Object (the blade, not the knife; the flame, not the lighter)

**Rules for pair selection:**
1. If the tool can have TWO states → specify both
2. If multiple identical pairs exist → take just one
3. One element can be "doubled" (two tools on one object, or one tool on two objects)

### Step 5: Mini-Task vs Maxi-Task Assessment

**Mini-task (default, try first):**
- Everything stays unchanged or simplifies
- Required action appears OR harmful action disappears
- Solution ONLY from internal resources
- Maximum conflict sharpening (no compromises!)

**Maxi-task (only if mini-task provably impossible):**
- Conflicting tool radically changes properties or disappears entirely
- External resources allowed
- May lead to scientific discovery

Output: State which type was chosen + reasoning.

### Step 5a: TP Selection via MPP (АРИЗ-85В Шаг 1.4)

From the two formulated contradictions (TP-1 and TP-2), select the ONE that **best serves the Main Production Process (ГПП)**.

**Rule:** The MPP is the system's primary function. For measurement tasks, MPP = product output (not the measurement itself). For service tasks, MPP = client value delivery.

After selecting: fix the chosen TP's "good" state and **forbid yourself from changing it**. The task becomes: "how to keep this state AND also get the benefit from the opposite state?"

### Step 5b: Conflict Amplification (АРИЗ-85В Шаг 1.5)

Drive the conflict to its **absolute limit**. Most conflicts are "many vs few" — amplify "few" → **"zero/absent"**.

Examples:
- "Few lightning rods" → "Absent conductor"
- "Small hole" → "No hole at all"
- "Weak shield" → "No shield"

**Why:** This definitively kills any compromise path and forces breakthrough thinking.

### Step 5c: Task Model Formulation (АРИЗ-85В Шаг 1.6)

Formulate the abstract Task Model using exactly this structure:

```text
1. Даны [усиленный инструмент] и [изделие].
2. [Усиленный инструмент] [хорошее действие],
   но [не обеспечивает / не делает] [плохое действие всё ещё].
3. Необходимо найти такой Икс-элемент, который,
   сохраняя способность [усиленного инструмента] [хорошее],
   обеспечивал бы [недостающее полезное действие].
```

**X-element is NOT a new device.** It can be: a change in temperature, pressure, phase state, or restructuring of existing elements/environment.

**After 1.6:** Return to Step 3 (1.1) and verify logical consistency from original situation → TP → amplified conflict → model. If chain breaks → backtrack.

### Step 6: Preliminary Localization

Quick-scan for:
- **OZ (Operational Zone):** WHERE does the conflict physically happen? (narrow to smallest possible space)
- **OV (Operational Time):** WHEN? T1 = conflict moment, T2 = just before, T3 = just after
- **RVS Test:** What happens if Size → 0? → ∞? Time → 0? → ∞? Cost → 0? → ∞?

RVS produces insights, not solutions. Note anything that "clicks".

### Step 7: Quick Causal Scan (RCA+ Lite)

Ask **"What is the cause?"** (NOT "Why?"):
1. Build 2-3 levels of horizontal causes (AND-connections)
2. Stop at: unmodifiable cause (law of physics) OR **contradiction-cause** (produces both harm AND benefit)
3. Mark any contradiction-causes found → these are gold

### Step 8: Diversion Check (Optional, for Investigation tasks)

Invert the task: "How could a saboteur deliberately CAUSE this problem using only the system's own resources?"
- If an answer exists → check: does this process happen naturally?
- If yes → you found a hidden mechanism

### Step 9: Output Package

Produce the following structured output.

## Output Format

```markdown
## 📋 Problem Formulation Report

### 1. Original Situation (detoxified)
[Simple-language description, no jargon]

### 2. Cluster Decomposition (if applicable)
| # | Sub-problem | Impact on MPP | Selected? |
|---|-------------|---------------|-----------|
| 1 | ...         | High/Med/Low  | ⭐/—      |

### 3. Mini-Task Formulation (ARIZ-85B 1.1)
**ТС:** для [purpose] включает [parts]
**ТП-1:** Если [A], то [+], но [-]
**ТП-2:** Если [NOT A], то [-] исчезает, но [+] тоже
**Цель:** при минимальных изменениях [result]

### 4. Conflict Pair
- **Изделие:** [object]
- **Инструмент:** [tool]
- **Selected TP:** TP-1 / TP-2 (via MPP analysis)
- **Type:** Mini-task / Maxi-task

### 5. Conflict Amplification
- **Amplified state:** [instrument → zero/absent]
- **Amplified conflict:** [what the absent instrument cannot do]

### 6. Task Model (ARIZ-85B 1.6)
1. Даны: [amplified instrument] и [object]
2. [amplified instrument] [good], но [bad]
3. Необходимо найти Икс-элемент, который [requirement]

### 7. Preliminary Localization
- **OZ:** [where, as narrow as possible]
- **OV:** T1=[conflict], T2=[before], T3=[after]
- **RVS insights:** [key observations from →0/→∞ experiments]

### 8. Causal Scan
[2-3 cause levels, AND-connections marked]
⚠️ Contradiction-causes: [list]

### 9. Recommended Route
→ Skeleton Map: [A/Б/В/Г/Д/Е/Ж/М/Н]
→ Next skill: [@skill_name]
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Use technical terms in formulation | Replace with simple "children's" words |
| Jump to solutions | Complete ALL steps before even thinking about solutions |
| Accept compromise ("optimal value") | Sharpen the conflict to the extreme |
| Mix multiple problems in one TP | Decompose cluster FIRST, select ONE problem |
| Write "Why?" in causal chain | Write "What is the cause?" — reveals physical conditions, not intentions |
| Formulate TP without opposite states | TP-1 and TP-2 MUST be mirror states of ONE element |
| Skip RVS test | Always run it — it breaks psychological inertia even when it seems "obvious" |
| Declare maxi-task without trying mini first | Mini-task is ALWAYS the first attempt |
| Skip conflict amplification | ALWAYS amplify to zero/absent — no half-measures |
| Treat X-element as a new device | X-element = change in existing resources (temp, phase, structure) |
| Skip verification loop after 1.6 | ALWAYS return to 1.1 and trace logical chain end-to-end |

## Next Step / Handoff

After completing Problem Formulation:
1. If cause unclear → `@causal_analysis` (full RCA+)
2. If parameter conflict → `@contradictions` → `@forty_principles`
3. If harmful interaction → `@oz_ov` → `@resource_analysis` → `@vepoli`
4. If need breakthrough → `@system_operator` → `@s_curve`
5. If reliability/failure → `@diversion_analysis` (full) → `@afd_failure_predictor`

## Gate Check

| Criterion | Required | Pass? |
|-----------|----------|-------|
| No technical jargon in formulation | Yes | ✅/❌ |
| TP-1 and TP-2 are mirror states of ONE element | Yes | ✅/❌ |
| "при минимальных изменениях" in goal | Yes | ✅/❌ |
| Conflict pair (Object + Tool) identified | Yes | ✅/❌ |
| TP selected via MPP criteria | Yes | ✅/❌ |
| Conflict amplified to zero/absent state | Yes | ✅/❌ |
| Task Model with X-element formulated | Yes | ✅/❌ |
| Mini-task attempted before maxi-task | Yes | ✅/❌ |
| OZ narrowed to physical conflict zone | Yes | ✅/❌ |
| Verification loop (1.6 → 1.1) passed | Yes | ✅/❌ |
| At least one causal level explored | Yes | ✅/❌ |
| Recommended route (skeleton map) specified | Yes | ✅/❌ |
