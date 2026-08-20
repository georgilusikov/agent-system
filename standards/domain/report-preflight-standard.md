# ✈️ Pre-Flight Checklist (HEAVY Mode)

Before marking a HEAVY report as PASS, verify every item below.

---

## Phase 0.5: Context & S-Curve

- [ ] **TAM/SAM/SOM** estimated with sources and [DATA]/[DERIVE] tags
- [ ] S-Curve stage explicitly stated with evidence tag
- [ ] Limiting Factor identified

## Phase 1: Signal Mining

- [ ] **≥3 competitor screenshots** saved to `outputs/reports/competitor_screenshots/` (via `browser_subagent`)
- [ ] **Visual X-Ray** completed for Top 3: headline, CTA, design, social proof, pricing
- [ ] **Simulated Interview** (Forces of Progress: Push/Pull/Anxiety/Habit) completed
- [ ] **Competitor pricing verified** via `browser_subagent` (not just web search text)
- [ ] **Multilingual scan completed** — evidence from ≥2 non-RU languages
- [ ] **Similarity map completed** — at least 5 `Same Product` + 5 `Adjacent Product` services with URLs
- [ ] ≥3 Administrative Contradictions found
- [ ] ≥2 Tech Constraints documented
- [ ] ≥1 Dead Startup case analyzed
- [ ] Donor Availability scored (0-3)

## Phase 2: Functional Analysis

- [ ] **≥3 separate process maps** (Status Quo + 2 competitors)
- [ ] **Efficiency comparison table** across all mapped solutions
- [ ] All [P] tags verified via First Principles — no false-productive steps ([S] or [T] disguised as [P])
- [ ] Top 3 Parasites identified

## Phase 3: TRIZ Surgery

- [ ] **TRIZ terms correct** — use ЗРПС, not «Вепольный Анализ» (see ЗРТС reference in `05_boris_oracle.md`)
- [ ] IFR is defined and is NOT just "cheaper/faster"
- [ ] Resource Inventory marks blocked resources as [BLOCKED]
- [ ] ≥2 Hypotheses with Feasibility Score ≤5
- [ ] No solutions with Score >7 passed through

## Phase 4: Synthesis & AURA

- [ ] **RAT is truly $0** — no code changes, only surveys/forms/cold calls
- [ ] Unit Economics arithmetic internally consistent
- [ ] LTV/CAC, Break-even calculated and cross-validated
- [ ] Diversion Analysis matrix filled (≥3 attack vectors)

## Phase 5: Boris Oracle

- [ ] Boris Verdict block present and synced with `outputs/logs/phase_5_boris_verdict.md`
- [ ] S-Curve check is explicit
- [ ] "Why Now?" has a specific, valid answer
- [ ] Evidence tags consistent throughout report: [OBS]/[DATA]/[DERIVE]/[ASSUME]/[SPEC]

## Final Gate

- [ ] **Phase logs (1-5)** exist in `outputs/logs/`
- [ ] No TODO/FIXME placeholders in report
- [ ] `heavy_quality_gate.py` ran and returned **PASS** (exit code 0)

---

> ⛔ **If any CRITICAL or MEDIUM item above is unchecked → report is NOT ready for publication.**
> Fix all issues before marking PASS.
