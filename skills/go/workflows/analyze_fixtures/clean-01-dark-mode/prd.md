# PRD: Dark mode toggle

## Problem

Пользователи работают вечером, яркий белый UI раздражает. 14% в feedback-форме просили dark mode. Хотим дать простой переключатель.

## User stories

### US-1: Toggle theme from settings
Как пользователь, я хочу переключать тему (light/dark/system) в настройках, чтобы выбрать комфортный вид.

**Acceptance:**
- В /settings переключатель с тремя опциями: Light, Dark, System
- Выбор сохраняется в localStorage
- При "System" тема следует за `prefers-color-scheme` OS

### US-2: Persist theme across sessions
Как пользователь, я хочу чтобы мой выбор темы сохранялся между сессиями и не менялся при каждом логине.

**Acceptance:**
- После выбора темы и перезагрузки страницы тема остаётся
- При первом заходе без выбора — применяется System
- Нет вспышки светлой темы при загрузке страницы с dark-выбором (FOUC prevention)

## NFR

- **Accessibility:** все текстовые комбинации foreground/background в обеих темах должны иметь contrast ratio ≥ 4.5:1 (WCAG AA).
