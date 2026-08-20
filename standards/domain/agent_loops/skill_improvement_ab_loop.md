# Skill Improvement A/B Loop Standard

**Название:** Skill Improvement — A/B Loop for Skill Refinement
**Дата создания:** 2026-04-25
**Контекст ошибки:** `improvement_loop.sh` (153 lines) hardcoded `claude-code` as the only LLM, mixed baseline copy with candidate generation in the same directory, and gave no explicit owner-approval gate before promoting candidate to canonical skill location. The pattern (A vs B comparison via deterministic eval) is sound; the implementation isn't safe.

---

## 🎯 Фундаментальное правило

**To improve a skill, snapshot the current version (A = baseline), generate a proposed variant (B = candidate) under a non-canonical staging path, run an identical evaluation set against both, and require explicit owner approval before any copy from staging → canonical location. Variants never auto-promote.**

---

## ⚠️ Что было не так

- Baseline + candidate stored side-by-side under same staging dir without strict separation.
- `claude-code` hardcoded as the only generator — provider-locked.
- No deterministic eval set contract — eval scripts assumed but not required.
- Auto-copy hint shown in script output (`cp ... → $SKILL_PATH/`) without explicit owner gate inside the loop.
- No record of A vs B token cost — only quality compared.

---

## 🔍 Почему это произошло

1. Script grew from a one-off improvement experiment, not a contract.
2. A/B test scripts (`run_ab_test.py`, `compare_ab_results.py`) were optional in source — loop ran "blind" if missing.
3. Owner approval was implicit ("read the comparison and decide") rather than enforced.

---

## ✅ Как предотвратить

### Inputs
`--skill-path <path>` (e.g. `_agent_shared/skills/triz/functional_analysis`), `--executor "<cmd>"` (per `model_adapter_contract.md`), `--eval-set <path>` (deterministic prompt set, REQUIRED), `--staging-dir` (default `.agent/skills_proposed/<skill_name>/`), `--output-dir <path>`, `--dry-run`.

### Steps
1. **Snapshot baseline (A).** Copy current skill → `<staging-dir>/baseline/`. Read-only after this point. Original at canonical location is never touched.
2. **Generate candidate (B).** Run executor with improvement prompt against `<staging-dir>/baseline/SKILL.md`. Write result to `<staging-dir>/candidate/SKILL.md`. Log to `<staging-dir>/improvement.log`.
3. **Eval A.** Run `<eval-set>` against `<staging-dir>/baseline/SKILL.md` → `<staging-dir>/tests/baseline_results.json`.
4. **Eval B.** Run `<eval-set>` against `<staging-dir>/candidate/SKILL.md` → `<staging-dir>/tests/candidate_results.json`.
5. **Compare.** Generate `<staging-dir>/tests/comparison.md` with: success rate, quality score, token cost (in / out), latency. Verdict ACCEPT / REJECT / INCONCLUSIVE.
6. **Owner gate.** Loop EXITS at this point. No automatic copy from candidate to canonical location.

### Safety invariants
- Canonical skill at `--skill-path` is read-only during the loop (no writes there).
- Baseline copy is read-only after step 1.
- Eval set is the SAME prompts for A and B — comparison is meaningful only if input identical.
- No automatic promotion (`cp <candidate>/SKILL.md <skill-path>/` is owner action, not loop action).
- Variants land in non-canon path (`.agent/skills_proposed/...`) until approved — never under `_agent_shared/skills/`.
- Eval set REQUIRED — without it the loop exits non-zero (no "blind" runs).
- No `git commit` from the loop (per `model_adapter_contract.md`).

### Verification
- `<staging-dir>/baseline/` and `<staging-dir>/candidate/` both exist after success.
- `comparison.md` contains all three metrics: quality, token cost, latency.
- `<skill-path>/` (canonical) byte-identical before vs. after run.
- 10-test verification matrix from `extraction_protocol.md`.

---

## 📝 Примечания

- Skill-format authority is `_agent_shared/skills/_meta/skill_creator/SKILL.md` — candidate generation prompts MUST reference it so improvements stay format-conformant.
- Improvement prompts are domain-aware: TRIZ skills, Дорофеев skills, finance skills each may need tailored improvement instructions; that belongs in the executor's adapter or in the eval-set definition, not in the loop.
- A/B comparison output is the artefact; promotion is a manual `cp` after owner reads `comparison.md`.

---

## 🔗 Cross-references

- `_agent_shared/standards/agent_loops/extraction_protocol.md` — parent contract + verification matrix.
- `_agent_shared/standards/multi_agent/model_adapter_contract.md` — executor abstraction.
- `_agent_shared/skills/_meta/skill_creator/SKILL.md` — skill format authority (canonical structure).
- Provenance (after R4c archive): `docs/archive/2026-04/loops/improvement_loop.sh`.

---

## 🔄 История изменений

| Дата | Изменение | Причина |
|------|-----------|---------|
| 2026-04-25 | Создание стандарта | R4a — extract A/B improvement pattern from `improvement_loop.sh`; enforce owner gate before promotion. |
