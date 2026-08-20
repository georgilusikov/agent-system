---
name: retro
description: 'Use when turning a finished session into reusable Codex rule/skill improvements. Triggers: "/retro", "lessons learned", "что Codex должен усвоить из этой сессии", "ретро по сессии", "improve codex rules from this run". NOT for: root-cause hunt of a bug (/debug), post-task self-critique of gaps (/pizdej).'
---

# Retro

Use this to turn a session into reusable Codex improvements. Do not use Claude
Code destinations literally unless the user asks for Claude; adapt destinations
to Codex.

## Protocol

1. Identify the session scope: current chat, repo task, agent run, or specific
   artifact.
2. Read relevant local instructions before proposing writes:
   - `/Users/georgijlusikov/.codex/AGENTS.md`
   - `/Users/georgijlusikov/.codex/rules/*.md`
   - relevant project `AGENTS.md`, roadmap, skill, or report
3. Extract:
   - mistakes Codex made that the user corrected;
   - useful non-obvious decisions/patterns;
   - recurring risks likely to happen again.
4. For each item, propose:
   - one-line imperative rule;
   - destination;
   - dedup status.
5. Dedup before proposing writes:
   - `rg -n -i "<3-5 keywords>" ~/.codex/AGENTS.md ~/.codex/rules ~/.codex/skills`
   - If overlap is about 60% or more, extend the existing destination instead
     of creating a new file.
6. Do not write files until the user explicitly approves the proposed rule list.

## Codex Destinations

- `~/.codex/AGENTS.md`: global behavior, search, evidence, skill routing.
- `~/.codex/rules/<name>.md`: narrow reusable rule or protocol.
- `~/.codex/skills/<skill>/SKILL.md`: repeatable workflow.
- Project `AGENTS.md` or roadmap: project-specific source of truth.
- Incident log/report: recurring systemic failure with concrete evidence.

## Output Shape

```text
RETRO
scope:
mistakes:
- issue:
  evidence:
  rule:
  destination:
  dedup:
useful_patterns:
- pattern:
  evidence:
  rule:
  destination:
recurring_risks:
- risk:
  prevention:
proposed_writes:
- file:
  change:
waiting_for_ok: yes
```

## Guardrails

- No fabricated evidence: if uncertain, say "possible, not confirmed".
- Do not treat a one-off typo as a rule unless it exposes a system gap.
- Prefer fewer, sharper rules over many generic reminders.
- Preserve user/project source of truth over global preference.
- This skill implements the `Learn From Mistakes` loop from
  `~/.codex/AGENTS.md`; follow its rule format (symptom -> mechanism).
- If a proposed rule already existed and the mistake still happened twice,
  do not write a third variant: report that the rule does not work and
  propose a different mechanism (execpolicy `.rules` guardrail, hook,
  gate script, or process change).
