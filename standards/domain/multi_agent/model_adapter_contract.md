# Model Adapter Contract Standard

**Название:** Model-Agnostic Executor Contract for Reusable Agent Tools
**Дата создания:** 2026-04-25
**Контекст ошибки:** Root agent-loop scripts (`ralph_loop.sh`, `dev_swarm_v4.py`, `architect_loop.sh`, `improvement_loop.sh`) hardcoded a specific provider CLI (Claude Code), used `--dangerously-skip-permissions`, called `git add .`, auto-committed, and embedded `/Users/...` paths. This locked the workspace to a single provider, a single host, and an unsafe staging behavior.

---

## 🎯 Фундаментальное правило

**Every reusable agent tool under `tools/` MUST accept an executor abstraction (CLI command + args), an output directory, max-iterations, dry-run mode, and `--no-commit` as the default. Provider-specific assumptions belong in adapters, not in tools.**

---

## ⚠️ Что было не так

- Tool spawned `claude --dangerously-skip-permissions` directly — no way to swap to Codex / Gemini / Jules / AgentNet.
- Tool ran `git add .` and `git commit` automatically — staged unrelated user changes, polluted history.
- Tool wrote artefacts to `~/<somewhere>` or `./<root>` instead of `--output-dir`.
- Tool had no `--max-iterations` or `--timeout` — runaway loop possible.
- Tool had no `--dry-run` — no safe way to verify config without spending tokens.

---

## 🔍 Почему это произошло

1. No standard for tool I/O — each loop script was author-shaped.
2. "It works on my machine" — host-specific paths leaked into reusable code.
3. "Claude Code is the runtime" — provider lock-in baked into tools meant to be portable.

---

## ✅ Как предотвратить

### Required CLI surface (every reusable tool)

```text
--executor <cmd>           # adapter command (e.g. "claude", "codex", "gemini-cli")
--output-dir <path>        # all artefacts go under <path>/{run.json,logs/,artifacts/,summary.md}
--max-iterations <N>       # hard cap; required for any loop tool
--timeout <sec>            # alternative or complement to --max-iterations
--dry-run                  # parse config, print plan, write nothing
--no-commit                # default; tool MUST NOT call git commit
--allow-commit             # explicit opt-in to enable a single scoped commit
--help                     # print this surface
```

### Forbidden inside reusable tools

- `git add .` or `git add --all` — stages unrelated changes.
- `git commit` without `--allow-commit` opt-in.
- Hardcoded `/Users/<name>/...` absolute paths.
- `--dangerously-skip-permissions` (or any provider equivalent) baked in.
- Auto-commit, auto-push, auto-merge as default behavior.
- `--legacy` / `--compat` shim that re-enables any of the above. Unsafe behavior is not preserved under any flag (per migration invariant in `MIGRATION_SPEC_AMENDMENTS_2026-04-25.md` §B15).

### Input contract (executor adapter)

```text
input:
  prompt: string           # task prompt
  cwd: path                # working directory (typically <output-dir>/sandbox/)
  timeout_sec: integer
  allowed_paths: list[path]
  output_contract: text | json schema
```

### Output contract (executor adapter return)

```text
output:
  success: boolean
  content: string          # human-readable summary
  artifacts: list[path]    # produced files (under output-dir)
  changed_files: list[path]
  error: string | null
  evidence: dict           # provider-specific traces, references, citations
  cost: { tokens_in: int, tokens_out: int, usd: float | null }
  retry: { attempt: int, max: int }
```

### Verification matrix per tool (10 tests)

Per `MIGRATION_SPEC_AMENDMENTS_2026-04-25.md` §B6 — each tool refactor commit MUST attach passing logs for:

1. `--help` exits 0 and lists all required flags.
2. `--dry-run` writes nothing to `--output-dir`.
3. Default run does NOT advance `git log` count (no auto-commit).
4. `--allow-commit` advances `git log` count by ≥1.
5. `rg "git add \.|git add --all" <tool>` is empty.
6. `rg "/Users/" <tool>` is empty.
7. `rg "dangerously-skip-permissions" <tool>` is empty.
8. Dirty-tree guard: tool exits non-zero on dirty repo without `--force`.
9. `--max-iterations=2` stops at 2 iterations (no runaway).
10. (script-specific) `rg "FINSIHED" <tool>` is empty for `ralph_loop`.

A refactor that fails any of these tests is not merge-eligible.

---

## 📝 Примечания

- Adapter implementations (Claude / Codex / Gemini / Jules / AgentNet) live separately under `_agent_shared/llm/` or `agent-meta/llm/` and conform to the input/output schemas above.
- Tools must NOT branch on provider name — they call the executor abstraction. Provider-specific quirks (e.g. response shape, streaming) are absorbed by the adapter.
- `cost`, `evidence`, `error`, and `retry` are required output fields — incomplete payloads are treated as adapter bugs.
- Behavior change is explicit, not silent: `--no-commit` is the new default; users who want pre-refactor commit behavior must pass `--allow-commit`. No `--legacy` shim.
- The verification matrix above is the gate. Owner approval memos for R4 (per migration spec) must explicitly accept the safety / behavior trade-off.

---

## 🔗 Cross-references

> **`docs/audits/*` — archive.** Эти аудиты остаются в монорепо и **в hub agent-meta не едут**;
> ссылки ниже на них — исторический контекст, а не действующий канон.

- `_agent_shared/standards/agent_loops/extraction_protocol.md` — extraction algorithm + universal safety rules (companion to this standard).
- `_agent_shared/standards/multi_agent/swarm_orchestration.md` (planned in R4) — multi-tool orchestration on top of the executor contract.
- `docs/audits/EXTRACTION_PROTOCOL_2026-04-25.md` §"Model-Agnostic Executor Contract" + §"Tool Refactor Requirements" — primary source.
- `docs/audits/MIGRATION_SPEC_AMENDMENTS_2026-04-25.md` §B6 — verification matrix; §B15 — `--allow-commit` opt-in; no legacy shim.
- `docs/audits/TARGET_AGENT_ARCHITECTURE_2026-04-25.md` §"Canonical vs Adapter Dialects" — adapter / canonical separation.

---

## 🔄 История изменений

| Дата | Изменение | Причина |
|------|-----------|---------|
| 2026-04-25 | Создание стандарта | Wave R1 — Minimum Viable Contracts; required before R4 tool refactor lands. |
