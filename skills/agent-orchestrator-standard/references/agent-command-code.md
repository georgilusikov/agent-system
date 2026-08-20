# Command Code Standard

Load this reference only when launching or writing prompts for `cmd` /
Command Code workers.

## When To Use

Use Command Code as a separate `cmd` transport for bounded implementation,
review, synthesis, or long-context inspection where one compact result is
enough. Prefer it over an interactive IDE lane when you need a short report, a
patch proposal, or a focused invariant review.

Avoid Command Code for open-ended multi-hour ownership unless the command is
wrapped in a clear result file contract and max-turn cap.

## Launch

Prefer `cmd`, not `commandcode`.

```bash
herdr agent start cc-<lane> --cwd <worktree> --focus -- \
  cmd -p '<bounded prompt that writes <result-file>>' --model <model> --max-turns 8 --skip-onboarding --trust
```

Nikita read-only scout pattern:

```bash
herdr agent start cc-<lane> --cwd <worktree> --focus -- \
  cmd --model deepseek-v4-flash --max-turns 4 --skip-onboarding --trust \
  -p 'Read-only Command Code scout. Do not edit files. Result file: <absolute tasks/...-result.md>. Write status/findings/evidence/pizdezh_check there before final. If you cannot write the result file, final status is blocked.'
```

For orchestration lanes, especially Nikita, Herdr-visible launch plus a durable
result file is the default. Direct non-Herdr `cmd` runs are acceptable only as
local throwaway probes; their findings are not acceptable evidence unless the
prompt writes a durable result file and the orchestrator records the command,
model, path, and exit status.

## Model Routing

Check `cmd --list-models` before hard-coding a model. Route by cost/evidence
fit, not by habit:

- Free/low/fast style lanes: DeepSeek Flash, Step Flash, GPT mini, Gemini Flash
  Lite, Mimo efficient. Best for scouts, grep-backed audits, summaries,
  formatting, simple reviews, and mechanical checks.
- Medium coding lanes: Qwen Plus, DeepSeek Flash/Pro, Kimi Code Highspeed,
  GLM Fast, Mimo Pro, MiniMax M2.x, GPT 5.4 mini/medium, Claude Haiku/Sonnet.
  Best for bounded implementation, failing tests, patch plans, command
  execution, and ordinary multi-file work.
- Strong/high lanes: GLM, Kimi Code, Qwen Max, MiniMax M3, Nemotron Ultra,
  Claude Fable/Opus, GPT 5.4/5.5, Gemini Flash/Pro when stronger reasoning is
  needed. Best for long-context synthesis, architecture, invariant review,
  ambiguous root cause, and failure clusters where rework is expensive.

Prefer cheaper open/source or Flash-style lanes for routine Command Code
delegation. Use frontier GPT/Claude/Pro-class models only when the expected
rework or review cost of a cheaper lane would exceed the model savings.

Before naming a model in a launch command, prefer checking `cmd --list-models`.
Do not describe GPT models as external agents when they run inside Codex-style
lanes; treat them as model tiers inside the chosen transport.

## Prompt Contract

```text
You are Command Code worker.
Scope: <repo/worktree + ticket/wave>.
Task: <bounded task>.
Result file: <absolute path under tasks/...>.

Read only the listed files/artifacts unless blocked.
Do not commit, push, run destructive commands, or use live/paid providers unless explicitly authorized.
Write detailed evidence to <result-file>. If you cannot write it, final status is blocked.
Do not print full logs, full diffs, full prompts, or extended reasoning.
Final output must be compact, max 8 lines: status, evidence, commands, residual risks.
```

Treat `rc=8` max-turn cap as incomplete unless the payload already contains
concrete evidence and a clear partial result.

## Acceptance

Accept Command Code output only after checking the Herdr session or recorded
command metadata, result file, command snippets, and current local files. A
confident prose answer is not proof. If a lane is not visible in Herdr and left
no durable payload/result file, mark it `attempted_no_evidence` and do not use
its findings for acceptance.
