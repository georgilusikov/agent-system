# Plan: Customer-facing API v1

## Phase 1: Endpoints

- **Step 1.1.** GET /api/v1/orders — handler с pagination и фильтрами.
- **Step 1.2.** GET /api/v1/orders/{id} — handler с 404-семантикой для чужих/несуществующих.
- **Step 1.3.** POST /api/v1/orders — pydantic-валидация payload.

## Phase 2: Data layer

- **Step 2.1.** Repository методы `list_orders(partner_id, filters, limit, offset)`, `get_order(partner_id, id)`, `create_order(partner_id, payload)`.

## Phase 3: Rate limiting

- **Step 3.1.** Middleware `RateLimiter` — 100 req/min per partner. Backing store — Redis.
- **Step 3.2.** При превышении → 429 с header `Retry-After`.

## Phase 4: Observability

- **Step 4.1.** Structured logging middleware — каждый запрос логируется как JSON с полями `partner_id`, `endpoint`, `status`, `latency_ms`.
- **Step 4.2.** Dashboard в Grafana: requests per partner, error rate, p95 latency.

## Dependencies

- Phase 3 blocked by Phase 1
- Phase 4 blocked by Phase 1
