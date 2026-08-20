---
name: codex-advisor
description: "Delegation loop: Antigravity as Manager+Worker, Codex as strategic Advisor. Use when user says 'делегируй', 'codex plan', 'codex review', 'запусти цикл', 'loop engineering', or wants autonomous task execution with external review."
---

# Codex Advisor — Delegation Loop Skill

## Architecture

```
YOU (Antigravity) = Manager + Worker
CODEX            = Advisor (plan + review only, never executes)
```

You orchestrate the full cycle. Codex only THINKS — you DO.

## When to use

- User gives a multi-step task or feature request
- User says "запусти цикл", "делегируй", "codex plan", "goal mode"
- Any task that benefits from external planning + review

## Workflow

### Phase 1: PLAN (call Codex)

Run Codex in non-interactive mode to get a plan:

```bash
codex exec -m o3 --ephemeral -o /tmp/codex_plan.md \
  "You are a Tech Lead advisor. DO NOT write code. DO NOT modify files.

PROJECT CONTEXT:
$(cat AGENTS.md 2>/dev/null || echo 'No AGENTS.md')

TASK:
<INSERT_USER_TASK>

OUTPUT FORMAT — return a numbered task list. For EACH task:
1. Task ID (T1, T2, ...)
2. GOAL: one-sentence desired end state
3. EVIDENCE: exact shell commands to verify success (pytest, ruff, curl, etc.)
4. CONSTRAINTS: what NOT to touch, max files, scope limits
5. DEPENDS: which tasks must be done first (or 'none')
6. COMPLEXITY: simple | medium | complex

Keep tasks atomic. Max 5 tasks. Each should take <10 minutes."
```

Read the plan from `/tmp/codex_plan.md`. If Codex returned garbage or the plan is unclear, re-run with more context.

### Phase 2: EXECUTE (you + subagents)

For each task in order (respecting dependencies):

1. **Spawn a subagent** with a clean context for each task
2. Pass ONLY the Three-Slot Goal to the subagent:
   ```
   GOAL: <from plan>
   EVIDENCE: <exact verification commands>
   CONSTRAINTS: <from plan>
   ```
3. Subagent executes: writes code, runs tests, fixes errors
4. **Deterministic gate** — run the verification commands from EVIDENCE:
   ```bash
   # Always run these:
   ruff check . 2>&1 | tail -5
   git diff --check
   # Plus task-specific commands from EVIDENCE
   ```
5. If gate FAILS → retry (max 3 attempts per task)
6. If gate PASSES → proceed to review

**Circuit breakers:**
- Max 3 retries per task → mark as BLOCKED, continue to next task
- Max 5 tasks per session
- If >50% tasks BLOCKED → stop, report to human

### Phase 3: REVIEW (call Codex)

After each task passes the deterministic gate, get Codex review:

```bash
# Generate diff for review
git diff HEAD > /tmp/task_diff.patch

codex exec -m o3 --ephemeral -o /tmp/codex_review.md \
  "You are a skeptical Code Reviewer. Review this diff for:
1. Does it match the goal? GOAL: <goal from plan>
2. Any slop? (dead code, TODOs, unused imports, hardcoded values)
3. Any regressions? (broken imports, missing error handling)
4. Tests actually test behavior, not implementation?

DIFF:
$(cat /tmp/task_diff.patch)

TEST RESULTS:
$(cat /tmp/test_results.txt 2>/dev/null || echo 'No test output')

VERDICT: APPROVE or REJECT.
If REJECT: list specific files and lines to fix."
```

**On APPROVE:** commit with `feat: <task-id> <summary>`, move to next task.
**On REJECT:** feed Codex's feedback back to a new subagent attempt (counts toward retry limit).

### Phase 4: REPORT (to human)

After all tasks processed, create a summary artifact:

```markdown
# Execution Report

## Tasks Completed
- [x] T1: <description> — APPROVED by Codex
- [x] T2: <description> — APPROVED by Codex

## Tasks Blocked
- [ ] T3: <description> — BLOCKED after 3 retries. Reason: <...>

## Stats
- Total time: <duration>
- Retries: <count>
- Codex calls: <plan: 1, reviews: N>

## Codex Review Highlights
<any notable feedback from reviews>
```

## Quick Reference

### Codex as Planner
```bash
codex exec -m o3 --ephemeral -o /tmp/codex_plan.md "<planning prompt>"
```

### Codex as Reviewer
```bash
codex review --uncommitted "Check for slop, dead code, and test quality"
# OR for branch review:
codex review --base main "Review all changes vs main branch"
```

### Codex as Architect (complex decisions)
```bash
codex exec -m o3 --ephemeral -o /tmp/codex_decision.md \
  "Given these two approaches: <A> vs <B>.
   Project context: <...>
   Which is better and why? Be specific."
```

## Rules

1. **Never skip the deterministic gate.** Tests + lint BEFORE Codex review.
2. **Never pass conversation history to subagents.** Only pass: goal + relevant files.
3. **Never let a subagent run >15 rounds.** Context decay kills quality.
4. **Always use `--ephemeral`** for Codex calls — no state pollution between calls.
5. **Always use `-o <file>`** to capture Codex output for parsing.
6. **If Codex is unavailable** (rate limit, network), fall back to self-review with pizdej-protocol.
