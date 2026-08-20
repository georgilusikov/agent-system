# Issues: Customer-facing API v1

## API-1 — GET /api/v1/orders endpoint
- **Phase:** 1.1
- **Est:** 1 day
- **Blocked by:** API-4
- **AC:** GET возвращает массив ордеров партнёра. Pagination через `limit` (max 100) и `offset`. Фильтры `status`, `created_after`. Валидные фильтры — 200, невалидные — 400.

## API-2 — GET /api/v1/orders/{id} endpoint
- **Phase:** 1.2
- **Est:** 0.5 day
- **Blocked by:** API-4
- **AC:** Валидный id партнёра → 200. Несуществующий или чужой → 404 (без различия).

## API-3 — POST /api/v1/orders endpoint
- **Phase:** 1.3
- **Est:** 1 day
- **Blocked by:** API-4
- **AC:** Валидный JSON payload → 201 с id. Отсутствие required полей → 400 с детализацией.

## API-4 — Repository layer
- **Phase:** 2.1
- **Est:** 1.5 days
- **Blocked by:** —
- **AC:** `list_orders`, `get_order`, `create_order` методы. Все фильтруют по partner_id на уровне SQL.

## API-5 — RateLimiter middleware
- **Phase:** 3.1
- **Est:** 1 day
- **Blocked by:** API-1, API-2, API-3
- **AC:** Middleware трекает req/min per partner в Redis. При превышении 100 req/min → 429 с `Retry-After: 60`.

## API-6 — Structured logging middleware
- **Phase:** 4.1
- **Est:** 0.5 day
- **Blocked by:** API-1, API-2, API-3
- **AC:** Каждый запрос пишется в JSON-лог с `partner_id`, `endpoint`, `status`, `latency_ms`.

## API-7 — Grafana dashboard
- **Phase:** 4.2
- **Est:** 0.5 day
- **Blocked by:** API-6
- **AC:** Dashboard показывает requests per partner, error rate per endpoint, p95 latency. Sprint-level alerts на error rate > 5%.
