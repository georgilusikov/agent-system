---
name: incident-logging
description: JSONL event log for AI management incidents. Use when a skill, rule, or standard failure should feed the learning loop.
version: 0.0.1
created: 2026-04-24
updated: 2026-04-24
scope: personal
status: active
owner: georgy
based_on: krasinsky-minimal-plus-pilot
applies_to:
  - /check
  - /why
  - /triage
  - /falsify
  - /pizdej
  - /anti-bias
incident_trigger: 2026-04-19 memory preflight miss showed that lessons must become observable events, not only narrative notes.
---

# Incident Logging Standard

## 1. Job / JTBD
When an agent finds a non-trivial system/process failure, it writes a small structured event so the system can later render, deduplicate, and patch rules/standards/skills.

Log incidents for:
- `/falsify` verdict `FAIL`.
- `/falsify` verdict `PARTIAL` with severity `medium` or higher.
- `/check` gap where root cause is not a trivial typo.
- `/why` process/system root cause.
- `/pizdej` finding that names a missed check, missed memory, or weak design injection.
- Repeated user correction of an existing rule, standard, or skill.

Do not log incidents for:
- A typo fixed immediately with no system/process lesson.
- Raw scratch notes with no RCA or design-injection candidate.
- Success patterns unless the lesson is non-obvious and likely reusable.

## 2. Definitions
- **JSONL source-of-truth:** `~/.claude/memory/ai.incidents.jsonl`.
- **Markdown render:** `~/.claude/memory/ai.incidents.md`, derived only by `~/.claude/bin/render-incidents.sh`.
- **Index:** `~/.claude/memory/incidents/INDEX.md`, human-readable list of longer RCA notes.
- **Long RCA:** optional Markdown note in `~/.claude/memory/incidents/` when JSONL summary is not enough.

## 3. Expected State
- JSONL event has `event_id`, `occurred_at`, `kind`, `severity`, `project`, `session_id`, `source`, `target`, `summary`, `summary_hash`, and `dedup_key`.
- `occurred_at` is valid UTC ISO8601, e.g. `2026-04-24T12:34:56Z`.
- `summary` is redacted, capped, and single-line; newlines/tabs/control characters are normalized to spaces.
- No event contains raw prompt, raw transcript, secrets, or personal data beyond a short summary.
- Duplicate events within the dedup window are skipped or explicitly marked as duplicates.
- Markdown render is regenerated from JSONL, not edited as a datastore.

## 4. Protocol
Write events through:

```bash
~/.claude/bin/log-incident.sh \
  --kind skill-gap \
  --severity medium \
  --source /check \
  --target ~/.claude/skills/check/SKILL.md \
  --summary "Expected State was missing before evidence collection"
```

Use severity:
- `low`: small quality gap, no repeated failure yet.
- `medium`: repeatable process gap or failed skill output.
- `high`: user-visible wrong result, bad routing, or unsafe recommendation.
- `critical`: data loss, secret exposure, destructive action, production-risk false PASS.

Dedup:
- `dedup_key = sha256(session_id + kind + severity + source + target + normalized_summary)`.
- Dedup window: `15 min`.
- Within the window, a repeated event should not create a new primary incident.

Retention:
- Keep last `500` active entries in `memory/ai.incidents.jsonl`.
- Archive older entries monthly to `memory/archive/ai.incidents-YYYY-MM.jsonl`.
- Never delete archived JSONL without explicit user approval.

## 5. Validation
```bash
bash -n ~/.claude/bin/log-incident.sh
~/.claude/bin/log-incident.sh --kind test --severity medium --summary "Test incident pipeline"
tail -1 ~/.claude/memory/ai.incidents.jsonl | jq -e '.event_id and .summary_hash and .dedup_key'
~/.claude/bin/render-incidents.sh
test -f ~/.claude/memory/ai.incidents.md
```

## 6. FORBIDDEN
- Do not append to `ai.incidents.md` as the source of truth.
- Do not log raw prompt or full transcript.
- Do not use `flock` on macOS; use `/usr/bin/lockf`.
- Do not mark a `FAIL`/serious `PARTIAL` done without either logging or explaining why it is not an incident.

## 7. Hard Fail
- JSONL record lacks `summary_hash` or `dedup_key`.
- Raw prompt, secret, or full transcript is written to JSONL.
- Markdown render is treated as concurrent datastore.
