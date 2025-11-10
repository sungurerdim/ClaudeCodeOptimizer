---
metadata:
  name: "TypeScript Async Patterns"
  activation_keywords: ["async", "promise", "await", "concurrent", "error"]
  category: "language-typescript"
---

# TypeScript Async Patterns

Master async/await patterns and Promise handling for robust asynchronous TypeScript code.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Core Async Concepts:**
- `async` functions return Promise automatically
- `await` pauses execution until Promise resolves
- `Promise.all()` runs multiple promises concurrently
- `Promise.race()` returns first completed promise
- `Promise.allSettled()` waits for all (includes rejected)

**Key Patterns:**
1. Always handle errors with try/catch or .catch()
2. Use `Promise.all()` for concurrent independent operations
3. Type Promise return values: `Promise<T>`
4. Avoid mixing callbacks and Promises (promisify callbacks)
5. Use AbortController for cancellable requests

**Error Handling:**
- Wrap async code in try/catch blocks
- Handle errors at appropriate level (don't swallow)
- Use custom error types for different failure modes
- Implement retry logic for transient failures

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Basic Async/Await:**
```typescript
// Type-safe async function
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

// Error handling
async function getUserSafely(id: number): Promise<User | null> {
  try {
    return await fetchUser(id);
  } catch (error) {
    console.error('Failed to fetch user:', error);
    return null;
  }
}
```

**Concurrent Execution:**
```typescript
// ✗ Sequential (slow) - 3 seconds total
async function fetchAllSequential() {
  const user = await fetchUser(1);      // 1 second
  const posts = await fetchPosts(1);    // 1 second
  const comments = await fetchComments(1); // 1 second
  return { user, posts, comments };
}

// ✓ Concurrent (fast) - 1 second total
async function fetchAllConcurrent() {
  const [user, posts, comments] = await Promise.all([
    fetchUser(1),
    fetchPosts(1),
    fetchComments(1),
  ]);
  return { user, posts, comments };
}

// ✓ Concurrent with error resilience
async function fetchAllSettled() {
  const results = await Promise.allSettled([
    fetchUser(1),
    fetchPosts(1),
    fetchComments(1),
  ]);

  return results.map(result =>
    result.status === 'fulfilled' ? result.value : null
  );
}
```

**Promise Utilities:**
```typescript
// Promise.race - timeout implementation
async function fetchWithTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number
): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), timeoutMs)
  );
  return Promise.race([promise, timeout]);
}

// Usage
try {
  const data = await fetchWithTimeout(fetchUser(1), 5000);
} catch (error) {
  console.error('Request timed out or failed');
}
```

**Retry Logic:**
```typescript
async function retry<T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  delayMs: number = 1000
): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) throw error;

      console.log(`Attempt ${attempt} failed, retrying...`);
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
  throw new Error('Unreachable');
}

// Usage
const user = await retry(() => fetchUser(1), 3, 2000);
```

**AbortController for Cancellation:**
```typescript
async function fetchWithCancel(
  url: string,
  signal: AbortSignal
): Promise<Response> {
  const response = await fetch(url, { signal });
  return response;
}

// Usage
const controller = new AbortController();

// Start request
const promise = fetchWithCancel('/api/data', controller.signal);

// Cancel after 5 seconds
setTimeout(() => controller.abort(), 5000);

try {
  const response = await promise;
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Request cancelled');
  }
}
```

**Async Iterators:**
```typescript
async function* generateNumbers(count: number) {
  for (let i = 0; i < count; i++) {
    await new Promise(resolve => setTimeout(resolve, 100));
    yield i;
  }
}

// Usage
async function processNumbers() {
  for await (const num of generateNumbers(10)) {
    console.log(num);
  }
}
```

**Error Handling Patterns:**
```typescript
// Custom error types
class APIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public response?: unknown
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// Type-safe error handling
async function fetchUserWithTypedErrors(
  id: number
): Promise<User> {
  const response = await fetch(`/api/users/${id}`);

  if (!response.ok) {
    throw new APIError(
      'Failed to fetch user',
      response.status,
      await response.json()
    );
  }

  return response.json();
}

// Handle specific errors
try {
  const user = await fetchUserWithTypedErrors(1);
} catch (error) {
  if (error instanceof APIError) {
    if (error.statusCode === 404) {
      console.log('User not found');
    } else if (error.statusCode >= 500) {
      console.log('Server error');
    }
  } else {
    console.log('Unknown error:', error);
  }
}
```

**Async Queue:**
```typescript
class AsyncQueue<T> {
  private queue: Array<() => Promise<T>> = [];
  private running = 0;

  constructor(private concurrency: number = 1) {}

  async add(fn: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push(async () => {
        try {
          const result = await fn();
          resolve(result);
          return result;
        } catch (error) {
          reject(error);
          throw error;
        }
      });
      this.process();
    });
  }

  private async process() {
    if (this.running >= this.concurrency || this.queue.length === 0) {
      return;
    }

    this.running++;
    const fn = this.queue.shift()!;

    try {
      await fn();
    } finally {
      this.running--;
      this.process();
    }
  }
}

// Usage - limit concurrent requests
const queue = new AsyncQueue(2);  // Max 2 concurrent
const promises = [1, 2, 3, 4, 5].map(id =>
  queue.add(() => fetchUser(id))
);
const users = await Promise.all(promises);
```

**Promise Wrapping (Promisify):**
```typescript
// Convert callback to Promise
function promisify<T>(
  fn: (callback: (error: Error | null, result?: T) => void) => void
): Promise<T> {
  return new Promise((resolve, reject) => {
    fn((error, result) => {
      if (error) reject(error);
      else resolve(result!);
    });
  });
}

// Usage
const readFile = (path: string, callback: (err: Error | null, data?: string) => void) => {
  // Legacy callback API
};

async function readAsync(path: string): Promise<string> {
  return promisify(callback => readFile(path, callback));
}
```

**Async Event Handling:**
```typescript
class AsyncEventEmitter<T extends Record<string, any>> {
  private handlers = new Map<keyof T, Set<(data: any) => Promise<void>>>();

  on<K extends keyof T>(
    event: K,
    handler: (data: T[K]) => Promise<void>
  ): void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);
  }

  async emit<K extends keyof T>(event: K, data: T[K]): Promise<void> {
    const handlers = this.handlers.get(event);
    if (!handlers) return;

    await Promise.all(
      Array.from(handlers).map(handler => handler(data))
    );
  }
}

// Usage
const emitter = new AsyncEventEmitter<{
  'user:save': { id: number };
}>();

emitter.on('user:save', async (data) => {
  await sendEmail(data.id);
});

await emitter.emit('user:save', { id: 1 });
```

**Testing Async Code:**
```typescript
import { describe, it, expect } from 'vitest';

describe('fetchUser', () => {
  it('should fetch user successfully', async () => {
    const user = await fetchUser(1);
    expect(user.id).toBe(1);
  });

  it('should handle errors', async () => {
    await expect(fetchUser(-1)).rejects.toThrow('HTTP 404');
  });

  it('should timeout after 5 seconds', async () => {
    await expect(
      fetchWithTimeout(fetchUser(1), 5000)
    ).rejects.toThrow('Timeout');
  });
});
```

**Anti-Patterns to Avoid:**
```typescript
// ✗ Don't mix async/await with .then()
async function bad() {
  return fetchUser(1).then(user => user.name);  // Confusing
}

// ✓ Consistent async/await
async function good() {
  const user = await fetchUser(1);
  return user.name;
}

// ✗ Don't forget to await
async function bad2() {
  fetchUser(1);  // Promise ignored!
  return 'done';
}

// ✓ Always await promises
async function good2() {
  await fetchUser(1);
  return 'done';
}

// ✗ Don't use async without await
async function bad3() {
  return 42;  // Unnecessary async
}

// ✓ Only use async when needed
function good3() {
  return 42;
}
```
