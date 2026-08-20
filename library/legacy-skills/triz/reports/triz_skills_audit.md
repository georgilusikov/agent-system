# TRIZ Skills Audit

- Дата: 2026-01-06
- Область: `_agent_shared/skills/triz/` (37 скиллов)
- Метод: автоматическая проверка наличия `SKILL.md`, `core_instructions.md`, `examples/`, `validators/`, `validators/gate_check.md` (см. JSON-дамп `triz_skills_audit.json`).

## Итоги
- Базовые файлы (`SKILL.md`, `core_instructions.md`) есть у всех 37 скиллов.
- 36 из 37 имеют примеры и валидаторы с `gate_check.md`.
- Недоукомплектован один скилл.

## Недостающие элементы
| Skill | Что добавить |
|-------|--------------|
| `master_triz_orchestrator` | `examples/` с рабочим примером; `validators/gate_check.md` с критериями руутинга/блок-условиями |

## Рекомендации
- Для `master_triz_orchestrator` добавить хотя бы один пример диспатча и валидатор (Gate: выбор агента, блок-условия, фолбэки).
- Остальные скиллы покрыты базовой структурой; содержимое валидаторов/примеров не оценивалось в этом проходе.
