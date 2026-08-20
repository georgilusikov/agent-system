# Plan: Reports Dashboard

## Phase 1: Data layer

- **Step 1.1.** Создать `/api/metrics?from=&to=` endpoint. Параметры валидируются pydantic-моделью.
- **Step 1.2.** Агрегирующие запросы в Clickhouse для MAU, revenue, churn. Кэш в Redis, TTL 5 мин.

## Phase 2: UI

- **Step 2.1.** React-страница `/dashboard`. Три карточки через `<MetricCard>` компонент с spark-line (библиотека `recharts`).
- **Step 2.2.** Date picker с пресетами 7d/30d/90d/custom. Состояние в URL через query params.
- **Step 2.3.** Автообновление через `useQuery` с `refetchInterval: 5 * 60 * 1000`.

## Phase 3: Polish

- **Step 3.1.** Loading skeletons для карточек.
- **Step 3.2.** Error boundary с retry.
- **Step 3.3.** Lighthouse audit для p95 < 2s.

## Dependencies

- Phase 2 blocked by Phase 1 (API должен быть готов)
- Phase 3 blocked by Phase 2
