# Incidents Index

Human-readable index for incident write-ups. The append-only event source is
`~/.claude/memory/ai.incidents.jsonl`; this file is navigation, not a datastore.

## Entries

| Date | Severity | Kind | Summary | Write-up |
|---|---|---|---|---|
| 2026-04-19 | high | process-failure | Memory preflight was skipped, causing repeated Krasinsky analysis work | [2026-04-19-skipped-memory-check.md](2026-04-19-skipped-memory-check.md) |
| 2026-07-06 | n/a | case-archive | 7 кейсов-обоснований правил, вынесены из CLAUDE.md при компрессии (loudnorm, git-log-review, seam-overclaim, resample, inert-wiring, producer-fallback, ETA) | [2026-07-06-claude-md-case-archive.md](2026-07-06-claude-md-case-archive.md) |
| 2026-06-04 | high | merge-integration | Integration regressions in a PR merge queue: owner gate preceded quality gate, targeted tests missed it | [2026-06-04-merge-queue-checkpoints.md](2026-06-04-merge-queue-checkpoints.md) |
| 2026-06-04 | high | multi-agent | 5-agent collision in one working tree + wrong-tree edits + venv deleted by `git add -A` symlink | [2026-06-04-parallel-agents-collisions.md](2026-06-04-parallel-agents-collisions.md) |
| 2026-06-11 | medium | tooling | iCloud sync of ~/Documents renamed a moved dir to ` 2`, desyncing the git worktree | [2026-06-11-worktree-icloud.md](2026-06-11-worktree-icloud.md) |
| 2026-06-12 | high | concurrency | Parallelized loop had two shared writers, not the one named in the ticket → cache-index corruption + double pay | [2026-06-12-parallelize-shared-state.md](2026-06-12-parallelize-shared-state.md) |
| 2026-07-19 | medium | delegation | Cloud-agent brief would have rebuilt existing stock b-roll/music modules; no `.env` in cloud | [2026-07-19-cloud-agent-briefs.md](2026-07-19-cloud-agent-briefs.md) |
| 2026-07-24 | high | measurement | `NVP_SPOKEN_WORD_BAND` override cut into a domain function; 4 consumers diverged, 9/13 rejects, measurement void | [2026-07-24-measurement-override-boundary.md](2026-07-24-measurement-override-boundary.md) |
| 2026-08-02 | medium | dead-mechanism | `session-start-memory.sh` written and working but registered in no settings.json — memory preflight is declarative again | [2026-08-02-declarative-hook-never-registered.md](2026-08-02-declarative-hook-never-registered.md) |
| 2026-08-02 | medium | unguarded-automation | drift-catcher committed a half-rewritten SKILL.md at 21:00 mid-session via `git add -A`; no active-session guard | [2026-08-02-autocommit-mid-session.md](2026-08-02-autocommit-mid-session.md) |

## Logging Policy

- Do not log raw prompts, secrets, personal data, or full transcripts.
- Log `summary` plus `summary_hash`; keep details in a reviewed Markdown write-up only when needed.
- JSONL is source-of-truth for metrics; Markdown is for human review.

## Known Limitations

- Claude CLI headless (`claude -p`) returns 401 auth in this environment; V4 pilot dual audit currently uses Gemini plus manual Claude chat when needed.
- Resolve later after Day 1-7 baseline unless it blocks a high-stakes review.
