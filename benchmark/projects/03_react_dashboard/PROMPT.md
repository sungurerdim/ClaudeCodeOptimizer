# Project: Analytics Dashboard

Build a responsive analytics dashboard using React and TypeScript.

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

## Success Criteria
- All components render correctly
- Charts update on filter changes
- Table sorting and pagination work
- WebSocket reconnects automatically
- Mobile responsive (breakpoints: sm, md, lg)
- No console errors/warnings
- Tests cover main user flows
