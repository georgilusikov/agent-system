# PRD: Reports Dashboard

## Problem

Аналитики тратят 2+ часа в неделю на ручную выгрузку данных из трёх SQL-дашбордов и их сведение в Excel. Хотим дать им одно место, где эти данные собраны и экспортируемы.

## User stories

### US-1: View consolidated dashboard
Как аналитик, я хочу видеть три ключевые метрики (MAU, revenue, churn) на одном экране, чтобы не переключаться между дашбордами.

**Acceptance:**
- Дашборд открывается за < 2 сек на desktop
- Три карточки с числом и spark-line за 30 дней
- Автообновление каждые 5 минут

### US-2: Filter by date range
Как аналитик, я хочу фильтровать метрики по произвольному date range (custom from/to), чтобы смотреть retrospective периоды.

**Acceptance:**
- Date picker с пресетами (7d/30d/90d/custom)
- Метрики пересчитываются на клиенте за < 500ms
- URL отражает выбранный range (shareable link)

### US-3: Export data to CSV
Как аналитик, я хочу экспортировать отфильтрованные данные в CSV, чтобы прикрепить к еженедельному отчёту в Notion.

**Acceptance:**
- Кнопка "Export CSV" рядом с каждой карточкой
- Файл содержит raw-данные за выбранный range, не агрегаты
- Имя файла: `{metric}_{from}_{to}.csv`

## NFR

- **Performance:** p95 latency < 2s
- **Browser support:** Chrome, Firefox, Safari (latest 2 versions)

## Out of scope

- Создание кастомных метрик (только предзаданные 3)
- Отправка отчётов по email/Slack
- Мобильная версия
