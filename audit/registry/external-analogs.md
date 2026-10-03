# Внешние аналоги AI-скиллов

Дата: 2026-10-01. Метод: 12 воркеров (по одному на тип), web-поиск + открытие страниц репозиториев; лицензии и живость сверены по метаданным/GitHub API, не из памяти. Репозиторий `~/workspace/audit-skillov/repo` — только чтение. Детали по типам — в `analogs/chunk-*.md`.

Правила: README аналога — гипотеза для эвала, не доказательство превосходства; если аналога нет — так и зафиксировано; лицензии «не MIT, как можно было бы предположить» — вынесены в раздел «Лицензионные флаги».

## Сводка по типам

| Тип | Скиллов | Строк-аналогов | Скиллы без аналога |
|---|---|---|---|
| meta-tooling | 16 | 27 | get-linked-context; retro (частично); sus (частично) |
| planning-design | 14 | 27 | wayfinder (кроме оригинала); system-value-architect (нет OSS-инструмента) |
| domain-design | 13 | 45 | — (у всех есть хотя бы аналог) |
| verification | 12 | 16 | anti-bias; check; principles-review |
| research-analysis | 11 | 18 | known-symptom-fixes |
| agent-orchestration | 9 | 19 | dispatching-parallel-agents (только частичный) |
| writing-content | 8 | 28 | sensory-writing-coach (прямого нет); teach (stateful-механика — нет) |
| creative-ideation | 5 | 17 | meta (диспетчер слоёв — нет) |
| code-review-quality | 5 | 18 | receiving-code-review; ponytail (инструментального нет) |
| implementation | 4 | 10 | executing-plans (ревью+STOP-протокол — пробел экосистемы); prototype LOGIC-ветка |
| data-visualization | 3 | 21 | blueprinter (прямого эстетического нет) |

Всего: **~246 строк-аналогов на 100 скиллов**. Уникальных инструментов/методик — порядка 150.

## meta-tooling (16)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| claude-skills | Universal SKILL.md Converter (andersonamaral2) | MIT | активен (~24.09.2026, v2.2) | Конвертация SKILL.md Claude↔Codex↔Qwen/Cursor/Deep Agents, валидаторы, batch | Только персистентная миграция, не runtime-трансляция; нет резолвера repo-local/global |
| claude-skills | Agent Skills specification (agentskills.io) | см. anthropics/skills | активна | Стандарт структуры skill-папки | Стандарт, не инструмент |
| find-skills | Skills CLI + skills.sh (vercel-labs/skills) | MIT | активен (2026-01-14, 47 релизов, 32.8k★) | ВСЯ механика: find/add/update/list/remove/init, установка в 75+ агентов | Статистика установок ≠ качество; скилл добавляет только workflow формулировки запроса |
| finishing-a-development-branch | GitHub CLI (cli/cli) | MIT | активен (206 релизов) | Исполнительная механика: gh pr create/merge, push, удаление веток | Нет test-gate, меню merge/PR/keep/discard, детекта worktree-состояния |
| get-linked-context | — | — | — | **аналога нет**: приватный локальный CLI-шим собственного продукта nodeterm | — |
| go | Semantic Router (aurelio-labs/semantic-router) | MIT | активен (~12.09.2026) | Семантическая маршрутизация интента | Маршрутизирует к моделям/API, не к workflow-файлам; библиотека, не агентный роутер |
| how-to-write-skills | anthropics/skills — skill-creator | Apache-2.0 | активен (179k★) | Официальный канон: progressive disclosure, template-skill | Anthropic-only школа; нет Gate A, гибрида AGENTS.md, русского слоя |
| how-to-write-skills | obra/superpowers — writing-skills | MIT | активен (v6.4.2) | Канон написания/верификации скиллов | Заточен под кроссплатформенность, не Claude-специфику |
| init-project | Claude Code /init | проприетарная | активен (v2.1.277+) | Генерация starter CLAUDE.md, интерактивный режим | Только CLAUDE.md; нет рамки КТО/ЧТО/КАК/РАДИ ЧЕГО; только Claude Code |
| init-project | AGENTS.md open standard | MIT | активен (60k+ репо) | Целевая артефактная модель: универсальный файл инструкций | Стандарт формата, не генератор |
| manage-nodeterm-canvas | Langflow | MIT | активен (155k★, 311 релизов) | Визуальный канвас, multi-agent orchestration | Ноды — LLM-пайплайн, не живые терминальные сессии; нет worktrees/kanban |
| pinokio | Pinokio (pinokiocomputer/pinokio) — **скилл-обёртка** | MIT (расхождение: релиз v8.0.0 анонсирует «End-to-End Open License») | жив (v8.0.0 ~07.2026) | Полное: pterm control plane | Скилл добавляет только агентный workflow и резолв pterm вне PATH |
| playwright | microsoft/playwright-cli — **скилл-обёртка** | Apache-2.0 | жив (Microsoft, 13711★, 25 релизов) | Полное и шире: сессии, monitoring-дашборд, codegen, официальные скиллы | Инструмент зрелее скилла; скилл не покрывает его новые возможности |
| resolving-merge-conflicts | git-imerge | GPL-2.0-or-later | дормант (2013) | Инкрементальный мерж, save/resume | Не понимает intent сторон; эра Python 2/3 |
| resolving-merge-conflicts | VS Code 3-way merge editor | MIT (Code - OSS) | жив (monthly) | Интерактивное разрешение конфликтов | UI для человека, не протокол для агента |
| resolving-merge-conflicts | agent-skills /merge-conflict-walkthrough (bryancollins99) | MIT | молодой (7 коммитов, 0★) | Процедурный walkthrough для агента | Только advisory, не пишет на диск |
| retro | Reflexion (noahshinn/reflexion) | MIT | исслед. код 2023, низкая активность | Вербальная саморефлексия → эпизодическая память | Per-task, не «сессия → правила»; нет дедупа и аппрува |
| retro | Parabol | AGPL-3.0 dual | жив | Ретроспективы: lessons → action items | Для человеческих команд; AGPL copyleft |
| retro | — | — | — | **прямого аналога «сессия → переиспользуемые правила с аппрувом» нет** | — |
| rules-and-hooks-maintenance | pre-commit framework | MIT | жив (v4.6.0) | Хуки как код, версионирование | Git-хуки ≠ Claude Code хуки; нет fail-open контракта |
| rules-and-hooks-maintenance | agent-extensions: pre-commit skill | CC-BY-4.0 | жив (~7 дней) | Скиллы для написания хуков | Только git-хуки; секции приёмки правок и DS-курса уникальны |
| sus | anthropics/skills (канон) | Apache-2.0 | жив (~175k★) | Канон формата SKILL.md | Нет аудита роутинга и коллизий триггеров |
| sus | awesome-claude-code | CC-BY-NC-ND 4.0 — **не OSS** | жив | Каталог экосистемы | Только каталог; нет анализа конфликтов |
| sus | — | — | — | **аналога измерения коллизий триггеров скриптом нет** | — |
| using-git-worktrees | git worktree (встроенная) | GPLv2 | жив | Сама механика worktree | Голая команда; протокол детекта/consent — в скилле |
| using-git-worktrees | wtx (bkildow/wtx) | MIT | жив (15 релизов) | Управление worktrees, setup/teardown хуки, wtx doctor | CLI для людей; навязывает bare-repo workflow |
| using-git-worktrees | wct (dmtr-p/wct) | MIT | жив | Worktree + tmux-окружение | Крошечный проект (2★); tmux-зависим |
| using-git-worktrees | superpowers: using-git-worktrees | MIT | жив (v6.3.0) | Тот же паттерн изолированных worktrees | Менее детальный протокол |
| write-a-skill | anthropics/skills: skill-creator | Apache-2.0 | жив | Канонический протокол создания SKILL.md | Нет Codex-дельт и механики drift-check |
| write-a-skill | superpowers: writing-skills | MIT | жив | Workflow написания скиллов | Нет дельт под Codex |

## planning-design (14)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| to-spec | mattpocock/skills (канонический оригинал) | MIT | активен | Полное: скилл — адаптация оригинала | это источник |
| to-spec | github/spec-kit | MIT | активен (v1.0.5, 2026-09-08) | Spec-фаза пайплайна, 41 хост-агент | Зрелость экосистемы = гипотеза для эвала |
| to-tickets | mattpocock/skills (оригинал) | MIT | активен | Полное | это источник |
| to-tickets | Task Master (eyaltoledano/claude-task-master) | **MIT + Commons Clause** (не чисто OSS) | активен (28k★, 92 релиза) | PRD→task graph, CLI+MCP | Commons Clause запрещает хостинг/перепродажу/конкурентов |
| to-tickets | BMAD-METHOD | MIT + кастомная преамбула | активен (v6.11.0) | Agile-пайплайн до build | Шире декомпозиции тикетов |
| writing-plans | obra/superpowers | MIT | активен (v6.4.2, 2026-09-25) | writing-plans — родной скилл семейства + drill eval harness | Upstream; редкий случай проверяемой зрелости (есть эвалы) |
| writing-plans | github/spec-kit | MIT | активен | plan-фаза пайплайна | гипотеза для эвала |
| triage | mattpocock/skills (оригинал) | MIT | активен | Полное | это источник |
| triage | rust-lang/triagebot | MIT/Apache-2.0 | активен (~2026-09-27) | Детерминированный триаж-бот | Без AI и agent-ready брифов |
| improve-codebase-architecture | mattpocock/skills (оригинал) | MIT | активен | Полное | это источник |
| improve-codebase-architecture | dependency-cruiser | MIT | активен (v17.4.3) | Dependency-hygiene, графы | Только JS/TS; нет «допроса кейса» |
| improve-codebase-architecture | ArchUnit | Apache-2.0 | активен (v1.5.0) | Исполняемые архитектурные тесты | Только Java; детерминированные правила |
| codebase-design | mattpocock/skills (оригинал) | MIT | активен | Полное | это источник |
| codebase-design | «A Philosophy of Software Design» (Остерхаут) | книга | — | Принципы модульного дизайна | Методология, не инструмент |
| domain-modeling | mattpocock/skills (оригинал) | MIT | активен | Полное | это источник |
| domain-modeling | joshrotenberg/adrs | Apache-2.0/MIT | активен (33 релиза, MCP) | ADR-часть скилла | Только ADR; нет C4/EventStorming |
| domain-modeling | adr-tools | **GPL-3.0** | — | Механика ADR из CLI | Copyleft-флаг |
| domain-modeling | Miragon/event-storming-modeler | MIT | активен | Цифровые EventStorming-доски | Не покрывает C4/ADR/агрегаты |
| wayfinder | mattpocock/skills (оригинал) | MIT | активен | Полное | иных аналогов не найдено |
| prioritize | rice-score-calculator | MIT | обновлён ~2026-07-10 | Только арифметика RICE | Скилл — ISRICE + фасилитация |
| critical-chain-design | rnwolf/ccpm-scheduler | MIT/Apache-2.0 | обновлён ~2026-07-28 (PyPI) | Детерминированный CCPM: буферы, Gantt | Библиотека+CLI, не агентный допрос |
| critical-chain-design | ironyjk/toc-agents | не проверена | средняя (~169 дней) | 11 Claude-агентов по TOC, включая /toc:ccpm | Лицензия не проверена |
| critical-chain-design | «Critical Chain» (Голдратт) | книга | — | Концептуальный фундамент | Методология, не инструмент |
| roadmap-planning | Leantime | **AGPLv3** | активен (~2026-09-25) | Goals-focused PM: roadmaps | AGPL copyleft; PM-система, не узкий фасилитатор |
| goal-plan | Leantime (модуль целей) | **AGPLv3** | активен | Модуль целей/OKR | Зрелого узкого OSS OKR-инструмента не найдено |
| user-story-mapping | zet-cher/storymap-gitlab | MIT | обновлён ~2026-09-04 | Story-mapping доска поверх GitLab | Молодой проект (2★); только GitLab |
| user-story-mapping | thunderdome-planning-poker | Apache-2.0 | активен | Planning poker + story mapping | «AI-Free by Design»; форк 0★ |
| system-value-architect | pm-skills foundation-lean-canvas | Apache-2.0 | активен (~13 дней) | Только canvas-фаза (lean canvas) | Sibling skill; нет discovery и architecture-фаз |
| system-value-architect | Lean Canvas / JTBD / The Mom Test | методики | — | Концептуальный фундамент | OSS-инструмента, соединяющего canvas+discovery+architecture, не найдено |

## domain-design (13)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| canvas-design | anthropics/skills (upstream) | Apache-2.0 | жив | Тот же скилл «canvas-design» — вендорная копия | базовая линия, не конкурент |
| canvas-design | Satori | **MPL-2.0** (не MIT) | жив (OG-генерация) | Машинный рендер JSX/CSS → SVG → PNG | Только подмножество CSS; нет арт-дирекшена |
| canvas-design | p5.js | **LGPL-2.1** (не MIT) | жив | Генеративное искусство на canvas | Нет стадии «манифеста движения» |
| design-communication-analyzer | 10 эвристик Нильсена | методика | жив (стандарт с 1994) | Часть протокола: когнитивная нагрузка | Нет 5-шагового протокола «намерение → интерпретация» |
| design-communication-analyzer | Cognitive walkthrough | методика | классика | Пошаговый разбор «поймёт ли пользователь» | Только задачи/шаги, нет семиотики |
| design-communication-analyzer | Laws of UX | методика | жив | Каталог законов восприятия | Справочник, не протокол |
| frontend-design | anthropics/skills (upstream) | Apache-2.0 | жив | Тот же скилл «frontend-design» | базовая линия |
| frontend-design | shadcn/ui | MIT | жив (124.9k★, v4) | Компонентная база production-интерфейсов | Нет арт-дирекшена против «AI slop» из коробки |
| frontend-design | Magic UI | MIT | жив (~11 дней) | 150+ анимированных компонентов | Только компоненты, нет методологии |
| frontend-design | web-interface-guidelines (vercel-labs) | MIT | жив | Гайдлайны выразительных интерфейсов | Документ, не код |
| frontend-ui-dark-ts | shadcn/ui | MIT | жив | Тёмная тема из коробки, copy-paste | Не дашборд-специфичен |
| frontend-ui-dark-ts | Flowbite | MIT | жив | Tailwind-компоненты с dark mode | Не React-специфичен |
| frontend-ui-dark-ts | TailAdmin | MIT | жив | Готовый тёмный дашборд (React 19) | 7 вариаций и 500+ компонентов — Pro (платно) |
| frontend-ui-dark-ts | free-tailwind-admin-dashboard-template | MIT | жив | Готовый дашборд на shadcn | Один шаблон, не UI-система |
| interior-design-expert | Sweet Home 3D | **GPL-2.0** | жив (релиз 7.5) | Планировка, 3D-превью | Десктопный Java-апп; нет AI, IES-расчётов, теории цвета |
| interior-design-expert | coloraide | MIT | жив (~4 дня) | Цветовая математика, гармонии | Поддержка Munsell не подтверждена; нет интерьерной специфики |
| landing-page-optimizer | GrowthBook | MIT open core (+ Enterprise License) | жив | A/B-тестирование, байесовская статистика | Только инфраструктура экспериментов; нет CRO-методологии |
| landing-page-optimizer | PostHog | MIT core (ee/ — отдельно) | жив (30k+★) | Аналитика, session replay, фичефлаги | Self-host требователен; нет методологии аудита |
| landing-page-optimizer | JTBD (Кристенсен) | методика | жив | Первый шаг скилла | Теория, не инструмент |
| landing-page-optimizer | NN/g landing page guidelines | методика | жив | Гайдлайны посадочных | Рекомендации, не 6-шаговый протокол |
| moai-domain-uiux | Style Dictionary | Apache-2.0 | жив (v4 DTCG) | Трансформация DTCG-токенов | Только токены; нет WCAG/иконок/гайданса |
| moai-domain-uiux | axe-core | **MPL-2.0** | жив (39M загрузок/нед) | Автотесты доступности | Покрывают ~30–50% проблем; не дизайн-гайданс |
| moai-domain-uiux | Lucide | ISC | жив (ежедневная синхронизация) | 1700+ иконок | Только иконки |
| moai-domain-uiux | Storybook | MIT | жив | Витрина дизайн-системы | Только витрина; нет токенов/методологии |
| moai-domain-uiux | web-interface-guidelines | MIT | жив | Гайдлайны интерфейсов | Документ, не инструментарий |
| mood-board-builder | MoodBored | Apache-2.0 | жив (создан 2026-09-22, 102 коммита) | Мудборд-воркспейс с LLM-чатом, MCP (14 инструментов) | Незрелый (2★, 0 релизов); AI требует внешних API-ключей |
| mood-board-builder | djai-open-canvas | MIT | жив (~48 дней) | Infinite canvas, экспорт PNG/PDF | Нет палитр/типографики как сущностей, нет AI |
| mood-board-builder | Penpot | **MPL-2.0** | жив (stable 2.8.1) | Доски, компоненты, self-host | Figma-класс; нет мудборд-специфики |
| multimodal-video-retakes-editor | Auto-Editor | Unlicense (public domain) | жив («pushed daily», 5.2k★) | CLI авто-монтажа: нарезка по транскрипту (whisper word-level), экспорт OTIO/NLE | Rule-based; **нет мультимодального отбора «лучшего дубля» через vision** — там скилл уникален |
| multimodal-video-retakes-editor | faster-whisper | MIT | жив (25.6k★) | ASR с word-level timestamps | Только ASR |
| multimodal-video-retakes-editor | OpenTimelineIO | Apache-2.0 | жив (зрелый) | API/формат таймлайнов, адаптеры NLE | Только представление таймлайна |
| multimodal-video-retakes-editor | mohhh-ok/moodboard | MIT | жив | Side-by-side отсмотр медиа + Agent Skills | Ручной просмотр человеком, не агентский отбор; только macOS |
| onboarding-optimizer | Driver.js | MIT | жив/стабилен (v1.4.0) | Продуктовые туры, подсветка элементов | Только реализация туров; нет аудит-методологии |
| onboarding-optimizer | Shepherd.js | **AGPL-3.0 + коммерческая** (не MIT) | жив | Туры по приложению | Лицензионный флаг для коммерческих продуктов |
| onboarding-optimizer | NN/g onboarding guidelines | методика | жив | Гайдлайны онбординга | Рекомендации, не протокол аудита |
| theme-factory | anthropics/skills (upstream) | Apache-2.0 | жив | Тот же скилл «theme-factory» | базовая линия |
| theme-factory | tweakcn | **Apache-2.0** (не MIT) | жив (10.4k★) | Визуальный редактор тем shadcn | Только CSS-переменные; нет шрифтовых пар |
| theme-factory | Radix Colors | MIT | стабилен | 12-шаговые шкалы, WCAG-контрасты | Фиксированные пресеты; только цвет |
| tremor-design-system | Tremor (upstream) | Apache-2.0 | **застой** (~20 мес без обновлений; поглощение Vercel 02/2025) | Сам инструмент, на котором построен скилл | Разработка стагнирует — риск для скилла |
| tremor-design-system | shadcn/ui | MIT | жив (124.9k★, v4) | Charts на Recharts + dashboard-блоки — прямой заменитель | Миграция требует переписывания; чарты проще ECharts |
| tremor-design-system | Apache ECharts | Apache-2.0 | жив (v6.x) | Мощные интерактивные графики | Не React-нативный; конфиг-ориентированный API |
| tremor-design-system | Recharts | MIT | жив | Базовая библиотека графиков (основа Tremor) | Только графики |
| web-artifacts-builder | anthropics/skills (upstream) | Apache-2.0 | жив | Тот же скилл «web-artifacts-builder» | базовая линия |
| web-artifacts-builder | vite-plugin-singlefile | MIT | застой (~19 мес) | Инлайн JS/CSS в один HTML | Минимальное сопровождение |
| web-artifacts-builder | shadcn/ui | MIT | жив | Компонентная база стека скилла | Только часть стека |

## verification (12)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| anti-bias | — | — | — | **аналога нет**: дебайсинг — только промпт-коллекции | — |
| bouncer | Flaught | MIT | активен (push 2026-09-20) | Ревью диффа независимой LLM в CI, JSON-артефакт | Очень молодой (2★); нет режимов quick/deep/consensus |
| bouncer | Aragora | MIT | активен (push 2026-10-01) | Мультимодельный кворум-ревью PR, Decision Receipt | Молодой (11★); нет quick/deep и plan-review |
| check | — | — | — | **аналога нет** (ближайшее — пререгистрация гипотез, академическая практика) | — |
| corridor-tester | Guerrilla HCI / hallway testing (Нильсен) | методика | канон с 1994 | Ядро: дешёвое коридорное тестирование | Не покрывает AI-симуляцию респондентов; без живых людей не исполнить |
| falsify | Hypothesis (property-based testing) | MPL-2.0 | активен (push 2026-09-28) | Автопоиск контрпримеров (shrinking) | Только код; нет evidence-пайплайна и вердикта |
| falsify | LitmusChaos | Apache-2.0 | активен (push 2026-09-30) | Фальсификация claim о готовности fault injection | Только инфра/K8s; нет агентского протокола |
| grilling | socratic-method (skill) | MIT | активен (push 2026-09-07) | Сократова интервью: stress/develop режимы | Промпт-коллекция (0★); нет обхода дерева решений |
| grilling | socratic_enhancer | не задекларирована | мёртв (push 2026-02-18) | Два Claude-агента ведут сократов диалог | Диалог между агентами, не с пользователем; заброшен |
| hypothesis-eval-loop | promptfoo | MIT | активен (push 2026-10-01, ~25.6k★) | Исполнение эвалов, before/after, LLM-as-judge, CI | Не покрывает карточку гипотезы, baseline-SHA, анти-постдикшн |
| hypothesis-eval-loop | DeepEval | Apache-2.0 | активен (push 2026-09-29, ~18.5k★) | Метрики эвалов, датасеты, CI | Не покрывает протокол «гипотеза до замера» |
| hypothesis-eval-loop | Inspect AI (UK AI Safety Institute) | MIT | активен (push 2026-10-01) | Инфраструктура эвалов, model-graded | Фокус safety, не регрессия правок скиллов |
| performance-profiling | Lighthouse | Apache-2.0 | активен (push 2026-09-30, ~30.8k★) | Web Vitals, аудит, Lighthouse CI — скрипт скилла обёртка над ним | Не покрывает рантайм-профилирование |
| performance-profiling | webpack-bundle-analyzer | MIT | активен (push 2026-09-25) | Bundle-анализ, treemap | Только webpack; нет Web Vitals |
| principles-review | — | — | — | **аналога нет** (OPA/Regal — НЕ аналог: проверяют артефакты, не здоровье системы правил) | — |
| security-best-practices | Semgrep | LGPL-2.1 (ядро) | активен (push 2026-10-01, ~16.8k★) | Мульти-языковой SAST, OWASP-правила | Не покрывает secure-by-default гайды и ручной аудит-отчёт |
| security-best-practices | OWASP ZAP | Apache-2.0 | активен (push 2026-10-01, ~15.9k★) | DAST-сканирование, OWASP Top 10 | Только веб; нет статического анализа |
| verification-before-completion | pre-commit | MIT | активен (push 2026-09-29, ~15.6k★) | Механизм гейта: хуки перед коммитом | Гейтует код, а не клеймы агента; нет evidence-before-claims |
| webapp-testing | Playwright (Microsoft) | Apache-2.0 | активен (push 2026-10-01, ~97k★) | Всё инструментальное ядро — скилл переупаковка Playwright | Только обёртка `with_server.py` добавляет lifecycle серверов |

## research-analysis (11)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| attentional-blindness-analyzer | wondelai/skills · ux-heuristics | MIT | частично проверена | Эвристический аудит интерфейсов, детект тёмных паттернов | Ядро — модель внимания (focus points, оценка нагрузки) — уникально |
| bottleneck-identifier | k6 (Grafana) | **AGPL-3.0** | активен (v1.6.0, ~31.7k★) | Полная механика нагрузочных тестов | AGPL copyleft; «узкое место» интерпретирует пользователь; скилл — пустая обёртка |
| debug | The Debugging Book (Zeller) | код MIT, текст CC BY-NC-SA 4.0 | цитируется активно | Научная база: воспроизводимость, delta debugging | Учебник для людей; нет «feedback loop first» |
| debug | stas00/the-art-of-debugging | CC-BY-SA-4.0 | активен (~27 дней) | Методология отладки + собственный SKILL.md для агентов | Фокус C/C++/Python/PyTorch; нет байесовской сортировки гипотез |
| known-symptom-fixes | — | — | — | **аналога нет**: жанр incident runbooks не переносим как навык агента | — |
| leverage | «Leverage Points» (Meadows, 1999) | свободная статья | классика | Лестница 12 точек воздействия — основа скилла | Статья, не инструмент; операционализация уникальна |
| research | gpt-researcher | Apache-2.0 | активен (~29.9k★, 74 релиза) | Deep-research движок: planner/execution, цитирования, эвалы, MCP | Требует API-ключей; скилл проще и дешевле |
| research | langchain-ai/open_deep_research | MIT | **архивирован** | Deep-research движок | Разработка остановлена |
| research | langchain-ai/local-deep-researcher | MIT | активен (~39 дней) | Reflect-and-requery цикл, локально | Требует локальных моделей; уже, чем скилл |
| research | 199-biotechnologies/claude-deep-research-skill | MIT | данные на апр 2026 | Claude Skill, 8-фазное исследование | Масштаб ниже gpt-researcher |
| systematic-debugging | obra/superpowers | MIT | активен (v6.3.0) | **Апстрим скилла**: скилл — производный порт | Апстрим зрелее по определению (эвалы, мульти-харнес) |
| systematic-debugging | The Debugging Book | код MIT, текст CC BY-NC-SA 4.0 | см. debug | Теоретическая основа | Не агентский протокол |
| theory-of-constraints | cameleonh/toc-agents | MIT | слабая (4 коммита, ~171 день) | Весь фреймворк Голдратта как агентские навыки | Почти заброшен; часть — roadmap, не реализация |
| theory-of-constraints | «The Goal» (Голдратт) | коммерческая книга | классика | Первоисточник: 5 focusing steps, DBR | Литература, не инструмент |
| thinking-theory-of-constraints | cameleonh/toc-agents | MIT | см. выше | Тот же аналог (скилл — дубль theory-of-constraints) | Та же оценка |
| tool-scout | vercel-labs/skills (npx skills CLI) | MIT | очень активен (v1.5.15, ~32.8k★) | Discovery/install/search инструментов-как-навыков | Уже, чем tool-scout (только agent skills, не весь ландшафт) |
| tool-scout | sindresorhus/awesome | CC0-1.0 | жив (~512k★) | Курируемый discovery-корпус | Статические списки; нет оценки и свежести |
| truth-seeker | FActScore | MIT | **заброшен** (~535 дней) | Атомарная декомпозиция + верификация фактов | Wikipedia как источник; нет линз/дебатов; скилл живее |
| truth-seeker | ClaimReview (schema.org) | открытый стандарт | стандарт жив | Формат вердикта claimReviewed/reviewRating | Формат данных, не анализ |

## agent-orchestration (9)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| agent-orchestrator-standard | LangGraph | MIT | активен (7092 коммита) | Control plane: циклы волн, состояние, роутинг | Не покрывает «менеджерскую» часть: worktree-линейки, cost-routing |
| agent-orchestrator-standard | CrewAI | MIT | активен (v1.15.20) | Ролевые crews, делегирование, метрики токенов | Нет wave-цикла со state-машиной; enterprise — paywall |
| agent-orchestrator-standard | Microsoft Agent Framework | MIT | активен (GA 04.2026) | Workflows, durable execution, мульти-агентная координация | Свежий, экосистема догоняет; не покрывает управленческую дисциплину |
| audit-fanout | PR-Agent (community-owned) | MIT | активен (~6 дней) | Мульти-агентный аудит кода | Не покрывает фиксированные оси A1–A6 и «якоря реальности»; только PR-диффы |
| codex-advisor | Archon | MIT | активен (релиз 2026-08-19) | Цикл «план → исполнение → валидация» YAML-workflows | Не разделяет роли Manager/Advisor; требует инфры агентов |
| codex-advisor | LangGraph plan-and-execute (паттерн) | MIT | mainstream 2025–2026 | Planner → Executor → Re-planner, фазы 1:1 | Паттерн, не продукт; нет GOAL/EVIDENCE-формата |
| cost-aware-delegation | LiteLLM | **MIT ядро + проприетарный enterprise/** (GitHub: NOASSERTION) | очень активен (1465 релизов) | 100+ провайдеров, cost tracking, load balancing, guardrails, бюджеты | Шлюз, не доктрина делегирования; нет правила «экономия > overhead» |
| cost-aware-delegation | Portkey AI Gateway | MIT (средняя уверенность) | активен | Та же идея: gateway, guardrails, мониторинг затрат | Шлюз, не политика; enterprise отдельно |
| cost-aware-delegation | OpenRouter | **проприетарный сервис** | активен (300+ моделей) | Роутинг по цене/качеству, прозрачные цены | Не OSS; зависимость от внешнего сервиса |
| delegate | BMAD-METHOD | MIT + кастомная преамбула | активен (v6.12.0) | Доктрина брифа исполнителя, роли-агенты | Нет 3 гейтов скилла и шаблона КОНТЕКСТ/ЭТАЛОН/ЗАПРЕТЫ |
| delegate | obra/superpowers | MIT | активен | Философия «бриф как артефакт» | Методика, не движок; нет формальной приёмки |
| dispatching-parallel-agents | CrewAI async_execution/kickoff_async | MIT | активен | Параллельный запуск независимых задач | Только фича фреймворка, не workflow-доктрина |
| goal-king | AutoGPT | **дуальная: Polyform Shield / MIT** | очень активен | Автономный цикл до закрытия цели | Не покрывает contract.md/ledger/anti-stall; классический loop устарел |
| goal-king | deepagents | MIT | активен (0.1.66) | Middleware долгоживущего агента, сабагенты, файловая память | Библиотека, не протокол закрытия roadmap |
| goal-king | BabyAGI | MIT | **протух** (~8 мес) | Прародитель паттерна «задача → приоритет → исполнение» | Архаичен, заброшен; только как родоначальник |
| handoff | OpenAI Agents SDK — handoff() | MIT | активен (v0.17.3) | Нативный примитив передачи управления с типизированным контекстом | Только механика; нет датированных handoff-документов |
| handoff | Google A2A Protocol | Apache-2.0 | активен (Linux Foundation, spec v1.0) | Меж-агентная передача как открытый стандарт | Протокол коммуникации, не методика переноса контекста |
| subagent-driven-development | obra/superpowers | MIT | активен | **Прямой апстрим скилла** | Нет артефактов implementer-prompt/reviewer-prompt как готовой процедуры |
| subagent-driven-development | Archon | MIT | активен | Исполнение implementation-плана workflow-движком | Нет доктрины «свежий сабагент + ревью каждой задачи» |

## writing-content (8)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| caveman | JuliusBrussee/caveman | Apache-2.0 | создан 2026-04-04, 822 коммита, 42 релиза | Тот же механизм ультра-кратких ответов + прокси + middleware; цитируется Adobe Research, JetBrains | Инфраструктура (прокси), не skill-файл |
| caveman | jarvis token-efficient skill | не верифицирована | обновлён ~10 дней назад | Skill-формат, ближайший по форме | Лицензия не проверена |
| doc-coauthoring | anthropics/skills (официальный апстрим) | Apache-2.0 | жив (179k★) | SKILL.md почти дословно совпадает → **`origin: own` в реестре, вероятно, ошибочна** | Документные скиллы — source-available, не OSS |
| feynman | cloudflare eli5 (фактический апстрим) | MIT | обновлён ~10 дней назад | «Simplify language, never facts», before/after | точный источник скилла |
| feynman | dhanesh/agent-skills feynman-walkthrough | MIT | обновлён 8 дней назад | Guided walkthrough, OKF-персистентность, spaced retrieval opt-in | Формат walkthrough, не персистентный режим |
| feynman | giant-brains-claude-skills feynman | не верифицирована | обновлён 29 дней назад | File-first, «techniques, not persona» | One-shot, не персистентный |
| feynman | leighstillard/feynman | не указана | 1 коммит | Skill + output style, 6 правил | Микроскопический проект |
| feynman | DreambigOu/ELI5 | не верифицирована | — | Аудиторно-адаптивное упрощение, есть эвалы | — |
| internal-comms | anthropics/skills (официальный апстрим) | Apache-2.0 | жив | Официальный апстрим | Независимых внешних аналогов не найдено |
| jtbd-scenarium-create | lecoo21/pm-skills define-jtbd-canvas | Apache-2.0 | обновлён 34 дня назад | JTBD-canvas | Нет 9-частного канона Standard 2.0 |
| jtbd-scenarium-create | lalulali/vespyr jtbd | не верифицирована | обновлён 48 дней назад | JTBD + HMW | Те же ограничения |
| jtbd-scenarium-create | prateekjain24/pmcopilot jtbd-canvas | не верифицирована | обновлён 185 дней назад | JTBD-шаблон | Те же ограничения |
| pdf | anthropics/skills (официальный апстрим) | source-available, **не OSS** | жив | Официальный апстрим скилла | — |
| pdf | ReportLab | BSD | latest 4.4.5 | Создание PDF с нуля: Canvas, Platypus, таблицы | Основной репо — Mercurial |
| pdf | WeasyPrint | BSD | обновлён 6 дней назад (9.6k★) | HTML/CSS → PDF, движок вёрстки | — |
| pdf | pdfplumber | MIT | v0.11.9 (2026-01-05) | Извлечение текста/таблиц, visual debugging | Только чтение |
| pdf | pypdf | BSD-3-Clause | версии 6.16.x | Merge/split, формы, метаданные | Слабое извлечение текста |
| pdf | PyMuPDF | **AGPL-3.0** (dual commercial) | ~10k★ | Самый полный стек: рендер, OCR, формы | **AGPL copyleft-риск** для проприетарного распространения |
| sensory-writing-coach | — | — | — | **прямого аналога нет**; частичные: seo-review-writer (маркетинговый фрагмент), writing_show_dont_tell_converter (проза) | — |
| teach | Khanmigo (Khan Academy) | **проприетарный** | — | Сократический тьютор, «never give the answer» | Не OSS; stateful-механику никто не покрывает |
| teach | Khanmigo Lite «Tutor Me» (утёкший промпт) | MIT | обновлён 7 дней назад | Сократический стиль, разбивка на части | Системный промпт, не skill |
| teach | Mr.-Ranedeer-AI-Tutor | не верифицирована | **discontinued** (~1005 дней) | Персонализированный AI-тьютор | Заброшен |
| teach | awesome-skills khan-academy | не верифицирована | не верифицирована | Skill-обёртка поверх Khan Academy | Не проверено |

## creative-ideation (5)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| algorithmic-art | p5.js | **LGPL-2.1** (не MIT) | активен (17 456 коммитов, 169 релизов, 24k★) | Весь исполнительный слой: seeded randomness, flow fields, particles | Нет слоя «философии»/манифеста — скилл уникален процессом, зависит от p5.js |
| algorithmic-art | Processing 4 | ядро LGPL-2.1, PDE GPL-2.0 | активен | Генеративное искусство, библиотека примеров | Десктоп/Java; нет web-интерактивности |
| algorithmic-art | openFrameworks | MIT | активен (18 147 коммитов) | Высокопроизводительное генеративное искусство | C++ и сложный сетап — непригоден для быстрой генерации агентом |
| algorithmic-art | nannou | MIT/Apache-2.0 dual | активен (релиз 0.20.0, 06.2026) | Rust-фреймворк генеративного арта | Высокий порог входа; нишевое сообщество |
| jobs-to-be-done | savvides/jtbd | MIT | активен (01.09.2026) | 8 скиллов: Switch-анализ, 4 силы прогресса, job stories, job map | 0 звёзд; требует транскрипты интервью; нет ODI-квантификации |
| jobs-to-be-done | Strategyn / ODI (Ulwick) | **proprietary** | компания активна | ODI: измерение неудовлетворённости, Opportunity Algorithm | Платный консалтинг; пересечение только на уровне идей |
| jobs-to-be-done | «Competing Against Luck» (Кристенсен) | книга | — | Теоретический фундамент | Не инструмент |
| meta | Six Thinking Hats (де Боно) | книга | — | Мультиперспективное мышление | Нет диспетчеризации слоёв и honesty-слоя |
| meta | henu-wang/six-thinking-hats | MIT | низкая (1 коммит, 0★) | Интерактивный проход по 6 шляпам | Незрелый; не покрывает слои meta |
| meta | autodos-thinking-frameworks | не проверена | обновлялся ~83 дня назад | 16 thinking frameworks как скилл | Каталог линз, не диспетчер; **точного аналога диспетчера слоёв нет** |
| reframing-problems | problem-framing-canvas (deanpeters) | **CC BY-NC-SA 4.0** (не OSS для коммерции) | активен (143 коммита, 8 релизов, 7.1k★) | MITRE Problem Framing Canvas + интерактивный ABC-коучинг | NC-лицензия запрещает коммерческое использование; PM-контекст, не тактический one-pass |
| reframing-problems | MITRE Problem Framing Canvas (методика) | свободный доступ | v3 | Три зоны канваса | Методика, не инструмент |
| reframing-problems | «Frame Innovation» (Dorst) | книга | — | 9 шагов frame creation | Книга; требует фасилитации |
| triz | triz-ai (PyPI-пакет) | MIT | активен (81 коммит, 22 релиза, 227 unit-тестов) | Роутер 6 методов, матрица 39×39, патентная база с векторным поиском | Требует LLM-ключа; 2 звезды; канон скилла (62 файла) шире |
| triz | triz-agents | MIT | низкая (3 коммита, 0★) | 9 команд TRIZ как Claude-агенты | Упрощённые промпты; незрелый |
| triz | Heinrich: The Inventing Machine | Apache-2.0 | низкая (~06.2026) | 7-модульный пайплайн с трассируемостью | Выглядит заброшенным |
| triz | Ideation International (коммерческий ТРИЗ-софт) | **proprietary** | компания существует | Профессиональный ТРИЗ-софт | Недоступен как OSS/для эвала |

## code-review-quality (5)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| code-review | reviewdog | MIT | активен (5845 коммитов, 46 релизов) | Standards-ось механически: «линтер→коммент в PR» | Нет Spec-оси; только детерминированные линтеры, без LLM |
| code-review | PR-Agent (Qodo → community-owned) | **MIT** (в задании ошибочно Apache-2.0) | активен (5749 коммитов, 38 релизов, 13.2k★) | Standards + заявленные «Requirement Gaps» (Spec) | Spec-зрелость только по README; **PRSense — не продукт Qodo** |
| code-review | Semgrep OSS | LGPL-2.1 (ядро) | активен (~16.8k★) | Мульти-языковой SAST | Нет Spec-оси; registry-правила — Commons Clause |
| code-review | SonarQube Community Build | LGPL-3.0 ядро; дистрибутив смешанный (SSALv1) | активен (26.8.x) | Quality gates, детект запахов/уязвимостей | Нет Spec-оси; тяжёлый self-host |
| code-review | Danger JS | MIT | активен (142 релиза) | Кодификация норм ревью в Dangerfile | Нет Spec-оси и AI-суждения |
| code-review | CodeRabbit | **закрытый коммерческий SaaS** | активен (2026) | Standards + Spec: walkthrough, line-by-line, 40+ линтеров, natural-language правила | Closed source; per-run вариативность LLM |
| code-review | Google eng-practices reviewer guide | **CC BY 3.0** (не 4.0) | живая методология | «What to Look For» ≈ Standards-ось | Методика, не инструмент |
| pizdej (Mode A) | Self-Refine | Apache-2.0 | dormant с 2023 | generate→feedback→refine | Нет фальсификации клеймов (ядро Mode A) |
| pizdej (Mode B) | Reflexion | MIT | исслед. код 2023, низкая активность | Актор/Оценщик/Саморефлексия + эпизодическая память | Mode A не покрыт |
| pizdej (Mode B) | aar-loop | не проверена | обновлён ~55 дней назад | Ручной Reflexion-цикл, уроки патчатся в skills/rules | Лицензия не проверена; нет калибровки уверенности |
| pizdej (Mode B) | Blameless postmortem (SRE Book) | **CC-BY-NC-ND-4.0** (не CC BY 4.0) | живая методология | action items ≈ design injection | Методика для инцидентов; NC/ND ограничивает адаптацию |
| pizdej (Mode B) | After Action Review (армия США) | public domain (методика) | с 1993 | 4 вопроса ≈ каркас Mode B | Нет калибровки уверенности и design injection |
| receiving-code-review | — | — | — | **аналога нет**: верификация фидбека нигде не автоматизирована | — |
| requesting-code-review | GitHub Docs «Requesting a pull request review» | CC BY 4.0 | живая документация | Механика запроса ревьюера на платформе | Нет связки git SHAs + шаблон code-reviewer.md |
| requesting-code-review | Google CL Author's Guide | CC BY 3.0 | живая методология | Методология подготовки изменений к ревью | Методика, не инструмент |
| ponytail | YAGNI (XP) | CC BY-SA (Wikipedia) | с 1990-х | Ступень 1 лестницы («нужно ли вообще?») | Только первая ступень; **инструментального аналога нет** |
| ponytail | Three Virtues of a Programmer | без лицензии | классика с 1991 | Философия «лени» как ценности | Не операционализирует лестницу |
| ponytail | engineering-lore YAGNI catalog | не проверена | обновлён ~38 дней назад | Трассировка происхождения YAGNI | Каталог, не инструмент |

## implementation (4)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| implement | Aider | Apache-2.0 | активен (v0.86.2, 02.2026; коммиты 09.2026) | Реализация задачи по описанию: pair-programmer, авто-коммиты, /test, architect-режим, SWE-bench лидерство | Нет TDD red-first; нет бюджета итераций; нет воспроизводимости |
| implement | OpenHands | MIT (теперь MIT-only) | активен (коммиты 09.2026; реструктурирован в Agent Canvas + software-agent-sdk) | Автономная реализация end-to-end, CodeAct-агент, event-sourced лог | Тяжёлая инфра (Docker); нет TDD; непредсказуемая стоимость |
| executing-plans | GitHub Spec Kit | MIT | активен (v1.0.5, 2026-09-08, ~133k★) | Письменный план как артефакт: constitution→specify→plan→tasks, checkpoints | Нет критического ревью плана до старта; нет STOP-протокола; исполнение зависит от хост-агента |
| executing-plans | OpenSpec (Fission AI) | MIT | активен (v1.11.0, 08.2026) | Change-папка как план, пошаговое исполнение, validate-гейты | Фокус на дельта-изменениях; нет ревью/эскалации/изоляции |
| prototype | bolt.diy | MIT (исходники); WebContainers API — коммерческая для for-profit | активен (~19.9k★, 8 релизов) | UI-ветка: генерация UI-вариантов по промпту в браузере | Только веб в песочнице; нет LOGIC-ветки; нет границы «не в продакшн» |
| prototype | Spike solution (XP) | методология | канон 1990-х | Throwaway-подход: наименьший код для проверки пути | Методика без механики; нет требования фиксировать вердикт |
| test-driven-development | pytest | MIT | активен (9.1.1) | Механика Red-Green: запуск, фикстуры, assert rewriting | Не навязывает «тест сначала»; не проверяет падение по правильной причине |
| test-driven-development | StrykerJS | Apache-2.0 | активен (обновлён 2026-07-17) | Мутационное тестирование: механическая проверка «тест упал по правильной причине» | Не навязывает red-first; дорогой прогон; JS/TS/.NET/Scala |
| test-driven-development | tdd SKILL (mthines/agent-skills) | MIT | активен (v1.2.0) | Тот же Red-Green-Refactor для агента + mutation checks в REFACTOR | Текст инструкции — агент может проигнорировать |
| test-driven-development | tdd-guard.sh (хук PreToolUse) | не указана | документирован (~15 дней) | Блокирует Write/Edit пока не активен TDD-цикл | Только наличие тест-файла; легко обходится; не покрывает Refactor |

## data-visualization (3)

| Скилл | Аналог | Лицензия | Живость | Покрытие | Ограничения |
|---|---|---|---|---|---|
| graphify | Graphify-Labs/graphify (**апстрим самого скилла**) | Apache-2.0 | активен (push 2026-09-30, ~122.9k★) | Всё: PyPI-пакет `graphifyy`, который скилл устанавливает и оркеструет | Не «аналог», а источник; ценность скилла — промпт-протокол + honesty-разметка рёбер |
| graphify | GitNexus | **PolyForm Noncommercial** (не OSS для коммерции) | активен (push 2026-10-01, ~47.7k★) | AST → knowledge graph, Leiden, execution flows, MCP | NC-лицензия; нет honesty-аудита рёбер; тяжелее |
| graphify | codeknow | MIT | push 2026-09-03 (3★) | tree-sitter → knowledge graph, blast radius | Крошечный; зрелость не доказана |
| graphify | Microsoft GraphRAG | MIT | активен (push 2026-09-28, ~36.2k★) | Knowledge graph из документов, community detection | Только документы, не код; нет HTML-виза |
| graphify | LightRAG | MIT | активен (push 2026-09-30, ~39.9k★) | Lightweight KG-RAG из документов | Документы, не код |
| graphify | Cognee | Apache-2.0 | активен (push 2026-10-01, ~31.3k★) | KG как память для агентов | Память, не навигация по кодовой базе |
| graphify | Graphiti (Zep) | Apache-2.0 | активен (push 2026-09-30, ~31.3k★) | Temporal KG для агентов | Эпизодическая память, не структура кода |
| graphify | Gephi | GPL-3.0 | активен (push 2026-09-27) | Виз/анализ графов, community detection | Не строит граф из папки; десктоп Java; copyleft |
| graphify | Neo4j (Community) | GPL-3.0 (Community) | активен (push 2026-09-22) | Хранение и Cypher-запросы | СУБД, не конструктор графа |
| graphify | FalkorDB | **SSPLv1** (не OSI-approved) | активен (push 2026-10-01) | Графовая СУБД под GraphRAG/LLM | Лицензионный флаг для коммерческого использования |
| blueprinter | Mermaid | MIT | активен (push 2026-09-30, ~90.5k★) | Диаграммы из текста: flowchart, C4, sequence, ER | Не даёт эстетики flat-blueprint; data-ink ratio ниже |
| blueprinter | D2 | MPL-2.0 | активен (push 2026-09-20, ~25.6k★) | Diagram-as-code, иконки, темы | Свой визуальный язык; не HTML/CSS |
| blueprinter | Structurizr DSL | Apache-2.0 | активен (push 2026-09-19) | «Модель как код» для C4 | Только C4; интерактивный просмотр — платный |
| blueprinter | C4-PlantUML | MIT | активен (push 2026-08-26) | C4 через PlantUML | Эстетика PlantUML; рендер в картинку |
| blueprinter | diagrams (Python) | MIT | активен (push 2026-09-22, ~42.7k★) | Python-код → архитектурные диаграммы | Только инфра-иконки; Graphviz-рендер |
| blueprinter | Graphviz | EPL-2.0 | активен | Layout-движок (DOT) — фундамент diagrams/PlantUML | Эстетика «из 90-х»; не генератор «под ключ» |
| visual-explainer | Marp (CLI/экосистема) | MIT | активен (push 2026-09-08) | Markdown → HTML/PDF/PPTX деки | Нет методологии сторителлинга; PPTX — картинки |
| visual-explainer | Slidev | MIT | активен (push 2026-09-16, ~48.9k★) | Markdown+Vue → интерактивные HTML-деки | Требует Node/Vue; не один self-contained файл |
| visual-explainer | reveal.js | MIT | активен (push 2026-09-30, ~72.4k★) | Зрелый HTML-презентационный фреймворк | Фреймворк, не генератор; нет explainer-методологии |
| visual-explainer | Manim (Community) | MIT | активен (push 2026-09-29, ~41.2k★) | Программные explainer-анимации (3Blue1Brown-стиль) | Другой медиум (видео); крутая кривая обучения |
| visual-explainer | PptxGenJS | MIT | push 2025-11-28 | Программная генерация презентаций из JS/TS | Выход PPTX, не HTML; API, не методология |

---

## Лицензионные флаги и коррекции (проверены, не из памяти)

- PR-Agent — **MIT**, не Apache-2.0; «Qodo PR-Agent / PRSense» как пара продуктов одной компании — неверно (PRSense — несвязанные проекты).
- Google SRE Book — **CC-BY-NC-ND-4.0**; Google eng-practices — **CC BY 3.0** (не 4.0).
- Satori — **MPL-2.0**; p5.js — **LGPL-2.1**; Shepherd.js — **AGPL-3.0 + коммерческая**; Lucide — ISC; axe-core — MPL-2.0.
- Task Master — **MIT + Commons Clause** (не чисто OSS: запрет хостинга/перепродажи/конкурентов).
- Leantime — **AGPLv3**; adr-tools — **GPL-3.0**; PyMuPDF — **AGPL-3.0** (dual commercial); Sweet Home 3D — **GPL-2.0**; Gephi/Neo4j Community — **GPL-3.0**.
- GitNexus — **PolyForm Noncommercial** (запрет коммерческого использования); FalkorDB — **SSPLv1** (не OSI-approved).
- LiteLLM — MIT-ядро + проприетарный `enterprise/` (GitHub: NOASSERTION); OpenRouter — проприетарный сервис; BMAD-METHOD — MIT с кастомной преамбулой; awesome-claude-code — **CC-BY-NC-ND** (не OSS, деривативы запрещены).
- anthropics/skills: большинство — Apache-2.0, но **документные скиллы (docx/pdf/pptx/xlsx) — source-available, не OSS**.
- **doc-coauthoring**: пометка `origin: own` в реестре, вероятно, ошибочна — SKILL.md почти дословно совпадает с официальным anthropics/skills.

## Скиллы-обёртки (аналог = сам инструмент)

- pinokio → Pinokio; playwright → microsoft/playwright-cli; webapp-testing → Playwright; performance-profiling → Lighthouse (скрипт-обёртка); graphify → Graphify-Labs/graphify (устанавливает PyPI-пакет); find-skills → Skills CLI (vercel-labs/skills) — вся механика покрыта; using-git-worktrees → git worktree (частично); systematic-debugging → obra/superpowers (производный порт).

## Честные «аналога нет»

get-linked-context; anti-bias; check; principles-review; known-symptom-fixes; receiving-code-review; ponytail (инструментального); wayfinder (кроме оригинала); system-value-architect (OSS-инструмента нет); blueprinter (прямого эстетического нет); sensory-writing-coach (прямого нет); teach (stateful-механика); meta (диспетчер слоёв); executing-plans (критическое ревью + STOP-протокол — пробел экосистемы); prototype LOGIC-ветка; retro (сессия→правила с аппрувом); sus (измерение коллизий триггеров); multimodal-video-retakes-editor (мультимодальный отбор лучшего дубля через vision); attentional-blindness-analyzer (ядро — модель внимания); leverage (операционализация).

## Топ-5: внешний инструмент явно зрелее скилла (гипотезы для эвала)

1. **bottleneck-identifier → k6**: скилл — пустой шаблон с нулём механик; k6 — production-инструмент нагрузочного тестирования (AGPL-3.0, ~31.7k★, активен). Самый яркий случай «скилл проигрывает аналогу».
2. **webapp-testing → Playwright**: скилл — тонкая обёртка (`with_server.py` поверх нативных Playwright-скриптов, ~97k★); инструментально не добавляет ничего.
3. **performance-profiling → Lighthouse**: единственный скрипт скилла — обёртка над Lighthouse (~30.8k★); Web Vitals и workflow полностью покрываются Lighthouse CI.
4. **test-driven-development → StrykerJS**: скилл проверяет «тест упал по правильной причине» глазами агента (субъективно); StrykerJS делает это механически через мутации — объективно и воспроизводимо.
5. **find-skills → Skills CLI (vercel-labs/skills)**: вся механическая часть скилла (find/add/update/list/remove/init, 75+ агентов, 47 релизов, MIT) покрыта зрелым продуктом; у скилла остаётся только workflow формулировки запроса.
