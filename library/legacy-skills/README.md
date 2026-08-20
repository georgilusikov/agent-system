# 📁 Skills Library

**Location:** `_agent_shared/skills/`
**Version:** 3.0.0
**Updated:** 2026-01-06
**Total Skills:** 50+

---

## 📊 TRIZ Domain (`triz/`) — 35 skills

### Core Analysis
| Skill | Purpose |
|-------|---------|
| [functional_analysis](triz/functional_analysis/) | Build functional model |
| [contradictions](triz/contradictions/) | Formulate TC/PC |
| [s_curve](triz/s_curve/) | Determine S-curve stage |
| [system_operator](triz/system_operator/) | 9-screens analysis |
| [causal_analysis](triz/causal_analysis/) | RCA+ Root Cause |
| [resource_analysis](triz/resource_analysis/) | Find hidden resources |
| [flow_analysis](triz/flow_analysis/) | Optimize flows |
| [value_analysis](triz/value_analysis/) | Cost/Value analysis (FSA) |
| [structural_analysis](triz/structural_analysis/) | Component connections |
| [akts](triz/akts/) | MPV + Inertia detection |
| [avf](triz/avf/) | Environment/Black Box analysis |
| [oz_ov](triz/oz_ov/) | Space-Time targeting |

### Solution Tools
| Skill | Purpose |
|-------|---------|
| [trimming](triz/trimming/) | Remove components |
| [forty_principles](triz/forty_principles/) | 40 Inventive Principles |
| [vepoli](triz/vepoli/) | Substance-Field models |
| [standards](triz/standards/) | 76 TRIZ Standards |
| [effects](triz/effects/) | Physical Effects Database |
| [ariz](triz/ariz/) | Full ARIZ algorithm |
| [arip](triz/arip/) | ARIZ Lite (quick) |
| [fos](triz/fos/) | Function-Oriented Search |
| [reverse_fos](triz/reverse_fos/) | Find markets for technology |
| [benchmarking](triz/benchmarking/) | Functional comparison |
| [oas_transfer](triz/oas_transfer/) | Feature Transfer/Hybridization |

### Creative/Psychological
| Skill | Purpose |
|-------|---------|
| [ikr](triz/ikr/) | Ideal Final Result |
| [mmch](triz/mmch/) | Little People Method |
| [rvs](triz/rvs/) | Size-Time-Cost Operator |
| [rtv](triz/rtv/) | Creative Imagination Router |
| [goldfish](triz/goldfish/) | Fantasy → Engineering |
| [robinson](triz/robinson/) | Survival mode (MacGyver) |
| [inversion](triz/inversion/) | Reverse problem solving |

### Evolution & Strategy
| Skill | Purpose |
|-------|---------|
| [zrts](triz/zrts/) | Laws of Evolution |
| [dynamization](triz/dynamization/) | Make systems flexible |
| [evolution_radar](triz/evolution_radar/) | 6-line evolution sweep (incl. Matching/Mismatching) |
| [antisystem](triz/antisystem/) | Use enemy's energy |
| [diversion_analysis](triz/diversion_analysis/) | Find vulnerabilities |
| [limits_strategy](triz/limits_strategy/) | Development limits |

---

## Forecasting Domain (`forecasting/`) — 1 skill

| Skill | Purpose |
|-------|---------|
| [boris_ikr](forecasting/boris_ikr/) | IKR-driven forecasting |
| [boris_v5](forecasting/boris_v5/) | Directed Evolution forecasting (main) |

---

## Hermeneutics Domain (`hermeneutics/`) — 5 skills

| Skill | Purpose |
|-------|---------|
| [hermeneutic_circle](hermeneutics/hermeneutic_circle/) | Iterative spiral: part↔whole understanding |
| [prejudice_audit](hermeneutics/prejudice_audit/) | Surface and revise hidden assumptions |
| [exegesis](hermeneutics/exegesis/) | Multi-layer text interpretation (PaRDeS/Quadriga) |
| [meaning_compression](hermeneutics/meaning_compression/) | Compress understanding to ≤3 sentence formula |
| [hermeneutic_dialogue](hermeneutics/hermeneutic_dialogue/) | Teaching, course design, Socratic coaching |

---

## Dev Domain (`dev/`) — 4 skills

| Skill | Purpose |
|-------|---------|
| [qa_notes](dev/qa_notes/) | QA handoff notes |
| [commit_style](dev/commit_style/) | Commit message style |
| [release_checklist](dev/release_checklist/) | Pre-release checklist |
| [post_task_checks](dev/post_task_checks/) | Minimal checks after changes |

---

## Workflow Domain (`workflow/`) — 3 skills

| Skill | Purpose |
|-------|---------|
| [bas_memory_capture](workflow/bas_memory_capture/) | Save BAS analysis state to Memory Bank |
| [triz_memory_capture](workflow/triz_memory_capture/) | Save TRIZ session state to Memory Bank |
| [youtube_memory_capture](workflow/youtube_memory_capture/) | Save episode summaries to Memory Bank |

---

## 🔧 Quick Reference

```text
1. Find skill by keyword (trigger)
2. Load SKILL.md (~30 lines metadata)
3. If match → Load core_instructions.md
4. Execute and validate via gate_check.md
```

## ➕ Add New Skill
```bash
./.agent/scripts/create_skill.sh <domain> <skill_name> "<description>"
```
