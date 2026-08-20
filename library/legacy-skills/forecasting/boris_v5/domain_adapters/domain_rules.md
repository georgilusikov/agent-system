# Domain Adapters (Boris v5)

## Product / Tech
- **Use:** system_operator, s_curve, zrts, contradictions, forty_principles, effects, standards, trimming, benchmarking, evolution_radar.
- **Focus:** PoA, S-curve evidence, technical constraints, value_analysis.
- **Согласование:** Проверить ритмику подсистем (частоты, скорости обработки, температурные режимы). Рассогласованность ритмов — частая причина отказов и потери КПД.
- **Anti-pattern:** Не путать стадию S-curve продукта и стадию S-curve технологии внутри продукта — они могут радикально различаться.

## Process
- **Use:** flow_analysis, limits_strategy, resource_analysis, trimming, contradictions, system_operator.
- **Focus:** E/M/I flows, bottlenecks, constraints, safety/regulations.
- **Согласование:** Проверить согласованность ритмов между этапами процесса (время цикла, партионность, пропускная способность). Рассогласованность создаёт буферы, запасы и простои.
- **Anti-pattern:** Не оптимизировать локальный этап, ухудшая глобальный поток (Theory of Constraints: оптимизация не-bottleneck бесполезна).

## Organization
- **Use:** system_operator, akts, antisystem, limits_strategy, benchmarking, toc_cloud.
- **Focus:** интангибельные линии (фрагментация/динамизация), политики, стимулы, MPV.
- **Согласование:** Ключевая линия эволюции для организаций. Рассогласованность ритмов между подразделениями (продажи vs разработка vs производство) — корень большинства организационных конфликтов. Инструмент: `@toc_cloud` (конфликт требований).
- **Anti-pattern:** Не применять технические ZRTS напрямую к организации (нет "перехода на микроуровень" для отдела продаж). Используйте линии эволюции осторожно, через аналогию.

## Personal Workflow
- **Use:** system_operator, akts, resource_analysis, limits_strategy, functional_analysis.
- **Focus:** когнитивная нагрузка, привычки, время, энергия, инструменты, фан-функции.
- **Согласование:** Проверить согласованность ритмов между задачами (deep work vs meetings vs email). Рассогласованность ритмов человека и инструментов → усталость и ошибки.
- **Anti-pattern:** Не предлагать "идеальную систему", если человек не готов к изменению привычек. Habit force из Phase 3 (Four Forces) — главный барьер.

## Auto (let Boris decide)
- Start as Product/Tech; if majority signals on Process → switch to Process adapter.
- Если SUA — организация или команда → Org adapter.
- Если SUA — личный процесс/привычка → Personal Workflow adapter.
