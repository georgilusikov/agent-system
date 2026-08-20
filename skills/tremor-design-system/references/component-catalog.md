# Tremor Component Catalog

## Table of Contents

- [Two Versions](#two-versions)
- [Visualization Components](#visualization-components)
- [Input Components](#input-components)
- [UI Components](#ui-components)
- [Utility Functions](#utility-functions)
- [Chart Color System](#chart-color-system)

## Two Versions

Tremor exists in two forms. Determine which version the user's project uses before generating code.

### Tremor Raw (tremor.so) — Copy-and-Paste

- **Import style**: `import { AreaChart } from "@/components/AreaChart"`
- **Requires**: React 18.2+, Tailwind CSS v4+, Radix UI, Recharts
- **Dependencies**: `@radix-ui/react-*`, `recharts`, `@internationalized/date`, `date-fns@3.6.0`, `react-day-picker@8.10.1`, `@react-aria/datepicker`, `@react-stately/datepicker`
- **Theming**: Tailwind CSS utility classes directly
- **Utility file**: Requires `chartUtils.ts` and `lib/utils.ts` with `cx()` helper
- **Components live in**: `src/components/` (user's project)
- **Dark mode classes**: `dark:` prefix on standard Tailwind utilities
- **Font**: Geist Font recommended (not required)

### Tremor NPM (npm.tremor.so) — Package Install

- **Import style**: `import { AreaChart, Card } from "@tremor/react"`
- **Requires**: React 18.2+, Tailwind CSS v3.4+
- **Dependencies**: `@tremor/react`, `@headlessui/react`, `@tailwindcss/forms`, `@remixicon/react`
- **Theming**: `tailwind.config.js` `theme.extend` with Tremor-specific tokens (`tremor-default`, `tremor-content`, etc.)
- **Dark mode classes**: `dark:text-dark-tremor-content`, `dark:bg-dark-tremor-background`, etc.
- **Tailwind config**: Must include `node_modules/@tremor/**/*.{js,ts,jsx,tsx}` in `content`

### Detection Signals

| Signal | Tremor Raw | Tremor NPM |
|--------|-----------|------------|
| Import path | `@/components/*` | `@tremor/react` |
| Tailwind version | v4+ | v3.4+ |
| CSS tokens | Standard Tailwind (`text-gray-900`) | Tremor tokens (`text-tremor-content`) |
| Package.json | No `@tremor/react` | Has `@tremor/react` |
| Component files | In project `src/components/` | In `node_modules` |

## Visualization Components

### AreaChart
Graph with lines and shaded areas.
```tsx
<AreaChart
  data={data}
  index="date"                    // x-axis key
  categories={["Sales", "Costs"]} // data series names
  colors={["blue", "emerald"]}    // optional, from chartColors
  valueFormatter={(n) => `$${n}`} // tooltip/axis format
  yAxisWidth={60}                 // optional
  type="default"                  // "default" | "stacked" | "percent"
  fill="gradient"                 // "gradient" | "solid" | "none"
  connectNulls={false}
  onValueChange={(v) => {}}       // makes chart interactive
  xAxisLabel="Month"
  yAxisLabel="Revenue"
  className="h-80"
/>
```

### BarChart
Vertical or horizontal bars.
```tsx
<BarChart
  data={data}
  index="date"
  categories={["SolarPanels", "Inverters"]}
  colors={["indigo", "rose"]}
  type="default"                  // "default" | "stacked" | "percent"
  layout="vertical"               // "vertical" | "horizontal"
  barCategoryGap="10%"
  onValueChange={(v) => {}}
  className="h-80"
/>
```

### LineChart
Line graph without area fill.
```tsx
<LineChart
  data={data}
  index="date"
  categories={["Revenue", "Expenses"]}
  colors={["blue", "red"]}
  connectNulls={false}
  onValueChange={(v) => {}}
  className="h-80"
/>
```

### DonutChart
Pie/donut visualization.
```tsx
<DonutChart
  data={data}                     // { name: string, value: number }[]
  index="name"
  category="value"
  colors={["blue", "cyan", "indigo"]}
  variant="donut"                 // "donut" | "pie"
  valueFormatter={(n) => `$${n}`}
  label="Total"                   // center label
  showLabel={true}
  className="h-40"
/>
```

### ComboChart
Combined bar and line on single or dual axis.
```tsx
<ComboChart
  data={data}
  index="date"
  barSeries={{
    categories: ["Revenue"],
    colors: ["blue"],
  }}
  lineSeries={{
    categories: ["Trend"],
    colors: ["amber"],
  }}
  className="h-80"
/>
```

### BarList
Horizontal bar rankings.
```tsx
<BarList
  data={[
    { name: "/home", value: 2019 },
    { name: "/about", value: 982 },
  ]}
  valueFormatter={(n) => `${n} views`}
/>
```

### CategoryBar
Segmented horizontal bar (e.g., budget allocation).
```tsx
<CategoryBar
  values={[40, 30, 20, 10]}
  colors={["emerald", "yellow", "orange", "red"]}
  markerValue={62}
  showLabels={true}
/>
```

### ProgressBar
```tsx
<ProgressBar value={72} color="blue" className="mt-2" />
```

### ProgressCircle
```tsx
<ProgressCircle value={72} size="md" color="blue">
  <span className="text-sm font-medium">72%</span>
</ProgressCircle>
```

### SparkChart
Inline micro-visualizations.
```tsx
<SparkAreaChart data={data} index="month" categories={["Performance"]} />
<SparkLineChart data={data} index="month" categories={["Performance"]} />
<SparkBarChart data={data} index="month" categories={["Performance"]} />
```

### Tracker
Status grid (e.g., uptime monitoring).
```tsx
<Tracker
  data={[
    { color: "emerald", tooltip: "Operational" },
    { color: "red", tooltip: "Downtime" },
    { color: "emerald", tooltip: "Operational" },
  ]}
/>
```

## Input Components

### Calendar, DatePicker, DateRangePicker
```tsx
<DatePicker />
<DateRangePicker />
<Calendar />
```

### Checkbox, RadioGroup, RadioCardGroup
```tsx
<Checkbox id="terms" />
<RadioGroup defaultValue="1">
  <RadioGroupItem value="1" id="r1" />
</RadioGroup>
```

### Select, SelectNative
```tsx
<Select defaultValue="1">
  <SelectTrigger />
  <SelectContent>
    <SelectItem value="1">Option 1</SelectItem>
  </SelectContent>
</Select>
```

### Input, Textarea, Slider, Switch, Toggle
Standard form controls styled to match the design system.

### DropdownMenu
```tsx
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="secondary">Options</Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem>Edit</DropdownMenuItem>
    <DropdownMenuItem>Delete</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

## UI Components

### Card
Foundation block for all dashboard compositions.
```tsx
<Card className="max-w-lg">
  <p className="text-tremor-default text-tremor-content">Revenue</p>
  <p className="text-3xl font-semibold">$34,743</p>
</Card>
```

### Table
```tsx
<TableRoot>
  <Table>
    <TableHead>
      <TableRow>
        <TableHeaderCell>Name</TableHeaderCell>
        <TableHeaderCell>Sales</TableHeaderCell>
      </TableRow>
    </TableHead>
    <TableBody>
      <TableRow>
        <TableCell>Peter</TableCell>
        <TableCell>$1,000,000</TableCell>
      </TableRow>
    </TableBody>
  </Table>
</TableRoot>
```

### Accordion, Badge, Button, Callout, Dialog, Divider, Drawer, Popover, Tabs, TabNavigation, Toast, Tooltip
Standard UI primitives. All accept `className` for Tailwind customization.

## Utility Functions

### cx() — Class merger
```ts
import { cx } from "@/lib/utils"
cx("base-class", condition && "conditional-class", className)
```

### chartUtils.ts — Required for charts
Contains `chartColors`, `getColorClassName()`, `getYAxisDomain()`, and `hasOnlyOneValueForKey()`.

Available chart colors: `blue`, `emerald`, `violet`, `amber`, `gray`, `cyan`, `pink`, `lime`, `fuchsia`, `indigo`, `rose`, `yellow`, `green`, `red`, `orange`, `teal`, `purple`, `sky`.

Each color maps to: `bg-{color}-500`, `stroke-{color}-500`, `fill-{color}-500`, `text-{color}-500`.

## Chart Color System

All chart components accept a `colors` prop — an array of color names from the system. Colors are applied in order to the `categories` array.

```tsx
// Two-series chart with explicit colors
<AreaChart
  categories={["Revenue", "Expenses"]}
  colors={["emerald", "rose"]}
/>
```

If `colors` is omitted, defaults cycle through: `blue`, `emerald`, `violet`, `amber`, `gray`, `cyan`, `pink`, `lime`, `fuchsia`.
