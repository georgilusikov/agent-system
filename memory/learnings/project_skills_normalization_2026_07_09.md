---
name: project-skills-normalization-2026-07-09
description: "Нормализация скиллов/стандартов Claude↔Codex↔workspace — что решено, что сделано, что осталось (Phase 3)"
metadata:
  node_type: memory
  type: project
  originSessionId: c83b5e37-ed89-4471-a45c-8f2c9297eebc
---

Сессия skills-standards-normalization (worktree курсор, ветка claude/skills-standards-normalization-b021ff), 2026-07-09.

**Ключевые решения (не пересматривать без новых данных):**
- Codex-версии скиллов = осознанные компактные EN-адаптации с runtime-спецификой (falsify: AGY/Fusion-гейты; retro: Codex-destinations). НЕ зеркалить, НЕ компилировать, НЕ заменять pointer'ами. Дрейф ловится `~/.claude/bin/skills-drift-check.sh` (19 пар, `--ack` после ревью), потребитель — §5 `/principles-review` weekly.
- `~/.codex/skills/claude-skills` — это АДАПТЕР (resolver + codex_translation.md, читает `~/.claude/skills` live), не дубль. Не деприкировать.
- Меты унифицированы: `0-how-to-write-standards.md` v0.1.0 (класс micro/method/contract = форма; scope personal/project/shared = место) ↔ `STRUCTURE_RULES.md` (workspace-сжатая). Противоречие мет = баг, чинить оба одним коммитом.
- Codex `write-a-skill` → deprecated pointer на `0-how-to-write-skills` (единственный дубль без runtime-ценности).

**Матрица пар:** `курсор/_agent_shared/reports/skills_dedup_matrix_2026-07-09.md` (reports/ гитигнорится — локальный файл).

**Осталось (Phase 3):** workspace-копии (`dev/check`, `dev/triage`, `dev/why_analysis`, `workflow/go`, `workflow/bouncer`) протухли с 2026-05-24 — реконсиляция по одной паре с diff-ревью. Кроме того канон-рефактор d8d2859a (description=роутинг) 2026-07-08 не перенесён в Codex-адаптации — быстрое ревью дельты, затем `skills-drift-check.sh --ack`. Не-дубли (pizdezh-check, retro, tdd-пары, find-skills, caveman) — не трогать, обоснование в матрице.

См. [[feedback-delegate-over-diy]], решение «НЕ зеркало» от 2026-07-06 в `~/.claude/skills/REGISTRY.md` (leverage entry).
