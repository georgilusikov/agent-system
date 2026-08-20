# Gate Check for Master TRIZ Orchestrator

## Mode A: Routing Dispatch
Applies when: orchestrator dispatches to a skill (no full report requested).
Output may be **JSON** (CLI/regression) or **markdown dispatch** (IDE). Both are valid.

### Minimum Criteria
| Check | Required | Actual | Pass? |
|---|---|---|---|
| Выбран конкретный skill для dispatch (`route_to` / `@skill_name`) | Да | ___ | ✅/❌ |
| Skill существует в Skill Map (`core_instructions.md`) | Да | ___ | ✅/❌ |
| Обоснование выбора (thought_process / причина выбора) присутствует | Да | ___ | ✅/❌ |
| Контекст/задание для выбранного скилла передано | Да | ___ | ✅/❌ |
| Оркестратор НЕ решает задачу сам (нет симуляции) | Да | ___ | ✅/❌ |

## Block Conditions (STOP)
- [ ] Оркестратор решает задачу сам (театральный анализ вместо handoff)
- [ ] Есть "я думаю, скилл сказал бы..." (симуляция вместо вызова)
- [ ] `route_to` = `@skill_name` или другой плейсхолдер

## Mode B: Report Assembly (classic_report_writer)
Applies when: user requests a full report/итог/решения. Orchestrator calls skills + `@final_triz_report`.

### Writer Quality Checks (classic_report_writer v1.1.0)
| Check | Required | Pass? |
|---|---|---|
| РВС-тест проведён (хотя бы 1 инсайт) | Да | ✅/❌ |
| Параметры Альтшуллера указаны в ТП (номера + принципы) | Да | ✅/❌ |
| >=1 вариант использует физ/хим эффект (@effects) | Да | ✅/❌ |
| ВПР рассмотрен (вредное как ресурс) | Да | ✅/❌ |
| Socratic Check записан в Execution Log (4/4) | Да | ✅/❌ |
| Execution Log содержит Branching, Secondary, Confidence | Да | ✅/❌ |
| Evidence tags расставлены на ключевых утверждениях | Да | ✅/❌ |
| Каждый вариант имеет No-Go + быстрый тест | Да | ✅/❌ |
