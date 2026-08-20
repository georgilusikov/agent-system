# Claude Code Lane Manager Standard

Load this reference only when launching or writing prompts for Claude Code
implementation lanes or lane-manager goal runs.

## When To Use

Use Claude Code for shared-core debugging, multi-subtask implementation lanes,
architecture-heavy changes, false-positive filtering, or when an agent should
own a coherent phase from restore through verification.

Prefer isolated worktrees. Do not give Claude the same files as another active
implementation lane unless the prompt explicitly coordinates a handoff.

## Launch

Verify the requested model starts. Always use the exact flag:
`--dangerously-skip-permissions`.

```bash
herdr agent start <agent-name> --cwd <worktree> -- claude --model <available-model> --dangerously-skip-permissions
herdr agent send <agent-name> '<goal prompt>'
herdr pane send-keys <pane_id> Enter
```

Then confirm the pasted `/goal` actually executed:

```bash
herdr agent read <agent-name> --source recent-unwrapped --lines 80 --format text
```

If the model is unavailable, close the pane and switch agent instead of retrying
blindly.

## Goal Prompt Additions

```text
/goal You are Claude Code lane manager in Goal Mode.
Work only in isolated worktree <path>.
Goal: <ticket/wave>.

Restore state from the listed source files and task contract.
Split into independent subtasks only when useful.
Keep workers inside this worktree and avoid overlapping edits.
Keep chat quiet: write details to result files, not the transcript.

Delegation: delegate only when it reduces wall-clock, context load, or risk.
Prefer one batched worker per coherent cluster.
Max 3 concurrent subagents, depth 2, unless the prompt says otherwise.

Challenge unsafe, overclaiming, paid/live, or brittle instructions.
Findings from other agents are hypotheses until checked against code/tests/artifacts.

Before final: diff check, targeted tests, lint/structured validation if touched,
and verifier or explicit residual risk.

Final <=12 lines, or <=20 only if blocked:
status, tickets, changed_files, checks, backlog/issues, risks, ready_to_merge.
```

## Acceptance

For trusted compact finals, use a fast acceptor path:

1. Read final report.
2. Check `git status --short --branch`.
3. Check `git diff --stat`.
4. Inspect key hunks only when scope/risk requires it.
5. Run targeted local checks or a batch gate before integration.

Escalate if final is vague, files are broad/unexpected, checks failed, live/paid
scope is ambiguous, or backlog/status closure overclaims evidence.
