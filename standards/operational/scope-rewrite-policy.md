---
name: scope-rewrite-policy
description: Scope-based policy for when agents may rewrite rules, standards, and skills after RCA.
version: 0.0.1
created: 2026-04-24
updated: 2026-04-24
scope: personal
status: active
owner: georgy
based_on: krasinsky-minimal-plus-pilot
applies_to:
  - /why
  - /falsify
  - /pizdej
incident_trigger: Krasinsky loop requires incident -> RCA -> patch, but shared files need review to avoid prompt bloat and cross-agent regressions.
---

# Scope Rewrite Policy

## 1. Job / JTBD
When an incident exposes weak instructions, the agent chooses the right rewrite gate by file scope so learning compounds without unsafe shared mutations.

## 2. Definitions
- **Personal:** `~/.claude/**`.
- **Project-local:** `*/.claude/**`, project `CLAUDE.md`, project `AGENTS.md`.
- **Shared workspace:** `_agent_shared/**`, shared monorepo docs/rules/config, files used by multiple projects or agents.

## 3. Expected State
- Personal gaps can be patched immediately after RCA and verified with `/check`.
- Project-local gaps can be patched when the project context supports it, then verified with `/check`.
- Shared workspace gaps require explicit review/gate before broad rewrite.

## 4. Protocol
Use path-based detection:

| Path | Scope | Policy |
|---|---|---|
| `~/.claude/**` | personal | Agent may patch after RCA, then run `/check`. |
| `projects/*/.claude/**` | project | Agent may patch if task is inside that project, then run `/check`. |
| Project `CLAUDE.md` / `AGENTS.md` | project | Patch only relevant section; run project tests if behavior changed. |
| `_agent_shared/**` | shared | Gate with review before edit unless user explicitly asked. |
| `shared/config/**` | shared | Gate with review and grep usages first. |

Rewrite only if the line does one of four things:
- prevents a repeated incident;
- reduces human effort;
- raises probability of correct result;
- makes an error observable.

## 5. Validation
- `git diff` shows the smallest instruction change that closes the RCA.
- `/check` output includes Expected State and confirms no nearby routing collision.
- For shared files, review/gate is documented before merge.

## 6. FORBIDDEN
- Do not batch personal fixes forever after RCA.
- Do not auto-rewrite shared instructions because a personal incident occurred.
- Do not add a new skill when a section in an existing skill closes the gap.

## 7. Hard Fail
- Scope is not identified before rewriting instructions.
- Shared file is changed without grep/review gate or explicit user request.
