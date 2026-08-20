# PRD: Customer-facing API v1

## Problem

Партнёры просят программный доступ к ордерам: сейчас они парсят HTML-экспорт. Нам надо выдать официальный REST API.

## User stories

### US-1: List orders
Как партнёр, я хочу получить список своих ордеров через GET /api/v1/orders, чтобы интегрировать в свой ERP.

**Acceptance:**
- GET /api/v1/orders возвращает массив ордеров партнёра
- Поддержка pagination (limit/offset, max limit = 100)
- Фильтры по `status` и `created_after`

### US-2: Get order details
Как партнёр, я хочу получить детали одного ордера через GET /api/v1/orders/{id}.

**Acceptance:**
- Валидный `id` партнёра → 200 с деталями
- Несуществующий `id` → 404
- `id` чужого партнёра → 404 (не раскрываем факт существования)

### US-3: Create order
Как партнёр, я хочу создать ордер через POST /api/v1/orders.

**Acceptance:**
- POST принимает JSON payload, валидирует required поля
- Успех → 201 с `id` созданного ордера
- Невалидный payload → 400 с деталями ошибок

## NFR

- **Security:** Все endpoints требуют JWT auth в header `Authorization: Bearer <token>`. Запрос без токена → 401. Невалидный/expired token → 401. Токен привязан к `partner_id`, данные других партнёров недоступны.
- **Rate limiting:** 100 req/min per partner.
- **Observability:** все запросы логируются с partner_id, endpoint, status, latency.

## Out of scope

- Webhooks (будут в v2)
- Bulk operations
- GraphQL
