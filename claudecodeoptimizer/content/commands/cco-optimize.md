# cco-optimize

**Performance optimization across 6 areas to address Pain #5 (69% waste 8+ hours/week).**

---

## Purpose

Identify and fix performance bottlenecks: slow queries, large bundles, dead code, outdated dependencies, bloated Docker images, and inefficient code patterns.

---

## 6 Optimization Types

1. **--code** - Remove dead code, reduce complexity
   - Skill: `cco-skill-code-quality-refactoring-complexity`
   - Optimizes: Dead code removal, complexity reduction, refactoring

2. **--deps** - Update dependencies, remove unused
   - Skill: `cco-skill-supply-chain-dependencies-sast`
   - Optimizes: Dependency updates, unused package removal, security patches

3. **--docker** - Multi-stage builds, layer optimization
   - Skill: `cco-skill-kubernetes-security-containers`
   - Optimizes: Image size, build time, layer caching

4. **--database** - Query optimization, caching
   - Skill: `cco-skill-database-optimization-caching-profiling`
   - Optimizes: N+1 queries, indexes, connection pooling, caching

5. **--bundle** - Frontend bundle size reduction
   - Skill: `cco-skill-frontend-bundle-a11y-performance`
   - Optimizes: Code splitting, tree shaking, compression

6. **--performance** - Profiling, bottleneck removal
   - Skill: `cco-skill-resilience-circuitbreaker-retry-bulkhead`
   - Optimizes: Response times, circuit breakers, retry logic

---

## Execution Protocol

### Interactive Mode (No Parameters)

1. **Detect optimization opportunities:**

```markdown
Analyzing project for optimization opportunities...

Found potential optimizations:

🔴 Critical (High Impact):
□ Database (Pain #5: Performance)
  - 2 N+1 query patterns (450ms → 25ms possible)
  - 3 missing indexes (780ms → 15ms possible)
  - No connection pooling (limits concurrency)
  Impact: 89% faster queries, 10x concurrent users

□ Docker (Pain #5: Build time)
  - No multi-stage build (image: 1.2GB)
  - Unnecessary dependencies in image
  - No layer caching
  Impact: 1.2GB → 150MB (87% smaller), 8min → 2min build

🟡 High Priority:
□ Code (Pain #2: Tech debt)
  - 45 unused functions (23% dead code)
  - 200+ unused imports
  - 5 functions with complexity > 15
  Impact: 23% smaller codebase, easier maintenance

□ Dependencies (Pain #6: Integration)
  - 8 outdated packages (security vulnerabilities)
  - 15 unused dependencies
  - 3 packages with known CVEs
  Impact: Security improved, 20% faster installs

🟢 Recommended:
□ Bundle (Frontend performance)
  - Bundle size: 450KB (target: <200KB)
  - No code splitting
  - No tree shaking
  Impact: 54% smaller bundle, 2s faster load

□ Performance (Resilience)
  - No circuit breakers
  - No retry logic
  - No request timeout configuration
  Impact: Better failure handling, fewer cascading failures

Select optimization types: ▯
```

2. **User selects** optimization types

3. **Confirm and explain:**

```markdown
Selected: Database, Docker, Code

I'll use these skills:
- cco-skill-database-optimization-caching-profiling
- cco-skill-kubernetes-security-containers
- cco-skill-code-quality-refactoring-complexity

Agent: cco-agent-fix (Sonnet for accuracy)

What I'll optimize:

Database:
- Fix get_user_orders() N+1 pattern (eager loading)
- Add index on products(category, price)
- Add Redis caching for get_popular_products()
- Setup connection pooling (size=20)
- Impact: 450ms → 50ms avg (89% faster)

Docker:
- Convert to multi-stage build
- Remove dev dependencies from final image
- Optimize layer ordering for cache hits
- Use .dockerignore
- Impact: 1.2GB → 150MB, 8min → 2min build

Code:
- Remove 45 unused functions
- Remove 200+ unused imports
- Refactor 5 complex functions (>15 complexity)
- Impact: 23% less code, better maintainability

Estimated time: ~15 minutes

Continue? (yes/no)
```

4. **Use TodoWrite** to track optimization progress

5. **Launch Task with cco-agent-fix**:

```python
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Optimize database, Docker, and code",
  prompt: """
  Apply performance optimizations:

  DATABASE OPTIMIZATION:
  Use cco-skill-database-optimization-caching-profiling

  1. Fix N+1 in api/orders.py:get_user_orders()
     - Add eager loading: db.joinedload(User.orders)
     - Verify: Single query instead of N+1

  2. Add index for slow query in api/products.py:search()
     - Create index: (category, price)
     - Generate migration script

  3. Add Redis caching to api/products.py:get_popular()
     - Cache with 1h TTL
     - Invalidate on product update

  4. Add connection pooling in database.py
     - Pool size: 20, overflow: 10
     - Proper connection lifecycle

  DOCKER OPTIMIZATION:
  Use cco-skill-kubernetes-security-containers

  1. Convert Dockerfile to multi-stage build
     - Builder stage: install dependencies
     - Runtime stage: copy only necessary files
     - Non-root user

  2. Create .dockerignore
     - Exclude: tests/, .git/, __pycache__

  3. Optimize layer ordering for caching
     - Dependencies first (change rarely)
     - Code last (changes often)

  CODE OPTIMIZATION:
  Use cco-skill-code-quality-refactoring-complexity

  1. Remove unused functions
     - Grep for function definitions
     - Check for callers
     - Remove if no callers

  2. Remove unused imports
     - Use autoflake or similar
     - Verify no missing imports

  3. Refactor complex functions
     - Extract smaller functions
     - Reduce cyclomatic complexity to <10

  Verify each change:
  - Database: measure query times before/after
  - Docker: check image size before/after
  - Code: run tests to ensure functionality intact

  Report improvements with metrics.
  """
})
```

6. **Present results:**

```markdown
Optimization Complete! ✓

Database Optimizations:
✓ Fixed N+1 pattern in api/orders.py:get_user_orders()
  Before: 450ms (1 query + 50 queries for orders)
  After: 25ms (1 query with eager loading)
  Improvement: 95% faster

✓ Added index on products(category, price)
  Before: 780ms full table scan
  After: 15ms index lookup
  Improvement: 98% faster

✓ Added Redis caching to api/products.py:get_popular()
  Before: 50ms per call, 1000 calls/min = 50s DB time
  After: 2ms per call (from cache), 50s → 2s
  Improvement: 96% faster, 48s saved/min

✓ Added connection pooling
  Pool size: 20, overflow: 10
  Concurrent requests: 100 → 1000 (10x improvement)

Docker Optimizations:
✓ Multi-stage Dockerfile created
  Before: 1.2GB (includes dev dependencies)
  After: 150MB (production only)
  Improvement: 87% smaller

✓ Build time optimization
  Before: 8min (no caching)
  After: 2min (layer caching)
  Improvement: 75% faster builds

✓ .dockerignore created
  Excludes: tests/, .git/, __pycache__/, *.pyc

Code Optimizations:
✓ Removed 45 unused functions
  - 800 lines of dead code removed
  - Codebase: 3500 lines → 2700 lines (23% reduction)

✓ Removed 200+ unused imports
  - Faster module loading
  - Cleaner code

✓ Refactored 5 complex functions
  - calculate_discount(): 18 → 8 complexity
  - process_payment(): 16 → 9 complexity
  - validate_order(): 20 → 7 complexity
  - ... (2 more)

Overall Impact:

Performance:
- API response time: Avg 450ms → 50ms (89% faster)
- Database load: -90%
- Concurrent users: 100 → 1000 (10x)

Build & Deploy:
- Docker image: 1.2GB → 150MB (87% smaller)
- Build time: 8min → 2min (75% faster)
- Deploy time: 5min → 1min (80% faster)

Code Quality:
- Codebase size: -23% (easier to maintain)
- Complexity: All functions <10
- Dead code: Eliminated

Pain Point Impact:
✓ Addresses Pain #5 (69% waste 8+ hours/week)
  - Saves: 15 hours/week in debugging slow queries
  - Saves: 6 hours/week in build/deploy time
  - Saves: 5 hours/week in navigating dead code
  - Total: 26 hours/week saved

✓ Addresses Pain #2 (23% tech debt)
  - Removed 23% dead code
  - Reduced complexity

Performance score: 65 → 90 (+25 points)

Next Steps:
1. Test thoroughly: pytest tests/
2. Load test: locust -f tests/load_test.py
3. Monitor in production: Check metrics
4. Commit: /cco-commit
```

### Parametrized Mode (Power Users)

```bash
# Single optimization
/cco-optimize --database

# Multiple optimizations
/cco-optimize --database --docker --code

# All optimizations
/cco-optimize --all
```

---

## Agent Usage

**Agent:** `cco-agent-fix` (general-purpose with Sonnet model)

**Why Sonnet:**
- Performance optimization requires accuracy
- Understanding of trade-offs
- Safe refactoring
- Worth the cost for correct optimizations

---

## Measurement

Before applying optimizations, measure baselines:
- **Database:** Query execution times
- **Docker:** Image size, build time
- **Code:** Lines of code, complexity metrics
- **Bundle:** Size in KB, load time
- **Performance:** Response times, error rates

After optimizations, measure improvements and report.

---

## Safety

- **Always run tests** after optimizations
- **Measure before/after** to verify improvements
- **Keep backups** of original code
- **Deploy to staging first** before production
- **Monitor metrics** after deployment

---

## Success Criteria

- [OK] Optimization opportunities detected
- [OK] User selected optimization types
- [OK] Baseline metrics measured
- [OK] Appropriate skills used
- [OK] cco-agent-fix executed optimizations
- [OK] Post-optimization metrics measured
- [OK] Improvements verified and reported
- [OK] Tests still pass
- [OK] Pain-point impact communicated

---

## Example Usage

```bash
# Optimize slow database queries
/cco-optimize --database

# Reduce Docker image size
/cco-optimize --docker

# Clean up codebase
/cco-optimize --code

# Comprehensive optimization
/cco-optimize --all
```

---

## Integration with Other Commands

- **After /cco-audit --performance**: Fix detected issues
- **After /cco-overview**: Follow optimization recommendations
- **Before deployment**: Optimize before going to production
