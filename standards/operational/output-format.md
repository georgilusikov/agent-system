---
name: output-format
description: Compact 5W+H rule for non-trivial state changes; avoids ritual in short answers.
version: 0.0.1
created: 2026-04-24
updated: 2026-04-24
scope: personal
status: active
owner: georgy
based_on: krasinsky-minimal-plus-pilot
applies_to:
  - final answers
  - /check
  - /falsify
  - /pizdej
incident_trigger: Need clear handoff after real changes without bloating every short answer.
---

# Output Format Standard

## 1. Job / JTBD
When the agent changes system state, the user should see what changed, why, how it was checked, and what remains.

## 2. Protocol
Use 5W+H only for non-trivial state changes:
- **What:** changed files / behavior.
- **Why:** user goal or incident closed.
- **Where:** exact files or commands.
- **When:** date/time only when relevant.
- **Who:** agent/user/owner when responsibility matters.
- **How verified:** tests, probes, review, or explicit gap.

Use short prose for:
- direct answers;
- simple command output;
- one-file trivial edit;
- casual clarification.

## 3. Expected State
- User can tell what happened without opening every diff.
- Verification status is visible.
- Remaining risks are named briefly.

## 4. FORBIDDEN
- Do not force 5W+H into a one-line answer.
- Do not hide failed tests under "done".
- Do not produce ritual sections with no new information.

## 5. Hard Fail
- Non-trivial state change without verification status.
- Recommendation with no "why" or scope.
