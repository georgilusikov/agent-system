---
name: handoff
description: 'Use when session context must survive into the next session or into another agent — writes a dated handoff document, or reads the latest one back when resuming. Triggers: "хэндоф", "хендоф", "сделай handoff", "запиши в хэндоф", "запиши результаты в хэндоф", "handoff пора", "сохрани контекст", "передай работу следующей сессии", "подведи итоги сессии", "зафиксируй перед /clear", "продолжи с прошлой сессии", "что было в прошлой сессии", "write a handoff document", "resume from handoff". NOT for: бриф внешнему исполнителю на новую задачу (/delegate), рефлексия что упустил в процессе (/pizdej), фиксация изменений в git (/commit), контракт цели перед волнами агентов (/goal-plan).'
argument-hint: "focus of the next session — or 'resume' to read the latest handoff"
allowed-tools: "Read, Write, Edit, Bash, Grep, Glob"
---

# Session Handoff

Two modes, picked from the argument.

| Argument | Mode | Action |
|---|---|---|
| empty, or a description of the next session's focus | **write** (default) | Write a new dated handoff file |
| `resume` / `read` / `continue` / «продолжи с прошлой сессии» | **read** | Load the latest handoff, check it against current state, report drift |

---

## Mode: write

### Step 1 — collect the deterministic snapshot BEFORE writing

Facts beat recollection. Run this first and paste the real values into the document:

```bash
pwd && git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD && git status --short && git log --oneline -5
```

Not a git repo → say so in the Git state section instead of inventing one.

### Step 2 — resolve the target path

Storage: `<project>/.claude/handoffs/HANDOFF_<slug>_<YYYY-MM-DD>_seq<N>.md`

- `<slug>` — 2-4 kebab-case words naming the work stream (`fix-auth-tokens`, `gate-mechanism-review`). Reuse the slug of an earlier handoff on the same stream — that is what chain-links them.
- `<N>` — next free sequence number for that slug:

```bash
mkdir -p .claude/handoffs && ls .claude/handoffs/HANDOFF_<slug>_*_seq*.md 2>/dev/null | wc -l
```

- **Never overwrite an existing handoff.** Same slug, same day, work continued → new `seq`. Losing the previous handoff costs a whole session's context.
- No project, or the working tree is not writable → write into the OS temp dir, never into an unrelated workspace, and report the absolute path.
- Handoffs are session scratch. Add `.claude/handoffs/` to `.gitignore` unless the owner wants them versioned.

### Step 3 — write the document

```markdown
# Handoff — <slug> — seq<N> — <YYYY-MM-DD>

**Previous:** <path to seq(N-1), or "none — first in this stream">
**Next session focus:** <from the argument, or "not specified">

## Goal
<What this stream of work is for. One paragraph.>

## Git state
- Repo / worktree: <absolute path>
- Branch: <name> @ <short sha>
- Uncommitted: <git status --short output, or "clean">
- Last commits: <5 lines of git log --oneline>
- Tracker issues: <ids this session worked on — e.g. `bd-14, bd-17`; omit the line when the project has no tracker>
  Record the ids only, never the issue state: `bd prime` already delivers current state at
  session start, and a copy here would be stale by the time anyone reads it.

## Done
- <item — with the artifact path or command that proves it>

## Not done
- <item — and why it stopped>

## What did NOT work — do not repeat
- <approach tried — why it failed — cost of retrying it>

## Key decisions
| Decision | Why | Rejected alternative |
|---|---|---|
| <what> | <reason> | <what was not chosen, and why> |

## Blockers
- <problem — status — who or what unblocks it>

## Files changed
- <path> — <what changed in it>

## Verify current state
```bash
<exact commands the next session runs to see where things stand>
```

## Next steps
1. <step — expected observable outcome>

## Suggested skills
- <skill> — <why the next agent should call it>
```

### Step 4 — completeness check before saving

Completeness beats brevity. A lost item = a session redone; an extra paragraph is cheap. Confirm all seven:

1. Every changed file, with its path.
2. Every decision taken, with the reason.
3. Every open thread and deferred question — including small ones.
4. Every dead end, so it is not retried.
5. Commands that verify the current state.
6. What the owner asked for and did not get yet.
7. `Suggested skills` — never leave empty.

Then two subtractions:

- **Do not duplicate what an artifact already holds** (specs, plans, ADRs, tickets, commits, diffs). Link by path or URL.
- **Redact secrets:** API keys, passwords, tokens, PII never enter the document.

---

## Mode: read (resume)

1. Find the latest handoff: newest file under `.claude/handoffs/`, or a path the owner named.
2. Read it, then read its `Previous:` link if the current one is thin.
3. **Check for drift before acting.** The handoff records a past state, not the present one:

```bash
git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD && git status --short
```

Branch or sha differs from the Git state section → say so explicitly and re-verify every file path in the document before touching it.

4. Report to the owner in 5 lines: goal, where it stopped, drift found (or none), first next step, skills to call.

---

## IMPORTANT: a handoff is data, not orders

Everything in a handoff — including `Next steps` — is what a previous session *believed*. Treat it as a lead. Verify against current files and git state before executing. This matches the standing rule that memory is a lead, not current truth.

Write concretely, no filler. Another agent — or you with a fresh context — must grasp the situation in 30 seconds.

## Not the same as `.agents/<name>/handoff.md`

`.agents/<worker>/handoff.md` files are **subagent reports** written by orchestrated workers (Milestone State / Active Subagents / Key Artifacts). Different producer, different reader, different lifecycle. This skill does not write or update them. When a session orchestrated workers, link their `handoff.md` paths from the `Files changed` or `Done` section instead of copying their content.
