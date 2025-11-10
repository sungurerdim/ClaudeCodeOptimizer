# Performance Optimization Guide

**Load on-demand when:** Performance tasks, optimization commands

---

## Philosophy

**Proactive performance engineering:** Analyze code continuously rather than waiting for production issues.

---

## Common Performance Bottlenecks

### 1. Algorithm Complexity

**Problem**: Nested loops creating O(n²) complexity

**❌ Bad** (O(n²)):
```python
def find_duplicates(items):
    duplicates = []
    for i in items:
        for j in items:
            if i == j and i not in duplicates:
                duplicates.append(i)
    return duplicates
```

**✅ Good** (O(n)):
```python
def find_duplicates(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

**Impact**: 100x faster for 1000 items

### 2. N+1 Query Problem

**Problem**: Database calls inside loops

**❌ Bad**:
```python
# Fetches 1 + N queries
users = db.query("SELECT * FROM users")
for user in users:
    orders = db.query(f"SELECT * FROM orders WHERE user_id = {user.id}")
```

**✅ Good**:
```python
# Single query with JOIN
results = db.query("""
    SELECT users.*, orders.*
    FROM users
    LEFT JOIN orders ON orders.user_id = users.id
""")
```

**Impact**: 10-100x response time improvement

### 3. Missing Indexes

**Problem**: Inefficient queries lacking proper indexes

**❌ Bad**:
```sql
-- No index on email
SELECT * FROM users WHERE email = 'user@example.com';
-- Table scan: 10000ms
```

**✅ Good**:
```sql
-- Add index
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'user@example.com';
-- Index lookup: 5ms
```

**Impact**: 1000x faster queries

### 4. Missing Caching

**Problem**: Repeated operations without caching

**❌ Bad**:
```python
def get_user_permissions(user_id):
    # Hits database every time
    return db.query(f"SELECT * FROM permissions WHERE user_id = {user_id}")

# Called 100 times = 100 DB queries
for user_id in user_ids:
    permissions = get_user_permissions(user_id)
```

**✅ Good**:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_user_permissions(user_id):
    return db.query(f"SELECT * FROM permissions WHERE user_id = {user_id}")

# Called 100 times = 10 unique IDs = 10 DB queries
for user_id in user_ids:
    permissions = get_user_permissions(user_id)
```

**Impact**: 90% reduction in database load

### 5. Redundant Data Processing

**Problem**: Processing same data multiple times

**❌ Bad**:
```python
def get_stats(data):
    return {
        "mean": sum(data) / len(data),
        "max": max(data),
        "min": min(data),
        "sorted": sorted(data),  # O(n log n)
        "median": sorted(data)[len(data) // 2],  # O(n log n) again!
    }
```

**✅ Good**:
```python
def get_stats(data):
    sorted_data = sorted(data)  # Sort once
    return {
        "mean": sum(data) / len(data),
        "max": data[-1] if sorted_data else None,
        "min": data[0] if sorted_data else None,
        "sorted": sorted_data,
        "median": sorted_data[len(sorted_data) // 2],
    }
```

**Impact**: 2x faster

---

## Two-Tool Performance Framework

### Quick Investigation (Claude.ai)

**Use for**:
1. Paste problematic functions for complexity analysis
2. Get specific optimization recommendations
3. Determine if issues are algorithmic, structural, or configuration-related
4. Decide between quick code changes or comprehensive architectural reviews

**Example query**:
```
"This function takes 5 seconds with 1000 items. How can I optimize it?

[paste code]
"
```

### Comprehensive Optimization (Claude Code)

**Use for**:
1. Request optimization analysis of critical paths
2. Let Claude identify bottlenecks across multiple files
3. Automatically create tests and implement fixes
4. Validate improvements with generated benchmarks

**Commands**:
```bash
# Analyze performance-critical code
/cco-analyze --focus=performance

# Optimize specific components
/cco-optimize-code

# Generate performance tests
/cco-generate tests --type=performance
```

---

## Strategic Implementation

### 1. Focus on Critical Paths

**Identify hotspots**:
```bash
# Profile with cProfile (Python)
python -m cProfile -o profile.stats main.py
python -m pstats profile.stats

# Analyze with CCO
/cco-analyze --focus=performance --path=api/
```

**Prioritize**:
- API endpoints with >100ms response time
- Database queries with >10ms execution time
- Functions called >1000 times per request
- Memory allocations >100MB per operation

### 2. Measure Before Optimizing

**Benchmark baseline**:
```python
import time

def benchmark(func, *args, iterations=1000):
    start = time.perf_counter()
    for _ in range(iterations):
        func(*args)
    end = time.perf_counter()
    avg_time = (end - start) / iterations
    print(f"{func.__name__}: {avg_time*1000:.2f}ms")

# Before optimization
benchmark(slow_function, data)

# After optimization
benchmark(fast_function, data)
```

**Use profiling tools**:
- **Python**: cProfile, py-spy, memory_profiler
- **JavaScript**: Chrome DevTools, Lighthouse
- **Database**: EXPLAIN ANALYZE, slow query log
- **Production**: New Relic, Datadog, Sentry Performance

### 3. Implement & Test

**Process**:
1. Identify bottleneck (profiling)
2. Implement optimization
3. Verify correctness (tests pass)
4. Measure improvement (benchmarks)
5. Deploy and monitor

**Commands**:
```bash
# Implement fix
# [code changes]

# Verify correctness
pytest tests/ -v

# Run benchmarks
python benchmarks/test_performance.py

# Compare results
# Before: 245ms | After: 12ms | Improvement: 20x
```

### 4. Prevent Regressions

**Add performance tests**:
```python
import pytest

@pytest.mark.performance
def test_query_performance():
    start = time.perf_counter()
    result = expensive_query()
    duration = time.perf_counter() - start

    assert duration < 0.1, f"Query took {duration}s, expected <0.1s"
    assert len(result) > 0
```

**CI integration**:
```yaml
# .github/workflows/performance.yml
- name: Run performance tests
  run: pytest tests/ -m performance --benchmark-only
```

---

## Expected Impact by Type

### Algorithm Optimization

- **O(n²) → O(n)**: Gains scale with dataset size
  - 100 items: 10x faster
  - 1000 items: 100x faster
  - 10000 items: 1000x faster

### Database Optimization

- **N+1 fix**: 10-100x improvement
- **Add index**: 100-1000x improvement
- **Query optimization**: 2-50x improvement

### Caching

- **In-memory cache**: 10-100x improvement
- **Redis/Memcached**: 5-50x improvement
- **CDN**: 10-1000x improvement (geo-distributed)

### Async I/O

- **Sequential → Parallel**: N×faster (N = concurrent ops)
- **Blocking → Non-blocking**: 2-10x throughput

---

## Optimization Checklist

**Before optimizing**:
- [ ] Profile code to identify actual bottleneck
- [ ] Measure baseline performance
- [ ] Set performance target (e.g., <100ms)
- [ ] Write performance tests

**During optimization**:
- [ ] Focus on measured bottleneck (not hunches)
- [ ] Keep code readable (P071: Anti-Overengineering)
- [ ] Verify correctness (all tests pass)
- [ ] Benchmark improvements

**After optimization**:
- [ ] Document optimization (comments, docs)
- [ ] Add regression tests
- [ ] Monitor in production
- [ ] Update performance docs if needed

---

## Tools & Commands

### Profiling

```bash
# Python
python -m cProfile -o profile.stats app.py
python -m pstats profile.stats

# Memory profiling
python -m memory_profiler app.py

# Live profiling
py-spy top --pid <PID>
```

### Benchmarking

```bash
# Python
python -m timeit "function_call()"

# Custom benchmarks
python benchmarks/run_all.py
```

### CCO Commands

```bash
# Analyze performance
/cco-analyze --focus=performance

# Optimize code
/cco-optimize-code

# Generate performance tests
/cco-generate tests --type=performance

# Audit performance principles
/cco-audit performance
```

---

## Principle References

- **P054-P058**: Performance Principles
  - P054: Caching Strategy
  - P055: Database Query Optimization
  - P056: Lazy Loading & Deferred Execution
  - P057: Async I/O for Network Operations
  - P058: Resource Pool Management

See: [@~/.cco/knowledge/principles/performance.md](../principles/performance.md)

---

*Part of CCO Documentation System*
*Load when needed: @~/.cco/knowledge/guides/performance-optimization.md*
