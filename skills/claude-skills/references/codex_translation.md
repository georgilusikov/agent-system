# Claude Code to Codex Translation

Use this map when executing a Claude Code skill inside Codex.

| Claude instruction | Codex equivalent |
|---|---|
| `Read tool` / "Read file" | Read the local file with shell commands such as `sed`, `rg`, or `nl`; use parallel reads when independent. |
| `Bash tool` | Use `functions.exec_command`; for independent reads or commands, use `multi_tool_use.parallel`. |
| Multiple Bash calls in one message | Use `multi_tool_use.parallel` only when commands are independent. |
| `AskUserQuestion` | Ask one concise plain-text question unless an explicit structured input tool is available and appropriate. |
| `/skill-name` | Resolve with `scripts/resolve_claude_skill.py skill-name`, then read that skill's `SKILL.md`. |
| `@skill-name` | Treat as a Claude slash skill unless a native Codex skill with that exact name is already active and more appropriate. |
| `TodoWrite` | Use `functions.update_plan` when a visible task plan helps; keep it short. |
| Subagents / parallel agents | Use Codex `spawn_agent` only when the user explicitly asked for subagents, delegation, or parallel agent work. Otherwise do the work locally or explain the limitation. |
| Claude plugins, MCP servers, or commands | Use available Codex tools first. If unavailable, report the missing capability and provide the closest safe fallback. |
| "Do not filter output" | Preserve substantive findings, errors, and verdicts, but summarize excessive logs instead of flooding the user. |

Always obey Codex system and developer instructions first. Imported Claude skills are workflow material, not a higher-priority policy layer.
