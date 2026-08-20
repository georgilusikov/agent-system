# Gate Check for Problem Formulator

## Minimum Criteria

| # | Check | Required | Actual | Pass? |
|---|-------|----------|--------|-------|
| 1 | Formulation uses simple words (no technical jargon) | Yes | ___ | ✅/❌ |
| 2 | TP-1 and TP-2 describe opposite states of ONE element | Yes | ___ | ✅/❌ |
| 3 | Goal contains "при минимальных изменениях" | Yes | ___ | ✅/❌ |
| 4 | Conflict pair identified (Object + Tool) | Yes | ___ | ✅/❌ |
| 5 | Object = what is processed/protected/measured | Yes | ___ | ✅/❌ |
| 6 | Tool = what DIRECTLY interacts (blade, not knife) | Yes | ___ | ✅/❌ |
| 7 | Mini-task attempted before maxi-task | Yes | ___ | ✅/❌ |
| 8 | OZ narrowed to physical conflict zone | Yes | ___ | ✅/❌ |
| 9 | OV split into T1/T2/T3 | Yes | ___ | ✅/❌ |
| 10 | RVS test performed (→0 and →∞ for at least 2 params) | Yes | ___ | ✅/❌ |
| 11 | At least 1 causal level explored | Yes | ___ | ✅/❌ |
| 12 | Route recommendation (skeleton map + next skill) | Yes | ___ | ✅/❌ |

## Block Conditions

If any of these are true, **STOP and escalate**:

- [ ] TP-1 and TP-2 describe DIFFERENT elements (not opposite states of the same one)
- [ ] No harmful effect identified — is this really a TRIZ task?
- [ ] Tool and Object are the same element — re-identify the pair
- [ ] Technical jargon remains in the formulation after Step 1
- [ ] Maxi-task declared without documented mini-task attempt

## Quality Signals (Soft)

| Signal | Expected | Notes |
|--------|----------|-------|
| Contradiction-cause found in RCA+ lite | Preferred | Gold if found — directly feeds @contradictions |
| Diversion check revealed hidden mechanism | Preferred | Only for Investigation tasks |
| Cluster properly decomposed | If applicable | At least 2 sub-problems identified and ranked |
| Environmental elements in system description | Preferred | Air, gravity, temperature, humidity |
| RVS produces non-obvious insight | Preferred | If all 6 experiments yield "nothing" → operator error |

## Confidence Adjustment

- All 12 checks pass: Confidence += 10%
- 1 check fails: Confidence -= 15%
- 2 checks fail: Confidence -= 30%
- ≥3 checks fail: Confidence = 50% max, require backtrack
- Block condition triggered: Confidence = 0%, STOP
