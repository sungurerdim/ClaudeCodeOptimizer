---
name: cco-optimize
description: Performance optimization with before/after metrics measurement
action_type: optimize
parameters:
  docker:
    keywords: [docker optimization, multi-stage build, layer optimization, image size reduction]
    category: infrastructure
    pain_points: [5]
  database:
    keywords: [database optimization, query profiling, query time measurement, performance metrics]
    category: database
    pain_points: [5]
  bundle:
    keywords: [bundle optimization, code splitting, tree shaking, compression, frontend performance]
    category: performance
    pain_points: [5]
  performance:
    keywords: [performance profiling, bottleneck removal, circuit breakers, retry logic, timeouts]
    category: performance
    pain_points: [5]
---

# cco-optimize

**Performance optimization with before/after metrics measurement to address Pain #5 (significant time waste).**

---

## Purpose

Measure and improve performance metrics: query times, image sizes, bundle sizes, and response times. Unlike /cco-fix which fixes issues, /cco-optimize focuses on **measuring improvements** with before/after metrics.

**Note:** For code cleanup (dead code, complexity) use `/cco-fix --tech-debt`. For dependency updates use `/cco-fix --supply-chain`.

---

## 4 Optimization Types

1. **--docker** - Multi-stage builds, layer optimization
   - Skill: `cco-skill-kubernetes-security-containers`
   - Measures: Image size (MB), build time (seconds), layer count
   - Optimizes: Multi-stage builds, .dockerignore, layer ordering

2. **--database** - Query profiling and optimization
   - Skill: `cco-skill-database-optimization-caching-profiling`
   - Measures: Query execution time (ms), query count, connection pool usage
   - Optimizes: Query plans, caching strategies, connection pooling

3. **--bundle** - Frontend bundle size reduction
   - Skill: `cco-skill-frontend-bundle-a11y-performance`
   - Measures: Bundle size (KB), chunk count, load time
   - Optimizes: Code splitting, tree shaking, compression

4. **--performance** - Profiling, bottleneck removal
   - Skill: `cco-skill-resilience-circuitbreaker-retry-bulkhead`
   - Measures: Response times (ms), error rates, throughput
   - Optimizes: Circuit breakers, retry logic, timeouts

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
- Database optimizations (N+1 fixes, indexes, caching - faster queries)
- Docker optimizations (multi-stage builds - smaller images)
- Code cleanup (remove dead code - smaller codebase)
- Dependency updates (security patches, remove unused)
- Bundle optimizations (code splitting - smaller bundles)
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

**IMPORTANT - Tab-Based Selection (Single Submit):**
AskUserQuestion supports **4 questions maximum** with **4 options maximum per question**. This structure provides:
- All optimization categories visible in one interface (tabs)
- Single submit for all selections
- "All [group]" option in each tab
- Dynamic selection count summary

**Analysis Required First:**
- Run actual analysis (Grep for N+1 queries, check Docker image size, count unused functions)
- Measure real metrics (actual image sizes, actual query times, actual bundle sizes)
- Generate options dynamically with REAL data from project analysis

```python
# Tab-based category selection (single submit)
AskUserQuestion({
  questions: [
    {
      question: "Select optimizations to run (with before/after metrics):",
      header: "Performance",
      multiSelect: true,
      options: [
        {
          label: "Docker",
          description: f"Image size {current_size}, build time {build_time} | Measures: MB, seconds"
        },
        {
          label: "Database",
          description: f"Query profiling | {query_count} queries | Measures: ms, count"
        },
        {
          label: "Bundle",
          description: f"Frontend bundle size: {bundle_size} | Measures: KB, chunks"
        },
        {
          label: "Performance",
          description: "Response times, circuit breakers | Measures: ms, error rate"
        }
      ]
    },
    {
      question: "Or select all:",
      header: "✅ All",
      multiSelect: true,
      options: [
        {
          label: "All Optimizations",
          description: "Run ALL optimizations with full metrics measurement"
        }
      ]
    }
  ]
})
```

**Note:** For code cleanup and dependency updates, use `/cco-fix --tech-debt` and `/cco-fix --supply-chain` respectively.

### Selection Processing

**After user submits, calculate and display selection summary:**

```markdown
## Selection Summary

**Your selections:**
- 🔴 Critical: [list selected]
- 🟡 High: [list selected]
- 🟢 Recommended: [list selected]

**Total: {{SELECTED_COUNT}} optimization categories selected**

⚠️ Only selected categories will be optimized.
Categories NOT selected will be skipped entirely.
```

# Stage 2: Individual Optimizations per Category
# For each selected category, show specific optimizations (paginated if >4)
# Example: If "Database Optimizations" selected
db_optimizations = analyze_database_issues()  # Returns REAL issues

AskUserQuestion({
  questions: [{
    question: f"Which Database optimizations? ({len(db_optimizations)} found):",
    header: "Database",
    multiSelect: true,
    options: generate_paginated_options(db_optimizations)
    # Each option shows REAL file:line, REAL metrics from analysis
  }]
})
```

**IMPORTANT:**
- If user selects "All Optimizations", apply ALL categories
- If user selects specific categories, show individual optimizations for each
- Generate all descriptions from REAL project analysis (not hardcoded examples)
- Skip categories not applicable to this project

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
- Setup connection pooling
- Impact: significantly faster queries

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

  Apply selected optimizations based on REAL project analysis.

  For each optimization category selected:
  - Use appropriate skill
  - Apply to ACTUAL files/functions found in analysis
  - Measure before/after metrics
  - Verify changes don't break functionality

  DATABASE: Use cco-skill-database-optimization-caching-profiling
  - Fix N+1 patterns in <real-file>:<real-function>
  - Add indexes for slow queries found
  - Add caching where appropriate
  - Setup connection pooling

  DOCKER: Use cco-skill-kubernetes-security-containers
  - Convert to multi-stage build
  - Create .dockerignore
  - Optimize layer ordering

  CODE: Use cco-skill-code-quality-refactoring-complexity
  - Remove unused functions found in analysis
  - Remove unused imports
  - Refactor complex functions to <10 complexity

  Verify each change:
  - Measure before/after metrics
  - Run tests to ensure functionality intact

  Report improvements with ACTUAL metrics.
  """
})
```

6. **Present results:**

**IMPORTANT - Dynamic Results Generation:**
Generate results from ACTUAL optimizations applied. Use this template with REAL metrics:

```markdown
Optimization Complete! ✓

[For each category optimized:]

[Category] Optimizations:
[For each optimization applied:]
✓ [ACTUAL optimization] in <real-file>:<real-function>
  Before: [ACTUAL_BEFORE_METRIC]
  After: [ACTUAL_AFTER_METRIC]
  Improvement: [CALCULATED_IMPROVEMENT]%

Overall Impact:

Performance:
- API response time: [BEFORE] → [AFTER] ([IMPROVEMENT]% faster)
- Database load: [REDUCTION]%
- Concurrent users: [BEFORE] → [AFTER] ([MULTIPLIER]x)

Build & Deploy:
- Docker image: [BEFORE] → [AFTER] ([REDUCTION]% smaller)
- Build time: [BEFORE] → [AFTER] ([IMPROVEMENT]% faster)

Code Quality:
- Codebase size: [REDUCTION]% (easier to maintain)
- Complexity: All functions <[MAX_COMPLEXITY]
- Dead code: [RESULT]

Pain Point Impact:
✓ Addresses Pain #5 (significant time waste)
  - [ACTUAL time savings based on optimizations]

✓ Addresses Pain #2 (tech debt)
  - [ACTUAL debt reduction]

Performance score: [BEFORE] → [AFTER] (+[DELTA] points)

Next Steps:
1. Test: [actual test command for this project]
2. Load test: [if applicable]
3. Monitor: [if applicable]
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
# Optimize database queries (with before/after metrics)
/cco-optimize --database

# Reduce Docker image size (with before/after metrics)
/cco-optimize --docker

# Optimize frontend bundle (with before/after metrics)
/cco-optimize --bundle

# Comprehensive optimization (all areas)
/cco-optimize --all

# With additional context (optional prompt)
/cco-optimize --database "Focus on payment queries"
/cco-optimize --docker "Target size under 100MB"
/cco-optimize --all "Conservative optimizations only, no breaking changes"

# For code cleanup, use fix instead:
/cco-fix --tech-debt

# For dependency updates, use fix instead:
/cco-fix --supply-chain
```

**Optional Prompt Support:**
Any text after the flags is treated as additional context for optimization. The AI will:
- Prioritize specific areas based on your guidance
- Apply constraints mentioned (size targets, compatibility)
- Adjust optimization aggressiveness
- Focus on domain-specific bottlenecks

---

## Integration with Other Commands

- **After /cco-audit --performance**: Fix detected issues
- **After /cco-audit --quick**: Follow optimization recommendations
- **Before deployment**: Optimize before going to production
