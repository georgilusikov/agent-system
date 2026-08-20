# Ralph Loop Standard

**Название:** Ralph Loop — Persistent Autonomous Plan Loop
**Дата создания:** 2026-04-25
**Контекст ошибки:** `ralph_loop.sh` shipped two known bugs: (1) typo `FINSIHED` in the completion check (line 33) silently disabled the exit branch, causing infinite loops; (2) `git add .` + auto-commit on every successful test ran, polluting history with unrelated user changes.

---

## 🎯 Фундаментальное правило

**An agent reads `implementation_plan.md`, executes ONE next task, updates the plan, and repeats until an exact-match completion marker is emitted. No `git add .`, no auto-commit by default, and the marker word is verified character-exact.**

---

## ⚠️ Что было не так

- Marker check used `grep -q "FINISHED"` while the agent was instructed to emit `FINSIHED` (typo) → loop never exited.
- Default branch ran `git add .` then `git commit` on test pass — staged unrelated changes.
- No `--max-iterations` cap → runaway potential.
- Hardcoded `claude-code` executor — provider-locked.
- Test-fail branch let the agent "fix" without bounded retry.

---

## 🔍 Почему это произошло

1. Author copy-pasted marker word into both halves but mistyped one.
2. "Hands-off" autonomy was prioritized over commit hygiene.
3. No external review gate — the script was its own reviewer.

---

## ✅ Как предотвратить

### Inputs
`--objective "..."`, `--executor "<cmd>"` (per `model_adapter_contract.md`), `--plan-file` (default `implementation_plan.md`), `--max-iterations N` (required), `--marker "FINISHED"` (configurable, exact-match), `--allow-commit` (opt-in), `--sleep-sec` (default 5).

### Steps
1. **Bootstrap.** If `<plan-file>` missing: agent generates it from objective. Plan-only run; no code yet.
2. **Loop body** (capped by `--max-iterations`):
   - Agent reads plan, executes ONE next uncompleted task, updates plan.
   - Capture output to `<output-dir>/iter-N.log`.
   - **Completion check:** `grep -Fxq "<marker>"` (fixed-string, line-exact) on output. Exact match — never substring.
   - Run tests if manifest detected (`package.json` → `npm test`, `Cargo.toml` → `cargo test`, `pyproject.toml` / `requirements.txt` → `pytest`).
   - On test fail: bounded retry (max 3 attempts) before escalating to user.
   - **Commit:** disabled by default. With `--allow-commit`: `git add <explicit paths from plan>` (NEVER `git add .`), then one commit with `Ralph Loop: <task-id>`.
3. **Sleep** `--sleep-sec` between iterations (default 5s) to bound CPU.

### Safety invariants
- Marker is a fixed string compared exactly — no regex, no fuzzy match.
- `git add .` FORBIDDEN — only explicit paths derived from plan.
- `--max-iterations` is REQUIRED, not optional.
- Test command is deterministic (no flaky retries silently masked).
- No auto-commit unless `--allow-commit` is explicitly passed.
- Source-file typo guard in CI: `rg "FINSIHED" tools/agent_loops/ralph_loop.*` MUST be empty.

### Source bugs preserved as warnings
- ⚠️ `FINSIHED` typo (line 33 of source) — completion never triggered. Refactored tool MUST normalize on `FINISHED` and add the typo guard above.
- ⚠️ `git add .` + `git commit -m "Ralph Loop: ..."` (lines 53-54) — refactor MUST gate behind `--allow-commit` AND replace `.` with explicit paths.

---

## 📝 Примечания

- This pattern fits single-objective autonomous runs; for multi-coder fan-out use `parallel_worktree_swarm.md`.
- Completion marker word is a contract between bootstrap prompt and check loop; reuse the same constant in both.
- Test runner detection logic must surface "no tests found" as a distinct state, not silent pass.

---

## 🔗 Cross-references

- `_agent_shared/standards/agent_loops/extraction_protocol.md` — parent contract + 10-test verification matrix (test #10 is the typo guard).
- `_agent_shared/standards/multi_agent/model_adapter_contract.md` — executor abstraction.
- Provenance (after R4c archive): `docs/archive/2026-04/loops/ralph_loop.sh`.

---

## 🔄 История изменений

| Дата | Изменение | Причина |
|------|-----------|---------|
| 2026-04-25 | Создание стандарта | R4a — extract pattern from `ralph_loop.sh`; preserve typo + auto-commit warnings. |
