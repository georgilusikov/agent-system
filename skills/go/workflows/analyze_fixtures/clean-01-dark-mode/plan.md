# Plan: Dark mode toggle

## Phase 1: Design tokens

- **Step 1.1.** Определить CSS-переменные в `:root` и `[data-theme="dark"]` для surface, text, border, accent. Все цвета — через tokens, без хардкода.

## Phase 2: Theme switcher

- **Step 2.1.** React-контекст `ThemeProvider` с тремя значениями (light/dark/system).
- **Step 2.2.** UI-компонент `<ThemeToggle>` с тремя radio-опциями в /settings.
- **Step 2.3.** Persistence в localStorage ключ `theme-preference`.

## Phase 3: FOUC prevention

- **Step 3.1.** Inline `<script>` в `<head>` index.html — читает localStorage и выставляет `data-theme` атрибут до рендера React.

## Phase 4: Accessibility

- **Step 4.1.** Audit всех foreground/background пар на WCAG AA. Инструмент — axe-core.
