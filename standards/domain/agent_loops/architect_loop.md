# Architect Loop Standard

**Название:** Architect Loop — Strategic Planning Pipeline (PRD → Critique → Tasks → Execute)
**Дата создания:** 2026-04-25
**Контекст ошибки:** `architect_loop.sh` (500 lines, BAS v5.0) hardcoded `npx -y opencode-ai run` as executor, embedded `/Users/.../projects/Business_Architect_System/` paths, ran without iteration cap on critique passes, and was tightly coupled to a single execution pilot. The pattern is reusable but the source is not.

---

## 🎯 Фундаментальное правило

**Strategic planning loop converts an idea into structured artefacts in fixed phases (PRD → CRITIQUE → TASKS → EXECUTE), one phase per file, capped by `--max-iterations`, and hands off to a project-specific execution pilot. Pattern is provider-agnostic; project binding is a parameter, not a hardcode.**

---

## ⚠️ Что было не так

- `CLAUDE_BASE_CMD=("npx" "-y" "opencode-ai" "run")` — provider-locked default.
- `BAS_PILOT="$SCRIPT_DIR/projects/Business_Architect_System/tools/execution_pilot.py"` — hardcoded project path baked into the loop.
- No iteration cap on critique re-runs in some branches → infinite-loop risk.
- Phase outputs written into project root mixed with logs — no audit-trail directory.
- `git commit` calls embedded in execution-pilot handoff path.

---

## 🔍 Почему это произошло

1. Author wrote the loop for one project (BAS) and never generalized.
2. `opencode-ai` was the only available CLI at the time of authoring.
3. Phase outputs were artefacts of debugging, not designed as audit trail.

---

## ✅ Как предотвратить

### Inputs
`--idea "..."` (required), `--screenshots FILE...`, `--urls URL...`, `--template DIR`, `--project-dir DIR` (output target), `--executor "<cmd>"` (per `model_adapter_contract.md`), `--max-iterations N` (default 5, required), `--pilot <cmd>` (project-specific execution pilot), `--output-dir <path>`.

### Phases
1. **PRD.** Generate `<output-dir>/prd.json` from idea + screenshots + URLs + optional template.
2. **CRITIQUE.** Generate `<output-dir>/critique.md` from `prd.json`. Lists weaknesses + missing acceptance criteria.
3. **REVISE PRD.** Re-emit `prd.json` informed by critique. Capped by `--max-iterations` (no unbounded re-critique loop).
4. **TASKS.** Generate `<output-dir>/TASKS.md` from final PRD. Each task has id, acceptance, dependencies.
5. **EXECUTE.** Hand off to `--pilot <cmd>` with `<output-dir>/TASKS.md`. Pilot is project-specific (e.g. BAS uses its own `execution_pilot.py`); the loop does not implement execution.

### Safety invariants
- `--max-iterations` is REQUIRED and applied to phase 3 (revise loop). Default 5; hard ceiling 10.
- Each phase output is a separate file under `--output-dir` (audit trail). Never overwrite previous phase files in-place.
- No `git commit` inside the loop body. Commit, if any, is the pilot's responsibility AND requires `--allow-commit` per `model_adapter_contract.md`.
- Project-specific bindings (BAS, other) are parameters via `--pilot` — never hardcoded.
- `--dry-run`: emit prompts and intended output paths; do not call executor.

### Verification
- All phase files exist under `<output-dir>/` after success.
- Phase 3 iteration count ≤ `--max-iterations`.
- Pilot exit code propagated; loop fails on pilot failure.
- 10-test verification matrix from `extraction_protocol.md`.

---

## 📝 Примечания

- The original BAS pattern (`projects/Business_Architect_System/tools/execution_pilot.py`) is one example of `--pilot`. New projects supply their own pilot.
- This is a planning loop, not a coding swarm. For parallel coder fan-out see `parallel_worktree_swarm.md`. For multi-model single-task synthesis see `dev_swarm.md`.
- Spy / Chrome-sync / competitor modes from the source script are out of scope for the standard — they belong in adapter-level addons if revived.

---

## 🔗 Cross-references

- `_agent_shared/standards/agent_loops/extraction_protocol.md` — parent contract.
- `_agent_shared/standards/multi_agent/model_adapter_contract.md` — executor abstraction.
- `_agent_shared/standards/agent_loops/parallel_worktree_swarm.md` — sibling pattern (different shape).
- Provenance (after R4c archive): `docs/archive/2026-04/loops/architect_loop.sh`.

---

## 🔄 История изменений

| Дата | Изменение | Причина |
|------|-----------|---------|
| 2026-04-25 | Создание стандарта | R4a — extract reusable pattern from BAS-specific `architect_loop.sh`; decouple from `opencode-ai` and BAS paths. |
