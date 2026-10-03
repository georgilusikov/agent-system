# Сверка сторонних скиллов с upstream — итог

Дата: 2026-10-01. Проверено 20 скиллов с origin=third-party в skills-registry.yaml.
Метод: чтение SKILL.md целиком (frontmatter + тело) → сверка поля origin в реестре → веб-поиск фактического upstream → проверка живости (дата последнего коммита/релиза) и расхождения версий.
Источники: чанки `upstream-check-chunk1.md`, `upstream-check-chunk2.md`, `upstream-check-chunk3.md`, `upstream-check-chunk4.md` (все в `registry/`). Чанк 4 собран ранее другим координатором и включён без изменений.

## Сводная таблица — все 20 скиллов

| # | Скилл | Фактический upstream | Жив | Расхождение версий | Маркировка third-party |
|---|---|---|---|---|---|
| 1 | bottleneck-identifier | jeremylongshore/claude-code-plugins-plus-skills (→ tons-of-skills-marketplace), `skills/10-performance-testing/bottleneck-identifier/SKILL.md` | Да (2798★, коммиты до 2026-09-22) | Вровень — посимвольная копия v1.0.0 (MIT) | Верна |
| 2 | code-review | mattpocock/skills, `skills/engineering/code-review/SKILL.md` | Да (273 341★, ~6 дней назад) | Форк с минимальными изменениями (русские триггеры, openai.yaml), по сути вровень | Верна |
| 3 | critical-chain-design | idkras/heroes-harness-playbook-gap-theory-for-ai-and-humans, `.agents/skills/critical-chain-design/SKILL.md` | Условно (3★, ~61 день назад) | Форк с изменениями (выброшены Gap Theory-обрамление, Reasoning Log; добавлены DoD, FORBIDDEN, Hard fail) | Верна |
| 4 | executing-plans | obra/superpowers, `skills/executing-plans` | Да (релиз v6.4.1 от 2026-09-18) | **Отстаём** — слепок ~v6.3.0; upstream в v6.4.1 полностью перестроил скилл (Native execution) | Верна |
| 5 | feynman | cloudflare/cloudflare-docs `.agents/skills/eli5` (+ alchaincyf/feynman-skill — только вдохновение именем) | Да (eli5 обновлён ~10 дней назад) | Форк идей, текст самописный, совпадений нет | Верна по сути; origin_detail вводит в заблуждение |
| 6 | finishing-a-development-branch | obra/superpowers (Jesse Vincent / Prime Radiant), `skills/finishing-a-development-branch` | Да (README 8 дней назад, ~136k★, MIT) | Форк с изменениями (адаптация, версия не зафиксирована) | Верна |
| 7 | frontend-design | anthropics/skills, `skills/frontend-design` | Да (файл 2026-06-09, 179k★) | Вровень — вендоренная копия | Верна |
| 8 | frontend-ui-dark-ts | microsoft/skills (MIT) — импорт через community-реестр | Да (README 6 дней назад, 175 скиллов) | Вровень (копия на момент PR #51, фев. 2026) | Верна; origin_detail неполон (фактический upstream — microsoft/skills) |
| 9 | hypothesis-eval-loop | idkras/heroes-harness-playbook-gap-theory-for-ai-and-humans, `.agents/skills/2-hypothesis-gap-falsification` | Да (v0.1.0 от 26.04.2026, статус active) | Адаптация концептов, каркас самописный | Верна — НЕ own с ложным следом |
| 10 | internal-comms | anthropics/skills, `skills/internal-comms/SKILL.md` | Да (в main, 179k★) | Вровень — посимвольная копия | Верна (уверенность поднята до высокой) |
| 11 | to-spec | mattpocock/skills, `skills/engineering/to-spec/SKILL.md` | Да (head d81f3a18, PR #536, ~18k+★) | Форк с изменениями + отстаёт (тело ≈ upstream ~2026-08-29; head убрал PRD-оговорку и `<spec-template>`) | Верна |
| 12 | to-tickets | mattpocock/skills, `skills/engineering/to-tickets/SKILL.md` | Да (тот же репозиторий) | Тело вровень, адаптирован только description | Верна |
| 13 | triage | mattpocock/skills, `skills/engineering/triage/SKILL.md` | Да (тот же репозиторий) | Тело вровень, адаптирован только description | Верна |
| 14 | user-story-mapping | deanpeters/product-manager-skills, `skills/user-story-mapping/SKILL.md` | Да (v0.79 ~29 дней назад, 6866★) | Вендоренная копия почти посимвольно (выброшены frontmatter-экстры и секция «## Input») | Верна по сути; origin_detail неточен (донор — product-manager-skills, не product-manager-prompts) |
| 15 | wayfinder | mattpocock/skills, `skills/engineering/wayfinder/SKILL.md` | Да (тот же репозиторий) | Тело вровень, адаптирован только description | Верна |
| 16 | moai-domain-uiux | modu-ai/moai-adk, `.moai/archive/skills/v3.0/moai-domain-uiux/SKILL.md` (Apache-2.0) | Да (релиз v3.1 от 2026-08-15, 1227★) | **Отстаём** — локально v2.0.0 от 2026-01-11 vs upstream v3.1.0 от 2026-03-28 | Верна |
| 17 | pdf | anthropics/skills, `skills/pdf` | Да (коммит по папке 2026-02-06, 179k★) | Форк с изменениями (текст переписан, scripts/forms.md/reference.md выброшены, добавлен openai.yaml) | Верна по сути; origin_detail содержит 2 ошибки |
| 18 | performance-profiling | sickn33/agentic-awesome-skills, `skills/performance-profiling` | Да (коммит репозитория 2026-10-01, релиз v18.11.0) | Вендоренная копия, **отстаём на одно изменение** (2026-07-29: `risk: unknown` → `risk: critical`) | Верна |
| 19 | pinokio | pinokiocomputer/pinokio (Cocktail Peanut, MIT) | Да (коммиты 02.09.2026, 8187★) | Неприменимо — скилл про использование инструмента | Верна |
| 20 | playwright | microsoft/playwright-cli, `skills/playwright-cli/SKILL.md` (Apache-2.0) | Да (коммит 2026-09-28, 13 711★) | Форк с изменениями + **отстаёт** (устаревшее имя пакета `@playwright/mcp` → upstream `@playwright/cli`; нет новых разделов: video recording, WebMCP, generate-locator и др.) | Верна |

## Выводы

**Маркировки: 20/20 подтверждены.** Ни одного случая own с ложным следом, ни одного ненайденного источника. Все 20 upstream живы (не архивированы). Три «особо сомнительных» случая разрешены в пользу маркировки:
- `internal-comms` — официально существует в anthropics/skills (подтверждено 4 независимыми provenance-записями); уверенность поднята с низкой до высокой.
- `hypothesis-eval-loop` — heroes-harness-playbook Красинского реален (v0.1.0, 26.04.2026), атрибуция явная; НЕ own с ложным следом.
- `feynman` — оба заявленных источника существуют; содержательный донор — только cloudflare eli5 (идеи верифицируются дословно), alchaincyf/feynman-skill — лишь вдохновение именем.

**Отставание от upstream (5 скиллов):**
- `executing-plans` — критично: upstream v6.4.1 (2026-09-18) полностью перестроил скилл (Native execution); локальный слепок ~v6.3.0 устарел по философии.
- `moai-domain-uiux` — v2.0.0 (2026-01-11) vs v3.1.0 (2026-03-28): Tailwind 3.4→4.x, TypeScript 5.5→5.9+, новые разделы.
- `playwright` — устаревшее имя npm-пакета и отсутствие новых разделов CLI.
- `to-spec` — тело ≈ upstream ~2026-08-29; текущий head расходится (убрана PRD-оговорка, `<spec-template>`).
- `performance-profiling` — одно изменение: `risk: unknown` → `risk: critical` (2026-07-29).

**Вровень (8):** bottleneck-identifier, frontend-design, frontend-ui-dark-ts, internal-comms, to-tickets, triage, user-story-mapping, wayfinder.
**Форк с изменениями без видимого отставания (5):** code-review (минимальные правки), critical-chain-design, feynman (форк идей), finishing-a-development-branch, pdf.
**Адаптация концептов (1):** hypothesis-eval-loop. **Неприменимо (1):** pinokio.

**Лицензионные флаги (не блокеры для маркировки, но юридический след):**
1. `pdf` — самый чувствительный: upstream заявляет `license: Proprietary.`, локально приложен текст Apache License 2.0. Расхождение лицензий проверить отдельно.
2. `user-story-mapping` — upstream CC BY-NC-SA 4.0 (non-commercial, share-alike); локально поле license отсутствует, только унаследованная Provenance-строка. NC-ограничение зафиксировать, если репо используется в коммерческом контексте.
3. `critical-chain-design` — upstream: код Apache 2.0 / текст CC BY 4.0 с обязательной атрибуцией; локально лицензия не заявлена, точного URL репозитория в SKILL.md нет (атрибуция в теле частично покрывает CC BY).
4. Matt Pocock ×5 (`code-review`, `to-spec`, `to-tickets`, `triage`, `wayfinder`) — upstream MIT (© 2026 Matt Pocock, требует сохранения copyright notice); локально атрибуции нет нигде (нет поля license, нет NOTICE/LICENSE). Рекомендация: единый NOTICE-файл на все пять.
5. `executing-plans`, `finishing-a-development-branch` — upstream MIT (obra/superpowers); локально поле license не заявлено.
6. `frontend-ui-dark-ts` — upstream MIT (microsoft/skills); локально поле license не заявлено.
7. `hypothesis-eval-loop` — лицензия upstream не проверялась; локально не заявлена — проверить отдельно.
8. Без флагов: bottleneck-identifier (MIT заявлен локально), frontend-design и internal-comms (маркер совпадает с upstream), feynman (текст самописный), moai-domain-uiux (Apache-2.0 заявлен), performance-profiling (`source: community`), pinokio (неприменимо).

**Прочее вне маркировки:**
- `user-story-mapping`: висячие кросс-ссылки на skills/proto-persona, skills/user-story, skills/problem-statement — этих скиллов локально нет. Кандидат на починку ссылок или добор.
- `internal-comms`: запись origin_detail в реестре была оборвана на полуслове — новая формулировка ниже это исправляет.

## Предложенные правки реестра — ТОЛЬКО НА УТВЕРЖДЕНИЕ, НЕ ПРИМЕНЕНЫ

Никаких изменений в `skills-registry.yaml` не вносилось. Список для утверждения Георгием:

1. `pdf.origin_detail` → «форк официального pdf из anthropics/skills; текст переписан под конвенции репо (визуальное ревью pdftoppm→PNG, пути tmp/pdfs/ и output/pdf/, русские триггеры, openai.yaml); scripts/, forms.md, reference.md выброшены; upstream заявляет license: Proprietary.»
2. `pinokio.origin_detail` → дополнить: «фактический upstream — https://github.com/pinokiocomputer/pinokio (Cocktail Peanut, MIT); скилл — оригинальная методика работы со сторонним продуктом через pterm control plane».
3. `code-review.origin_detail` → «вендоренная копия mattpocock/skills `skills/engineering/code-review/SKILL.md` (MIT); локальные правки: русские триггеры в description, NOT-for-ссылки на /check и /bouncer, добавлен agents/openai.yaml».
4. `bottleneck-identifier.origin_detail` → «вендоренная копия jeremylongshore/claude-code-plugins-plus-skills `skills/10-performance-testing/bottleneck-identifier/SKILL.md` v1.0.0 (MIT, author Jeremy Longshore <jeremy@intentsolutions.io>); репозиторий переименован в jeremylongshore/tons-of-skills-marketplace».
5. `critical-chain-design.origin_detail` → «форк скилла Ильи Красинского из idkras/heroes-harness-playbook-gap-theory-for-ai-and-humans `.agents/skills/critical-chain-design/SKILL.md`; выброшены Credentials, Gap Theory-обрамление, Reasoning Log Protocol; добавлены DoD, FORBIDDEN, Hard fail; upstream: код Apache 2.0, текст CC BY 4.0 с обязательной атрибуцией».
6. `executing-plans.origin_detail` → «вендоренная копия obra/superpowers `skills/executing-plans` версии ~v6.3.0 (MIT); upstream v6.4.1 (2026-09-18) перестроил скилл в Native execution — слепок устарел, кандидат на обновление».
7. `feynman.origin_detail` → «русская самописная карточка режима простого объяснения; механики адаптированы из cloudflare/cloudflare-docs `.agents/skills/eli5` (context before details; запрет снисходительных слов; simplify language, never facts; Apache-2.0); alchaincyf/feynman-skill (MIT) — только вдохновение названием, текст не заимствовался».
8. `finishing-a-development-branch.origin_detail` → «obra/superpowers (Jesse Vincent / Prime Radiant, MIT) — вендоренная копия skills/finishing-a-development-branch с локальной адаптацией (detached HEAD, упрощённый frontmatter); версия не зафиксирована».
9. `frontend-design.origin_detail` → без изменений (уже корректно).
10. `frontend-ui-dark-ts.origin_detail` → «фактический upstream — microsoft/skills (MIT): скилл переименован из fluent-ui-dark-ts (PR #38), mobile-compat из PR #51; импорт через community-реестр (frontmatter source: community, risk: unknown, date_added 2026-02-27)».
11. `hypothesis-eval-loop.origin_detail` → «адаптация концептов heroes-harness-playbook (idkras, Илья Красинский, v0.1.0): `.agents/skills/2-hypothesis-gap-falsification` (baseline/threshold/critical chain, вердикты confirmed/partial/falsified); каркас самописный, копия не посимвольная; карточка гипотезы — адаптация templates/03-hypothesis-card.md».
12. `internal-comms.origin_detail` → «официальный internal-comms из anthropics/skills (skills/internal-comms); вендоренная копия без изменений; уверенность — высокая».
13. `to-spec.origin_detail` → «Matt Pocock — https://github.com/mattpocock/skills (skills/engineering/to-spec), MIT; description адаптирован под локальный формат, тело ≈ upstream ~2026-08-29 (текущий head расходится: убрана PRD-оговорка и <spec-template>)».
14. `to-tickets.origin_detail` → «Matt Pocock — https://github.com/mattpocock/skills (skills/engineering/to-tickets), MIT; description адаптирован, тело вровень с upstream».
15. `triage.origin_detail` → «Matt Pocock — https://github.com/mattpocock/skills (skills/engineering/triage), MIT; description адаптирован, тело вровень (AGENT-BRIEF.md/OUT-OF-SCOPE.md на месте)».
16. `user-story-mapping.origin_detail` → «deanpeters — https://github.com/deanpeters/product-manager-skills (skills/user-story-mapping/SKILL.md), CC BY-NC-SA 4.0; вендоренная копия (выброшены frontmatter-экстры и секция "## Input"); product-manager-prompts — лишь прародитель идеи per Provenance».
17. `wayfinder.origin_detail` → «Matt Pocock — https://github.com/mattpocock/skills (skills/engineering/wayfinder), MIT; description адаптирован, тело вровень с upstream».
