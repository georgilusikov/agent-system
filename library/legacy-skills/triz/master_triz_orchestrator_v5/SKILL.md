---
skill_id: master_triz_orchestrator_v5
name: master-triz-orchestrator-v5
skill_name: TRIZ Orchestrator v5
version: 5.0.0
category: orchestration
triggers: ["TRIZ", "ТРИЗ", "solve problem", "/triz"]
dependencies: ["final_triz_report"]
architecture: python_native
description: 'TRIZ TRIZ Orchestrator v5 — use for triggers in SKILL.md: triggers: [''TRIZ'', ''ТРИЗ'', ''solve problem'', ''/triz''], ''final_triz_report''.'
---

# 🏗 TRIZ Orchestrator v5 — Python-Native Routing

> **v5 replaces prompt-based routing with Python code.**

## Key Differences from v4.2

| Aspect | v4.2 (Prompt) | v5 (Python) |
|--------|--------------|-------------|
| Routing | LLM reads full orchestrator prompt | Python `triage_agent.py` with short prompt |
| Micro-chains | Text rules in prompt | `validators.py` — Python assertions |
| Gateways | NLP-based ("решение очевидно?") | JSON checklists with programmatic checks |
| Anti-triggers | Text in Anti-Trigger Matrix | Python `if/else` in `validators.py` |
| Backtracking | Not enforced | Hard limits: 2/phase, 3 total |

## Architecture

```
Task → triage_agent.py → map (А-Н, DC)
     → state_machine.py → step-by-step skill calls
         ├── validators.py (micro-chain enforcement)
         ├── gateway checks (JSON checklists)
         └── backtracking (if gate fails)
     → final_output (routing report)
```

## Files

| File | Lines | Purpose |
|------|:-----:|---------|
| `triage_agent.py` | ~140 | Task → Map classification (single LLM call) |
| `state_machine.py` | ~270 | Main pipeline: skills → gateways → backtrack |
| `validators.py` | ~160 | Hard Micro-Chains + Anti-Triggers (code) |
| `runner.py` | ~80 | CLI interface for testing |

## Usage

```bash
# CLI
python3 runner.py --task "Клапан протекает через 2 недели..." --model glm-5

# JSON output
python3 runner.py --task "..." --json --output result.json

# Regression test
python3 shared/scripts/routing_regression_runner.py --cli v5 --cases all
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TRIZ_API_KEY` | — | API key for LLM calls |
| `TRIZ_API_BASE` | `https://open.z.ai/v1` | API base URL |
| `TRIZ_MODEL` | `glm-5` | Model name |
