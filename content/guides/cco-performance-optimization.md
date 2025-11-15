# Performance Optimization Guide

**Load on-demand when:** Performance tasks, optimization commands

---

## Philosophy

**Proactive performance engineering:** Analyze code continuously rather than waiting for production issues.

**Related Principles:**
- **U_EVIDENCE_BASED**: Measure before claiming performance improvements
- **P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE**: Profile before optimizing

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

**Related Principles:**
- **P_DB_OPTIMIZATION**: Optimize database queries

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

**Related Principles:**
- **P_CACHING_STRATEGY**: Implement strategic caching

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

**Related Principles:**
- **P_CONTINUOUS_PROFILING**: Continuous performance monitoring
- **P_OBSERVABILITY_WITH_OTEL**: Monitor with OpenTelemetry
- **U_MINIMAL_TOUCH**: Focus on actual bottlenecks, not hunches

**Identify hotspots**:
```bash
# Profile with cProfile (Python)
python -m cProfile -o profile.stats main.py
python -m pstats profile.stats
```

**Prioritize**:
- API endpoints with >100ms response time
- Database queries with >10ms execution time
- Functions called >1000 times per request
- Memory allocations >100MB per operation

### 2. Measure Before Optimizing

**Related Principles:**
- **U_EVIDENCE_BASED**: Establish baseline metrics
- **P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE**: Never optimize without profiling

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

**Related Principles:**
- **U_CHANGE_VERIFICATION**: Verify improvements with benchmarks
- **U_TEST_FIRST**: Write performance tests first
- **U_NO_OVERENGINEERING**: Keep optimizations simple and readable

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

**Related Principles:**
- **P_ASYNC_IO**: Use non-blocking I/O operations
- **P_LAZY_LOADING**: Load data only when needed

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
- [ ] Keep code readable (U_NO_OVERENGINEERING: No Overengineering)
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

---

## Principle References

This guide incorporates the following CCO principles:

**Universal Principles:**
- **U_EVIDENCE_BASED**: Evidence-Based Verification → `.claude/principles/U_EVIDENCE_BASED.md`
- **U_NO_OVERENGINEERING**: No Overengineering → `.claude/principles/U_NO_OVERENGINEERING.md`
- **U_MINIMAL_TOUCH**: Minimal Touch Policy → `.claude/principles/U_MINIMAL_TOUCH.md`
- **U_CHANGE_VERIFICATION**: Change Verification Protocol → `.claude/principles/U_CHANGE_VERIFICATION.md`
- **U_TEST_FIRST**: Test-First Development → `.claude/principles/U_TEST_FIRST.md`

**Performance Principles:**
- **P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE**: Profile Before Optimizing → `.claude/principles/P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE.md`
- **P_CONTINUOUS_PROFILING**: Continuous Profiling → `.claude/principles/P_CONTINUOUS_PROFILING.md`
- **P_CACHING_STRATEGY**: Caching Strategy → `.claude/principles/P_CACHING_STRATEGY.md`
- **P_DB_OPTIMIZATION**: Database Query Optimization → `.claude/principles/P_DB_OPTIMIZATION.md`
- **P_LAZY_LOADING**: Lazy Loading → `.claude/principles/P_LAZY_LOADING.md`
- **P_ASYNC_IO**: Async I/O (Non-Blocking Operations) → `.claude/principles/P_ASYNC_IO.md`

**Observability:**
- **P_OBSERVABILITY_WITH_OTEL**: Observability with OpenTelemetry → `.claude/principles/P_OBSERVABILITY_WITH_OTEL.md`
- **P_HEALTH_CHECKS**: Health Check Implementation → `.claude/principles/P_HEALTH_CHECKS.md`
