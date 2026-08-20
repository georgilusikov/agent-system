# 🔀 Boris v5 – TRIZ Router (canonical)

This file defines how Boris selects TRIZ tools for each phase and domain.  The router uses a decision table based on the **phase**, **domain** and optional signals (such as whether a bottleneck is suspected).  It never calls the master orchestrator directly and limits itself to a maximum of four frameworks per phase.

Framework IDs ниже соответствуют локальным skills в `_agent_shared/skills/triz/<id>/`.

## 📥 Input schema

```yaml
Input:
  phase_id: int                # Phase number (0–5)
  domain: enum                 # product | process | org | tech | personal | auto
  locked_system:
    SUA: string
    Boundary: string
    KPI: string
    Stakeholders: list[string]
  constraints: list[string]    # constraints collected from previous phases
  signals:
    bottleneck_suspected?: bool
    timing_uncertain?: bool
    distribution_matters?: bool
    physical_conflict?: bool
```

## 📤 Output schema

```yaml
Output:
  selected_frameworks:
    - id: string          # e.g. "system_operator_ai"
      path: string        # path in projects/elena_triz/ai_obsidian/tools/
      rationale: string   # human-readable rationale
      priority: int       # 1 = primary, 2 = secondary, 3 = tertiary
  skip_rationale?: string # optional explanation when no frameworks are needed
```

## 🔎 Decision matrix by phase

### Phase 0 – Lock

Lock is executed entirely by internal logic.  No external TRIZ frameworks are invoked.  The router returns an empty list with a skip rationale:

```yaml
selected_frameworks: []
skip_rationale: "Lock uses internal logic for SUA, boundary, KPI, stakeholders, PoA and IKR; no TRIZ frameworks required"
```

### Phase 1 – Scan (System map)

| Condition                               | Framework                 | Path                                | Priority | Rationale                                   |
|-----------------------------------------|---------------------------|--------------------------------------|----------|---------------------------------------------|
| Always                                  | system_operator           | `_agent_shared/skills/triz/system_operator/` | 1        | Build the 9‑Screen and system map            |
| Always                                  | resource_analysis         | `_agent_shared/skills/triz/resource_analysis/` | 1        | Identify free resources                     |
| bottleneck_suspected = true             | limits_strategy           | `_agent_shared/skills/triz/limits_strategy/` | 2        | Analyse bottlenecks and limits             |
| domain = process                        | flow_analysis             | `_agent_shared/skills/triz/flow_analysis/` | 2        | Map flows if process is dominant           |
| domain in [tech, product]               | value_analysis            | `_agent_shared/skills/triz/value_analysis/` | 3        | Provide quantitative metrics if needed     |
| signals.historical_patterns? = true     | zrts                      | `_agent_shared/skills/triz/zrts/` | 2        | Compare system with evolutionary laws      |
| If harm_map complex OR historical_analysis deep | causal_analysis    | `_agent_shared/skills/triz/causal_analysis/` | 2        | Build cause-effect diagram for root cause identification (Zlotin Problem Formulator) |

### Phase 2 – Reality Check

| Condition                               | Framework                 | Path                                | Priority | Rationale                                   |
|-----------------------------------------|---------------------------|--------------------------------------|----------|---------------------------------------------|
| Always                                  | antisystem                | `_agent_shared/skills/triz/antisystem/` | 1        | Discover threats: Replace/Bypass/Commoditise/Regulate |
| timing_uncertain = true OR domain in [product, tech] | s_curve              | `_agent_shared/skills/triz/s_curve/` | 1        | Determine stage of evolution               |
| distribution_matters = true OR domain = process | flow_analysis          | `_agent_shared/skills/triz/flow_analysis/` | 2        | Verify path to boundary and distribution   |
| domain in [product, tech, org]          | zrts                   | `_agent_shared/skills/triz/zrts/` | 3        | Suggest evolution lines and transitions     |
| signals.scenario_generation? = true OR domain in [product, tech, org] | benchmarking | `_agent_shared/skills/triz/benchmarking/` | 2        | Compare with analogues / scenarios         |
| domain in [org, personal]               | akts        | `_agent_shared/skills/triz/akts/` | 3        | Analyse value/constraints for organisations |

### Phase 3 – Value

Phase 3 uses internal JTBD and market logic; no external TRIZ frameworks are invoked.  The router returns an empty list with a skip rationale:

```yaml
selected_frameworks: []
skip_rationale: "Value analysis is internal (JTBD, four forces, WTP proxies, friction, non‑consumption); no TRIZ frameworks called"
```

### Phase 4 – TRIZ Solve

The router decides based on the nature of the root blockade:

| Condition                               | Framework                 | Path                                | Priority | Rationale                                   |
|-----------------------------------------|---------------------------|--------------------------------------|----------|---------------------------------------------|
| Always                                  | functional_analysis    | `_agent_shared/skills/triz/functional_analysis/` | 1        | Map functions and harmful interactions      |
| If a Technical Contradiction (TC) exists | contradictions         | `_agent_shared/skills/triz/contradictions/` | 1        | Provide TC principles and guidance          |
| If TC exists                            | forty_principles       | `_agent_shared/skills/triz/forty_principles/` | 2        | Lookup inventive principles                 |
| If Physical Contradiction (PC) exists   | contradictions         | `_agent_shared/skills/triz/contradictions/` | 1        | Solve PC via separation                     |
| If bottleneck is mismatching/rhythm     | dynamization           | `_agent_shared/skills/triz/dynamization/` | 2        | Apply matching/mismatching patterns         |
| If multiple harmful interactions        | standards              | `_agent_shared/skills/triz/standards/` | 2        | Apply TRIZ standards for harm mitigation    |
| Always                                  | trimming               | `_agent_shared/skills/triz/trimming/` | 2        | Suggest trimming and removal of functions   |
| If complexity is high                   | effects                | `_agent_shared/skills/triz/effects/` | 3        | Suggest physical/chemical effects           |
| If conflict is on value or policy       | vepoli                | `_agent_shared/skills/triz/vepoli/` | 3        | Model the value/policy interactions        |
| signals.scenario_lookup? = true         | benchmarking   | `_agent_shared/skills/triz/benchmarking/` | 2        | Use analog/scenario library                |
| signals.micro_patterns? = true          | zrts             | `_agent_shared/skills/triz/zrts/` | 2        | Apply evolution laws/lines                 |
| signals.translation_needed? = true       | akts       | `_agent_shared/skills/triz/akts/` | 3        | Translate into value/constraints language   |
| If root blockade unclear OR cause-effect chain complex | causal_analysis | `_agent_shared/skills/triz/causal_analysis/` | 1 | Decompose root blockade into cause-effect chain, auto-generate task list (Zlotin Problem Formulator) |

### Phase 5 – Audit & Next

Audit is internal to Boris: it consolidates constraints, assumptions, experiments, calculates scores and calibrates confidence.  The router is not called.

## 🧪 Notes and limitations

- The router never calls more than **four frameworks** in a single phase; if more would apply, it chooses the highest priorities first.
- Domain adapters can override the default routing; see `domain_adapters/domain_rules.md` for specifics.
- The router logs every decision and the selected frameworks with rationales; these logs are included in the Reasoning Trace.
