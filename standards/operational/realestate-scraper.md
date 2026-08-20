---
name: realestate-scraper
description: Методология скрапинга недвижимости (realt, kufar, onliner, domovita). Покрывает URL collection с валидацией формата, rate limiting через Chrome MCP, cross-source dedup через BallTree, freshness фильтрацию, source priority, ML predictions с указанием источника.
version: 0.0.1
created: 2026-04-19
incident_trigger: Compile-trigger — 5 правил по теме realestate scraping накопилось в ~/.claude/rules/ (data-freshness, scraper-urls, realestate-dedup, chrome-mcp-batching, feature-consistency). Без единого стандарта — каждый скрапер собирается с нуля, типичные ошибки повторяются. Решение — единая методология для всех источников.
---

# Realestate Scraper Standard v0.0.1

## Job-to-be-done сценарии

Когда применять этот стандарт:

- **JTBD-1: Скрапинг новых объявлений с realt / kufar / onliner / domovita** — собрать свежие listings, без потерь, с правильным URL форматом
- **JTBD-2: Cross-source dedup** — есть таблица из нескольких источников, надо схлопнуть дубли по координатам/комнатам/площади
- **JTBD-3: Показ актуальных данных пользователю** — выборка из БД для ответа («топ объявлений», «найди X»), без stale data
- **JTBD-4: ML prediction для одной квартиры из разных источников** — объяснить почему числа разные, не подавать как факт
- **JTBD-5: Массовая загрузка через Chrome MCP** — открыть N quartal в браузере без раздувания контекста и rate-limit-ов

## Точка G (output critria)

После применения стандарта:

- [ ] Все URL в БД имеют верифицированный финальный формат (после редиректа), не "сохранили дефолт")
- [ ] Cross-source dedup применён, дубликаты сокращены ≥80% (haversine + rooms + area)
- [ ] Все показанные пользователю listings имеют `scraped_at` ≤ 48 часов
- [ ] Активные ссылки прошли HTTP-проверку (200, не 404/архив) перед публикацией
- [ ] Chrome MCP batching не превысил 5-10 параллельных tabs (kufar 3-5)
- [ ] ML predictions залогированы с `source` и `feature_completeness`
- [ ] Source priority применён при keep="first": `kufar > realt > domovita > onliner`

## Методология

### §1. URL collection с валидацией формата (ОБЯЗАТЕЛЬНО ДО массового сохранения)

**Перед `INSERT INTO listings url=...` или `df['url'] = template.format(...)`:**

```python
import requests

# 1. Сформируй ОДИН URL по предполагаемому шаблону
test_url = template.format(object_id=12345)
print(f"Will save: {test_url}")

# 2. Проверь финальный URL после редиректа
response = requests.head(test_url, allow_redirects=True, timeout=10)
final_url = response.url
print(f"Final after redirect: {final_url}")

# 3. Если final_url ≠ test_url — используй final формат для всех INSERT
if final_url != test_url:
    print("⚠️ Format mismatch! Adjust template before mass save.")
```

**Известные подводные камни:**
- `realt.by/sale/flats/object/12345/` (со слешем) → редирект на каталог. **Правильно:** `realt.by/sale-flats/object/12345/` (с дефисом)
- kufar: проверь финальный canonical URL (есть утм-метки, regional redirects)

Чек-лист:
- [ ] Один тестовый URL открыт и проверен в реальном браузере (не только requests)
- [ ] Финальный URL после редиректа использован в шаблоне
- [ ] HTTP-статус для test_url = 200 (не 301/302/404)

### §2. Chrome MCP rate limiting + batching

**Запрет:** не вызывай больше **5-10 параллельных** Chrome tab операций в одном сообщении.

| Источник | Max параллельных | Pause между батчами |
|---|---|---|
| kufar | **3-5** (rate-limit чувствителен!) | 5-10 секунд |
| realt | 5-10 | минимально |
| onliner | 5-7 | минимально |
| domovita | 5-7 | минимально |

**Workflow для 20 URL на kufar:**
```
Batch 1: tabs_create_mcp × 4 параллельно
↓ wait 10s
Batch 2: tabs_create_mcp × 4 параллельно
↓ wait 10s
... etc
```

Между батчами — короткий `tabs_context` для проверки прогресса. Не делай `tabs_context` в каждом батче — он возвращает full context (большой JSON со всеми вкладками).

**Симптом нарушения:** kufar возвращает «Доступ ограничен» / 429 на части вкладок. Если видишь — снижай batch size до 3.

### §3. Cross-source dedup (haversine + rooms + area)

Простой `drop_duplicates(subset=['address'])` **НЕ работает** — адреса транслитерируются по-разному:
- `"ulica nikoly tesly"` (kufar) vs `"Минск Николы Теслы ул."` (realt) — это одна квартира

Координаты от Yandex/Google geocoder совпадают до 4-5 знака. Используй BallTree с haversine:

```python
from sklearn.neighbors import BallTree
import numpy as np
import pandas as pd

# 1. Coordinates в радианах
coords = np.radians(df[['latitude', 'longitude']].values)

# 2. Build BallTree
tree = BallTree(coords, metric='haversine')

# 3. Query: радиус 50 метров = 50 / 6_371_000 радиан
EARTH_RADIUS_M = 6_371_000
RADIUS_M = 50
radius_rad = RADIUS_M / EARTH_RADIUS_M

# 4. For each row find neighbors
duplicates_groups = []
seen = set()
for i, row in df.iterrows():
    if i in seen:
        continue
    indices = tree.query_radius(coords[i:i+1], r=radius_rad)[0]
    # Filter: same rooms + area_total within ±2 m²
    same_listing = [
        j for j in indices
        if df.loc[j, 'rooms'] == row['rooms']
        and abs(df.loc[j, 'area_total'] - row['area_total']) <= 2
    ]
    if len(same_listing) > 1:
        duplicates_groups.append(same_listing)
        seen.update(same_listing)

# 5. Apply source priority при keep="first"
SOURCE_PRIORITY = {'kufar': 0, 'realt': 1, 'domovita': 2, 'onliner': 3}
df['source_priority'] = df['source'].map(SOURCE_PRIORITY)
df = df.sort_values('source_priority').drop_duplicates(
    subset=['lat_rounded', 'lon_rounded', 'rooms', 'area_total_rounded'],
    keep='first'
)
```

**Source priority** обоснован полнотой схемы:
1. **kufar** — самые богатые фичи (ремонт, описание, контакт, фото)
2. **realt** — официальный, но беднее по features
3. **domovita** — средне
4. **onliner** — самая бедная схема

### §4. Freshness filtering (перед показом пользователю)

```python
from datetime import datetime, timedelta, timezone

CUTOFF = datetime.now(timezone.utc) - timedelta(hours=48)
fresh_listings = df[df['scraped_at'] >= CUTOFF]
```

**Триггеры для применения:** запрос содержит «realt», «kufar», «найди X в БД», «топ объявлений», любой scraper-related.

### §5. Link verification перед публикацией

Если показываешь пользователю URLs (Telegram бот, отчёт, чат):

```python
import requests

def verify_url(url: str) -> tuple[bool, int]:
    try:
        r = requests.head(url, allow_redirects=True, timeout=5)
        # 200 = active, 404/410 = removed, 301/302 → check final
        if r.status_code == 200:
            # Дополнительно: финальный URL не редиректит на каталог
            if any(part in r.url for part in ['/object/', '/listing/', '/ad/']):
                return True, 200
            return False, r.status_code  # редирект на каталог = убран
        return False, r.status_code
    except requests.RequestException:
        return False, 0  # network error

# Применяй перед публикацией
df['url_active'] = df['url'].apply(lambda u: verify_url(u)[0])
publish_df = df[df['url_active']]
```

### §6. ML predictions с указанием источника

Запрет: подавать prediction для одной квартиры из разных источников как факт. Это **диагностика модели**, не результат.

```python
# ✅ Правильно: лог feature_completeness и source
prediction_log = {
    'listing_id': 'apt-001',
    'source': 'kufar',
    'predicted_price': 650,
    'feature_completeness': 0.95,  # 19/20 полей заполнены
    'features_used': ['area', 'rooms', 'floor', 'renovation', ...],
    'features_missing': [],
}

# ❌ Неправильно: одна цена без контекста
predicted_price = 650  # из какого источника? с каким набором фичей?
```

**Объяснение пользователю при divergence:**
> Якуба Коласа 43-2: $650/мес из kufar (включает «Дизайнерский ремонт»), $461/мес из realt (без поля «ремонт»). Разница 41% объясняется feature gap, не качеством модели.

## Когнитивные искажения агента в этой области

### Stale data illusion
**Симптом:** Показ объявлений из БД без проверки `scraped_at`. Пользователь видит цену — звонит — объявление снято месяц назад.
**Защита:** ВСЕГДА фильтр `scraped_at ≤ 48h` перед показом. Триггер — просто слова «найди / покажи / топ».

### URL format assumption
**Симптом:** Сохранил URL по шаблону без проверки. Все ссылки редиректят на каталог. Никто не замечает пока не открывает.
**Защита:** §1 — открыть 1 пример в браузере ДО массового INSERT.

### Address dedup illusion
**Симптом:** `df.drop_duplicates(subset=['address'])` → дубли остались (адреса разные транслитерации).
**Защита:** §3 — BallTree haversine + rooms + area. Адрес — никогда не source of truth для dedup.

### Chrome batching greed
**Симптом:** «открою сразу 20 URL для скорости» → раздут контекст + kufar даёт 429 → теряются 60% вкладок.
**Защита:** §2 — kufar 3-5, realt 5-10. Между батчами короткий tabs_context.

### Source-blind ML predictions
**Симптом:** «Модель сказала $650» — без указания что из kufar и с features X. Пользователь думает это truth.
**Защита:** §6 — каждый prediction с source + feature_completeness в лог.

### Survivor URL bias
**Симптом:** Показал 10 ссылок пользователю, не проверил какие активные. 4 из 10 — 404 / архив.
**Защита:** §5 — verify HTTP перед публикацией.

## Связанные скиллы

- `/check` — для §1 (verify URL format) и §5 (verify publish-ready URLs)
- `/why` — если dedup даёт неожиданные результаты (например удалил оригиналы)
- `/anti-bias` — для preprocessing ML predictions (camera test на «$650 это факт?»)
- `/falsify` — перед публикацией большого dataset для пользователя

## Changelog

- **0.0.1** (2026-04-19) — начальная версия. Compile из 5 rules: data-freshness, scraper-urls, realestate-dedup, chrome-mcp-batching, feature-consistency.

## FORBIDDEN в этой области

- Mass `INSERT` URLs без §1 теста на 1 примере (URL format mismatch)
- `df.drop_duplicates(subset=['address'])` для cross-source (адреса транслитерируются по-разному)
- Показ listings пользователю без §4 freshness filter (`scraped_at ≤ 48h`)
- `tabs_create_mcp` × 18 параллельно для kufar (rate-limit, потеря данных)
- ML prediction без поля `source` в логе
- Публикация ссылок без §5 HTTP verification

## Hard fail

- §1 pre-check URL format пропущен → массовый INSERT с broken URLs
- §3 cross-source dedup без haversine (только address) → 30%+ дубликатов остаётся
- §4 freshness filter не применён перед публикацией → пользователь видит снятые объявления
- ML predictions без source field → пользователь принимает за факт что является диагностикой модели
