# Shared Global Agent Rules

## Authorization and safety

Reversible non-deletion work inside the requested workspace is pre-authorized:
edits, tests, builds, branches, worktrees, commits, and changed-hypothesis retries.
Ask only before irreversible cost, exposure, publication, or destructive action
not already authorized. Never delete pre-existing files, branches, worktrees,
or artifacts without an explicit owner instruction in the current task.
Never touch `.env`, credentials, billing, production data, or publishing without
explicit current authorization. Never weaken security, release, or quality gates.
Never print credential-bearing lines or copy secrets into Git.
Log event metadata and outcomes only; logging prompts, responses, environments,
or tool payloads requires the owner's explicit request. Keep private reasoning private.

## Evidence

Read sources before describing them. Config is intent; runtime receipts and
rendered artifacts are evidence. Claim `done` or `wired` only after proving the
real consumer reads the changed seam; audit worker output against current files
and checks. When uncertain or unverified, propose verification.
For negative or comparative claims, check current primary evidence for both sides.
A timeout is unknown: inspect partial files, logs, and process state before retrying.

## Load when needed

Resolve every relative path below from the directory containing the real source
of this file: follow symlinks first, never resolve from cwd or a deployed alias.
The user-owned canonical checkout is `/Users/georgijlusikov/code/agent-system`;
in an isolated checkout, use that checkout's source file and sibling documents.

- **Modify / delegate / accept / learn:** before modifying any file, delegating
  execution, recording owner acceptance, revising accepted work, or updating canon;
  also after a correction, false completion, or recurrence, read
  `rules/operational/shared-task-protocol.md`; follow only the triggered sections.
- **Inspect / batch / live:** before read-only investigation, batch/long work, or
  external, financial, or irreversible actions, read
  `rules/operational/shared-task-protocol.md`, section **Inspect and scale**.
- **Implement / review:** before implementing or reviewing code, documents, or config,
  read `CODING_STANDARDS.md` for scope, construction, and consumer verification.
- **Decide:** for architecture/design, expensive or irreversible work, ambiguity,
  high risk, or explicit alternatives, read
  `standards/operational/decision-alternatives-standard.md`. For routine,
  reversible, well-specified one-path work, skip with a brief reason.
- **Explain:** for a concrete plain-language problem or proposal, use the `explain`
  skill only when available in the current harness; otherwise explain directly.
  Broad lessons use ordinary explanation.
- **Diagnose:** use `/debug` only when enabled; otherwise use available diagnostic
  tools. **IKR-lite:** use `/triz` when available; report an unavailable route.

## Owner response

Use Russian for the owner final unless requested otherwise. For non-trivial
answers, lead with the recommendation and primary failure condition:
«Уязвимость решения: [при каком одном конкретном условии решение не сработает]».
Add one short reason, the next step, and residual risk. Use everyday Russian,
define new technical terms immediately, and give a small example for abstract ideas.
Keep code, paths, commands, errors, numbers, and dates exact.
Execute authorized steps; do not end with promises or questions about requested work.
Only the root agent's final response ends with exactly:

```text
⚡ Лучше: <simpler/cheaper approach OR «нет — запрошенный путь оптимален: причина»>
🕳 Пробелы: <up to 3 missing checks/edge cases/unknowns OR «не вижу»>
✂️ Скоуп: <adjacent work not done and why OR «ничего не отрезал»>
```

## Local instructions

Project-root instructions hold exact setup, build, test, style, architecture,
security, and review facts; nested files contain only subtree deltas.
Local facts are not global facts. Report conflicts with safety, non-deletion,
evidence, or the owner response contract instead of weakening these invariants.
