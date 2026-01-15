# Project: Analytics Dashboard

Build a responsive analytics dashboard using React and TypeScript.

---

## Autonomous Operation

**Execute this task completely without user interaction:**

1. **Proceed autonomously** - Make reasonable decisions without asking
2. **Implement all requirements** - Complete every feature listed below
3. **Write working code** - All components must render and function
4. **Include tests** - Test coverage for main user flows
5. **Handle errors gracefully** - Error boundaries and fallback UI
6. **No slash commands** - Do NOT use `/help`, `/commit`, or any `/` commands (not available in this execution mode)

**Prioritized execution order:**
1. Project setup (Vite, TypeScript, Tailwind)
2. Layout and navigation structure
3. Metric cards with mock data
4. Charts section (line, bar, pie, area)
5. Data table with sorting/pagination
6. Filters (date range, category, status)
7. WebSocket integration for real-time
8. Tests

---

## Requirements

### Core Features

1. **Dashboard Overview**
   - Key metrics cards (total users, revenue, conversion rate, active sessions)
   - Cards show current value + % change from previous period
   - Click card to see detailed breakdown

2. **Charts Section**
   - Line chart: Daily active users (last 30 days)
   - Bar chart: Revenue by category
   - Pie chart: Traffic sources distribution
   - Area chart: User engagement over time
   - All charts interactive (hover tooltips, click to filter)

3. **Data Table**
   - Recent transactions/events table
   - Columns: ID, User, Event, Amount, Timestamp, Status
   - Sortable columns (click header)
   - Pagination (10/25/50 per page)
   - Search/filter functionality
   - Export to CSV

4. **Filters**
   - Date range picker (preset: Today, Last 7 days, Last 30 days, Custom)
   - Category multi-select
   - Status filter (dropdown)
   - All filters update all components

5. **Real-time Updates**
   - WebSocket connection for live metrics
   - New data animates in
   - Connection status indicator
   - Auto-reconnect on disconnect

### Technical Requirements

- React 18+ with TypeScript
- Vite for build
- Recharts for visualizations
- TanStack Query for data fetching
- Zustand for state management
- Tailwind CSS for styling
- Vitest for testing
- MSW for API mocking

### Project Structure

```
dashboard/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── components/
│   │   ├── cards/
│   │   ├── charts/
│   │   ├── table/
│   │   ├── filters/
│   │   └── common/
│   ├── hooks/
│   ├── stores/
│   ├── services/
│   ├── types/
│   └── utils/
├── tests/
├── public/
└── package.json
```

### Component Specifications

**MetricCard**
```typescript
interface MetricCardProps {
  title: string;
  value: number | string;
  change: number; // percentage
  trend: 'up' | 'down' | 'neutral';
  icon: ReactNode;
  onClick?: () => void;
}
```

**DataTable**
```typescript
interface DataTableProps<T> {
  data: T[];
  columns: ColumnDef<T>[];
  pagination: PaginationState;
  onSort: (column: string, direction: 'asc' | 'desc') => void;
  onFilter: (filters: FilterState) => void;
  onExport: () => void;
}
```

---

## Success Criteria

| Priority | Requirement | Validation |
|----------|-------------|------------|
| P0 | All components render correctly | No console errors |
| P0 | Charts display data | Visual verification |
| P1 | Charts update on filter changes | Filter triggers re-render |
| P1 | Table sorting and pagination work | Click column to sort |
| P1 | Mobile responsive | Works at sm, md, lg breakpoints |
| P2 | WebSocket reconnects automatically | Disconnect/reconnect test |
| P2 | Tests cover main user flows | Vitest passes |

**Deliverables:** Working React dashboard, responsive design, test suite.
