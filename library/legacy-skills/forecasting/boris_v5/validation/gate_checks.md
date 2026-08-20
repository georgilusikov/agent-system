# Boris v5 Gate Checks

## Phase 0 (Lock)
- [ ] SUA + Boundary + KPI зафиксированы
- [ ] PoA-цепочка описана
- [ ] Stakeholders перечислены
- [ ] Constraints (время/деньги/регуляция/данные) зафиксированы
- [ ] Если включён ранний STOP: есть причина + Pivot Option + проверка/вопрос

## Phase 1 (Scan)
- [ ] Supersystems ≥ depth.min
- [ ] Subsystems ≥ depth.min
- [ ] Main constraint/limit найден
- [ ] Resources и Harmful functions собраны
- [ ] Предел/порог и “другая кривая” после порога названы
- [ ] Если включён STOP после Phase 1: есть лимит-hard + 2–3 маршрута переезда + 1 проверка

## Phase 2 (Reality)
- [ ] S-curve стадия с доказательствами (≥3 индикатора из s_curve_rubric.md)
- [ ] Base/Bull/Bear сформированы с вероятностями
- [ ] Вероятности обоснованы reference class или pre-mortem (не 50/30/20 по умолч.)
- [ ] Антисистемы/угрозы перечислены
- [ ] Risk Register содержит пороги/триггеры + ранние сигналы
- [ ] Условия успеха (где “точно работает”) выписаны и измеримы
- [ ] Аналоги/прецеденты ≥2: результат + что переносим/не переносим (PoA/ограничения)

## Phase 3 (Value)
- [ ] JTBD/4 Forces/WTP/Friction/Non-consumption оценены
- [ ] Verdict по ценности вынесен (и почему)
- [ ] Plausibility check выполнен для сильных WTP/эконом-утверждений (при необходимости)

## Phase 4 (Solve)
- [ ] TC/PC сформулировано (или явный отказ)
- [ ] Candidates ≥ depth.min, PoA-diversity учтена
- [ ] Top-3 выбраны с разными ветками
- [ ] Есть минимум 1 кандидат по “Протоколу Литвина”
- [ ] Solution–Scenario Matrix заполнена (Top-3 × Base/Bull/Bear)
- [ ] Есть кандидат “нулевой системы” или аргументированный отказ

## Phase 5 (Audit)
- [ ] Risk Register заполнен (Prob/Impact/Signal/Mitigation)
- [ ] Assumptions → Experiments
- [ ] Core-PIZDEJ пройден
- [ ] Confidence откалиброван
- [ ] Ключевые гипотезы/риски имеют маркер + фальсификацию + тест
- [ ] Advocate Pass: 3 контрмеры на диверсию
- [ ] Confidence Decomposition заполнена
- [ ] Raw Score рассчитан; Context-fit Score либо рассчитан по правилам, либо N/A
- [ ] Machine Gate JSON выведен последним блоком отчёта, числа сходятся с разделами выше (см. `phases/phase_5_audit.md` → «Machine Gate»)

## Core Compliance
- [ ] **No Simulation:** Проверка по `_agent_shared/core/validators/gate_check_no_simulation.md`. Агент вызывает инструменты (TRIZ), а не симулирует их работу.
