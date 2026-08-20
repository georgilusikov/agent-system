# Protocol: UI Component Matrix

**Applicability**: Frontend Tasks (React, Vue, HTML/CSS).
**Trigger**: Any task involving "Create page", "Add button", "Design interface".

## Rule
Before writing any implementation code (JSX/TSX), you must generate a `UI_COMPONENT_MATRIX.md` table. This ensures visual consistency and prevents "Frankenstein UI".

## Template

```markdown
# UI Component Matrix: [Feature Name]

## Design Variables
- **Color Palette**: `bg-base-100` (Main), `text-primary` (Accent)
- **Typography**: `font-sans` (Inter)
- **Spacing**: `p-4`, `gap-2`

## Components

| Component Name | Visual Description (Tailwind) | Idle State | Hover State | Active/Focus State | Logic Binding |
|----------------|-------------------------------|------------|-------------|--------------------|---------------|
| `MainButton`   | Rounded-xl, `h-12`, Glass     | `bg-white/10` | `bg-white/20` | `scale-95` | `onClick={handleClick}` |
| `InputArgs`    | Bordered, `bg-base-200`       | `border-base-300` | `border-primary` | `ring-2 ring-primary` | `value={arg}` |

## Layout Strategy
- **Container**: `max-w-4xl mx-auto`
- **Grid**: `grid-cols-1 md:grid-cols-2`
- **Routing**: Use `HashRouter` (Tauri/Local compatibility)

## Atomic Element Check
- **Close Buttons**: Must reset parent state (e.g. `setShow(false)`).
- **Z-Index**: Overlays must have explicit high z-index and background visibility logic.
```

## Enforcement
1. **Pre-check**: Does `globals.css` exist? Use its variables.
2. **Consistency**: Do not mix `px-` values with Tailwind utilities if possible.
3. **Verification**: After implementation, verify that the code matches this matrix.
