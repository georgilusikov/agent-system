# Parallel Worktree Swarm Standard

**Название:** Parallel Worktree Swarm — Multi-Coder Harness
**Дата создания:** 2026-04-25
**Контекст ошибки:** `ralph_swarm.sh` spawned N coder agents in worktrees but committed unsafe defaults (no dirty-tree guard, no patch dry-run, mixed worktree placement, hardcoded `BASE_BRANCH` usage). Required a documented contract before tool refactor.

---

## 🎯 Фундаментальное правило

**Run N coder agents in N isolated `git worktree` directories under a configurable `--workdir`, collect per-coder patches, run a single reviewer step, and apply patches to base only after reviewer sign-off. No coder writes outside its own worktree.**

---

## ⚠️ Что было не так

- Coder worktrees placed inside main checkout — risk of cross-write.
- `git checkout BASE_BRANCH` without dirty-tree guard.
- Patches applied without dry-run preview.
- Reviewer step optional and silent on failure.
- Cleanup not configurable — leftover worktrees accumulated.

---

## 🔍 Почему это произошло

1. Author optimized for speed, not isolation.
2. No standard separated coder vs reviewer responsibilities.
3. `git apply --3way` failure path bypassed instead of escalated.

---

## ✅ Как предотвратить

### Inputs
`--base-branch`, `--objective`, `--backlog FILE` или `--task-ids "D20,D21"`, `--coders N` (default 3), `--executor "<cmd>"` (per `model_adapter_contract.md`), `--workdir <path>` (default `.workdir/parallel_swarm`), `--cleanup`.

### Steps
1. **Plan.** Generate `<workdir>/plan.json` via planning agent (objective + tasks + acceptance + suggested_paths + agent_role).
2. **Worktrees.** `git worktree add` one branch per coder under `<workdir>/worktrees/coder-N/`. Never inside main checkout.
3. **Coders.** Each coder runs the executor on its slice of tasks; touches only relevant files; writes a note to `<workdir>/notes/coder-N.md`.
4. **Patches.** `git diff` per worktree → `<workdir>/patches/coder-N.patch`. Empty patches skipped.
5. **Reviewer.** Single reviewer agent verifies acceptance criteria + flags unrelated changes. Failure aborts apply step.
6. **Apply.** Only after reviewer pass: `git apply --3way` each non-empty patch to base. Conflict aborts and surfaces patch path.

### Safety invariants
- Worktrees ALWAYS under `--workdir`, never in main checkout root.
- Dirty-tree guard before `git checkout <base>` and before `git apply`.
- Cleanup is opt-in via `--cleanup` and runs only on success.
- Each coder isolated — no cross-write between worktrees.
- No `git add .` (per parent contract).
- No auto-commit; reviewer report is the artefact.
- `--dry-run`: stop after plan + worktree creation; print intended patches.

### Verification
- Per-worktree: exit code recorded in `<workdir>/logs/coder-N.log`.
- Patch dry-run: `git apply --check <patch>` before real apply.
- Reviewer log non-empty and ends with `REVIEW_PASS` or `REVIEW_FAIL`.
- Verification matrix from `extraction_protocol.md` (10 tests) MUST pass before merge.

---

## 📝 Примечания

- Provider routing via VibeProxy is optional — the executor abstraction handles model selection.
- Task slicing defaults to round-robin by index; override via `--slice-strategy`.
- This pattern complements `dev_swarm.md` (single-task, multi-model) — they are not interchangeable.

---

## 🔗 Cross-references

- `_agent_shared/standards/agent_loops/extraction_protocol.md` — parent contract + verification matrix.
- `_agent_shared/standards/multi_agent/model_adapter_contract.md` — executor abstraction.
- Provenance (after R4c archive): `docs/archive/2026-04/loops/ralph_swarm.sh`.

---

## 🔄 История изменений

| Дата | Изменение | Причина |
|------|-----------|---------|
| 2026-04-25 | Создание стандарта | R4a — extract pattern from `ralph_swarm.sh` before tool refactor. |
