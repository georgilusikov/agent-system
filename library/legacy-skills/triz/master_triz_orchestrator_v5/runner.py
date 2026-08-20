#!/usr/bin/env python3
"""
TRIZ Orchestrator v5 — CLI Runner

Usage:
    python3 -m master_triz_orchestrator_v5.runner --task "Клапан протекает..."
    python3 runner.py --task "Клапан протекает..." --model glm-5

Environment:
    TRIZ_API_KEY or Z_AI_API_KEY — API key for LLM
    TRIZ_API_BASE — API base URL (default: https://open.z.ai/v1)
    TRIZ_MODEL — Model name (default: glm-5)
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from master_triz_orchestrator_v5.state_machine import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="TRIZ Orchestrator v5 CLI")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--api-base", default=None, help="API base URL")
    parser.add_argument("--api-key", default=None, help="API key")
    parser.add_argument("--model", default=None, help="Model name")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--output", default=None, help="Save output to file")
    args = parser.parse_args()

    llm_kwargs = {}
    if args.api_base:
        llm_kwargs["api_base"] = args.api_base
    if args.api_key:
        llm_kwargs["api_key"] = args.api_key
    if args.model:
        llm_kwargs["model"] = args.model

    result = run_pipeline(args.task, **llm_kwargs)

    if args.json:
        output = json.dumps(
            {
                "triage": {
                    "map": result.triage.map_code,
                    "map_name": result.triage.map_name,
                    "confidence": result.triage.confidence,
                    "reasoning": result.triage.reasoning,
                },
                "steps": [
                    {
                        "skill": s.skill,
                        "output": s.output[:500],
                        "confidence": s.confidence,
                        "gate_passed": s.gate_passed,
                        "warnings": s.warnings,
                    }
                    for s in result.steps
                ],
                "backtracks": result.backtracks,
                "called_skills": result.state.called_skills,
            },
            ensure_ascii=False,
            indent=2,
        )
    else:
        output = result.final_output

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
