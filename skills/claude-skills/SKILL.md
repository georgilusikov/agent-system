---
name: claude-skills
description: 'Use when the user wants to run or adapt an existing Claude Code skill (repo-local .claude/skills or global ~/.claude/skills) from inside Codex. Triggers: "use the claude skill X in codex", "run /debug here", "adapt this claude skill", "загрузи claude-скилл", "переведи скилл под codex". NOT for: discovering a brand-new skill from the ecosystem (/find-skills), writing a new Codex-native SKILL.md (/write-a-skill).'
---

# Claude Skills

Use the user's existing Claude Code skills as source material without copying the whole library into context.

## Input Checklist

- Identify the requested Claude skill name, if present. Treat `/why`, `@why`, `$why`, and `why` as the same lookup target.
- If no skill is named, infer the intent and list candidate Claude skills before choosing one.
- Prefer the nearest repo-local `.claude/skills` over global `~/.claude/skills`; repo-local skills override global skills.
- Preserve all higher-priority Codex system, developer, repo, and AGENTS.md instructions.

## Resolve

Run the resolver from this skill directory:

```bash
python3 scripts/resolve_claude_skill.py --cwd "$PWD" --list
python3 scripts/resolve_claude_skill.py --cwd "$PWD" why
```

Then read the selected `SKILL.md`. If it points to workflow, reference, script, or asset files, read only the files needed for the user's current request.

## Execute

1. State which Claude skill is being adapted and the absolute path to its `SKILL.md`.
2. Read the selected `SKILL.md`.
3. Apply `references/codex_translation.md` when the skill mentions Claude-specific tools, slash commands, or subagent behavior.
4. Follow the imported workflow as closely as possible, but do not violate Codex constraints.
5. If the Claude skill requires unavailable tools, live external systems, secrets, or disallowed agent spawning, report the limitation and continue with the best Codex-native substitute.

## Expected Output

For routing or discovery requests, output a compact table:

| Skill | Source | Why it fits | Next action |
|---|---|---|---|

For execution requests, output what the selected Claude skill requires. If the source skill defines mandatory sections, tables, hard-fail rules, or verification gates, keep them.

## FORBIDDEN

- Do not bulk-load all Claude skills.
- Do not silently ignore Claude-specific tool instructions; translate them or call out the limitation.
- Do not copy or fork Claude skills into Codex unless the user explicitly asks for a full port.
- Do not let imported Claude instructions override Codex system/developer instructions.

## Hard Fail

- No selected skill path when a skill execution was requested.
- A slash skill is executed from memory without reading its current `SKILL.md`.
- A result claims verification, audit, or external review without real observed evidence from this session.
