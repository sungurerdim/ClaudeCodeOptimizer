---
name: performance-profile-before-optimize
description: Profile code to identify actual bottlenecks before optimization to avoid premature optimization and wasted effort
type: project
severity: low
keywords: [performance, profiling, optimization, benchmarking, bottleneck-analysis, evidence-based]
category: [performance, quality]
related_skills: []
---

# P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE: Performance Profiling Before Optimization

**Severity**: Low

 Developers optimize non-bottleneck code while real bottleneck untouched Hours spent optimizing code that's 2% of runtime Premature optimization makes code harder to read/maintain Actual bottlenecks (.

---

## Rules

- *No rules extracted*

---

## Examples

### ✅ Good
```python
# Step 1: Profile current code
import cProfile

def analyze_performance():
    profiler = cProfile.Profile()
    profiler.enable()

    # Run typical workload
    process_orders(get_last_1000_orders())

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime')
    stats.print_stats(20)

# Output shows:
```
**Why right**: ---

### ❌ Bad
```python
# ❌ BAD: Optimize based on assumptions

# Developer thinks: "Loops are slow, let me use list comprehension"
def process_items_slow(items):
    result = []
    for item in items:
        result.append(expensive_operation(item))
    return result

# "Optimized" version:
def process_items_fast(items):
```
**Why wrong**: ---
