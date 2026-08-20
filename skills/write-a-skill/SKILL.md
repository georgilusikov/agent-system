---
name: write-a-skill
description: 'Use when creating or substantially rewriting a Codex SKILL.md. Canon protocol lives in Claude skill 0-how-to-write-skills; this file adds Codex runtime deltas only. Triggers: "напиши скилл для codex", "новый codex-скилл", "write a codex skill", "перепиши codex SKILL.md". NOT for: writing Claude-side skills or the protocol itself (canon 0-how-to-write-skills), the vendor wizard bundled with the Codex app (.system/skill-creator — auto-updated upstream, not our canon), a simple one-line edit of an existing skill (edit directly).'
---

# Write a Skill (Codex adaptation)

Canon: `~/.claude/skills/0-how-to-write-skills/SKILL.md` — READ IT FIRST (directly
or via the claude-skills resolver). This file is delta-only; canon content is not
duplicated here.

## Codex deltas

1. **Language & size**: Codex skills are compact EN adaptations (target ≤150
   lines), not mirrors of Claude canon. Runtime-specific content only.
2. **Frontmatter**: only `name` + `description`. Claude-only fields
   (`allowed-tools`, `model`, `disable-model-invocation`) do not apply.
3. **Placement**: `~/.codex/skills/{name}/SKILL.md`. Archive to
   `~/.codex/skills-archive/` (one-in-one-out, ~28 active names max).
4. **Pairing**: a Codex skill adapting an existing Claude skill = drift pair —
   add it to the PAIRS list in `~/.claude/bin/skills-drift-check.sh`; weekly
   `/principles-review` §5 consumes the report. `--ack` after manual review.
5. **Registry**: update `~/.claude/skills/REGISTRY.md` (single source of truth
   for installed skills across runtimes).
6. **Canon rules that apply unchanged** (2026-07-18, details in canon): golden
   set (§6 step 5.5, `references/golden/`; golden = smoke/regression seed —
   improvement claims need untouched holdout + repeated paired trials), workflow
   place (upstream/downstream in Related skills), outcome log (§7.1), external
   skill intake checklist (§8), and the methodology/eval selector in
   `references/methodology-field-guide.md`.
7. **Commit**: `~/.codex` is a git repo — commit skill changes immediately,
   message = what + WHY.

## Related skills (place in workflow)

- BEFORE: claude-skills resolver (locate canon), overlap check against
  `~/.codex/skills/` listing.
- AFTER: skills-drift-check pair registration, REGISTRY.md entry, git commit.

## Hard fail

- Codex skill written without reading the current canon SKILL.md (memory is not
  a source).
- Full copy of canon body into a Codex skill (drift farm; delta-only allowed).
- New Claude↔Codex pair not added to the skills-drift-check PAIRS list.
