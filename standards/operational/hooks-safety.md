---
name: hooks-safety
description: Safety contract for future Claude hooks. This pilot does not add UserPromptSubmit or Schedule hooks.
version: 0.0.1
created: 2026-04-24
updated: 2026-04-24
scope: personal
status: active
owner: georgy
based_on: krasinsky-minimal-plus-pilot
applies_to:
  - hooks
  - /falsify
  - /check
incident_trigger: Planned hook ideas had feedback-loop and context-pollution risk; safety contract must exist before hooks are added.
---

# Hooks Safety Standard

## 1. Job / JTBD
When a future hook is introduced, it must be easy to disable, bounded in latency, privacy-safe, and non-blocking.

## 2. Definitions
- **Hook:** script invoked by Claude runtime events.
- **Kill switch:** `AI_MGMT_HOOKS=0`.
- **Silent fail:** hook exits `0` after writing diagnostics, so the session is not blocked.

## 3. Expected State
- Every future hook starts with:

```bash
[[ "${AI_MGMT_HOOKS:-1}" == "0" ]] && exit 0
```

- Hook timeout is `1s` for prompt/session hooks unless a user explicitly approves more.
- Hook never logs raw prompt, raw transcript, secrets, or full user text.
- Hook writes latency/error logs to a bounded file.
- `SessionStart` memory hook may add context, but `CLAUDE.md` Memory preflight remains the real gate.

## 4. Protocol
Before adding a hook:
- Write sample stdin JSON.
- Define expected stdout/stderr/exit code.
- Add kill-switch check as the first executable line.
- Add timeout wrapper.
- Add redaction: hash + short summary only.
- Run the hook with valid, empty, and malformed stdin.

## 5. Validation
```bash
AI_MGMT_HOOKS=0 ~/.claude/hooks/the-hook.sh
timeout 1 ~/.claude/hooks/the-hook.sh < sample.json
```

PASS means no session block, no raw prompt logging, and deterministic JSON output if output is required.

## 6. FORBIDDEN
- No UserPromptSubmit hook during the first 7 days of this pilot.
- No Schedule automation during the first 7 days of this pilot.
- No hook that modifies `settings.json` without `/update-config` style review.
- No hook that feeds its own metrics back into the model prompt.

## 7. Hard Fail
- No kill switch.
- Raw prompt is written to disk.
- Hook failure blocks normal session start.
