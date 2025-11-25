---
name: cco-skill-performance
description: Profile-first application performance optimization covering memory management, CPU profiling, algorithm complexity, async patterns, and resource pooling. No premature optimization.
keywords: [performance, profiling, memory, CPU, async, concurrency, Big O, complexity, optimization, bottleneck, cProfile, py-spy, memory leak, resource pool]
category: performance
related_commands:
  action_types: [audit, optimize, fix]
  categories: [performance]
pain_points: [5]
---

# Application Performance Optimization

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


## Domain
Backend/application performance: memory, CPU, algorithms, async, profiling. (Database optimization → database optimization skill, Frontend → frontend skill)

## Purpose
Identify and fix performance bottlenecks through profiling-first approach. Avoid premature optimization.

**Solves**: Memory leaks, CPU hotspots, algorithm inefficiency, blocking I/O, resource exhaustion

**Impact**: Response time reduction, throughput increase, resource cost savings

---

---

## Core Principle: Profile Before Optimize

**CRITICAL**: Never optimize without profiling data.

```python
# ❌ BAD: Premature optimization
def process_items(items):
    # "This loop is slow, let me optimize"
    return [i ** 2 for i in items]  # Actually fast, not the bottleneck

# ✅ GOOD: Profile first
import cProfile
cProfile.run('process_items(large_list)')
# Output shows: get_data() takes 95% time, not the loop
```

**Profiling Tools by Language:**

| Language | CPU Profiler | Memory Profiler |
|----------|--------------|-----------------|
| Python | cProfile, py-spy | memory_profiler, tracemalloc |
| Node.js | --prof, clinic.js | heapdump, memwatch |
| Java | JProfiler, async-profiler | VisualVM, MAT |
| Go | pprof | pprof (heap) |
| Rust | perf, flamegraph | heaptrack |

---

## CPU Profiling

### Python: cProfile + snakeviz

```python
# Profile script
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
result = expensive_operation()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

**Output interpretation:**
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1000    5.234    0.005   15.678    0.016 api.py:45(fetch_data)
    50000    8.901    0.000    8.901    0.000 utils.py:12(parse_json)
```

- **tottime**: Time in function (excluding calls)
- **cumtime**: Time including called functions
- **Focus**: High cumtime functions first

### Python: py-spy (Production-Safe)

```bash
# Attach to running process (no code changes)
py-spy top --pid 12345

# Generate flame graph
py-spy record -o profile.svg --pid 12345

# Profile command
py-spy record -o profile.svg -- python app.py
```

### Node.js: Clinic.js

```bash
# Install
npm install -g clinic

# CPU profiling
clinic doctor -- node app.js

# Flame graph
clinic flame -- node app.js
```

---

## Memory Profiling

### Python: tracemalloc

```python
import tracemalloc

tracemalloc.start()

# Code to profile
data = load_large_dataset()
process(data)

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("Top 10 memory allocations:")
for stat in top_stats[:10]:
    print(stat)
```

### Python: memory_profiler

```python
from memory_profiler import profile

@profile
def memory_heavy_function():
    data = [i ** 2 for i in range(1000000)]
    filtered = [x for x in data if x % 2 == 0]
    return filtered
```

**Output:**
```
Line #    Mem usage    Increment   Line Contents
     3    38.0 MiB     0.0 MiB   def memory_heavy_function():
     4   114.5 MiB    76.5 MiB       data = [i ** 2 for i in range(1000000)]
     5   133.2 MiB    18.7 MiB       filtered = [x for x in data if x % 2 == 0]
```

### Memory Leak Detection

```python
# ❌ BAD: Memory leak via closure
class DataProcessor:
    def __init__(self):
        self.callbacks = []

    def register(self, callback):
        self.callbacks.append(callback)
        # Callbacks hold references forever

# ✅ GOOD: Weak references
import weakref

class DataProcessor:
    def __init__(self):
        self.callbacks = []

    def register(self, callback):
        self.callbacks.append(weakref.ref(callback))

    def notify(self):
        # Clean up dead references
        self.callbacks = [cb for cb in self.callbacks if cb() is not None]
        for cb_ref in self.callbacks:
            cb = cb_ref()
            if cb:
                cb()
```

---

## Algorithm Complexity (Big O)

### Common Complexities

| Complexity | Name | Example | 1M items |
|------------|------|---------|----------|
| O(1) | Constant | Dict lookup | 1 op |
| O(log n) | Logarithmic | Binary search | 20 ops |
| O(n) | Linear | List scan | 1M ops |
| O(n log n) | Linearithmic | Merge sort | 20M ops |
| O(n²) | Quadratic | Nested loops | 1T ops |
| O(2ⁿ) | Exponential | Subsets | ∞ |

### Optimization Patterns

```python
# ❌ BAD: O(n²) - Nested loop lookup
def find_duplicates_slow(items):
    duplicates = []
    for i, item in enumerate(items):
        for j, other in enumerate(items):
            if i != j and item == other:
                duplicates.append(item)
    return duplicates

# ✅ GOOD: O(n) - Hash set
def find_duplicates_fast(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)

# Performance: 10,000 items
# Slow: ~50 seconds
# Fast: ~0.001 seconds
```

```python
# ❌ BAD: O(n) - List contains check
def process_if_valid_slow(item, valid_list):
    if item in valid_list:  # O(n) each time
        return process(item)

# ✅ GOOD: O(1) - Set contains check
valid_set = set(valid_list)  # One-time O(n) conversion

def process_if_valid_fast(item):
    if item in valid_set:  # O(1) each time
        return process(item)
```

---

## Async & Concurrency

### Async I/O (I/O-bound)

```python
import asyncio
import aiohttp

# ❌ BAD: Sequential HTTP calls
def fetch_all_sync(urls):
    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response.json())
    return results
# 100 URLs × 200ms each = 20 seconds

# ✅ GOOD: Concurrent HTTP calls
async def fetch_all_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch_one(session, url):
    async with session.get(url) as response:
        return await response.json()
# 100 URLs concurrent = ~200ms total
```

### Thread Pool (CPU-bound with GIL release)

```python
from concurrent.futures import ThreadPoolExecutor
import requests

# Good for I/O-bound (GIL released during I/O)
def fetch_with_threads(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(requests.get, urls))
    return results
```

### Process Pool (CPU-bound)

```python
from concurrent.futures import ProcessPoolExecutor
import math

# CPU-intensive computation
def compute_heavy(n):
    return sum(math.sqrt(i) for i in range(n))

# ❌ BAD: Single process
results = [compute_heavy(n) for n in range(1000000, 10000000, 100000)]

# ✅ GOOD: Multi-process
with ProcessPoolExecutor() as executor:
    results = list(executor.map(compute_heavy,
                                range(1000000, 10000000, 100000)))
```

### When to Use What

| Pattern | Use Case | GIL Impact |
|---------|----------|------------|
| `asyncio` | I/O-bound (HTTP, DB, files) | N/A (single thread) |
| `ThreadPoolExecutor` | I/O-bound, simple parallelism | Released during I/O |
| `ProcessPoolExecutor` | CPU-bound computation | Bypasses (separate processes) |

---

## Resource Pooling

### Connection Pool Pattern

```python
# ❌ BAD: Create connection per request
def get_data(query):
    conn = create_connection()  # Expensive: ~50ms
    result = conn.execute(query)
    conn.close()
    return result

# ✅ GOOD: Connection pool
from queue import Queue
import threading

class ConnectionPool:
    def __init__(self, create_conn, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.create_conn = create_conn
        for _ in range(pool_size):
            self.pool.put(create_conn())

    def get_connection(self):
        return self.pool.get()

    def return_connection(self, conn):
        self.pool.put(conn)

    def execute(self, query):
        conn = self.get_connection()
        try:
            return conn.execute(query)
        finally:
            self.return_connection(conn)

# Usage
pool = ConnectionPool(create_connection, pool_size=20)
result = pool.execute(query)  # Reuses existing connection
```

### Object Pool Pattern

```python
# For expensive-to-create objects
class ExpensiveObject:
    def __init__(self):
        self.data = load_heavy_resource()  # 500ms

# ❌ BAD: Create each time
def process_slow(item):
    obj = ExpensiveObject()  # 500ms overhead
    return obj.process(item)

# ✅ GOOD: Object pool
class ObjectPool:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.pool = [ExpensiveObject() for _ in range(5)]
        return cls._instance

    def get(self):
        return self.pool.pop() if self.pool else ExpensiveObject()

    def return_obj(self, obj):
        self.pool.append(obj)
```

---

## Lazy Loading

### Lazy Initialization

```python
# ❌ BAD: Load everything at startup
class HeavyService:
    def __init__(self):
        self.ml_model = load_model()  # 10 seconds
        self.large_cache = load_cache()  # 5 seconds
        # Startup: 15 seconds even if never used

# ✅ GOOD: Lazy loading
class HeavyService:
    def __init__(self):
        self._ml_model = None
        self._large_cache = None

    @property
    def ml_model(self):
        if self._ml_model is None:
            self._ml_model = load_model()
        return self._ml_model

    @property
    def large_cache(self):
        if self._large_cache is None:
            self._large_cache = load_cache()
        return self._large_cache
```

### Generator for Large Data

```python
# ❌ BAD: Load all into memory
def process_all_users():
    users = db.fetch_all_users()  # 1M users in memory
    for user in users:
        process(user)

# ✅ GOOD: Generator (streaming)
def get_users_batch():
    offset = 0
    batch_size = 1000
    while True:
        batch = db.fetch_users(offset=offset, limit=batch_size)
        if not batch:
            break
        yield from batch
        offset += batch_size

def process_all_users():
    for user in get_users_batch():  # ~1000 users in memory at a time
        process(user)
```

---

## Micro-Optimizations (Use Sparingly)

**RULE**: Only after profiling confirms these are bottlenecks.

### String Concatenation

```python
# ❌ BAD: String concat in loop (O(n²) memory)
result = ""
for item in items:
    result += str(item)  # Creates new string each time

# ✅ GOOD: Join (O(n))
result = "".join(str(item) for item in items)
```

### List Comprehension vs Loop

```python
# Slightly slower
result = []
for x in data:
    if x > 0:
        result.append(x * 2)

# Slightly faster (10-30%)
result = [x * 2 for x in data if x > 0]
```

### Built-in Functions

```python
# ❌ Slow: Custom implementation
def custom_sum(items):
    total = 0
    for item in items:
        total += item
    return total

# ✅ Fast: Built-in (C implementation)
total = sum(items)
```

### Local Variables

```python
# ❌ Slower: Global lookup
import math
def compute(items):
    return [math.sqrt(x) for x in items]

# ✅ Faster: Local reference
def compute(items):
    sqrt = math.sqrt  # Local lookup
    return [sqrt(x) for x in items]
```

---

## Anti-Patterns

### ❌ Premature Optimization

```python
# ❌ BAD: Optimizing without profiling
def get_user(user_id):
    # "Let me cache this for performance"
    if user_id in cache:
        return cache[user_id]
    user = db.get_user(user_id)  # Actually only called once per request
    cache[user_id] = user
    return user

# ✅ GOOD: Profile first
# cProfile shows: get_user() is 0.1% of total time
# Actual bottleneck: serialize_response() is 90%
```

### ❌ Over-Caching

```python
# ❌ BAD: Cache everything
@cache_forever
def get_user_settings(user_id):
    return db.get_settings(user_id)
# Problem: Stale data, memory bloat

# ✅ GOOD: Strategic caching
@cache(ttl=300)  # 5 min TTL
def get_user_settings(user_id):
    return db.get_settings(user_id)
```

### ❌ Blocking in Async Context

```python
# ❌ BAD: Blocking call in async function
async def get_data():
    data = requests.get(url)  # Blocks entire event loop!
    return data.json()

# ✅ GOOD: Async HTTP
async def get_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### ❌ Ignoring Memory

```python
# ❌ BAD: Load entire file
def process_log():
    lines = open('huge.log').read().split('\n')  # 10GB in memory
    return analyze(lines)

# ✅ GOOD: Stream processing
def process_log():
    with open('huge.log') as f:
        for line in f:  # One line at a time
            yield analyze_line(line)
```

---

## Performance Testing

### Benchmarking with timeit

```python
import timeit

# Compare implementations
setup = "data = list(range(10000))"

# Test 1
time1 = timeit.timeit(
    "sum(data)",
    setup=setup,
    number=10000
)

# Test 2
time2 = timeit.timeit(
    "[x for x in data]",
    setup=setup,
    number=10000
)

print(f"sum(): {time1:.4f}s")
print(f"list comp: {time2:.4f}s")
```

### Load Testing with locust

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_users(self):
        self.client.get("/api/users")

    @task(3)  # 3x more likely
    def get_products(self):
        self.client.get("/api/products")
```

```bash
locust -f locustfile.py --host=http://localhost:8000
```

---

## Checklist

### Before Optimizing
- [ ] Profiled with actual data (not assumptions)
- [ ] Identified specific bottleneck function/line
- [ ] Measured baseline performance
- [ ] Set target metric (e.g., "reduce p99 from 500ms to 100ms")

### Memory
- [ ] No memory leaks (tracemalloc, memory_profiler)
- [ ] Large data streamed, not loaded fully
- [ ] Weak references for caches/callbacks
- [ ] Object pools for expensive objects

### CPU
- [ ] Algorithm complexity appropriate (O(n) vs O(n²))
- [ ] CPU-bound tasks use ProcessPoolExecutor
- [ ] No blocking calls in async context
- [ ] Built-in functions preferred over custom

### I/O
- [ ] Async for I/O-bound operations
- [ ] Connection pooling for databases/HTTP
- [ ] Batch operations where possible
- [ ] Lazy loading for heavy resources

### After Optimizing
- [ ] Measured improvement (not assumed)
- [ ] No regression in other areas
- [ ] Code still readable and maintainable
- [ ] Documented why optimization was needed
