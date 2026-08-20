---
skill_id: estimate_calibration
skill_name: Estimate Calibration (ETA / effort)
version: 1.0.0
category: forecasting
triggers:
  - "сколько займёт"
  - "оцени время"
  - "ETA"
  - "успеем ли"
  - "estimate"
  - "оцени сложность"
dependencies: []
description: "Calibrated ETA/effort estimation before announcing. Three anchors: wall-clock measurement on 1-2 real samples, reference class (similar past cases with recorded facts), decomposition into components with named bottleneck. Output MUST include: sample measurement (or explicit reason it is impossible), 1-3 reference cases, decomposition, P50/P90 interval instead of point estimate. NOT for: ranking a list (use ISRICE); probability of a cause hypothesis (use dev/triage)."
---

# Estimate Calibration — калиброванная оценка ETA/effort

Оценка из головы врёт в 2-5×: «2-4 часа» оборачивались ~10ч (5 мин/кейс × 116).
Три опоры вместо интуиции: замер, reference class, декомпозиция. Анонс — интервалом.

## Когда НЕ применять

- Задача < 15 минут → просто делай
- Что делать первым → ISRICE-приоритизация
- Вероятность причины → `dev/triage`

## §1. Expected State

Что значит «готово» (артефакт + проверка). Оценка без критерия готовности занижена —
забываются верификация, фиксы, повторные прогоны.

## §2. Замер на реальных сэмплах (главная опора)

Прогони 1-2 РЕАЛЬНЫХ единицы работы, замерь wall-clock. `ETA = t × N × overhead`.
- Сэмпл из реальных данных, не синтетика (синтетика быстрее и проще реальности)
- overhead ≥ 1.3 (ретраи, rate limits, flaky, паузы)
- Замер невозможен → явно почему + расширенный интервал в §5

## §3. Reference class

1-3 похожих ПРОШЛЫХ кейса с фактической длительностью: memory/incidents, git log
(даты коммитов волны), записи прошлых сессий. «Сколько заняло похожее в прошлый раз»,
не «сколько по ощущению». Память агрегирует и приукрашает — ищи записанные факты.

## §4. Декомпозиция

Слагаемые: подготовка + N×единица + верификация + фиксы (обычно 20-40% от основного).
Назови узкое место — оно определяет P90. Одно число без слагаемых = шум.

## §5. Интервал и анонс

**P50 и P90**, не точка. P90/P50 > 3 → скажи прямо «оценка ненадёжна, сузит только
замер». Для unattended run — чекпойнт: «через X минут проверю первые M результатов».

## Известные грабли

- ETA из головы для долгого прогона → пользователь ловит сюрприз посреди прогона
- Синтетический сэмпл проходит быстро там, где реальный контент в разы дольше
- Забытая верификация: оценил основную работу, забыл verify+фиксы
- «Слишком сложно» без 15 минут попытки

## FORBIDDEN

- ETA точкой без интервала
- Прогон > 30 мин без замера на реальном сэмпле
- Выдуманные замеры/reference-кейсы — нет данных = честный широкий интервал
- overhead = 1.0

## Hard fail

- Нет ни замера, ни reference class, ни декомпозиции → настроение, не оценка
- P50 без P90 → output невалиден
- Замер был возможен, но пропущен → оценка невалидна by design
