---
name: visual-explainer
description: 'Use when the deliverable is a self-contained offline HTML slide deck or diagram page (magazine-quality, открывается файлом в браузере). Triggers: "сделай презентацию", "собери слайды", "html-дек", "оформи как слайд-дек", "generate a slide deck", "визуальный эксплейнер". NOT for: чарты и дашборды как система (/dataviz), inline-виджет в чате (visualize), публикация на claude.ai (Artifact), Figma (/figma-*).'
---

# Visual Explainer — offline HTML slide decks

Форк visual-explainer-course-skill (2026-08-01): взяты references/ + templates/,
SKILL.md переписан (оригинальный вёл мимо метода), surf CLI и rick.ai-пути удалены.
Доставка: **один self-contained HTML-файл** на диске — не Artifact, не чат-виджет.

**Цена внимания: полное чтение references ≈ 44k токенов.** Читать их ТОЛЬКО когда
дек реально генерируется, не при роутинге.

## When to Use
- нужен дек/эксплейнер как файл: презентация, walkthrough, отчёт-история;
- диаграмма с зумом/паном как отдельная страница (templates/mermaid-flowchart.html).

## When NOT to Use
- график/дашборд → /dataviz; виджет в чате → visualize; публикация → Artifact;
- «нарисуй схему» без требования файла → mermaid-фенс прямо в ответе.

## Протокол
1. **Инвентаризация → маппинг → композиция** (метод из references/slide-patterns.md,
   НЕ «скопируй шаблон и замени текст»): аудитория, одна главная мысль, story arc;
   каждому слайду — композиция (centered / split / edge / full-bleed), не более
   двух centered подряд.
2. **Пресет**: один из 4 (Midnight Editorial, Warm Signal, Terminal Mono, Swiss
   Clean) — на все слайды. Не смешивать.
3. **Сборка** от templates/slide-deck.html: SlideEngine, autoFit() до init,
   density limits из slide-patterns.md (буллеты ≤5-6, KPI ≤6 символов, код ≤10 строк).
4. **Mermaid** — только по references/libraries.md: theme base, метки в кавычках,
   classDef без color:, запрещённые AI-slop цвета.
5. **Проверка**: открыть в браузере (или honest NOT CHECKED), 0 незакрытых тегов,
   Mermaid провалидировать парсером, а не глазами.

Эталон вывода: [examples/golden_deck.html](examples/golden_deck.html) — 9 слайдов,
Terminal Mono, все элементы метода, бут-фикс применён.

## Известные грабли
- **Бут-баг исходного шаблона**: падение CDN Mermaid убивает ВСЮ навигацию —
  выноси bootDeck()/autoFit() из module-скрипта + страховочный setTimeout
  (в golden_deck.html уже исправлено, шаблон бандла — нет).
- **Drift внутри references**: css-patterns.md и slide-patterns.md описывают
  Mermaid-контейнер по-разному — канон slide-patterns.md.
- «7 разделов → 18-25 слайдов» из slide-patterns.md — режим конвертации спеки;
  для дека владельцу на решение действует «один слайд = одна мысль», не раздувай.
- CSS-класс `.node` не использовать — коллизия с внутренними классами Mermaid.

## Definition of Done
- [ ] один HTML-файл, открывается локально, внешних хостов ≤3 (CDN Mermaid, шрифты)
- [ ] пресет един на всех слайдах; двух centered подряд нет
- [ ] density limits соблюдены; autoFit присутствует
- [ ] Mermaid провалидирован парсером; бут-фикс применён
- [ ] нет PII и секретов в контенте

## FORBIDDEN
- Слайды по запросу «сделай схему/график» без явного запроса дека (opt-in only)
- Читать 44k референсов на этапе роутинга (только при генерации)
- Смешивать пресеты или вводить свои цвета поверх пресетных палитр
- Внешние хосты сверх CDN Mermaid + Google Fonts (self-contained ломается)

## Hard fail
- Дек выдан без проверки браузером И без честного «NOT CHECKED» — невалиден
- module-скрипт без бут-фикса (CDN-падение убивает навигацию) — невалиден
