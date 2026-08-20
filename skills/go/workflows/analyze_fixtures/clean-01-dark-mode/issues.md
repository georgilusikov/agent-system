# Issues: Dark mode toggle

## DARK-1 — Design tokens and CSS variables
- **Phase:** 1.1
- **Est:** 1 day
- **Blocked by:** —
- **AC:** Все цвета в приложении используют CSS-переменные. Переменные определены для light и `[data-theme="dark"]`. Storybook показывает обе темы.

## DARK-2 — ThemeProvider context
- **Phase:** 2.1
- **Est:** 0.5 day
- **Blocked by:** DARK-1
- **AC:** Context выставляет `data-theme` атрибут на `<html>`. Поддерживает значения light/dark/system. При system — слушает `prefers-color-scheme` listener.

## DARK-3 — ThemeToggle UI in /settings
- **Phase:** 2.2
- **Est:** 0.5 day
- **Blocked by:** DARK-2
- **AC:** В /settings три radio-опции. Выбор мгновенно меняет тему. Selected-state визуально корректен в обеих темах.

## DARK-4 — localStorage persistence
- **Phase:** 2.3
- **Est:** 0.25 day
- **Blocked by:** DARK-2
- **AC:** ThemeProvider пишет в `theme-preference` при смене. На mount читает значение, дефолт — `system`.

## DARK-5 — FOUC prevention inline script
- **Phase:** 3.1
- **Est:** 0.5 day
- **Blocked by:** DARK-4
- **AC:** Inline скрипт в `<head>` выставляет `data-theme` до React-рендера. Нет вспышки светлой темы при загрузке страницы с dark-выбором.

## DARK-6 — WCAG AA contrast audit
- **Phase:** 4.1
- **Est:** 1 day
- **Blocked by:** DARK-1
- **AC:** axe-core проходит для всех страниц в обеих темах без contrast-violations. Ручная проверка ключевых UI-элементов (кнопки, формы, алерты) на ≥ 4.5:1.
