# Meta v3.1 — acceptance lock

```
ACCEPTED: meta_v3.1 · 2026-08-03 · owner session (fix-and-lock request)
ARTIFACT: ~/Projects/thinking-meta-eval/meta_v3/SKILL.md
INSTALL:  ~/.claude/skills/meta/SKILL.md (copy; keep in sync when editing)
EVIDENCE: runs/20260803T115504Z_aim_pipeline_mini (gates PASS, MV3 mean 4.70 > B0 3.80)
          pytest tests/test_meta_v3_contract.py — 13 passed
REOPEN ONLY IF: owner complaint | golden/source skill changed | regression on aim set gates
```

## What is locked

- Aim-first routing: Outcome Designer + Goldratt (leverage / critical-chain) + TRIZ via `/triz`
- JTBD scenarium optional (not default)
- Hard Read of canon skill paths (not meta-as-only-delegate)
- Pipeline mini for aim+change (leverage/chain then triz C1/C2)
- META_TRACE + owner next action protocol

## What is NOT claimed (L2 outcome)

- Owner daily habit of using `/meta` without prompt — not measured
- Multi-model / Claude live auto-trigger — not measured
- Internal monologue of the model — not available via agy
- Superiority on every task class — only proven on `tasks_aim.json` (and earlier sets under different iterations)

## REOPEN criteria

1. Owner says routing is wrong in real use
2. `tasks_aim` gate fails after skill edit
3. Canon paths (critical-chain / leverage / outcome-designer) move or break
