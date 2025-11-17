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

### Step 0: Introduction and Confirmation (ALWAYS FIRST)

**Before doing ANYTHING, present this introduction and get user confirmation:**

```markdown
# Optimize Command

**What I do:**
I identify and fix performance bottlenecks across 6 areas: database queries, Docker images, code quality, dependencies, frontend bundles, and resilience patterns.

**How it works:**
1. I analyze your project to find optimization opportunities (N+1 queries, large images, dead code, etc.)
2. I measure current metrics (query times, image sizes, bundle sizes)
3. You select which optimizations to apply (individual steps or groups)
4. I apply optimizations and measure improvements
5. I report before/after metrics with impact analysis

**What you'll get:**
- Database optimizations (N+1 fixes, indexes, caching - 89% faster queries)
- Docker optimizations (multi-stage builds - 1.2GB → 150MB)
- Code cleanup (remove dead code - 23% smaller codebase)
- Dependency updates (security patches, remove unused)
- Bundle optimizations (code splitting - 450KB → 200KB)
- Resilience patterns (circuit breakers, retry logic)

**Time estimate:** 10-30 minutes depending on optimizations selected

**Changes WILL be made to your code** - all optimizations are measured and verified.
```

**Then ask for confirmation using AskUserQuestion:**

```python
AskUserQuestion({
  questions: [{
    question: "Do you want to start optimizing the project?",
    header: "Start Optimize",
    multiSelect: false,
    options: [
      {
        label: "Yes, start optimization",
        description: "Analyze and optimize performance bottlenecks"
      },
      {
        label: "No, cancel",
        description: "Exit without making any changes"
      }
    ]
  }]
})
```

**CRITICAL:**
- If user selects "No, cancel" → EXIT immediately, do NOT proceed
- If user selects "Yes, start optimization" → Continue to Step 1

---

### Interactive Mode (No Parameters)

1. **Analyze project for real optimization opportunities first**, then **present specific optimization steps using AskUserQuestion**:

**IMPORTANT:** The steps below are EXAMPLES. You MUST:
- Run actual analysis (Grep for N+1 queries, check Docker image size, count unused functions)
- Measure real metrics (actual image sizes, actual query times, actual bundle sizes)
- List EACH specific optimization as a separate option with its category in parentheses
- Replace ALL example steps with REAL project-specific optimizations
- Include actual file paths and line numbers
- Skip options for optimizations not applicable to this project

```python
AskUserQuestion({
  questions: [{
    question: "Which optimization steps should I apply? Select specific optimizations you want:",
    header: "Optimize",
    multiSelect: true,
    options: [
      # Database optimizations - Each specific fix
      {
        label: "Fix N+1 query in api/orders.py:45",
        description: "(Database, 2 min) get_user_orders() - Add eager loading | 450ms → 25ms | 🔴 CRITICAL"
      },
      {
        label: "Fix N+1 query in api/products.py:67",
        description: "(Database, 2 min) get_related_products() - Use joinedload | 380ms → 20ms | 🔴 CRITICAL"
      },
      {
        label: "Add index on products(category, price)",
        description: "(Database, 1 min) Create migration for composite index | 780ms → 15ms | 🔴 CRITICAL"
      },
      {
        label: "Add index on orders(user_id, created_at)",
        description: "(Database, 1 min) Create migration for composite index | 650ms → 10ms | 🔴 CRITICAL"
      },
      {
        label: "Add Redis caching for get_popular_products()",
        description: "(Database, 3 min) 1h TTL cache | 50ms → 2ms, saves 48s/min | 🔴 CRITICAL"
      },
      {
        label: "Setup connection pooling",
        description: "(Database, 2 min) Pool size 20, overflow 10 | 10x concurrency | 🔴 CRITICAL"
      },

      # Docker optimizations - Each specific improvement
      {
        label: "Create multi-stage Dockerfile",
        description: "(Docker, 3 min) Builder + runtime stages | 1.2GB → 150MB (87% smaller) | 🔴 CRITICAL"
      },
      {
        label: "Create .dockerignore file",
        description: "(Docker, 1 min) Exclude tests/, .git/, __pycache__ | Faster builds | 🔴 CRITICAL"
      },
      {
        label: "Optimize Docker layer ordering",
        description: "(Docker, 2 min) Dependencies first, code last | 8min → 2min build (75% faster) | 🔴 CRITICAL"
      },
      {
        label: "Remove dev dependencies from image",
        description: "(Docker, 1 min) Production-only packages | 200MB → 150MB | 🔴 CRITICAL"
      },

      # Code optimizations - Each specific cleanup
      {
        label: "Remove unused function: utils/old_helpers.py:format_date()",
        description: "(Code, 1 min) Dead code, no callers found | 🟡 HIGH"
      },
      {
        label: "Remove unused function: services/deprecated.py:old_auth()",
        description: "(Code, 1 min) Dead code, replaced by new_auth() | 🟡 HIGH"
      },
      {
        label: "Remove all unused imports (200+ imports in 15 files)",
        description: "(Code, 2 min) Use autoflake | Faster module loading | 🟡 HIGH"
      },
      {
        label: "Refactor calculate_discount() - complexity 18 → 8",
        description: "(Code, 3 min) services/pricing.py:45 - Extract smaller functions | 🟡 HIGH"
      },
      {
        label: "Refactor process_payment() - complexity 16 → 9",
        description: "(Code, 3 min) api/payments.py:120 - Simplify control flow | 🟡 HIGH"
      },

      # Dependencies optimizations - Each specific update
      {
        label: "Update requests 2.28.0 → 2.31.0",
        description: "(Dependencies, 1 min) Security patch for CVE-2023-32681 | 🟡 HIGH"
      },
      {
        label: "Update flask 2.0.1 → 2.3.0",
        description: "(Dependencies, 1 min) Security patches | 🟡 HIGH"
      },
      {
        label: "Remove unused dependency: beautifulsoup4",
        description: "(Dependencies, 1 min) Not imported anywhere | 🟡 HIGH"
      },
      {
        label: "Remove unused dependency: pandas",
        description: "(Dependencies, 1 min) Not imported anywhere, large package | 🟡 HIGH"
      },

      # Bundle optimizations - Each specific technique
      {
        label: "Add code splitting for routes",
        description: "(Bundle, 3 min) React.lazy() for each route | 450KB → 300KB | 🟢 RECOMMENDED"
      },
      {
        label: "Enable tree shaking",
        description: "(Bundle, 2 min) Webpack config optimization | 300KB → 200KB | 🟢 RECOMMENDED"
      },
      {
        label: "Add Gzip compression",
        description: "(Bundle, 1 min) Nginx/server config | 200KB → 60KB transfer | 🟢 RECOMMENDED"
      },

      # Performance optimizations - Each specific resilience feature
      {
        label: "Add circuit breaker for external API",
        description: "(Performance, 3 min) Prevent cascade failures | 🟢 RECOMMENDED"
      },
      {
        label: "Add retry logic with exponential backoff",
        description: "(Performance, 2 min) Handle transient failures | 🟢 RECOMMENDED"
      },
      {
        label: "Add request timeout configuration",
        description: "(Performance, 1 min) Prevent hanging requests | 🟢 RECOMMENDED"
      },

      # Group options
      {
        label: "All Database Optimizations",
        description: "✅ Apply all 6 database optimizations above (N+1 fixes, indexes, caching, pooling)"
      },
      {
        label: "All Docker Optimizations",
        description: "✅ Apply all 4 Docker optimizations above (multi-stage, ignore, layers, deps)"
      },
      {
        label: "All Code Optimizations",
        description: "✅ Apply all 5 code optimizations above (remove dead code, remove imports, refactor complex)"
      },
      {
        label: "All Dependency Optimizations",
        description: "✅ Apply all 4 dependency optimizations above (updates, removals)"
      },
      {
        label: "All Bundle Optimizations",
        description: "✅ Apply all 3 bundle optimizations above (splitting, tree shaking, compression)"
      },
      {
        label: "All Performance Optimizations",
        description: "✅ Apply all 3 performance optimizations above (circuit breaker, retry, timeout)"
      },
      {
        label: "All Optimizations",
        description: "✅ Apply ALL optimization steps above (comprehensive performance improvement)"
      }
    ]
  }]
})
```

**IMPORTANT:**
- If user selects "All Optimizations", ignore other selections and apply ALL steps
- If user selects "All [Category] Optimizations", apply all steps in that category
- Otherwise, apply ONLY the individually selected steps
- Steps can be executed in parallel when they don't conflict (different files)

2. **Present optimization plan:**

```markdown
Selected: [list selected optimizations or "All Optimizations"]

Skills I'll use:
- [list skills for selected optimizations]

Agent: cco-agent-fix (Sonnet for accuracy)

What I'll optimize:

[For each selected optimization, explain what will be done]

Example for Database:
- Fix get_user_orders() N+1 pattern (eager loading)
- Add index on products(category, price)
- Add Redis caching for get_popular_products()
- Setup connection pooling (size=20)
- Impact: 450ms → 50ms avg (89% faster)

Estimated time: ~[X] minutes
```

3. **Confirm optimization** using AskUserQuestion:

```python
AskUserQuestion({
  questions: [{
    question: "Ready to apply the selected optimizations?",
    header: "Confirm",
    multiSelect: false,
    options: [
      {
        label: "Yes, start optimization",
        description: "Apply all selected optimizations"
      },
      {
        label: "No, cancel",
        description: "Cancel and return to optimization selection"
      }
    ]
  }]
})
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
