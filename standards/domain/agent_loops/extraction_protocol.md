# Agent-Loop Extraction Protocol Standard

**Название:** Extraction Protocol — Root Scripts → Standards + Tools
**Дата создания:** 2026-04-25
**Контекст ошибки:** Root agent-loop scripts (`ralph_swarm.sh`, `ralph_loop.sh`, `ralph_loop_miner.sh`, `architect_loop.sh`, `improvement_loop.sh`, `dev_swarm_v4.py`) carried valuable workflow patterns but were unsafe (`git add .`, hardcoded paths, `--dangerously-skip-permissions`) and provider-locked. Several were edited or moved before any standard described their contract, resulting in lost intent and unsafe re-runs.

---

## 🎯 Фундаментальное правило

**Convert a root script into a reusable tool by writing the standard FIRST, getting owner approval, then refactoring the tool against the model-adapter contract with safety guardrails. Never move or rewrite a script before its standard exists.**

---

## ⚠️ Что было не так

- Refactor before standard: tools changed before their invariants were written down — old behavior lost, new behavior under-specified.
- Provider-locked tools: scripts hardcoded `claude --dangerously-skip-permissions` instead of an executor abstraction.
- Unsafe defaults: `git add .` + auto-commit, no `--max-iterations`, no `--dry-run`, hardcoded `/Users/...`.
- Frozen-area leak: scripts wrote artefacts into project output dirs without explicit `--output-dir`.

---

## 🔍 Почему это произошло

1. No protocol — each script extraction was ad-hoc.
2. "Refactor first, document later" — but later never came; tooling drifted.
3. Standards directory (`_agent_shared/standards/`) had no `agent_loops/` slot, so there was no obvious place to write the contract.

---

## ✅ Как предотвратить

### General Extraction Algorithm

For each script being extracted:

1. **Freeze source.** Record current path, hash, short purpose.
2. **Extract intent.** Write the reusable workflow in plain language.
3. **Extract invariants.** What must always be true for safe operation.
4. **Extract interfaces.** Inputs, outputs, env vars, files created, exit codes.
5. **Extract risks.** Destructive commands, infinite loops, branch mutations, secrets, hardcoded paths.
6. **Write standard FIRST.** Create the concise standard under `_agent_shared/standards/agent_loops/<name>.md` (or `_agent_shared/standards/multi_agent/<name>.md` if cross-agent orchestration is involved).
7. **Owner approves the standard.** No tool change until the standard is signed off (per migration approval memo pattern).
8. **Refactor the tool.** `mkdir -p tools/agent_loops` → `git mv` script → patch in place to add required flags, remove unsafe behavior, plug into executor abstraction.
9. **Syntax checks.** `bash -n <tool>.sh` or `python3 -m py_compile <tool>.py`.
10. **Per-tool verification matrix** (see below) — 10 tests; commit fails if any test fails.
11. **Commit per tool.** One tool per commit; per-tool rollback enabled.
12. **Adapter notes.** Document Claude / Codex / Gemini / Jules / AgentNet differences inside the standard, not the tool.
13. **Registry update.** Add the standard to `_agent_shared/standards/README.md` table; add the tool path to relevant `tools/` README if one exists.

### Universal Safety Rules

Apply to every extracted tool:

| Rule | Reason |
|---|---|
| No `git add .` in agent loops. | Stages unrelated user/agent changes. |
| No auto-commit unless `--allow-commit` is passed. | Commits must be reviewable and scoped. |
| No infinite loop without `--max-iterations` or `--timeout`. | Prevents runaway spend and stuck sessions. |
| No hardcoded absolute user paths (`/Users/...`). | Breaks portability. |
| No provider-specific CLI as the only executor. | Future system supports any AI runtime. |
| No `--dangerously-skip-permissions` (or provider equivalent) baked in. | Tool must not bypass safety prompts by default. |
| No `--legacy` / `--compat` shim that re-enables removed unsafe behavior. | Unsafe behavior is not preserved under any flag. |
| Always write logs / artefacts under `--output-dir`. | Avoids root clutter and frozen-area leaks. |
| Always preserve tests / logs / reports unless explicitly archived. | Prevents loss of evidence. |
| Worktrees must be isolated, cleanup must be explicit. | Avoids dirty-base and branch collisions. |
| Marker-file frozen-area check before & after run. | Detects accidental writes into protected paths. |
| Dirty-tree guard. | Tool exits non-zero on dirty repo unless `--force`. |

### Verification Matrix Per Tool (10 tests)

Per `docs/audits/MIGRATION_SPEC_AMENDMENTS_2026-04-25.md` §B6 — every tool refactor commit MUST attach passing logs for these 10 tests:

| # | Test | Pass criterion |
|---|---|---|
| 1 | `--help` | Exit 0; lists `--dry-run`, `--executor`, `--output-dir`, `--max-iterations`, `--no-commit`, `--allow-commit`. |
| 2 | Dry-run no FS write | `--dry-run` produces empty `--output-dir`. |
| 3 | No auto-commit by default | `git log` count unchanged after default run. |
| 4 | `--allow-commit` opt-in works | `git log` count differs by ≥1 after run with the flag. |
| 5 | No `git add .` | `rg "git add \.\|git add --all" <tool>` is empty. |
| 6 | No hardcoded `/Users/` | `rg "/Users/" <tool>` is empty. |
| 7 | No `--dangerously-skip-permissions` | `rg "dangerously-skip-permissions" <tool>` is empty. |
| 8 | Dirty-tree guard | Run on dirty repo without `--force` exits non-zero. |
| 9 | `--max-iterations=2` stops at 2 | Iteration count == 2, not infinite. |
| 10 | Per-script typo guard | e.g. `rg "FINSIHED" tools/agent_loops/ralph_loop.sh` is empty. |

A refactor that fails any of these is not merge-eligible.

### Verification Commands (before & after extraction)

```bash
# Before extraction (record baseline)
bash -n <root>.sh
python3 -m py_compile <root>.py
rg -n "git add \\.|git commit|dangerously-skip-permissions|/Users/|\\.agent/" <root files> > /tmp/extraction_unsafe_baseline.txt

# After extraction (verify hardening)
bash -n tools/agent_loops/*.sh tools/triz/*.sh
python3 -m py_compile tools/agent_loops/*.py
for t in tools/agent_loops/*.sh tools/agent_loops/*.py; do "$t" --help >/dev/null && echo "$t HELP_OK"; done
rg -n "git add \\.|/Users/|dangerously-skip-permissions" tools/agent_loops tools/triz   # must be empty
python3 _agent_shared/scripts/compile_rules.py --target list                            # rule compiler unaffected
```

---

## 📝 Примечания

- This standard is the parent contract for the per-script standards listed in R4 (`parallel_worktree_swarm.md`, `ralph_loop.md`, `persistent_mining_loop.md`, `architect_loop.md`, `dev_swarm.md`, `improvement_loop.md`).
- Per-script standards add what is unique to each loop (sentinel completion, role taxonomy, plan file contract, etc.); they inherit the universal safety rules and verification matrix from this standard.
- Tools that handle git history (commit, branch, worktree) MUST run from the main checkout root (not from `.claude/worktrees/`). Worktrees are review-only.
- Frozen-area protection (per `MIGRATION_SPEC_2026-04-25.md` §1.3): use a marker file pattern (`touch /tmp/pre-RX-marker` then `find <frozen> -newer "$MARKER"`); never `find -newer <git-tag>` (tags are not paths).
- Original scripts must NOT be deleted in the same wave that creates the new tool — keep both until the new tool's verification matrix has passed in production at least once.

---

## 🔗 Cross-references

> **`docs/audits/*` — archive.** Эти аудиты остаются в монорепо и **в hub agent-meta не едут**;
> ссылки ниже на них — исторический контекст, а не действующий канон.

- `_agent_shared/standards/multi_agent/model_adapter_contract.md` — executor abstraction this protocol depends on.
- `_agent_shared/standards/process/rule_dialects.md` — companion R1 standard for the rule layer.
- `docs/audits/EXTRACTION_PROTOCOL_2026-04-25.md` _(archive)_ — original audit-stage protocol; this standard is the permanent home.
- `docs/audits/AGENT_LOOPS_SCRIPT_DECISIONS_2026-04-25.md` — per-script verdicts (`salvage_to_tool`, `salvage_to_standard_reference`, etc.).
- `docs/audits/MIGRATION_SPEC_2026-04-25.md` §2.4 (R4) — extraction wave plan.
- `docs/audits/MIGRATION_SPEC_AMENDMENTS_2026-04-25.md` §B6 + §B15 — verification matrix + `--allow-commit` opt-in policy.

---

## 🔄 История изменений

| Дата | Изменение | Причина |
|------|-----------|---------|
| 2026-04-25 | Создание стандарта | Wave R1 — Minimum Viable Contracts; ports `docs/audits/EXTRACTION_PROTOCOL_2026-04-25.md` into a permanent standard. Required before R4 tool extraction begins. |
