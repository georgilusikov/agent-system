# AGENTS.md and cross-agent instruction practices

Checked 2026-08-20 against first-party documentation.

## Findings

1. **Keep the global file small and truly global.** Codex loads global guidance on every run, then appends project and nested guidance; closer files win. The combined project guidance defaults to a 32 KiB cap. Anthropic likewise says concise, specific instructions are followed more consistently. Put only cross-project working agreements in the global file. ([OpenAI](https://developers.openai.com/codex/guides/agents-md), [Anthropic](https://code.claude.com/docs/en/memory))

2. **Put repository facts at the repository root and subsystem deltas near the code.** Good root content is exact setup/build/test commands, project conventions, architecture constraints, security pitfalls, and review expectations. Nested files should contain only the delta for that subtree. This matches Codex root-to-CWD discovery, Gemini's global/workspace/JIT hierarchy, Claude's user/project/directory scopes, and the AGENTS.md convention. ([OpenAI](https://developers.openai.com/codex/guides/agents-md), [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/), [Claude Code](https://code.claude.com/docs/en/memory), [AGENTS.md](https://agents.md/))

3. **Do not make users launch from the canon repository.** Launch each agent from the Git repository—or the relevant subdirectory—where it should work. Codex stops discovery at the current directory; Gemini uses the current workspace and trusted-root hierarchy. The global symlink supplies personal defaults regardless of the project. ([OpenAI](https://developers.openai.com/codex/guides/agents-md), [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/))

4. **Use one canonical payload, but keep native entrypoints.** A shared file linked to `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`, and the other runtime entrypoints avoids content drift. Claude officially supports symlinks in `.claude/rules/`; Gemini supports changing `context.fileName` and Markdown imports. Do not depend on cross-tool import syntax unless every active runtime supports and resolves it identically. ([Claude Code](https://code.claude.com/docs/en/memory), [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/))

5. **Separate orientation, workflow, enforcement, and runtime configuration.** Put durable bearings and always-relevant conventions in `AGENTS.md`; multi-step or occasional procedures in skills; model/tool/settings choices in native config; deterministic checks and blocking policy in hooks. Anthropic explicitly distinguishes contextual instructions from enforced client settings and recommends hooks when an action must be blocked. ([Claude Code memory](https://code.claude.com/docs/en/memory), [Claude Code hooks](https://code.claude.com/docs/en/hooks-guide))

6. **Keep machine-checkable rules out of prose when a native gate exists.** OpenAI recommends concise review rules and reserving formatting/lint checks for CI. Hooks are appropriate for protected-file guards, validation, state capture, and logging because they run at lifecycle events rather than relying on model compliance. ([OpenAI](https://developers.openai.com/codex/guides/agents-md), [Claude Code](https://code.claude.com/docs/en/hooks-guide), [Gemini CLI](https://geminicli.com/docs/hooks/))

7. **Treat hooks as privileged code.** Gemini warns that hooks execute arbitrary code with user privileges and fingerprints changed project hooks. Use narrow matchers, bounded timeouts, sanitized JSON I/O, no secret-bearing payload logs, and one writer per rewritten input. Claude notes parallel hooks that rewrite the same input have nondeterministic winners. ([Gemini CLI](https://geminicli.com/docs/hooks/), [Claude Code](https://code.claude.com/docs/en/hooks-guide))

8. **Make the active instruction stack inspectable.** Verify after changes from the real runtime: Codex can be asked to list loaded sources; Gemini exposes `/memory show` and `/memory reload`; Claude exposes `/context` and `/memory`. Version-control the canonical instructions and review changes like documentation. ([OpenAI](https://developers.openai.com/codex/guides/agents-md), [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/), [Claude Code](https://code.claude.com/docs/en/memory))

## Recommended delta for this repository

- Keep the global `AGENTS.md` near its current size; add only operational invariants that apply to every project.
- Restore exact verification, consumer discovery, retry-with-new-hypothesis, secret-safe logging, and source-control provenance rules.
- Do not restore project-specific ML, browser, deployment, Nodeterm, or Beads procedures globally; route them through skills or project files.
- Use native Gemini hooks for the smallest shared safety set: protected workspace paths, pre-compression/session handoff, and bounded audit events.
- Log configuration changes through Git commits. If runtime audit logging is enabled, log event metadata and outcomes—not prompts, model responses, environment variables, or tool payloads by default.
