# Hook best practices — 2026-08-20

## Verdict

Keep hooks deterministic, narrow, fast, local, and mostly advisory. Use them to
enforce only objective pre-action safety boundaries. Do not use context size or
a generic “are you done?” judgment to stop an agent.

## Current context guards

The deployed guards do **not** technically stop work:

- Codex and Claude context guards print reminders and exit `0`.
- Gemini `PreCompress` records a checkpoint; the official contract makes this
  event asynchronous and advisory, so it cannot block or alter compression.
- AGY `PreInvocation` only injects a message at 80 steps.
- AGY `Stop` continues only while `fullyIdle` is false; it is unrelated to
  context size.

The problem is wording, not flow control: Codex/Claude call a threshold a “HARD
LIMIT” and tell a non-goal session to launch a fresh session; AGY tells the
agent to finish a milestone and avoid expanding scope. That can cause a model
to wrap up prematurely even though the process is not blocked.

**Recommendation:** remove token/step threshold instructions. Keep only native
compaction checkpoints: persist the objective, decisions, completed checks and
next action before compaction; after compaction, reread them and continue the
same task. Never return `continue: false`, exit `2`, `decision: block/deny`, or
AGY `terminationBehavior: terminate` based on context size. Codex and Gemini
both expose explicit pre/post-compaction lifecycle events, so guessing a limit
from transcript internals is unnecessary. Codex also warns that its transcript
format is not a stable hook interface.

Sources: [Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Gemini hooks reference](https://geminicli.com/docs/hooks/reference/),
[Gemini context management](https://geminicli.com/docs/reference/configuration/),
[Antigravity hooks](https://antigravity.google/docs/hooks).

## Worth adding or changing

### P0 — change now

1. **Make context handling compaction-only and non-blocking.** Remove the
   Codex/Claude token parser and AGY step threshold; retain `PreCompact` /
   `PostCompact` or `PreCompress` state handoff. This is smaller and relies on
   stable native events.
2. **Add explicit names/descriptions and tight timeouts to every hook.** Use
   roughly 1–3 seconds for local guards. Both Codex and Gemini otherwise allow
   much larger defaults, so a hung hook can visibly stall the loop.
3. **Use exact matchers.** Run shell guards only for shell tools and write
   checks only for write tools. Gemini, Claude, Grok and Codex all document
   matchers as the way to avoid unnecessary synchronous processes.
4. **Harden Gemini privacy defaults.** Enable
   `security.environmentVariableRedaction.enabled` and set
   `telemetry.logPrompts` to `false`. Gemini documents that hook processes
   inherit the CLI environment and redaction is disabled by default. Allow-list
   only variables a hook actually needs.
5. **Verify loaded hooks after install.** Use each runtime's native `/hooks`
   view and keep one production-shaped receipt per adapter. Codex, Claude and
   Grok all expose hook provenance/trust in their hook UI.

### P1 — add only where the project needs it

6. **PreToolUse secret/destructive-operation guard.** Limit it to objective
   patterns such as committing a detected credential or explicit destructive
   filesystem commands. Keep native sandbox/permission rules as the primary
   security boundary: Grok explicitly fails open on hook crash/timeout, and a
   regex hook cannot safely parse every shell construct.
7. **Post-write formatter or targeted validator.** Project-local only, matched
   to actual edit tools and file types. Do not put language-specific formatters
   in the global system.
8. **Stop verification for explicit long-running goals only.** Run a cheap,
   deterministic existing project check and honor re-entry fields such as
   `stop_hook_active`. A global Stop hook can loop, add latency, and mistakes a
   normal end-of-turn for task completion.
9. **Metadata-only audit logging.** If needed, log timestamp, event, runtime,
   workspace, tool name, decision and exit status. Do not log raw prompts,
   tool arguments, responses, environment variables, or transcript contents.
   Keep runtime logs out of Git.
10. **Notifications for unattended runs.** Make these asynchronous where the
    runtime supports it and never let notification failure affect work.

Sources: [Gemini hook best practices](https://geminicli.com/docs/hooks/best-practices/),
[Claude Code hook guide](https://code.claude.com/docs/en/hooks-guide),
[official Grok Build hook guide](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md),
[Codex hooks](https://learn.chatgpt.com/docs/hooks).

## Shared implementation rules

- Keep one shared **policy**, but retain thin native adapters because schemas,
  field names, exit codes, time units, concurrency and trust differ.
- Parse JSON with a real parser; emit only valid JSON on stdout and diagnostics
  on stderr when required by the runtime.
- Validate event name, tool name and input types. Treat prompt/tool payloads as
  untrusted data.
- Default operational and observability hooks to fail-open. A security control
  that must fail closed belongs in native permission/sandbox policy or needs a
  separately tested availability design.
- Roll out new blockers as warning-only first; provide a narrow documented
  override and retain pass, violation, override and malformed-input fixtures.
- Version hook code/config, but exclude caches, state, logs and transcripts.
- Never assume hook order. Codex and Claude document concurrent matching hooks;
  one hook's denial does not prevent sibling side effects from starting.

## Do not add

- A context-token or turn-count hook that stops, hands off or starts a new task.
- A model-based “is the work complete?” hook on every turn.
- Global test suites, formatters or dependency installers at Stop/AfterAgent.
- `AfterModel` processing for every streamed chunk unless there is a measured
  redaction requirement.
- Central HTTP logging until local metadata logs have a real consumer and a
  privacy/retention policy.
- One universal hook script that pretends vendor schemas are identical.

## Primary sources

- OpenAI, **Codex Hooks**: https://learn.chatgpt.com/docs/hooks
- OpenAI, **Codex configuration reference**: https://learn.chatgpt.com/docs/config-file/config-reference
- Google, **Gemini CLI hooks reference**: https://geminicli.com/docs/hooks/reference/
- Google, **Gemini CLI hook best practices**: https://geminicli.com/docs/hooks/best-practices/
- Google, **Gemini CLI configuration**: https://geminicli.com/docs/reference/configuration/
- Google, **Antigravity hooks**: https://antigravity.google/docs/hooks
- xAI, **Grok Build hooks**: https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md
- xAI, **Grok hooks feature page**: https://docs.x.ai/build/features/hooks
- Anthropic, **Claude Code hook guide**: https://code.claude.com/docs/en/hooks-guide
- Anthropic, **Claude Code hooks reference**: https://code.claude.com/docs/en/hooks
