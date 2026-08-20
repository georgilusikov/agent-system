---
name: bouncer
description: 'Use when a FINISHED artifact needs an independent second opinion from an external model (Gemini/Codex), not from the session that produced it. Triggers: "внешний аудит", "второе мнение", "прогони через гемини", "прогони через gemini", "запусти через грок", "проверь через кодекс", "прогони через bouncer", "оцени чужой моделью", "dual review". NOT for: ревью диффа ветки или PR против стандартов и спеки (/code-review), опровержение release-claim end-to-end (/falsify), периодический аудит системы правил против META_PRINCIPLES (/principles-review), самопроверка своего результата (/check), рефлексия процесса (/pizdej).'
---

# Bouncer — External Quality Audit (Multi-Backend, Parallel)

Independent audit by Gemini and/or Codex. Absorbs the former `/dual-review` (Codex plan review).

## Invocation

Natural language → parse intent:

| User says | Backends | Mode |
|---|---|---|
| "bouncer", "score", "audit" | 1× Gemini | quick |
| "deep audit", "verify everything" | 1× Gemini | deep |
| "dual review", "review plan", "cross-check plan" | 1× Codex | plan-review |
| "second opinion", "both models", "gemini + codex" | 1× Gemini + 1× Codex | quick |
| "two geminis", "2 gemini" | 2× Gemini | quick |
| "consensus audit", "triple review" | 2× Gemini + 1× Codex (or user-specified) | quick/deep |

If ambiguous — ask ONE clarifying question via AskUserQuestion: which backends + how many + mode.

## Backends

| Backend | Strength | Cost | Script |
|---|---|---|---|
| **Gemini** | Prose, strategy, creative, holistic view | API call 5-120s | `bouncer-check.py` (quick) / `bouncer-deep.py` (deep) |
| **Codex** | Code, plans, structured analysis, iterative | CLI call per cycle | `bouncer-codex.sh` |

## Protocol

### Step 1 — Gather context (once, shared by all audits)

```bash
git diff --stat --no-color
git diff --no-color
git diff --cached --stat --no-color
git diff --cached --no-color
```

Read `CLAUDE.md` from cwd if exists.

Build `assistant_text` — thorough summary of what was done:
- code: files changed, bugs fixed, tests, commands run
- creative: what created, goal, audience, decisions
- plans: plan content, scope, tech stack, assumptions
- research: findings, sources, conclusions

### Step 2 — Build JSON input (one shared object)

```json
{
  "assistant_text": "...",
  "diff_stat": "...",
  "diff_text": "...",
  "context": "...",
  "cwd": "/abs/path",
  "mode": "quick|deep|plan-review"
}
```

### Step 3 — Dispatch parallel audits

**Critical:** send ALL audit commands in ONE message via multiple Bash tool calls for true parallelism.

For N Gemini + M Codex audits:

```bash
# Gemini quick (× N)
echo '<JSON>' | python3 ~/.claude/skills/bouncer/scripts/bouncer-check.py

# Gemini deep (× N, deep mode)
echo '<JSON>' | python3 ~/.claude/skills/bouncer/scripts/bouncer-deep.py

# Codex (× M)
echo '<JSON>' | ~/.claude/skills/bouncer/scripts/bouncer-codex.sh
```

Each audit gets a label: `gemini-1`, `gemini-2`, `codex-1` for traceability.

### Step 4 — Aggregate

Produce verdict table:

| Audit | Score | Verdict | Top gap | Top risk |
|---|---|---|---|---|
| gemini-1 | 7/10 | NEEDS_REVISION | ... | ... |
| gemini-2 | 8/10 | APPROVED | ... | ... |
| codex-1 | 6/10 | NEEDS_REVISION | ... | ... |

**Consensus rules:**
- ALL APPROVED → overall APPROVED
- ANY blocking issue (critical gap) → NEEDS_REVISION, list the blocker
- Split verdicts → present both views, let user decide

### Step 5 — Present results

Show:
1. Per-audit raw outputs (do NOT filter)
2. Aggregated verdict table
3. Consensus verdict + unique insights from each backend
4. Handoff: for `plan-review` → step 6 iteration; for others → end.

### Step 6 — Plan-review iteration (Codex-only, up to 3 cycles)

If mode=plan-review and verdict=NEEDS_REVISION:
1. Update plan with accepted suggestions (+ rationale for rejected)
2. Re-dispatch Codex with follow-up prompt including what was accepted/rejected
3. Exit on APPROVED or after cycle 3

Append to `implementation_plan.md`:
```markdown
## External Review (via bouncer)
**Backends:** codex (3 cycles)
**Verdict:** APPROVED (cycle 2/3)
**Accepted:** [list]
**Rejected (with reason):** [list]
```

## Rules

- Do NOT filter script output.
- Script error (missing API key, import, CLI not found) → show to user, do not retry silently.
- `assistant_text` is the heaviest field — be thorough.
- Parallel counts cap at 3 per backend (6 total) to avoid rate-limits.
- When user asks for "both models" without numbers → default 1× Gemini + 1× Codex.

## Migration note

The former `/dual-review` command (iterative Codex plan review) is now `/bouncer plan-review`. Trigger phrases "dual review", "review plan", "cross-check plan" activate it.

## Content-depth gate (обязателен для вердикта)

Вердикт внешнего аудитора принимается, только если его evidence содержит **конкретные
значения из источника** — минимум 3-5 на утверждение: имена тестов и что каждый проверяет,
id, числа, hex/rgba, цитаты кода. «Проверил, всё сходится», «N тестов зелёные» — это
`NOT CHECKED`: аудитор не показал, что открывал артефакт. Пересказ от внешней модели
опаснее своего — его нечем фальсифицировать.

## Guardrails

- **Успех транспорта ≠ успех аудита.** Скрипт отработал ≠ артефакт проверен.
- Ошибка скрипта/модели (нет API-ключа, import, CLI не найден) — показывается
  пользователю, не «ретраится тихо» и не выдаётся за успех.
- Реальный внешний бэкенд недоступен → делай явно помеченный НЕ-внешний
  self-аудит; не подавай его как второе мнение.
- Внешний аудит НЕ заменяет локальные проверки артефактов, когда claim зависит от
  локальных файлов или runtime-поведения (`/check` всё равно обязателен).
- Сырой материал из вывода ревьюера не фильтруется; синтезируется только решение.

## Owner effort digest

Финальный блок — таблица `next action | усилие владельца 0-100 | делаю сам | только владелец`.
Любой клик/ответ/решение владельца = минимум 50. Шагов нет → строка «Нет шагов для человека»
+ причина.
