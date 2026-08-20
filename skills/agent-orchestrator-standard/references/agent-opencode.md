# OpenCode Standard

Load this reference only when launching or writing prompts for OpenCode workers.

## When To Use

Use OpenCode for bounded implementation, review, or synthesis when a
provider-prefixed model is useful, Command Code is busy, or the OpenCode Go/free
models are a better cost fit. Keep the lane compact: one task, one worktree, one
result shape.

Avoid OpenCode for counted Nikita verifier acceptance when the chosen model is
OpenRouter-backed, unless owner policy explicitly allows OpenRouter for that
run.

## Launch

Prefer Herdr so the orchestrator can monitor and close the pane:

```bash
herdr agent start oc-<lane> --cwd <worktree> --focus -- \
  opencode run --model <provider/model> --format json '<bounded prompt>'
```

Direct one-shot runs are acceptable for very small checks:

```bash
opencode run --model <provider/model> --format json --dir <worktree> '<bounded prompt>'
```

Check current models before hard-coding a provider:

```bash
opencode models
opencode providers list
```

## Model Routing

Observed local credentials include OpenCode Go and Z.AI Coding Plan, plus
environment-backed OpenRouter/xAI. Prefer in this order unless the task demands
otherwise:

- `opencode/*-free`: cheapest scouts and low-risk checks.
- `opencode-go/qwen3.7-plus`, `opencode-go/qwen3.6-plus`: practical coding and
  bounded implementation.
- `opencode-go/deepseek-v4-flash`, `opencode-go/deepseek-v4-pro`: invariant
  review, debugging, and architecture checks.
- `opencode-go/glm-5.2`, `opencode-go/kimi-k2.7-code`: long-context or
  multi-file reasoning.
- `opencode-go/minimax-m3`, `opencode-go/minimax-m2.7`: product/watchability or
  multimodal-leaning critique.
- `openrouter/*`: only when explicitly allowed; do not count it for default
  Nikita verifier acceptance.

## Prompt Contract

```text
You are OpenCode worker.
Scope: <repo/worktree + ticket/wave>.
Task: <bounded task>.

Read only the listed files/artifacts unless blocked.
Do not commit, push, run destructive commands, or use live/paid providers unless explicitly authorized.
Write detailed evidence to <result-file> when requested.
Do not print full logs, full diffs, full prompts, or extended reasoning.
Final output must be compact: status, evidence, commands, residual risks.
```

## Acceptance And Cleanup

OpenCode output is not evidence by itself. Inspect files, commands, diffs, and
artifacts locally before accepting. If no durable report is needed, close the
Herdr pane after final output is inspected. Use `opencode session list` and
`opencode session delete <sessionID>` only for sessions created by the current
orchestration and confirmed disposable.
