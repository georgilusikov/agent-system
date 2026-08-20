---
name: skills-consolidation-2026-07-10
description: "Решения сессии консолидации скиллов Claude+Codex 2026-07-10 — что слито, что в архиве, что отложено"
metadata:
  node_type: memory
  type: project
  originSessionId: f7b66e6e-d038-4a5a-9fa7-b956d2ca447f
---

Сессия 2026-07-10, консолидация скиллов (цель пользователя: ~13 запоминаемых имён, паритет Claude/Codex).

**Сделано (коммиты):** fraud-table в /check из fable-method (`~/.claude d1495fd`, `~/.codex 032ab84`); Codex `pizdej` = merge pizdezh-check+critical-reflection, nikita-orchestrator в архив (`de040ee`); Codex 47→28 скиллов, tier1-3 архив в `~/.codex/skills-archive/` (`6c75ccf`); mattpocock refresh — to-spec/to-tickets/implement/diagnosing-bugs/wayfinder в `~/.codex/skills/` и `go/workflows/`, старые в `skills-archive/go-workflows-matt-stale/` (`5e29319`); /go расширен маршрутами roadmap/goal/delegate/estimate/ship/prioritize (`a22166e`).

**Решения (не пересматривать без новых данных):**
- anti-bias НЕ сливать с pizdej: разная фаза (ex-ante решение vs ex-post проверка), /check зависит от anti-bias.
- fusion←bouncer merge ОТКЛОНЁН (78% < гейт 85%): семантика разная, ссылки в CLAUDE.md disambiguation + workspace CLAUDE.md сломаются. Вместо этого — строка в bouncer «исполняется через fusion-панель» (не сделано).
- /go = роутер-указатели, тела скиллов не переносить (Codex читает каноны напрямую).

**Сделано дополнительно:** merge `debug ← why+triage` ВЫПОЛНЕН (~/.claude 334f18e, ~/.codex 71d2239): Mode L/H, ссылки обновлены в CLAUDE.md (212/215 строк), go/falsify/leverage/estimate/prioritize/principles-review/0-how-to-write-skills/sus. mattpocock triage → архив triage-mattpocock. goal-plan §8 Plan Challenge + §9 Clarifying Questions (46020de). Codex получил свой go-роутер (eae935d). Решение: goal-plan/goal-king раздельно, king на испытательном (2-3 прогона, слабые → архив).

**Отложено (ожидает):**
- ~/.claude/skills/raw/ (данные, не скилл) и triage-workspace/ (мусор) — не убраны.
- REGISTRY.md строки fusion нет; mattpocock-таблица помечена исторической.
- Идея из fable-method: eval/scenarios (golden set ловушек) для /check и /bouncer — в backlog.

Usage-факты: подсчёт чтений SKILL.md по 227 Codex-сессиям 30д; шумовой пол ≈2-3 (сессия нормализации 2026-07-09 читала всё). Связано: [[project_skills_normalization_2026_07_09]].
