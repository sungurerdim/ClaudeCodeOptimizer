---
title: Python Performance Optimization Skill
category: performance
description: Profiling, optimization, bottleneck analysis
metadata:
  name: "Python Performance Optimization"
  activation_keywords: ["performance", "profiling", "optimization", "cprofile", "memory"]
  category: "language-python"
  language: "python"
principles: ['U_EVIDENCE_BASED', 'P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE', 'P_CONTINUOUS_PROFILING', 'U_NO_OVERENGINEERING']
use_cases:
  project_purpose: [backend, data-pipeline, ml, analytics]
  project_maturity: [active-dev, production]
---

# Python Performance Optimization

Master Python performance profiling and optimization techniques for faster, more efficient code.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**Profiling Tools:**
- `cProfile`: Built-in CPU profiler (production-ready)
- `line_profiler`: Line-by-line execution time analysis
- `memory_profiler`: Memory usage per line
- `py-spy`: Sampling profiler for running processes
- `scalene`: CPU + GPU + memory profiler

**Optimization Strategy:**
1. Profile first - measure before optimizing
2. Identify bottlenecks (80/20 rule: 80% time in 20% code)
3. Optimize algorithms before micro-optimizations
4. Use appropriate data structures (dict vs list, set for lookups)
5. Consider PyPy for compute-intensive code (2-7x speedup)

**Common Bottlenecks:**
- Nested loops (O(n²) complexity)
- String concatenation in loops (use join())
- Global variable lookups (cache in local scope)
- Repeated attribute access (cache in variable)
- Missing comprehensions (slower than for loops)

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

**cProfile Basic Usage:**
```python
import cProfile
import pstats

def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    return total

# Profile function
cProfile.run('slow_function()', 'profile_stats')

# Analyze results
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest functions
```

**Decorator for Profiling:**
```python
import cProfile
import pstats
from functools import wraps
import io

def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()

        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(10)
        print(s.getvalue())
        return result
    return wrapper

@profile
def my_function():
    # Code to profile
    pass
```

**Line-by-Line Profiling:**
```python
# Install: pip install line_profiler
from line_profiler import profile

@profile
def slow_function():
    result = []
    for i in range(10000):
        result.append(i ** 2)  # This line's time measured
    return result

# Run: kernprof -l -v script.py
```

**Memory Profiling:**
```python
# Install: pip install memory_profiler
from memory_profiler import profile

@profile
def memory_intensive():
    big_list = [i for i in range(1000000)]
    big_dict = {i: i**2 for i in range(1000000)}
    return len(big_list) + len(big_dict)

# Run: python -m memory_profiler script.py
```

**Optimization: Data Structures:**
```python
# ✗ Slow: List membership test O(n)
def slow_lookup(items):
    valid_ids = [1, 2, 3, 4, 5]
    return [item for item in items if item['id'] in valid_ids]

# ✓ Fast: Set membership test O(1)
def fast_lookup(items):
    valid_ids = {1, 2, 3, 4, 5}
    return [item for item in items if item['id'] in valid_ids]

# ✓ Fast: Dict for lookups
def fast_mapping(items):
    lookup = {item['id']: item for item in items}
    return lookup.get(42)  # O(1)
```

**Optimization: String Operations:**
```python
# ✗ Slow: String concatenation in loop
def slow_string_build(words):
    result = ""
    for word in words:
        result += word + " "  # Creates new string each iteration
    return result

# ✓ Fast: Use join()
def fast_string_build(words):
    return " ".join(words)

# ✓ Fast: Use f-strings for formatting
def fast_format(items):
    return [f"Item: {item['name']}" for item in items]
```

**Optimization: Comprehensions:**
```python
# ✗ Slower: append in loop
def slow_filter(numbers):
    result = []
    for n in numbers:
        if n % 2 == 0:
            result.append(n * 2)
    return result

# ✓ Faster: List comprehension
def fast_filter(numbers):
    return [n * 2 for n in numbers if n % 2 == 0]

# ✓ Fastest: Generator for memory efficiency
def memory_efficient(numbers):
    return (n * 2 for n in numbers if n % 2 == 0)
```

**Optimization: Caching:**
```python
from functools import lru_cache, cache

# Cache expensive function results
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Python 3.9+: Unbounded cache
@cache
def expensive_computation(x):
    # Complex calculation
    return x ** 10

# Clear cache when needed
fibonacci.cache_clear()
```

**Optimization: Local Variable Caching:**
```python
# ✗ Slow: Repeated attribute access
def slow_process(items):
    for item in items:
        result = item.data.process().transform().value
        print(result)

# ✓ Fast: Cache attribute lookups
def fast_process(items):
    for item in items:
        data = item.data  # Cache attribute
        result = data.process().transform().value
        print(result)

# ✓ Fast: Cache function lookups
def fast_loop(items):
    append = result.append  # Cache method
    for item in items:
        append(item)  # Faster than result.append(item)
```

**NumPy for Numerical Operations:**
```python
import numpy as np

# ✗ Slow: Pure Python
def slow_sum(numbers):
    return sum([x ** 2 for x in numbers])

# ✓ Fast: NumPy vectorization (100x faster)
def fast_sum(numbers):
    arr = np.array(numbers)
    return np.sum(arr ** 2)
```

**PyPy for CPU-Intensive Code:**
```bash
# Install PyPy
# Ubuntu: apt install pypy3
# macOS: brew install pypy3

# Run script with PyPy (2-7x faster for compute)
pypy3 script.py

# Note: PyPy slower for I/O, not compatible with all C extensions
```

**Profiling with py-spy:**
```bash
# Install: pip install py-spy

# Profile running process
py-spy top --pid 12345

# Generate flamegraph
py-spy record -o profile.svg -- python script.py

# Sample without stopping process
py-spy record --pid 12345 --duration 60
```

**Benchmarking with timeit:**
```python
import timeit

# Compare implementations
setup = "data = list(range(1000))"

time1 = timeit.timeit(
    "[x**2 for x in data]",
    setup=setup,
    number=10000
)

time2 = timeit.timeit(
    "list(map(lambda x: x**2, data))",
    setup=setup,
    number=10000
)

print(f"Comprehension: {time1:.4f}s")
print(f"Map: {time2:.4f}s")
```

**Performance Tips:**
- Use `__slots__` in classes to reduce memory (50% savings)
- Use `enumerate()` instead of `range(len())`
- Use `itertools` for efficient iteration
- Avoid premature optimization - profile first
- Consider Cython or Numba for critical code paths
- Use `multiprocessing` for CPU-bound parallelism
- Use `asyncio` for I/O-bound concurrency
