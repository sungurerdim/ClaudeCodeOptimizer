---
description: Performance bottlenecks, optimization opportunities audit
category: audit
cost: 2
principles: ['P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE', 'P_CACHING_STRATEGY', 'P_DB_OPTIMIZATION', 'P_LAZY_LOADING', 'P_ASYNC_IO', 'P_CONTINUOUS_PROFILING']
---

# cco-audit-performance - Performance Optimization Audit

**Identify performance bottlenecks and optimization opportunities in your codebase.**

---

## Architecture & Model Selection

**Data Gathering**: Haiku (Explore agent, quick)
- Fast performance profiling and bottleneck detection
- Database query analysis
- Caching validation
- Cost-effective for metric collection

**Analysis**: Sonnet (Plan agent)
- Performance impact assessment
- Optimization strategy recommendations
- Trade-off analysis (performance vs complexity)

**Execution Pattern**:
1. Launch 2 parallel Haiku agents:
   - Agent 1: Application performance (caching, async, lazy loading)
   - Agent 2: Database performance (queries, indexes, N+1)
2. Aggregate with Sonnet for optimization recommendations
3. Generate prioritized performance improvement plan

**Model Requirements**:
- Haiku for scanning (15-20 seconds)
- Sonnet for analysis and recommendations

---

## Action

Use Task tool to launch parallel performance audit agents.

### Step 1: Parallel Performance Scans

**CRITICAL**: Launch BOTH agents in PARALLEL in a SINGLE message.

#### Agent 1: Application Performance Scan

**Agent 1 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Application performance audit

MUST LOAD FIRST:
1. @CLAUDE.md (Performance section)
2. @~/.cco/principles/performance.md
3. Print: "✓ Loaded 2 docs (~2,000 tokens)"

Audit principles:
- P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE: Profile Before Optimize
- P_CACHING_STRATEGY: Caching Strategy
- P_LAZY_LOADING: Lazy Loading
- P_ASYNC_IO: Async I/O (Non-Blocking Operations)
- P_CONTINUOUS_PROFILING: Continuous Profiling

Scan for:
- Missing caching (frequently called functions, API responses, database queries)
- Synchronous I/O that should be async (file I/O, network calls, database queries)
- Eager loading that should be lazy (large datasets, images, modules)
- Hot paths without profiling (frequently executed code paths)
- N+1 query patterns (loops making database queries)
- Large data structures in memory (should use streaming)
- Inefficient algorithms (O(n²) where O(n log n) possible)
- Unnecessary computations (repeated calculations)

Check for:
- Cache hit rates (are caches effective?)
- Response time bottlenecks (slow endpoints)
- Memory usage patterns (leaks, excessive allocation)
- CPU-bound operations (should be optimized or offloaded)

Report with file:line references and performance impact.
```

#### Agent 2: Database Performance Scan

**Agent 2 Prompt:**
```
Subagent Type: Explore
Model: haiku
Description: Database performance audit

MUST LOAD FIRST:
1. @CLAUDE.md (Performance section)
2. @~/.cco/principles/performance.md
3. Print: "✓ Loaded 2 docs (~2,000 tokens)"

Audit principles:
- P_DB_OPTIMIZATION: Database Query Optimization
- P_CACHING_STRATEGY: Query Result Caching
- P_LAZY_LOADING: Lazy Loading Relationships

Scan for:
- Missing database indexes (slow queries on unindexed columns)
- N+1 query problems (loops making individual queries)
- SELECT * queries (should select specific columns)
- Missing query result caching (repeated identical queries)
- Lack of connection pooling (creating new connections repeatedly)
- Long-running queries (>1 second)
- Missing pagination (loading all results at once)
- Eager loading all relationships (should be selective)
- Missing database query logging (can't identify slow queries)

Check for:
- Query execution plans (using EXPLAIN)
- Index usage (are indexes being used?)
- Query count per request (should be minimized)
- Database connection patterns (are connections reused?)

Report with file:line references, query examples, and optimization suggestions.
```

### Step 2: Performance Analysis & Recommendations

**After both agents complete**, use Sonnet Plan agent:

**Agent 3 Prompt:**
```
Subagent Type: Plan
Model: sonnet
Description: Performance optimization analysis

Task: Analyze performance findings and provide optimization recommendations.

Input:
- Agent 1 findings (application performance)
- Agent 2 findings (database performance)

Analysis steps:
1. Merge all performance findings
2. Assess performance impact (latency, throughput, resource usage)
3. Identify critical bottlenecks (highest impact on user experience)
4. Calculate performance debt (total optimization potential)
5. Prioritize by: Impact × Frequency × Effort
   - Impact: How much faster? (ms saved, % improvement)
   - Frequency: How often hit? (requests/second)
   - Effort: How hard to fix? (hours)
6. Provide specific optimization commands
7. Estimate performance gains (before → after metrics)
8. Consider trade-offs (complexity vs performance gain)

Output format:
- Findings by impact (CRITICAL > HIGH > MEDIUM > LOW)
- Each finding includes: principle, file:line, performance impact, fix command
- Master optimization plan with priority tiers
- Performance debt estimate (total potential improvement)

Focus on practical, high-impact optimizations.
```

---

## Output Format

Report performance issues with impact analysis:

```
Performance Audit Results
=========================

CRITICAL (severe bottlenecks):
  - P_DB_OPTIMIZATION: N+1 query in src/api.py:45
    Impact: 2000ms → 50ms (40x faster)
    Frequency: 100 requests/second
    Issue: Loop making 200 individual queries
    Command: /cco-fix performance --type n-plus-one --file src/api.py:45

  - P_CACHING_STRATEGY: Missing cache on expensive computation (src/analytics.py:123)
    Impact: 5000ms → 10ms (500x faster)
    Frequency: 50 requests/second
    Issue: Recalculating same result repeatedly
    Command: /cco-fix performance --type add-cache --file src/analytics.py:123 --ttl 1h

HIGH (significant impact):
  - P_ASYNC_IO: Synchronous file I/O blocking requests (src/upload.py:67)
    Impact: 1500ms → 100ms (15x faster)
    Frequency: 20 requests/second
    Issue: Blocking I/O in request handler
    Command: /cco-fix performance --type async-io --file src/upload.py:67

  - P_DB_OPTIMIZATION: Missing index on user.email (queries taking 800ms)
    Impact: 800ms → 5ms (160x faster)
    Frequency: 200 requests/second
    Issue: Full table scan on 1M rows
    Command: /cco-fix performance --type add-index --table users --column email

MEDIUM (noticeable impact):
  - P_LAZY_LOADING: Eager loading all relationships (src/models.py:34)
    Impact: 400ms → 50ms (8x faster)
    Frequency: 30 requests/second
    Issue: Loading 10 relationships when only 2 needed
    Command: /cco-fix performance --type lazy-load --file src/models.py:34

  - P_DB_OPTIMIZATION: SELECT * instead of specific columns (src/api.py:89)
    Impact: 200ms → 50ms (4x faster)
    Issue: Transferring 100 columns when only 5 needed
    Command: /cco-fix performance --type select-columns --file src/api.py:89

LOW (minor optimization):
  - P_PERFORMANCE_PROFILE_BEFORE_OPTIMIZE: Missing profiling instrumentation
    Impact: Can't identify future bottlenecks
    Issue: No performance monitoring
    Command: /cco-generate profiling --framework opentelemetry
```

---

## Recommended Actions

**Analyze performance findings and provide impact-driven prioritization:**

```
⚡ Performance Optimization Plan (Impact-Based Priority)
========================================================

IMMEDIATE (Critical Bottlenecks):
──────────────────────────────────
1. Fix N+1 query pattern
   Command: /cco-fix performance --type n-plus-one --file src/api.py:45
   Impact: CRITICAL - 40x faster (2000ms → 50ms)
   Effort: 1 hour
   User Impact: 100 req/s × 1.95s saved = 195s/s saved

2. Add caching to expensive computation
   Command: /cco-fix performance --type add-cache --file src/analytics.py:123 --ttl 1h
   Impact: CRITICAL - 500x faster (5000ms → 10ms)
   Effort: 30 minutes
   User Impact: 50 req/s × 4.99s saved = 249.5s/s saved

THIS WEEK (High Impact):
─────────────────────────
3. Convert file I/O to async
   Command: /cco-fix performance --type async-io --file src/upload.py:67
   Impact: HIGH - 15x faster (1500ms → 100ms)
   Effort: 2 hours
   User Impact: 20 req/s × 1.4s saved = 28s/s saved

4. Add database index on email
   Command: /cco-fix performance --type add-index --table users --column email
   Impact: HIGH - 160x faster (800ms → 5ms)
   Effort: 30 minutes (with migration)
   User Impact: 200 req/s × 0.795s saved = 159s/s saved

THIS SPRINT (Noticeable):
─────────────────────────
5. Implement lazy loading
   Command: /cco-fix performance --type lazy-load --file src/models.py:34
   Impact: MEDIUM - 8x faster (400ms → 50ms)
   Effort: 1.5 hours
   User Impact: 30 req/s × 0.35s saved = 10.5s/s saved

6. Optimize SELECT queries
   Command: /cco-fix performance --type select-columns --file src/api.py:89
   Impact: MEDIUM - 4x faster (200ms → 50ms)
   Effort: 1 hour
   User Impact: Reduced bandwidth, faster queries

BACKLOG (Monitoring):
─────────────────────
7. Add continuous profiling
   Command: /cco-generate profiling --framework opentelemetry
   Impact: LOW - Enables future optimization
   Effort: 3 hours
   User Impact: Proactive bottleneck detection

Performance Debt: 9.5 hours | Total Improvement: 642s/s capacity increase
```

**Command Generation Logic:**
1. **Impact = (Time Saved) × (Request Frequency)**
   - Time Saved: Before latency - After latency
   - Request Frequency: Requests per second hitting this code
   - User Impact: How much total time saved per second

2. **Priority Tiers:**
   - IMMEDIATE: >100ms saved per request, high frequency (fix today)
   - THIS WEEK: 50-100ms saved, medium frequency (fix this week)
   - THIS SPRINT: 10-50ms saved, low frequency (fix this sprint)
   - BACKLOG: Infrastructure/monitoring (fix when convenient)

3. **Command Features:**
   - Specific optimization type: `--type n-plus-one`, `--type add-cache`
   - Target metrics: Before → After latency
   - Configuration: `--ttl`, `--strategy`, `--column`
   - Effort estimate: Realistic implementation time

4. **Trade-off Analysis:**
   - Performance gain vs code complexity
   - Cache consistency vs speed
   - Memory usage vs CPU usage
   - Optimization cost vs benefit

---

## Related Commands

- `/cco-fix performance` - Apply performance optimizations automatically
- `/cco-audit-code-quality` - Code quality audit
- `/cco-audit-comprehensive` - Full comprehensive audit
