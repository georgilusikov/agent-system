# TRIZ Domain Profile: Software (IT / Программное обеспечение)

## Mapping: IT-мир → TRIZ

### Substances (S)
| IT-объект | TRIZ-роль |
|---|---|
| Данные, записи, сообщения | **S1 (Изделие)** |
| Сервис, функция, алгоритм | **S2 (Инструмент)** |
| Middleware, кеш, прокси | **S3 (Добавка/Посредник)** |
| Пользователь, оператор | **Надсистема** |

### Fields (F) — IT-аналоги
| MATHEM | IT-аналог |
|---|---|
| Mechanical | Вычислительная нагрузка (CPU/Memory pressure) |
| Acoustic | Логирование, алерты, мониторинг (сигналы) |
| Thermal | Латентность, задержка (тепловая аналогия для bottleneck) |
| Chemical | Трансформация данных (ETL, парсинг, сериализация) |
| Electric | API-вызовы, events, webhooks (потоки данных) |
| Magnetic | Очереди, pub/sub, event bus (управление без прямой связи) |

## Типичные противоречия (ТП)
1. **Performance ↔ Reliability** — скорость vs error handling, retries, HA
2. **Flexibility ↔ Complexity** — extensibility vs cognitive load, maintenance cost
3. **Security ↔ Usability** — auth friction vs user experience
4. **Consistency ↔ Availability** — CAP theorem в распределённых системах
5. **Feature Speed ↔ Technical Debt** — time-to-market vs code quality

## Приоритетные навыки
1. `@contradictions` — IT-проблемы часто сводятся к trade-offs
2. `@functional_analysis` — декомпозиция системы на компоненты + поиск паразитных функций
3. `@trimming` — удаление лишних сервисов/зависимостей
4. `@causal_analysis` — RCA для багов, инцидентов, performance issues
5. `@ikr` — идеальное решение: "система САМ решает проблему без дополнительных ресурсов"

## Ресурсы типичные
- **Вещественные (Data)**: логи, метрики, кеш, БД, конфиг, env variables
- **Энергетические (Compute)**: CPU idle, memory slack, network bandwidth, GPU
- **Информационные**: stack traces, request headers, timestamps, user behavior data
- **Временные**: off-peak hours, batch windows, CI/CD pipeline gaps
- **Пространственные (Architectural)**: edge nodes, CDN, serverless, colocation

## Anti-Patterns (Типичные ошибки)
- ❌ Добавлять новый сервис/зависимость без анализа trimming (свёртывания)
- ❌ Решать performance issues добавлением ресурсов (вместо нахождения root cause)
- ❌ Игнорировать информационные ресурсы (данные, которые УЖЕ есть в системе)
- ❌ Не формулировать ФП (Функциональное Противоречие) — а сразу кидаться в implementation
- ❌ Забывать про ИКР: "Микросервис сам себя мониторит и чинит"

---

## IT/Software-параметры для формулировки противоречий

| # | Параметр | Пример формулировки ТП |
|---|---|---|
| 1 | Latency (задержка) | ↔ Data Consistency |
| 2 | Throughput (пропускная способность) | ↔ Resource Cost |
| 3 | Uptime / Availability | ↔ Deployment Frequency |
| 4 | Developer Velocity | ↔ Code Quality / Tech Debt |
| 5 | Test Coverage | ↔ Build Speed |
| 6 | System Complexity | ↔ Feature Richness |
| 7 | Data Freshness (real-time) | ↔ Infrastructure Cost |
| 8 | Security Hardening | ↔ Developer Experience (DX) |
| 9 | API Surface (extensibility) | ↔ Breaking Change Risk |
| 10 | Observability Depth | ↔ Performance Overhead |
| 11 | Horizontal Scalability | ↔ State Management Complexity |
| 12 | Migration Safety | ↔ Migration Speed |
| 13 | User Privacy | ↔ Personalization Quality |
| 14 | Onboarding Simplicity | ↔ Power-User Capability |
| 15 | Autonomy of Teams | ↔ System-Wide Consistency |
| 16 | Release Frequency | ↔ Stability / Rollback Safety |
| 17 | Caching Aggressiveness | ↔ Data Accuracy |
| 18 | Monorepo Cohesion | ↔ Independent Deployability |
| 19 | AI Model Accuracy | ↔ Inference Latency / Cost |
| 20 | Feature Flag Granularity | ↔ Configuration Complexity |

---

## Линии эволюции IT-систем

### 1. Архитектура
Монолит → SOA (Service-Oriented) → Микросервисы → Serverless / FaaS → AI-агенты (автономные сервисы) → Zero-Code Infrastructure (ИКР: инфраструктура сама себя создаёт)

### 2. Интерфейс пользователя
CLI → GUI (Desktop) → Web UI → Mobile-first → Voice UI (VUI) → Ambient / Zero-UI (система действует без интерфейса, через AI-агента)

### 3. Данные и аналитика
Ручной ввод → SQL/BI (запросы) → Автоматические дашборды → ML-пайплайны → Real-time AI-инференс → Self-improving Data Systems (данные сами улучшают систему)

### 4. Деплой и доставка
Ручной деплой → CI (Continuous Integration) → CD (Continuous Delivery) → GitOps → Progressive Delivery (canary / feature flags) → Self-healing Deployment (система сама откатывает и чинит)

### 5. Тестирование
Ручное QA → Unit-тесты → Integration + E2E → Property-based / Fuzzing → AI-generated Tests → Self-verifying Systems (система сама находит и тестирует гипотезы о багах)

### 6. Безопасность
Периметр (firewall) → Defense-in-depth → Zero Trust → Runtime Protection (RASP) → AI-driven Threat Detection → Self-defending Systems (ИКР: система сама блокирует атаки без человека)

### 7. Модель управления (Control Model)
Ручное управление (скрипты) → Программное (жёсткая логика) → Адаптивное (с датчиками обратной связи) → Предиктивное (Machine Learning) → Самоорганизующееся (ИКР: система сама меняет свои правила)

**Использование:** Определите текущую позицию IT-системы на каждой линии. Прогнозируйте следующий шаг. Если переход блокируется — сформулируйте ТП из таблицы параметров выше и передайте в `@contradictions`.
