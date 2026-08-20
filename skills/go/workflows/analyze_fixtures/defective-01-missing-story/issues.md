# Issues: Reports Dashboard

## DASH-1 — API endpoint /api/metrics
- **Phase:** 1.1
- **Est:** 1 day
- **Blocked by:** —
- **AC:** GET /api/metrics?from=2026-01-01&to=2026-01-31 возвращает JSON с 3 метриками. Невалидный range → 400.

## DASH-2 — Clickhouse aggregation queries
- **Phase:** 1.2
- **Est:** 2 days
- **Blocked by:** DASH-1
- **AC:** Запросы для MAU/revenue/churn выполняются < 500ms на проде-датасете. Redis cache hit rate > 80% при повторных запросах.

## DASH-3 — MetricCard component
- **Phase:** 2.1
- **Est:** 1 day
- **Blocked by:** DASH-1
- **AC:** Карточка рендерит число + spark-line за 30 дней. Storybook story с тремя состояниями (loading/data/error).

## DASH-4 — Dashboard page layout
- **Phase:** 2.1
- **Est:** 0.5 day
- **Blocked by:** DASH-3
- **AC:** `/dashboard` показывает 3 `<MetricCard>` в grid-layout. Responsive на 1440px+.

## DASH-5 — Date picker with URL state
- **Phase:** 2.2
- **Est:** 1 day
- **Blocked by:** DASH-4
- **AC:** Пресеты 7d/30d/90d/custom. URL обновляется при смене range. Shareable link восстанавливает выбор.

## DASH-6 — Auto-refresh every 5 min
- **Phase:** 2.3
- **Est:** 0.5 day
- **Blocked by:** DASH-4
- **AC:** Dashboard автоматически рефетчит данные раз в 5 минут без flash/flicker.

## DASH-7 — Loading skeletons
- **Phase:** 3.1
- **Est:** 0.5 day
- **Blocked by:** DASH-4
- **AC:** Пока данные грузятся, карточки показывают skeleton вместо пустоты.

## DASH-8 — Error boundary
- **Phase:** 3.2
- **Est:** 0.5 day
- **Blocked by:** DASH-4
- **AC:** API падает → показывается "Failed to load, retry" вместо crash всего приложения.

## DASH-9 — Lighthouse performance audit
- **Phase:** 3.3
- **Est:** 1 day
- **Blocked by:** DASH-7, DASH-8
- **AC:** Lighthouse score ≥ 90. p95 load time < 2s в Chrome DevTools throttling 4G.
