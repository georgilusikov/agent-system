---
name: triz
description: 'Router for the owner TRIZ toolkit: picks one framework or chain and loads only its canon body (progressive disclosure). Triggers: «упрости систему», «сократи детали», «убери лишние стадии», «противоречие в требованиях», «идеальный конечный результат», «функциональный анализ», «ФСА», "trimming", «тримминг», «триминг», «тримминг триза», "АРИЗ", "ТРИЗ", "ИКР", «как ИКР», "S-curve". NOT for: ранжирование готового списка задач или гипотез (/prioritize); поиск горлышка без противоречия (/leverage); RCA конкретного падения или трейсбека (/debug); внешний аудит готовой работы (/bouncer).'
---

# TRIZ — один вход в ТРИЗ-инструментарий

Это **роутер**, а не метод. Тел фреймворков здесь НЕТ: роутер выбирает инструмент
или цепочку и заставляет прочитать её канон-файл перед работой.

**Канон-корень (`<T>` ниже):** resolve this file's repository root, then use
`library/legacy-skills/triz/`.

Полный список (62 SKILL.md) — `_agent_shared/SKILLS_INDEX.md` §1 TRIZ.
Готовые маршруты с гейтами (карты А–Н) — `<T>/master_triz_orchestrator_v5/skeleton_maps.md`.

## Протокол роутинга

1. **Класс задачи.** Определи по симптому владельца, а не по названию метода.
2. **Выбор.** Один фреймворк из карты ИЛИ одна цепочка. Не бери два «на всякий случай».
3. **Чтение.** Прочитай `<T>/<skill>/SKILL.md` ЦЕЛИКОМ (у каждого свой Gate Check).
4. **Работа** строго по прочитанному телу — его шагами и его терминами.
5. **Результат** в формате того фреймворка (его Output + Gate Check), не в вольном.
6. Задача расплывчатая («что-то не так», много симптомов) → сначала цепочка C8,
   либо суб-роутер `<T>/problem_discovery/SKILL.md` (6 сценариев S1–S6).

## Карта фреймворков

| Фреймворк | Когда | Файл (`<T>/…`) |
|---|---|---|
| `socratic` | задача расплывчата, нужны уточняющие вопросы до анализа | `socratic/SKILL.md` |
| `problem_map` | клубок симптомов → компактная карта до постановки | `problem_map/SKILL.md` |
| `problem_formulator` | из описания в ТП-1/ТП-2 (АРИЗ-85В ч.1) | `problem_formulator/SKILL.md` |
| `problem_discovery` | суб-роутер: 6 сценариев поиска проблемы | `problem_discovery/SKILL.md` |
| `kt_is_is_not` | «раньше работало, теперь нет» — локализация отклонения | `kt_is_is_not/SKILL.md` |
| `causal_analysis` | RCA+: причинно-следственные цепочки нежелательного эффекта | `causal_analysis/SKILL.md` |
| `triz_troubleshooter` | странное поведение, парадокс, «не как ожидалось» | `triz_troubleshooter/SKILL.md` |
| `functional_analysis` | модель системы: полезные/вредные/паразитные функции | `functional_analysis/SKILL.md` |
| `value_analysis` | ФСА: дорогие узлы с низкой ценностью («золотые унитазы») | `value_analysis/SKILL.md` |
| `akts` | MPV: за что реально платит клиент, скрытые стейкхолдеры, рудименты | `akts/SKILL.md` |
| `flow_analysis` | потоки В/Э/И, узкие места, КПД, утечки | `flow_analysis/SKILL.md` |
| `informational_flow_analysis` | инфопотоки, seq→parallel (Демукрон) | `informational_flow_analysis/SKILL.md` |
| `structural_analysis` | топология связей, жёсткие сцепки | `structural_analysis/SKILL.md` |
| `causal_loop_diagram` | проблема возвращается: петли, задержки, policy resistance | `causal_loop_diagram/SKILL.md` |
| `diversion_analysis` | pre-mortem: как это сломать намеренно | `diversion_analysis/SKILL.md` |
| `afd_failure_predictor` | скрытые/отложенные дефекты (Певзнер) | `afd_failure_predictor/SKILL.md` |
| `stpa_analysis` | контуры управления, небезопасные управляющие действия | `stpa_analysis/SKILL.md` |
| `contradictions` | конфликт требований, компромисс — ТП и ФП | `contradictions/SKILL.md` |
| `forty_principles` | разрешение ТП по матрице 39×39 + 40 приёмов | `forty_principles/SKILL.md` |
| `arip` | быстрый АРИЗ для простого ТП | `arip/SKILL.md` |
| `ariz` | тяжёлая задача: АРИЗ-85В, 9 частей, ОЗ/ОВ, ВПР, ФП | `ariz/SKILL.md` |
| `vepoli` | вещество-поле, МАТХЭМ | `vepoli/SKILL.md` |
| `standards` | 76 стандартов на решение (после веполя) | `standards/SKILL.md` |
| `trimming` | свёртывание: убрать компонент/стадию, сохранив функцию | `trimming/SKILL.md` |
| `ikr` | ИКР: «X САМО…», прорыв вместо оптимизации | `ikr/SKILL.md` |
| `resource_analysis` | ВПР: скрытые ресурсы для «бесплатного» решения | `resource_analysis/SKILL.md` |
| `effects` | нужен физический/химический/геометрический механизм | `effects/SKILL.md` |
| `fos` / `benchmarking` | функционально-ориентированный поиск, аналоги, best-in-class | `fos/SKILL.md`, `benchmarking/SKILL.md` |
| `oas_transfer` | перенос свойств, гибридизация систем | `oas_transfer/SKILL.md` |
| `microstandards` | lookup готового паттерна решения | `microstandards/SKILL.md` |
| `s_curve` | стадия зрелости системы | `s_curve/SKILL.md` |
| `limits_strategy` | количественный предел развития, остаточный резерв | `limits_strategy/SKILL.md` |
| `zrts` | законы развития ТС, моно-би-поли | `zrts/SKILL.md` |
| `system_operator` | 9 экранов: над/под-система × прошлое/настоящее/будущее | `system_operator/SKILL.md` |
| `dynamization` | сделать жёсткое гибким/адаптивным | `dynamization/SKILL.md` |
| `morphological_analysis` | систематический перебор конфигураций | `morphological_analysis/SKILL.md` |
| `rtv` (+`mmch`,`goldfish`,`robinson`,`rvs`,`inversion`,`dnd`) | застрял, нужен снос психбарьера | `rtv/SKILL.md` |
| `experiment_designer` | дешёвый falsifier-тест концепции | `experiment_designer/SKILL.md` |
| `critic` / `reflection_gate` | адвокат дьявола / self-check перед выдачей | `critic/SKILL.md`, `reflection_gate/SKILL.md` |
| `case_logger` | прецеденты (1416 YAML кейсов) | `case_logger/SKILL.md` |
| `final_triz_report` | собрать итоговый отчёт для владельца | `final_triz_report/SKILL.md` |
| `master_triz_orchestrator_v5` | нужен полный конвейер с гейтами и валидаторами | `master_triz_orchestrator_v5/SKILL.md` |

## Цепочки (дорожная карта эффективности)

Вход-симптом → шаги. Каждый шаг = прочитать тело и отработать его Gate Check.

- **C1. «Дорого / лишние детали»** → `functional_analysis` → `value_analysis` → `trimming`;
  свёртывание породило конфликт → `contradictions` → `forty_principles`. *(карта Б)*
- **C2. «Упрости систему / убери стадии»** → `functional_analysis` → `trimming`;
  функция осталась без носителя → `resource_analysis` (кто ещё может её нести).
- **C3. «Противоречие в требованиях»** → `contradictions` → `forty_principles`;
  приёмы не сняли ФП → `ariz` (или `arip` для простого ТП).
- **C4. «Сломалось, раньше работало»** → `kt_is_is_not` → `causal_analysis`;
  причина парадоксальна → `triz_troubleshooter`. *(S2 / карта А)*
- **C5. «Как может сломаться» (проактивно)** → `diversion_analysis` → `afd_failure_predictor`;
  есть контур управления (контроллер/сенсор/интерлок) → `stpa_analysis`. *(S3)*
- **C6. «Медленно / низкий КПД / bottleneck»** → `functional_analysis` → `flow_analysis`;
  проблема возвращается после локальных фиксов → `causal_loop_diagram`. *(S4)*
- **C7. «Стоит ли развивать / устарело»** → `s_curve` → `limits_strategy` → `system_operator`;
  нужен прогноз следующего шага → `zrts`. *(S5)*
- **C8. «Непонятно что решать»** → `socratic` → `problem_map` → `problem_formulator`
  → дальше в C1–C7 по получившейся постановке. *(S1)*
- **C9. «Нужен идеал, а не оптимизация»** → `ikr` → `resource_analysis` → `trimming`.
- **C10. «Вредное взаимодействие / нужен механизм»** → `vepoli` → `standards`;
  стандарт требует физики → `effects`.
- **C11. «Своего решения нет, ищем чужое»** → `benchmarking` → `fos` → `oas_transfer`.

Любая цепочка перед выдачей владельцу: `critic` → при необходимости `final_triz_report`.

## Известные грабли

- **Канон живёт в workspace «курсор».** Путь `<T>` не существует (другая машина,
  переезд, снятый worktree) → честно сказать: «канон ТРИЗ не найден по пути `<T>`»
  и остановиться. **Не реконструировать фреймворк по памяти** — тела скиллов
  содержат матрицы, 76 стандартов, правила A–F и Gate Check, которых в голове нет.
- `master_triz_orchestrator` (без `_v5`) — archive/legacy, битые ссылки. Брать v5.
- Аудит `_agent_shared/TRIZ_SKILLS_MASTER_AUDIT.md` (2026-01) помечает часть скиллов
  как слабые (`avf`, `causal_analysis`, `benchmarking`) и указывает пути к устаревшим
  копиям в `projects/elena_triz/` — эти пути мертвы, канон только `<T>`.
- Триггеры скиллов пересекаются (`ФП` есть и у `contradictions`, и у `ariz`) —
  выбор делает роутер по классу задачи, а не по совпадению слова.

## DoD

1. Назван класс задачи и выбранный фреймворк/цепочка (с номером C-N).
2. Перечислены **прочитанные** файлы (абсолютные пути).
3. Выход в формате фреймворка + его Gate Check пройден построчно.
4. Названо, что осталось непроверенным.

## FORBIDDEN

- Работать по фреймворку, не прочитав его тело.
- Пересказывать ТРИЗ из общей памяти модели вместо канон-файла.
- Смешивать два фреймворка в один «улучшенный» — берётся один, целиком.
- Подменять Gate Check фреймворка своим суждением «и так нормально».
- Чинить/дописывать канон-файлы в `_agent_shared/` из этого скилла.

## Hard fail

- Файл фреймворка не прочитан, а результат выдан → результат невалиден, переделать.
- Путь `<T>` не существует, а фреймворк «применён» → выдумка, стоп и доклад владельцу.
- Gate Check выбранного фреймворка не пройден, но выдан вывод → невалидно.
