---
metadata:
  name: "Testing with Vitest"
  activation_keywords: ["test", "vitest", "mock", "component", "coverage"]
  category: "language-typescript"
---

# Testing with Vitest

Master Vitest testing patterns for fast, modern TypeScript testing with great DX.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Vitest Overview:**
- Vite-powered test framework (extremely fast)
- Jest-compatible API (easy migration)
- Built-in TypeScript support
- Native ESM support
- Watch mode with HMR-like speed
- Built-in coverage with c8

**Key Patterns:**
1. Use `describe` blocks for test organization
2. Mock external dependencies with `vi.mock()`
3. Use `beforeEach`/`afterEach` for setup/cleanup
4. Test async code with async/await
5. Use snapshots sparingly (prefer explicit assertions)

**Test Structure:**
- Unit tests: Test individual functions/classes
- Integration tests: Test module interactions
- Component tests: Test UI components
- E2E tests: Use Playwright/Cypress separately

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Basic Test Setup (vitest.config.ts):**
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,  // No imports needed for describe, it, expect
    environment: 'node',  // or 'jsdom' for browser APIs
    coverage: {
      provider: 'c8',
      reporter: ['text', 'html', 'lcov'],
      exclude: ['**/*.test.ts', '**/node_modules/**'],
    },
    setupFiles: './tests/setup.ts',
  },
});
```

**Basic Tests:**
```typescript
import { describe, it, expect } from 'vitest';
import { sum, divide } from './math';

describe('math functions', () => {
  it('should add two numbers', () => {
    expect(sum(2, 3)).toBe(5);
    expect(sum(-1, 1)).toBe(0);
  });

  it('should divide two numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  it('should throw on division by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });
});
```

**Mocking:**
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchUser, UserService } from './user-service';

// Mock module
vi.mock('./api-client', () => ({
  apiClient: {
    get: vi.fn(),
  },
}));

describe('UserService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should fetch user', async () => {
    const mockUser = { id: 1, name: 'Alice' };
    const { apiClient } = await import('./api-client');

    vi.mocked(apiClient.get).mockResolvedValue(mockUser);

    const user = await fetchUser(1);

    expect(user).toEqual(mockUser);
    expect(apiClient.get).toHaveBeenCalledWith('/users/1');
  });
});
```

**Spies and Stubs:**
```typescript
import { describe, it, expect, vi } from 'vitest';

describe('event handling', () => {
  it('should call callback on event', () => {
    const callback = vi.fn();
    const emitter = new EventEmitter();

    emitter.on('test', callback);
    emitter.emit('test', { data: 'value' });

    expect(callback).toHaveBeenCalledOnce();
    expect(callback).toHaveBeenCalledWith({ data: 'value' });
  });

  it('should spy on existing method', () => {
    const obj = { method: () => 'original' };
    const spy = vi.spyOn(obj, 'method');

    obj.method();

    expect(spy).toHaveBeenCalled();
    expect(spy).toHaveReturnedWith('original');
  });

  it('should stub method return value', () => {
    const obj = { method: () => 'original' };
    vi.spyOn(obj, 'method').mockReturnValue('mocked');

    expect(obj.method()).toBe('mocked');
  });
});
```

**Async Testing:**
```typescript
import { describe, it, expect } from 'vitest';

describe('async operations', () => {
  it('should fetch data', async () => {
    const data = await fetchData();
    expect(data).toBeDefined();
  });

  it('should handle errors', async () => {
    await expect(fetchInvalidData()).rejects.toThrow('Not found');
  });

  it('should resolve promise', () => {
    return expect(fetchData()).resolves.toEqual({ status: 'ok' });
  });
});
```

**Setup and Teardown:**
```typescript
import { describe, it, expect, beforeEach, afterEach, beforeAll, afterAll } from 'vitest';

describe('database operations', () => {
  let db: Database;

  beforeAll(async () => {
    // Runs once before all tests
    db = await Database.connect();
  });

  afterAll(async () => {
    // Runs once after all tests
    await db.disconnect();
  });

  beforeEach(async () => {
    // Runs before each test
    await db.clear();
  });

  afterEach(async () => {
    // Runs after each test
    await db.rollback();
  });

  it('should insert record', async () => {
    await db.insert({ name: 'Alice' });
    const count = await db.count();
    expect(count).toBe(1);
  });
});
```

**Parametrized Tests:**
```typescript
import { describe, it, expect } from 'vitest';

describe.each([
  { input: 2, expected: 4 },
  { input: 3, expected: 9 },
  { input: 4, expected: 16 },
])('square($input)', ({ input, expected }) => {
  it(`should return ${expected}`, () => {
    expect(square(input)).toBe(expected);
  });
});

// Alternative syntax
it.each([
  [1, 1],
  [2, 4],
  [3, 9],
])('square(%i) should equal %i', (input, expected) => {
  expect(square(input)).toBe(expected);
});
```

**Testing React Components:**
```typescript
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('should render with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click</Button>);

    fireEvent.click(screen.getByText('Click'));

    expect(onClick).toHaveBeenCalledOnce();
  });

  it('should be disabled', () => {
    render(<Button disabled>Click</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

**Testing Hooks:**
```typescript
import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('should increment counter', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

**Snapshot Testing:**
```typescript
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('should match snapshot', () => {
    const { container } = render(
      <UserProfile user={{ name: 'Alice', email: 'alice@example.com' }} />
    );

    expect(container).toMatchSnapshot();
  });

  // Inline snapshots (better for small data)
  it('should format user data', () => {
    expect(formatUser({ name: 'Alice' })).toMatchInlineSnapshot(`
      {
        "name": "Alice",
        "displayName": "Alice",
      }
    `);
  });
});
```

**Coverage Configuration:**
```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'c8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.ts'],
      exclude: [
        '**/*.test.ts',
        '**/*.spec.ts',
        '**/types.ts',
        '**/index.ts',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
});

// Run with coverage
// npm test -- --coverage
```

**Custom Matchers:**
```typescript
import { expect } from 'vitest';

expect.extend({
  toBeWithinRange(received: number, min: number, max: number) {
    const pass = received >= min && received <= max;
    return {
      pass,
      message: () =>
        pass
          ? `expected ${received} not to be within range ${min} - ${max}`
          : `expected ${received} to be within range ${min} - ${max}`,
    };
  },
});

// Usage
it('should be in range', () => {
  expect(5).toBeWithinRange(1, 10);
});
```

**Testing Errors:**
```typescript
import { describe, it, expect } from 'vitest';

describe('error handling', () => {
  it('should throw error', () => {
    expect(() => {
      throw new Error('Test error');
    }).toThrow('Test error');
  });

  it('should throw specific error type', () => {
    expect(() => {
      throw new TypeError('Wrong type');
    }).toThrow(TypeError);
  });

  it('should reject with error', async () => {
    await expect(Promise.reject(new Error('Failed')))
      .rejects
      .toThrow('Failed');
  });
});
```

**Test Utilities:**
```typescript
// tests/utils.ts
import { vi } from 'vitest';

export function createMockFetch(data: any) {
  return vi.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve(data),
    } as Response)
  );
}

export function waitFor(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Usage
import { createMockFetch } from './utils';

it('should use mock fetch', async () => {
  global.fetch = createMockFetch({ users: [] });
  const data = await fetchUsers();
  expect(data.users).toEqual([]);
});
```

**Anti-Patterns to Avoid:**
```typescript
// ✗ Don't test implementation details
expect(component.state.count).toBe(1);  // Fragile

// ✓ Test behavior
expect(screen.getByText('Count: 1')).toBeInTheDocument();

// ✗ Don't use arbitrary timeouts
await new Promise(resolve => setTimeout(resolve, 1000));

// ✓ Use waitFor from testing library
await waitFor(() => expect(screen.getByText('Loaded')).toBeInTheDocument());

// ✗ Don't share state between tests
let user: User;  // Global state is bad

// ✓ Create fresh state in beforeEach
beforeEach(() => {
  user = createTestUser();
});
```
