---
name: sus
description: 'Use when auditing skill routing, trigger conflicts, missing activation, or SUS/skill surface. Triggers: "скилл не сработал", "почему не активировался скилл", "конфликт триггеров", "аудит скиллов", "skill routing", "какие скиллы установлены", "два скилла ловят один запрос". NOT for: поиск и установка нового скилла из экосистемы (/find-skills) и написание или переписывание самого SKILL.md (/0-how-to-write-skills).'
---

# SUS

SUS means Skill Usage Surface: keep the active skill set discoverable, narrow,
and routed before broad orchestration.

## Protocol

1. Inspect the actual skill roots and current `SKILL.md` descriptions before
   claiming a routing issue.
2. Classify the request:
   - verification -> `check`, `pizdej`, or `falsify`;
   - root cause/debug -> `debug` (Mode L/H) or `diagnosing-bugs` (systematic loop
     is a deprecated pointer since 2026-07-06);
   - process reflection -> `pizdej`;
   - external audit -> `bouncer`;
   - prioritization/choice -> `prioritize` and/or `anti-bias`;
   - skill creation/edit -> `write-a-skill` (superpowers:writing-skills is a
     deprecated pointer since 2026-07-06);
   - bottleneck/leverage/blind-spot discovery -> `claude-skills` adapter
     (`leverage`) or canon `_agent_shared/skills/business/leverage_hunting`;
   - ETA/effort estimation -> `claude-skills` adapter (`estimate`) or canon
     `forecasting/estimate_calibration`;
   - external-executor briefing -> `claude-skills` adapter (`delegate`) or
     canon `workflow/delegation_brief`;
   - worker coordination -> `agent-orchestrator-standard`.
3. Prefer tightening an over-broad description over adding another broad router.
4. Prefer small native Codex skills for frequent triggers; use `claude-skills`
   only when the user asks for a Claude slash skill that was not ported.
5. Measure, do not eyeball: `~/.claude/bin/trigger_collisions.py` counts trigger
   phrases shared between two skills (exact match and word-boundary containment,
   `NOT for` excluded). Run it before and after edits — the delta is the evidence.
   Bare one-word triggers (`проверь`, `test`, `запусти`, `audit`) are the usual root.
6. After edits, verify frontmatter parses and list the installed skill paths:
   `~/.claude/bin/validate_skills.py --all` and `--root ~/.codex/skills --all`.

## Guardrails

- Do not add a new router that hides specialized skills.
- Do not claim a skill is installed until its `SKILL.md` exists in a visible
  skill root.
