---
metadata:
  name: "Node.js Performance Optimization"
  activation_keywords: ["performance", "v8", "event loop", "memory", "optimization"]
  category: "language-typescript"
---

# Node.js Performance Optimization

Master Node.js performance optimization techniques for TypeScript applications.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Performance Fundamentals:**
- Event loop: Single-threaded async I/O model
- V8 engine: JIT compilation and optimization
- Memory management: Heap, stack, garbage collection
- Profiling tools: Node.js profiler, clinic.js, 0x
- Worker threads: For CPU-intensive tasks

**Key Patterns:**
1. Profile before optimizing (measure, don't guess)
2. Keep event loop unblocked (avoid synchronous operations)
3. Use streams for large data (don't load everything in memory)
4. Cache expensive computations
5. Use worker threads for CPU-bound work

**Common Bottlenecks:**
- Synchronous file I/O blocking event loop
- Memory leaks from unclosed resources
- Inefficient regex patterns
- Large JSON parsing
- Unoptimized database queries

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**Built-in Profiler:**
```bash
# CPU profiling
node --prof app.js

# Process log file
node --prof-process isolate-0x*.log > processed.txt

# Heap snapshot
node --inspect app.js
# Open chrome://inspect in Chrome
# Take heap snapshot
```

**clinic.js Suite:**
```bash
# Install
npm install -g clinic

# Doctor - overall health check
clinic doctor -- node app.js

# Flame - CPU profiling
clinic flame -- node app.js

# Bubbleprof - async operations
clinic bubbleprof -- node app.js

# Heap profiler
clinic heapprofiler -- node app.js
```

**Event Loop Monitoring:**
```typescript
import { performance } from 'perf_hooks';

// Measure event loop lag
let lastCheck = performance.now();

setInterval(() => {
  const now = performance.now();
  const lag = now - lastCheck - 1000;  // Expected 1000ms

  if (lag > 100) {
    console.warn(`Event loop lag: ${lag}ms`);
  }

  lastCheck = now;
}, 1000);

// Better: Use lag monitoring library
import lag from 'event-loop-lag';
const lagMonitor = lag(1000);

setInterval(() => {
  console.log(`Event loop lag: ${lagMonitor()}ms`);
}, 5000);
```

**Avoiding Blocking Operations:**
```typescript
import { readFile, readFileSync } from 'fs';
import { promisify } from 'util';

// ✗ Blocking - freezes event loop
function badRead() {
  const data = readFileSync('large-file.txt', 'utf-8');
  return data;
}

// ✓ Non-blocking - async
const readFileAsync = promisify(readFile);

async function goodRead() {
  const data = await readFileAsync('large-file.txt', 'utf-8');
  return data;
}

// ✓ Even better - streaming
import { createReadStream } from 'fs';

function streamRead() {
  const stream = createReadStream('large-file.txt');
  return stream;
}
```

**Stream Processing:**
```typescript
import { createReadStream, createWriteStream } from 'fs';
import { pipeline } from 'stream/promises';
import { Transform } from 'stream';

// ✗ Bad - loads entire file in memory
async function badProcess(inputPath: string, outputPath: string) {
  const data = await readFileAsync(inputPath, 'utf-8');
  const processed = data.toUpperCase();  // 1GB file = 1GB memory
  await writeFileAsync(outputPath, processed);
}

// ✓ Good - streaming with constant memory
async function goodProcess(inputPath: string, outputPath: string) {
  const transform = new Transform({
    transform(chunk, encoding, callback) {
      callback(null, chunk.toString().toUpperCase());
    },
  });

  await pipeline(
    createReadStream(inputPath),
    transform,
    createWriteStream(outputPath)
  );
}
```

**Worker Threads for CPU-Intensive Tasks:**
```typescript
// main.ts
import { Worker } from 'worker_threads';

function runWorker(data: number[]): Promise<number> {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./worker.js', {
      workerData: data,
    });

    worker.on('message', resolve);
    worker.on('error', reject);
    worker.on('exit', (code) => {
      if (code !== 0) {
        reject(new Error(`Worker stopped with exit code ${code}`));
      }
    });
  });
}

// worker.ts
import { parentPort, workerData } from 'worker_threads';

function cpuIntensive(data: number[]): number {
  // Heavy computation
  return data.reduce((sum, n) => sum + n ** 2, 0);
}

const result = cpuIntensive(workerData);
parentPort?.postMessage(result);
```

**Memory Optimization:**
```typescript
// ✗ Memory leak - event listeners not cleaned
class BadService {
  constructor() {
    process.on('SIGINT', () => this.cleanup());
  }
}

// ✓ Proper cleanup
class GoodService {
  private cleanupHandler = () => this.cleanup();

  constructor() {
    process.on('SIGINT', this.cleanupHandler);
  }

  destroy() {
    process.removeListener('SIGINT', this.cleanupHandler);
  }

  private cleanup() {
    // Cleanup logic
  }
}

// ✗ Large objects in closure
function badCache() {
  const cache = new Map();  // Grows forever
  return (key: string) => cache.get(key);
}

// ✓ LRU cache with size limit
import LRU from 'lru-cache';

function goodCache() {
  const cache = new LRU({ max: 500, ttl: 1000 * 60 * 5 });
  return (key: string) => cache.get(key);
}
```

**JSON Performance:**
```typescript
import { performance } from 'perf_hooks';

// ✗ Slow - JSON.parse/stringify for large objects
function badClone(obj: any) {
  return JSON.parse(JSON.stringify(obj));
}

// ✓ Faster - structured clone (Node 17+)
function goodClone(obj: any) {
  return structuredClone(obj);
}

// For JSON parsing - use streaming for large files
import { parser } from 'stream-json';
import { streamArray } from 'stream-json/streamers/StreamArray';

async function parseJsonStream(path: string) {
  const stream = createReadStream(path)
    .pipe(parser())
    .pipe(streamArray());

  for await (const { value } of stream) {
    // Process each array element individually
    console.log(value);
  }
}
```

**Database Query Optimization:**
```typescript
// ✗ N+1 queries
async function badGetUsers() {
  const users = await db.query('SELECT * FROM users');

  for (const user of users) {
    user.posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [user.id]);
  }

  return users;
}

// ✓ Single query with JOIN
async function goodGetUsers() {
  const result = await db.query(`
    SELECT users.*, posts.*
    FROM users
    LEFT JOIN posts ON posts.user_id = users.id
  `);

  // Group by user
  return groupByUser(result);
}

// ✓ Batch queries
async function batchGetUsers() {
  const users = await db.query('SELECT * FROM users');
  const userIds = users.map(u => u.id);

  const posts = await db.query(
    'SELECT * FROM posts WHERE user_id IN (?)',
    [userIds]
  );

  return mergeUsersPosts(users, posts);
}
```

**Caching Strategies:**
```typescript
import { createClient } from 'redis';

// In-memory cache
const cache = new Map<string, { value: any; expires: number }>();

function getWithCache<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number = 60000
): Promise<T> {
  const cached = cache.get(key);

  if (cached && cached.expires > Date.now()) {
    return Promise.resolve(cached.value);
  }

  return fetcher().then(value => {
    cache.set(key, { value, expires: Date.now() + ttl });
    return value;
  });
}

// Redis cache
const redis = createClient();

async function getWithRedis<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number = 60
): Promise<T> {
  const cached = await redis.get(key);

  if (cached) {
    return JSON.parse(cached);
  }

  const value = await fetcher();
  await redis.setEx(key, ttl, JSON.stringify(value));
  return value;
}
```

**Profiling Decorators:**
```typescript
function measure() {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const original = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const start = performance.now();
      try {
        return await original.apply(this, args);
      } finally {
        const duration = performance.now() - start;
        console.log(`${propertyKey} took ${duration.toFixed(2)}ms`);
      }
    };
  };
}

class UserService {
  @measure()
  async getUser(id: number) {
    // Method automatically timed
    return await db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}
```

**V8 Optimization Tips:**
```typescript
// ✗ Polymorphic functions (slow)
function badAdd(a: any, b: any) {
  return a + b;  // Different types = deoptimization
}

// ✓ Monomorphic functions (fast)
function goodAdd(a: number, b: number): number {
  return a + b;  // Always numbers = optimized
}

// ✗ Hidden class changes (slow)
const obj: any = {};
obj.a = 1;  // Hidden class v1
obj.b = 2;  // Hidden class v2 (different shape)

// ✓ Consistent object shape (fast)
const obj2 = { a: 0, b: 0 };  // Single hidden class
obj2.a = 1;
obj2.b = 2;

// ✗ Arguments object (slow)
function badFunc() {
  return Array.from(arguments);
}

// ✓ Rest parameters (fast)
function goodFunc(...args: any[]) {
  return args;
}
```

**Performance Monitoring:**
```typescript
import { performance, PerformanceObserver } from 'perf_hooks';

// Mark performance points
performance.mark('start-operation');
await performOperation();
performance.mark('end-operation');

// Measure duration
performance.measure('operation', 'start-operation', 'end-operation');

// Observe measurements
const obs = new PerformanceObserver((items) => {
  items.getEntries().forEach((entry) => {
    console.log(`${entry.name}: ${entry.duration}ms`);
  });
});

obs.observe({ entryTypes: ['measure'] });
```

**Anti-Patterns to Avoid:**
```typescript
// ✗ Don't use sync methods in production
const data = readFileSync('file.txt');  // Blocks event loop

// ✗ Don't create excessive promises
for (let i = 0; i < 10000; i++) {
  promises.push(fetchData(i));  // Memory spike
}

// ✓ Limit concurrency
const concurrency = 10;
for (let i = 0; i < items.length; i += concurrency) {
  await Promise.all(items.slice(i, i + concurrency).map(process));
}

// ✗ Don't ignore backpressure in streams
readable.on('data', (chunk) => {
  writable.write(chunk);  // Can overwhelm writable
});

// ✓ Handle backpressure
readable.on('data', (chunk) => {
  if (!writable.write(chunk)) {
    readable.pause();
  }
});
writable.on('drain', () => readable.resume());
```
