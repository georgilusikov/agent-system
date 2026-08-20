---
name: research
description: 'Use when the user wants a topic researched against primary sources, docs or API facts gathered, or reading legwork delegated to a background agent, with findings saved as a Markdown file in the repo. Triggers: "research this", "investigate the docs for X", "найди по первоисточникам", "делегируй ресёрч фоновому агенту". NOT for: an explicit Gemini Deep Research request via headless Chrome (/deep-research) — a different mechanism not available in this Codex environment.'
---

# Research (Codex protocol)

Related: `~/.claude/skills/deep-research/SKILL.md` covers explicit "Gemini Deep
Research" requests via headless Chrome (`mcp__gemini-research__deep_research`,
reusing `notebooklm-mcp` cookies). That MCP server is **not configured in this
Codex environment** (`~/.codex/config.toml` has `notebooklm`, `playwright`,
`linear`, `node_repl`, `computer-use` — no `gemini-research`), so this is not a
delta on top of it the way `write-a-skill` is a delta on `0-how-to-write-skills`.
The two skills are complementary, not duplicates: deep-research's own
description explicitly excludes this case ("NOT for: обычное исследование по
первоисточникам с сохранением находок в репозиторий (/research)"). Keep both.

## Protocol

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** — official docs, source code, specs, first-party APIs — not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.

## When Gemini Deep Research becomes available in Codex

If `gemini-research` is ever wired into this environment's MCP config, route
explicit "deep research via Gemini" requests to that tool per
`~/.claude/skills/deep-research/SKILL.md`; keep this skill for everything else.
