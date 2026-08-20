# Tremor Dashboard Patterns

## Table of Contents

- [KPI Card Row](#kpi-card-row)
- [Chart + Summary Section](#chart--summary-section)
- [Data Table with Filters](#data-table-with-filters)
- [Overview Dashboard Layout](#overview-dashboard-layout)
- [Status/Monitoring Grid](#statusmonitoring-grid)
- [Comparison Layout](#comparison-layout)

## KPI Card Row

The most common dashboard pattern: a row of metric cards at the top.

```tsx
// Tremor Raw style
const kpis = [
  { title: "Revenue", metric: "$34,743", change: "+12.3%", changeType: "positive" },
  { title: "Users", metric: "2,345", change: "-3.1%", changeType: "negative" },
  { title: "Orders", metric: "1,234", change: "+8.2%", changeType: "positive" },
]

<div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
  {kpis.map((kpi) => (
    <Card key={kpi.title}>
      <p className="text-sm text-gray-500 dark:text-gray-500">{kpi.title}</p>
      <p className="mt-1 text-3xl font-semibold text-gray-900 dark:text-gray-50">
        {kpi.metric}
      </p>
      <Badge
        className="mt-2"
        variant={kpi.changeType === "positive" ? "success" : "error"}
      >
        {kpi.change}
      </Badge>
    </Card>
  ))}
</div>
```

## Chart + Summary Section

Chart with contextual summary metrics above.

```tsx
<Card>
  <div className="flex items-start justify-between">
    <div>
      <p className="text-sm text-gray-500">Total Revenue</p>
      <p className="mt-1 text-3xl font-semibold text-gray-900">$45,231</p>
    </div>
    <Badge variant="success">+20.1%</Badge>
  </div>
  <AreaChart
    className="mt-6 h-72"
    data={chartdata}
    index="date"
    categories={["Revenue"]}
    colors={["blue"]}
    valueFormatter={(n) => `$${Intl.NumberFormat("us").format(n)}`}
  />
</Card>
```

## Data Table with Filters

Table with search/filter controls.

```tsx
const [search, setSearch] = useState("")
const filtered = data.filter((item) =>
  item.name.toLowerCase().includes(search.toLowerCase())
)

<Card>
  <div className="flex items-center justify-between">
    <h3 className="text-lg font-semibold text-gray-900">Sales People</h3>
    <Input
      placeholder="Search..."
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      className="max-w-xs"
    />
  </div>
  <TableRoot className="mt-4">
    <Table>
      <TableHead>
        <TableRow>
          <TableHeaderCell>Name</TableHeaderCell>
          <TableHeaderCell className="text-right">Sales</TableHeaderCell>
          <TableHeaderCell className="text-right">Region</TableHeaderCell>
          <TableHeaderCell className="text-right">Status</TableHeaderCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {filtered.map((item) => (
          <TableRow key={item.name}>
            <TableCell className="font-medium">{item.name}</TableCell>
            <TableCell className="text-right">{item.sales}</TableCell>
            <TableCell className="text-right">{item.region}</TableCell>
            <TableCell className="text-right">
              <Badge variant={item.status === "active" ? "success" : "warning"}>
                {item.status}
              </Badge>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableRoot>
</Card>
```

## Overview Dashboard Layout

Full dashboard composition: KPIs → Chart → Table.

```tsx
<div className="space-y-6">
  {/* KPI Row */}
  <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
    {kpis.map((kpi) => <KpiCard key={kpi.title} {...kpi} />)}
  </div>

  {/* Charts Row */}
  <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
    <Card>
      <h3 className="text-lg font-semibold">Revenue Over Time</h3>
      <AreaChart className="mt-4 h-72" data={revenueData} index="date"
        categories={["Revenue"]} colors={["blue"]} />
    </Card>
    <Card>
      <h3 className="text-lg font-semibold">Sales by Category</h3>
      <DonutChart className="mt-4 h-72" data={categoryData}
        index="name" category="value" />
    </Card>
  </div>

  {/* Table */}
  <Card>
    <h3 className="text-lg font-semibold">Recent Transactions</h3>
    <TransactionsTable data={transactions} />
  </Card>
</div>
```

## Status/Monitoring Grid

For ops dashboards with status indicators.

```tsx
<Card>
  <h3 className="text-lg font-semibold">Service Health</h3>
  <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
    {services.map((service) => (
      <div key={service.name} className="flex items-center justify-between rounded-lg border p-4">
        <div>
          <p className="font-medium">{service.name}</p>
          <p className="text-sm text-gray-500">{service.latency}ms avg</p>
        </div>
        <div className="flex items-center gap-3">
          <SparkLineChart
            data={service.history}
            index="time"
            categories={["latency"]}
            className="h-8 w-20"
          />
          <Badge variant={service.status === "healthy" ? "success" : "error"}>
            {service.status}
          </Badge>
        </div>
      </div>
    ))}
  </div>
  <Tracker className="mt-6" data={uptimeData} />
</Card>
```

## Comparison Layout

Side-by-side metrics with tab navigation.

```tsx
<Card>
  <TabNavigation>
    <TabNavigationLink href="#" active>Overview</TabNavigationLink>
    <TabNavigationLink href="#">Details</TabNavigationLink>
    <TabNavigationLink href="#">Settings</TabNavigationLink>
  </TabNavigation>

  <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
    <div>
      <p className="text-sm font-medium text-gray-500">This Period</p>
      <p className="mt-1 text-2xl font-semibold">$23,456</p>
      <BarChart className="mt-4 h-48" data={currentData}
        index="date" categories={["Sales"]} colors={["blue"]} />
    </div>
    <div>
      <p className="text-sm font-medium text-gray-500">Previous Period</p>
      <p className="mt-1 text-2xl font-semibold">$19,234</p>
      <BarChart className="mt-4 h-48" data={previousData}
        index="date" categories={["Sales"]} colors={["gray"]} />
    </div>
  </div>
</Card>
```
