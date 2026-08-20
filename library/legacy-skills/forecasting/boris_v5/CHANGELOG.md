# История изменений (Boris v5)

Формат: дата → что изменено → где (путь к файлу) → зачем.

## 2026-01-30

### Режимы прогнозирования (Forecasting Modes)
Добавлена система из 6 режимов прогнозирования, которые определяют фокус анализа:
- **🌀 Эволюционный** — куда система придёт по законам развития (S-curve, ZRTS)
- **⚔️ Конкурентный** — как обойти лидеров рынка (КПЛ, MPV, корреляция)
- **🛡️ Defensive** — что может убить систему (Anti-system, AFD)
- **🎯 Directed** — как привести в желаемое будущее (IKR, Directed Evolution)
- **🔬 Exploratory** — какие варианты будущего возможны (сценарии, РВС)
- **🔥 Full Spectrum** — самый мощный режим, применяет ВСЕ подходы (depth=deep)

Режим определяется в Phase 0 (автоматически или по запросу пользователя) и влияет на все последующие фазы.
Файлы: `core_instructions.md`, `phases/phase_0_lock.md`

### Интеграция metodolog.ru (Boris-focused audit)
Проведён специализированный аудит 130K строк статей с фокусом на прогнозирование. Извлечено 162 находки, 98 из них actionable.

- **Phase 0:** Добавлен "Оператор РВС" (Размер-Время-Стоимость) для выявления пределов развития через экстремумы параметров.
  Файл: `phases/phase_0_lock.md`
- **Phase 1:** Добавлено "Правило 80/20" (скрытые знания) — 80% информации в головах, не документах.
  Файл: `phases/phase_1_scan.md`
- **Phase 1:** Добавлен Anti-pattern "академический прогноз" — веер вариантов вместо одного решения.
  Файл: `phases/phase_1_scan.md`
- **Phase 2:** Добавлен "Метод патентной динамики" для определения стадии S-кривой.
  Файл: `phases/phase_2_reality.md`
- **Phase 2:** Добавлен "Baseline: инерционный прогноз (66%)" — минимальная планка для сравнения.
  Файл: `phases/phase_2_reality.md`
- **Phase 3:** Добавлен "Анализ условий устаревания" — поиск условий, при которых функция станет ненужной.
  Файл: `phases/phase_3_value.md`
- **Phase 3:** Добавлен Anti-pattern "социальный шум" — краудсорсинг без репутационной фильтрации.
  Файл: `phases/phase_3_value.md`
- **Phase 4:** Добавлен "Directed Evolution (DE)" — метод управления развитием системы.
  Файл: `phases/phase_4_solve.md`
- **Phase 4:** Добавлен Anti-pattern "ступор от противоречий".
  Файл: `phases/phase_4_solve.md`

### Интеграция metodolog.ru
- **Phase 1:** Добавлена "Эвристика разнообразия" — приоритет разнообразию источников над авторитетностью при сборе данных для прогноза.
  Файл: `phases/phase_1_scan.md`
- **Phase 2:** Добавлен "Закон мульти-уровня" (Злотин, Зусман) — развитие через использование ресурсов разных уровней одновременно.
  Файл: `phases/phase_2_reality.md`
- **Phase 2:** Добавлен Anti-pattern "кейс CCS" (Минакер) — эксперты часто принимают зрелые технологии (Stage III) за растущие.
  Файл: `phases/phase_2_reality.md`
- **Phase 4:** Добавлен "Критерий приоритизации противоречий" — чем сильнее отрицательная корреляция параметров у лидеров рынка, тем важнее устранить это противоречие.
  Файл: `phases/phase_4_solve.md`

## 2026-01-17

### Канонизация v5
- Создана каноническая папка `_agent_shared/skills/forecasting/boris_v5/` (база v4.1) с обновлёнными метаданными и core-инструкциями.
- Старые версии (v2, v3, v3_2, v4, v4_1) перенесены в `_archive/boris_old_versions/` как исторические.

## 2026-01-09

### Интервью про стимулы и “скрытые провалы”
- Добавлен блок вопросов про KPI/стимулы, “как будут геймить метрику”, требования к прохождению QA/приёмки и редкие режимы, где чаще ломается.
  Файл: `_agent_shared/skills/forecasting/boris_v5/phases/phase_0_lock.md`

### Проверка отдалённых последствий (Кобра‑эффект / “благими намерениями…”)
- Добавлена обязательная проверка 2–3 порядка последствий для Top‑3 решений и ключевых mitigations: вакуум, стимульный откат, перенос/утечка, ловушка процесса.
  Файл: `_agent_shared/skills/forecasting/boris_v5/phases/phase_5_audit.md`
- Добавлен шаблон таблицы (мера → эффекты → реакция акторов → ранние сигналы → контрмеры → эксперимент) и правило: критичные 2–3‑порядковые эффекты должны попадать в Risk Register как отдельные риски.
  Файл: `_agent_shared/skills/forecasting/boris_v5/phases/phase_5_audit.md`

### Шаблон отчёта и принципы
- В шаблон отчёта добавлена строка про “проверку отдалённых последствий (2–3 порядок)”.
  Файл: `_agent_shared/skills/forecasting/boris_v5/templates/report_template.md`
- В core-инструкции добавлен принцип “Отдалённые последствия” как обязательная финальная валидация (ранние сигналы + эксперименты).
  Файл: `_agent_shared/skills/forecasting/boris_v5/core_instructions.md`

### Дальний прогноз (3 оси + enabling technologies + надсистема)
- В Phase 2 добавлена “карта дальнего прогноза” в 3 осях (ZRTS/S‑curve + MPV + рынок/надсистема) и обязательный список enabling technologies; включено в Gate Check для горизонта 10 лет и depth=deep.
  Файл: `_agent_shared/skills/forecasting/boris_v5/phases/phase_2_reality.md`
- В шаблон отчёта добавлен пункт про карту дальнего прогноза.
  Файл: `_agent_shared/skills/forecasting/boris_v5/templates/report_template.md`
- В core-инструкции добавлен принцип “Дальний прогноз” как обязательная часть анализа на 3–10 лет.
  Файл: `_agent_shared/skills/forecasting/boris_v5/core_instructions.md`

### “Чёрный прогноз” как усиление AFD
- В Phase 5 уточнено, что AFD должен учитывать “стелс” (пройти QA/приёмку и проявиться в реальном режиме) и для серьёзных случаев выполняться по узлам/функциям (“разбор по косточкам”).
  Файл: `_agent_shared/skills/forecasting/boris_v5/phases/phase_5_audit.md`

### Протокол Литвина (серые зоны → скачок принципа действия)
- В Phase 4 добавлен протокол: “серая зона” → радикальный trimming → “объект сделай сам” → поле/эффект → мост к ресурсам надсистемы; требование: минимум 1 кандидат должен быть получен этим протоколом.
  Файл: `_agent_shared/skills/forecasting/boris_v5/phases/phase_4_solve.md`
- В шаблон отчёта добавлен пункт про протокол Литвина.
  Файл: `_agent_shared/skills/forecasting/boris_v5/templates/report_template.md`
- В core-инструкции добавлен принцип “Скачок по Литвину”.
  Файл: `_agent_shared/skills/forecasting/boris_v5/core_instructions.md`

### Качество без усложнения (маркеры/пороги/проверки)
- В core-инструкции добавлены принципы “Дисциплина маркеров” и “Дисциплина порогов” для ключевых выводов и рисков.
  Файл: `_agent_shared/skills/forecasting/boris_v5/core_instructions.md`
- В Phase 2 Risk Register добавлен столбец “Порог/триггер”, а также быстрый plausibility check для сильных утверждений.
  Файл: `_agent_shared/skills/forecasting/boris_v5/phases/phase_2_reality.md`
- В Phase 3 добавлен plausibility check для WTP/экономики.
  Файл: `_agent_shared/skills/forecasting/boris_v5/phases/phase_3_value.md`
- В Phase 5 уточнено: для [ASSUME] нужен маркер + фальсификация; для рисков обязателен порог/триггер; remote consequences запускается по триггеру (стимулы/правила).
  Файл: `_agent_shared/skills/forecasting/boris_v5/phases/phase_5_audit.md`
- Gate checks дополнены требованиями по порогам/маркерам/plausibility.
  Файл: `_agent_shared/skills/forecasting/boris_v5/validation/gate_checks.md`

### Триггеры глубины (чтобы не раздувать всегда)
- Добавлены триггеры повышения глубины (safety/legal, rare‑but‑severe, high cost, смена кривой, data‑poor+strong claims) и правило “иначе можно quick с честным cap”.
  Файл: `_agent_shared/skills/forecasting/boris_v5/core_instructions.md`

### Quick Kill + Executive Summary + Raw/Context-fit Score
- Добавлен `Quick Kill` (ранний STOP + Pivot Option) на старте Phase 0 и после карты системы в Phase 1.
  Файлы: `_agent_shared/skills/forecasting/boris_v5/phases/phase_0_lock.md`, `_agent_shared/skills/forecasting/boris_v5/phases/phase_1_scan.md`
- Введены правила для `Raw Score` и `Context-fit Score` (и когда второй запрещён), а также уточнён Verdict.
  Файл: `_agent_shared/skills/forecasting/boris_v5/phases/phase_5_audit.md`
- Шаблон отчёта переведён на русский и усилен “итоговой карточкой на 1 экран”.
  Файл: `_agent_shared/skills/forecasting/boris_v5/templates/report_template.md`
- Гейт‑чеки расширены под новые обязательные секции (Quick Kill, Success Conditions, матрица решений, Advocate Pass, декомпозиция уверенности).
  Файл: `_agent_shared/skills/forecasting/boris_v5/validation/gate_checks.md`
- Обновлён статус задач бэклога под фактически внедрённые изменения.
  Файл: `_agent_shared/skills/forecasting/boris_v5/BACKLOG.md`
