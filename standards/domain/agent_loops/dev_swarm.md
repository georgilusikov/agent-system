# Dev Swarm Standard

**Название:** Dev Swarm — Hierarchical Multi-Model Orchestration with Cross-Critique
**Дата создания:** 2026-04-25
**Контекст ошибки:** `dev_swarm_v4.py` (1085 lines) is the only ACTIVE root agent-loop script and is cited from `CLAUDE.md` line 16 (`python3 dev_swarm_v4.py --mode quality "task"`). It already routes through VibeProxy and supports multi-model orchestration but lacks `--output-dir`, `--max-iterations`, `--dry-run`, structured cost output per stage, and dirty-tree guard. Pattern is the most valuable to preserve.

---

## 🎯 Фундаментальное правило

**Single-task multi-model pipeline: cheap manager decomposes → 3 generators produce candidate solutions in parallel → ONE critic cross-evaluates all 3 (token-efficient) → high-quality synthesizer emits final solution. All requests routed through VibeProxy; mode + per-stage model are CLI-selectable; cost and confidence are explicit fields, not implicit.**

---

## ⚠️ Что было не так

- No `--output-dir`; logs land in `<repo>/_logs/dev_swarm/` regardless of caller.
- No `--max-iterations` or `--timeout` on synthesis retry path.
- `--dry-run` absent — config bugs caught only after spending tokens.
- Cost field present per call but not aggregated per stage in structured JSON output.
- No dirty-tree guard before synthesis writes any file artefacts.

---

## 🔍 Почему это произошло

1. Author optimized for one-shot CLI use, not as a callable library.
2. VibeProxy abstraction was added later than the orchestration shell.
3. Cost tracking grew per-call before there was a stage taxonomy.

---

## ✅ Как предотвратить

### Pipeline (4 stages)
1. **Manager** — cheap fast model (e.g. Gemini 3 Flash). Decomposes task; emits strict-JSON plan with `task_type`, `complexity`, `subtasks[]`, `acceptance[]`.
2. **Parallel Swarm** — 3 generators (e.g. Gemini 3 Pro + GLM-5 + GPT-5.3 Codex). Each produces a candidate solution against the plan. Run via `asyncio.gather`.
3. **Cross-Critique** — ONE critic model (e.g. GPT-5.1 / MiniMax). Evaluates all 3 candidates in a single call (token-efficient vs. 3 separate critiques). Emits per-candidate score + diff suggestions.
4. **Synthesis** — high-quality model (e.g. Claude Sonnet 4.5). Final answer informed by candidates + critique.

### Modes
- `--mode fast` — manager + single generator only. Cheap, fast.
- `--mode quality` — full 4-stage pipeline. Default for non-trivial tasks.

### Lazy escalation
- Try cheap critic first. If `confidence < 0.80` OR critic call fails → escalate critic to expensive model (Claude / GPT-5 Pro).
- Escalation count per run capped by `--max-escalations N` (default 1).

### Inputs
`--task "..."` (required), `--mode {fast,quality}`, `--output-dir <path>` (required for quality mode), `--max-iterations N`, `--max-escalations N`, `--dry-run`, `--manager-model`, `--generator-models <m1,m2,m3>`, `--critic-model`, `--synthesizer-model`, `--no-commit` (default), `--allow-commit`.

### Provider routing
- All HTTP calls → `http://localhost:8318/v1/chat/completions` (VibeProxy). No direct provider keys in tool.
- Per `model_adapter_contract.md`: model selection via CLI flags; tool does NOT branch on provider name.

### Safety invariants
- All requests via VibeProxy (no direct OpenAI / Anthropic / Google calls in tool code).
- `--dry-run` writes nothing under `--output-dir`; prints planned model calls and prompts.
- Output is structured JSON with stages: `[manager, generators[3], critique, synthesis]`, each with `model`, `tokens_in`, `tokens_out`, `usd`, `latency_ms`, `confidence`.
- Confidence is an explicit field, not implicit (per anti-bias rule in this repo).
- Dirty-tree guard before any artefact write under `--output-dir`.
- `--max-iterations` REQUIRED for quality mode synthesis-retry path.
- No `git commit` in tool; orchestration only.

### Verification
- 10-test verification matrix from `extraction_protocol.md`.
- Round-trip dry-run: structured plan emitted, zero HTTP calls beyond plan validation.
- VibeProxy reachable check on startup; tool exits non-zero with actionable message if not.

---

## 📝 Примечания

- Source `dev_swarm_v4.py` is ACTIVE and cited from `CLAUDE.md`. R4b will refactor IN PLACE into `tools/agent_loops/dev_swarm.py` with the safety flags above. No behavior change to the pipeline itself.
- Sibling patterns: `parallel_worktree_swarm.md` (multi-task fan-out), `architect_loop.md` (planning, not coding).
- Higher-level orchestration (chaining `dev_swarm` runs into a project plan) belongs in a future `multi_agent/swarm_orchestration.md` standard if the need arises.
- Per-stage cost aggregation is a hard requirement for the structured-JSON output — incomplete payloads are tool bugs.

---

## 🔗 Cross-references

- `_agent_shared/standards/agent_loops/extraction_protocol.md` — parent contract + verification matrix.
- `_agent_shared/standards/multi_agent/model_adapter_contract.md` — executor abstraction; output schema contract.
- `_agent_shared/standards/multi_agent/swarm_orchestration.md` — planned higher-level orchestration standard (not yet written).
- Provenance: `dev_swarm_v4.py` (active source); refactor target `tools/agent_loops/dev_swarm.py` (R4b).

---

## 🔄 История изменений

| Дата | Изменение | Причина |
|------|-----------|---------|
| 2026-04-25 | Создание стандарта | R4a — document the active dev-swarm pattern before R4b refactor adds safety flags. |
