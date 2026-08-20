# Шаблон отчёта Boris v5

> Принцип: отчёт на русском, без жаргона. Любой важный вывод должен иметь **маркер/порог** и **как проверить** (эксперимент/данные).

## 🧾 Итоговая карточка (1 экран)

| Идея / SUA | Вердикт (GO/CAUTION/STOP) | Raw Score /100 | Context-fit Score /100 | Confidence | Robustness |
|---|---:|---:|---:|---:|---:|
|  |  |  |  |  |  |

- **Главный риск (1 предложение):** …
- **Главная ставка/решение (1 предложение):** …
- **Следующий шаг (1 эксперимент, 1 метрика, 1 срок):** …

> `Context-fit Score` разрешён только если выписаны **Условия успеха** и есть хотя бы 1 быстрый эксперимент/план проверки этих условий. Иначе ставьте `N/A`.

## 🧩 Фаза 0 — Фиксация системы (Lock)
- SUA / Boundary / KPI / Stakeholders
- PoA-цепочка: Input → Mechanism → Output → Effect → KPI Event
- IKR ladder: User / Payer / Blocker(Regulator)
- Constraints: время/деньги/регуляция/данные; Bio/Safety фильтр
- Quick Kill (если применимо): STOP + Pivot Option

## 🗺️ Фаза 1 — Скан системы (System Map)
- Расширенный 9-экран System Operator: надсистемы (≥N), система (прошлое/настоящее/IKR), подсистемы (≥N) — всё с Evidence
- Resources / Harmful functions / Main constraint (лимит/предел)
- Drift/Constraints check
- Quick Kill Gate (если лимит делает проект невозможным)
- Reasoning Trace (OBS/DERIVE/DECISION)

## 🌍 Фаза 2 — Реальность и прогноз
- S-curve: стадия с обоснованием (≥3 [OBS/DATA]); если данных мало — [ASSUME] + тест
- Карта дальнего прогноза: 3 оси (ZRTS/S-curve + MPV + рынок/надсистема) + enabling technologies
- Base / Bull / Bear: вероятности (сумма 100%), триггеры, ранние сигналы, KPI-диапазоны
- Условия успеха (Success Conditions): где **точно** сработает (канал/аудитория/режимы/метрики)
- Где сломается: где **не** сработает и почему (лимит/контекст/регуляция)
- Маршруты “переезда” (канал/PoA/аудитория/рынок): 2–3 маршрута
- Альтернативная кривая: таблица (PoA/канал/рынок, ограничения, риск, триггер переключения)
- Аналоги/прецеденты: минимум 2 (успех/провал/pivot) + что берём/не берём и почему (в терминах PoA/ограничений)
- Reasoning Trace

## 🎯 Фаза 3 — Ценность (Value)
- JTBD / 4 Forces / WTP proxies / Friction / Non-consumption
- Вердикт по ценности: есть ли ценность (да/нет/низкая уверенность) + почему
- Reasoning Trace

## 🧠 Фаза 4 — Решения и альтернативы
- Root blockade / TC / PC (или обоснованный отказ)
- Candidates (≥5/8/10 по глубине) с PoA-diversity
- Протокол Литвина: “серая зона” → радикальный trimming → “объект сделай сам” → поле/эффект → мост к надсистеме (минимум 1 кандидат)
- Top-3: ICE + ветка PoA
- Если Top-3 не срабатывают: корень провала, альтернативный путь (перенос функции/смена PoA/рынка), авто-handoff (limits/contradictions/benchmarking/effects/vepoli)
- Матрица “Решение × Сценарий”: Top-3 vs Base/Bull/Bear (✅/⚠️/❌)
- Reasoning Trace

## 🛡️ Фаза 5 — Аудит, риски, эксперименты
- Risk Register (Risk, Source, Prob, Impact, Порог/триггер, Early Signal, Mitigation, Protection Level)
- Assumptions → Experiments (у каждого [ASSUME]/[SPEC]: маркер + фальсификация + тест)
- Продуктовая петля: как эксперименты меняют Confidence/Score и разблокируют Bear/переезд
- Проверка отдалённых последствий (2–3 порядок): вакуум/стимулы/перенос/ловушка процесса + ранние сигналы + эксперименты
- Advocate Pass: 3 контрмеры на диверсию + 7 уровней защиты
- Raw Score / Context-fit Score (правила и расчёт)
- Pivot Cascade (если есть Pivot): мини-анализ нового SUA (Lock + S-curve + Base/Bull/Bear) + сравнение с исходным
- Core-PIZDEJ self-check summary
- Confidence Decomposition + итоговый Confidence/Robustness

## 📌 Рекомендации / Следующие шаги
- Эксперименты / Владельцы / Сроки / Метрики
- Быстрые победы vs ставки “в глубину”
