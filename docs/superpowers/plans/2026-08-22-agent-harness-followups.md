# Agent Harness Follow-ups Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development to implement this plan task-by-task.

**Goal:** When a bounded runtime changes state, deploys the canon, captures a verified learning, or checks a provider capability, the system leaves only metadata evidence and exposes a safe next action; it must not store prompts, responses, transcripts, tool payloads, credentials, or environment values.

**Architecture:** Add one small metadata-only receipt adapter around the existing hash-chain writer, then connect the existing state and installer seams to it through explicit opt-in contexts. Add two provider-free executable seams: a redacted memory-candidate capture command and a bounded provider capability canary. Keep live model output discarded and report unavailable channels as `NOT RUN`; this wave never invokes a model.

**Tech Stack:** Python 3 standard library, existing JSONL receipt/memory contracts, POSIX shell hooks, existing CLI runtimes.

## Global Constraints

- Keep journals and candidate ledgers outside the repository with restrictive permissions.
- Never persist or print prompts, responses, transcripts, tool payloads, credentials, or environment values.
- Existing callers without an explicit receipt context remain behavior-compatible.
- Every new mutation path has one focused executable self-check.
- Do not install a new dependency or provider; missing capability is `NOT RUN`, not `PASS`.
- Real-home deployment is not part of this wave unless a fresh read-only deployed check reports drift; any such apply requires pre-state evidence, a backup snapshot, and a rollback canary.

---

### Task 1: Wire metadata receipts into mutable runtime seams

**Files:**
- Create: `scripts/runtime_receipts.py`
- Modify: `scripts/agent_run_state.py`
- Modify: `scripts/install.py`
- Create: `scripts/test_runtime_receipts.py`
- Modify: `scripts/test_agent_run_state.py`
- Modify: `scripts/test_install_symlink_escape.py`

**Interfaces:**
- `runtime_receipts.ReceiptContext(journal, repo_root, run_id, actor, runtime, task_id=None, bead_id=None, source_commit=None)`
- `runtime_receipts.emit_change(context, event_id, operation, target, before_hash, after_hash, outcome, evidence_refs=(), error_class=None)` delegates parent selection to the existing journal chain.
- `agent_run_state` mutators accept optional `receipt_context` and emit after a real state-file change.
- `install.py --apply/--rollback` accepts optional `--receipt-journal`, `--run-id`, `--task-id`, `--bead-id` and emits one deployment receipt after the reversible operation.

- [ ] **Step 1: Add the failing receipt-adapter test.**

  In `scripts/test_runtime_receipts.py`, create a temporary journal outside a temporary repo, call `emit_change` twice with a parent chain, assert the validated records contain only metadata, and assert a forbidden key or in-repo journal is rejected.

- [ ] **Step 2: Run the focused test and observe the missing module/API failure.**

  Run: `python3 scripts/test_runtime_receipts.py`
  Expected: FAIL before the adapter exists.

- [ ] **Step 3: Implement the adapter and state/installer wiring.**

  The adapter delegates validation and hash chaining to `change_receipts.append_receipt`, computes file SHA-256 only for paths explicitly supplied by the caller, derives an RFC3339 UTC timestamp internally, normalizes `evidence_refs` to a JSON list, and never accepts arbitrary metadata keys. State and installer paths pass the before/after file hashes and use a stable operation event id so retries are idempotent. The production-shaped test invokes every connected mutator with a temporary context and asserts one receipt per real file change.

- [ ] **Step 4: Run focused checks.**

  Run: `python3 scripts/test_runtime_receipts.py && python3 scripts/test_agent_run_state.py && python3 scripts/test_install_symlink_escape.py`
  Expected: all commands exit 0 and print their existing `PASS` lines.

- [ ] **Step 5: Commit the task.**

  Run: `git add scripts/runtime_receipts.py scripts/agent_run_state.py scripts/install.py scripts/test_runtime_receipts.py scripts/test_agent_run_state.py scripts/test_install_symlink_escape.py && git commit -m "feat: wire metadata receipts into runtime seams"`

### Task 2: Add a safe automatic memory-candidate capture seam

**Files:**
- Create: `scripts/memory_capture.py`
- Create: `scripts/test_memory_capture.py`
- Modify: `standards/domain/agent-memory-standard.md`

**Interfaces:**
- `memory_capture.capture_verified_candidate(ledger, candidate, receipt, repo_root)` delegates to `memory_candidates.create_candidate` only after the receipt is `verified` and `metadata-only`.
- CLI reads candidate metadata from a JSON file or stdin, never from a model transcript, and writes only the resulting candidate ledger outside Git.

- [ ] **Step 1: Add the failing capture test.**

  Test that a verified receipt creates a `draft` candidate, a failed receipt is rejected, and a candidate containing `prompt`/`response`/`environment` is rejected without changing the ledger.

- [ ] **Step 2: Run `python3 scripts/test_memory_capture.py` and observe the missing module failure.**

- [ ] **Step 3: Implement the thin adapter.**

  Do not infer a learning from raw model output. Require explicit redacted fields (`statement`, `applicability`, `limits`, `result_metric`, and evidence references); owner/reviewer approval remains in `memory_candidates.py`.

- [ ] **Step 4: Run `python3 scripts/test_memory_capture.py && python3 scripts/test_memory_candidates.py`.**

- [ ] **Step 5: Commit with `git add scripts/memory_capture.py scripts/test_memory_capture.py standards/domain/agent-memory-standard.md && git commit -m "feat: add verified memory capture seam"`.**

### Task 3: Add bounded provider capability canaries

**Files:**
- Create: `scripts/provider_canary.py`
- Create: `scripts/test_provider_canary.py`
- Modify: `standards/domain/agent_loops/bounded_parallel_delegation.md`

**Interfaces:**
- `provider_canary.run_canary(executable, argv, provider, runtime, model, timeout_seconds, run_id, evidence_ref)` returns metadata `{provider, runtime, model, status, canary, exit_code, elapsed_ms, reason, redaction_status}`.
- The subprocess receives the caller-provided command but stdout/stderr are discarded; command arguments are never persisted.
- Missing executable, timeout, and non-zero exit are `NOT RUN` or `FAIL` with metadata only.

- [ ] **Step 1: Add tests for missing executable, successful bounded command, timeout, and forbidden output fields.**
- [ ] **Step 2: Run `python3 scripts/test_provider_canary.py` and observe the missing module failure.**
- [ ] **Step 3: Implement with `shutil.which`, `subprocess.run`, `DEVNULL`, monotonic timing, and a hard timeout.**
- [ ] **Step 4: Run only zero-cost capability checks (`command -v`, `--version`, or `--help`) for `codex`, `agy`, `gemini`, `claude`, `dsh`, and `luna`; retain only capability/exit/latency metadata outside Git. Do not invoke a model.**
- [ ] **Step 5: Commit with `git add scripts/provider_canary.py scripts/test_provider_canary.py standards/domain/agent_loops/bounded_parallel_delegation.md && git commit -m "feat: add metadata-only provider canaries"`.**

### Task 4: Connect the new seams to acceptance evidence

**Files:**
- Modify: `scripts/check.py`
- Create: `scripts/test_runtime_acceptance.py`
- Modify: `work/report-gl-ejw-14.md` (outside the repository if the report is regenerated)
- Modify: `outputs/agent-harness-acceptance.md` (outside the repository if the summary is regenerated)

**Interfaces:**
- `check.py --repo` validates the new modules and their focused self-check entrypoints.
- The acceptance canary creates a temporary state file, emits a receipt, captures a redacted draft memory candidate, and validates a provider `NOT RUN` result without touching the real home.

- [ ] **Step 1: Add the failing acceptance test for the complete metadata-only chain.**
- [ ] **Step 2: Implement the smallest checker additions and canary.**

  Run: `python3 scripts/test_runtime_acceptance.py`
  Expected: `PASS metadata-only runtime acceptance` and no writes outside the test temporary directory.

- [ ] **Step 3: Run the full focused suite, `git diff --check`, `python3 scripts/check.py --repo`, and the read-only `python3 scripts/check.py --deployed`.**

  Expected: each command exits 0 and prints `PASS`; if deployed check is not `PASS`, do not apply.
- [ ] **Step 4: Do not apply to the real home when deployed check passes. If it reports drift, stop and request a fresh owner-approved apply with pre-state evidence and the exact rollback command `python3 scripts/install.py --rollback <snapshot>`.**
- [ ] **Step 5: Update acceptance evidence with exact PASS/FAIL/NOT RUN results and leave unavailable live providers open.**

  Validate `/Users/georgijlusikov/Documents/Codex/2026-08-22/codex-threads-01a01f16-d2c9-7dd2-9717/outputs/agent-harness-acceptance.md` and `work/report-gl-ejw-14.md` for the denylist (`prompt`, `response`, `transcript`, `payload`, `credential`, `secret`, `token`, `environment`) and record whether real-home apply was skipped or backed by pre-state, snapshot, and rollback evidence.

## Acceptance

The outcome is accepted only if the new self-checks pass, the repository and deployed checks pass, receipts and memory remain metadata-only, and live capability results distinguish `PASS`, `FAIL`, and `NOT RUN` without storing model content. Provider-specific auth, quota, and unavailable DSH/Luna channels remain explicit owner-gated follow-ups.

---

### Task 5: Cover memory and evaluation projection producers

**Files:**
- Modify: `scripts/memory_candidates.py`
- Modify: `scripts/memory_capture.py`
- Modify: `scripts/evaluate_before_after.py`
- Modify: `scripts/test_memory_candidates.py`
- Modify: `scripts/test_memory_capture.py`
- Modify: `scripts/test_evaluate_before_after.py`

**Interfaces:**
- Existing mutators accept optional `runtime_receipts.ReceiptContext` and emit one receipt only after a real external-ledger/result-file mutation.
- CLI entrypoints accept an explicit external receipt journal and metadata identity; no raw candidate/result content enters the receipt.

- [ ] Add production-shaped tests for candidate create/review/approve/rollback and evaluator write-result receipts, including no-op retries.
- [ ] Wire the optional receipt context with external-journal safety, stable event IDs, before/after hashes, and package/script imports.
- [ ] Run the memory/evaluator/receipt self-checks in direct and module modes, then run `python3 scripts/check.py --repo`.

The task is complete only when the standard's “state, task, hook, deployment, or projection mutation” claim is true for the repository's known memory/evaluation producers; unavailable task/Beads writers remain explicitly absent rather than fabricated.

## Возражения критика

| # | линия атаки | возражение | severity | что изменить |
|---|---|---|---|---|
| 1 | ненаблюдаемые критерии | Task 4, Step 2: «реализовать минимальные дополнения checker’а и canary» не задаёт точной команды, ожидаемого вывода или проверяемого файла. | advisory | Указать конкретный executable check и ожидаемые `PASS/FAIL/NOT RUN`. |
| 2 | ненаблюдаемые критерии | Task 4, Step 5: обновление внешних acceptance-файлов упомянуто условно, но не определено, как доказать отсутствие prompt/response/tool payloads. | advisory | Добавить проверку ключей и точные пути итоговых evidence-файлов. |
| 3 | первый падающий шаг | Task 1, Step 3: `emit_change(..., evidence_refs=())` использует tuple по интерфейсу плана, а существующий `change_receipts.append_receipt` принимает только JSON-list; прямая передача упадёт на первой записи. | advisory | Явно нормализовать `evidence_refs` в list перед делегированием. |
| 4 | необратимые шаги без отката | Task 4, Step 4 теперь запрещает real-home apply при успешной deployed-проверке и требует pre-state/backup/rollback при drift; прежний critical устранён. | advisory | В acceptance evidence отдельно зафиксировать, что apply не выполнялся либо были все три доказательства. |
| 5 | подмена задачи | Goal сформулирован как metadata-only состояние и безопасное следующее действие, а не только как создание файлов; подмена outcome на output устранена. | advisory | Сохранить в acceptance итоговое наблюдаемое состояние, не только список PASS-тестов. |
| 6 | противоречие принятым решениям | Найденное `ACCEPTED: meta_v3.1` относится к `skills/meta` и план его не переоткрывает; противоречия принятым решениям не обнаружено. | advisory | Ничего обязательного; сохранить текущий scope. |

VERDICT: ADVISORY (план выдаётся с возражениями)  
Почему: три прежних critical устранены на уровне scope и защитных условий; остаются два наблюдаемых уточнения и остаточный риск нормализации adapter-интерфейса.

## Фактический статус реализации

- Task 1–4: завершены и проверены ранее.
- Task 5: завершён в `dd6aa1d` и `8db4f70`; state, installer, memory и
  evaluation producers выполняют receipt preflight до мутации, а одинаковые
  retry восстанавливают отсутствующий receipt.
- Hook privacy follow-up: завершён в `cc092ed` и `6c3553e`; incident parking и
  precompact handoff сохраняют только metadata, без transcript path/content, а
  content-bearing Gemini audit требует отдельный `GEMINI_AUDIT_ALLOW_CONTENT=1`.
  Self-check запускается из `scripts/check.py --repo`.
- Acceptance extension: завершён в `fbb9b5e`; runtime canary проверяет receipts
  для memory и evaluation producers. Test-only hook files не считаются runtime
  consumer paths для deployed drift.

Проверено: focused direct/module tests, hook canaries, `python3 scripts/check.py
--repo`, `python3 scripts/check.py --deployed`, `py_compile`, `git diff --check`.
