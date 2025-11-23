---
name: cco-optimize
description: Performance optimization with before/after metrics measurement

principles: [U_EVIDENCE_BASED_ANALYSIS, U_MINIMAL_TOUCH, C_EFFICIENT_FILE_OPERATIONS]
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
  agents:
    keywords: [agent optimization, model selection, parallelization, cost optimization, task orchestration]
    category: performance
    pain_points: [5]
---

# cco-optimize

**Performance optimization with before/after metrics measurement to address Pain #5 (significant time waste).**

---

## Purpose


## Execution Guarantee

This command performs COMPLETE optimization analysis and application.
No premature scope reduction regardless of workload.

**Estimated time: Provided for transparency, NOT to limit scope.**
Measure and improve performance metrics: query times, image sizes, bundle sizes, and response times. Unlike /cco-fix which fixes issues, /cco-optimize focuses on **measuring improvements** with before/after metrics.

**Note:** For code cleanup (dead code, complexity) use `/cco-fix --tech-debt`. For dependency updates use `/cco-fix --supply-chain`.

---


## Step 0: Introduction and Confirmation

**Welcome to cco-optimize - Performance Optimization**

This command analyzes and optimizes your codebase for performance.

### What This Command Does

**Optimization Types:**
- Caching improvements
- Bundle size reduction
- Query optimization
- Agent usage efficiency
- Response time improvements

### What You'll Be Asked

1. **Confirmation** (Start optimization analysis)
2. **Optimization Selection** (Which optimizations to apply)
3. **Pre-Flight Confirmation** (Review changes before applying)

### Time Commitment

- Analysis: 3-8 minutes
- Application: 5-15 minutes
- Total: 8-23 minutes

### What You'll Get

**Optimizations Applied:**
- Performance improvements with metrics
- Before/after measurements
- Complete verification

```python
AskUserQuestion({
  questions: [{
    question: "Ready to start performance optimization?",
    header: "Confirm Start",
    multiSelect: false,
    options: [
      {
        label: "Start Optimization",
        description: "Begin performance analysis and optimization"
      },
      {
        label: "Cancel",
        description: "Exit cco-optimize"
      }
    ]
  }]
})
```

---

## 5 Optimization Types

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

5. **--agents** - Agent/model usage optimization
   - Uses agent orchestration patterns for parallel execution
   - Skill: `cco-skill-content-optimization-automation` (for Claude Code content)
   - Measures: Model costs, execution time, parallelization efficiency
   - Optimizes: Model selection (opus→haiku), parallel execution, agent type selection
   - Analyzes: All `.md` files in `.claude/` and `content/` directories
   - Detects: Wrong model usage, sequential→parallel opportunities, inefficient agent calls

---

## Agent Optimization Analysis Algorithm (--agents)

**See [AGENT_STANDARDS.md](../AGENT_STANDARDS.md) for agent delegation patterns and [C_AGENT_ORCHESTRATION_PATTERNS.md](~/.claude/principles/C_AGENT_ORCHESTRATION_PATTERNS.md) for optimization patterns.**

**Optimize-Specific Agent Analysis:**

**Phase 0: File Exclusion**
- See [AGENT_STANDARDS.md - File Discovery & Exclusion](../AGENT_STANDARDS.md#file-discovery--exclusion)
- Focus: `.claude/`, `content/` directories only

**Phase 1: Discovery**
- Grep `Task()` calls in `.claude/commands/`, `content/skills/`, `content/agents/`
- Extract model selection, parallelization patterns

**Phase 2: Analysis** (See [C_AGENT_ORCHESTRATION_PATTERNS.md](~/.claude/principles/C_AGENT_ORCHESTRATION_PATTERNS.md))
- **Violations Detected**: Model selection (opus for simple, haiku for complex), sequential→parallel opportunities, wrong agent type
- **Over-use**: Agent for grep/read/edit/bash (replace with direct tools)
- **Under-use**: Sequential loops, large single operations (should parallelize)

**Phase 3: Report** (See [COMMAND_PATTERNS.md - Pattern 8](../COMMAND_PATTERNS.md#pattern-8-dynamic-results-generation))
- **High Priority**: Model selection issues (60% cost savings)
- **Medium Priority**: Parallelization opportunities (50% time savings), unnecessary agents ($0.08-0.12 per call)
- **Recommendations**: Model upgrades for complex tasks

**Phase 4: Auto-Fix**
- Model selection: Direct Edit (opus→haiku, haiku→sonnet)
- Parallelization: Add TODO comments or auto-convert
- Over-use: Replace Task() with direct tools (Glob/Read/Bash)
- Under-use: Add parallelization suggestions

---

## Execution Protocol

**See [COMMAND_PATTERNS.md](../COMMAND_PATTERNS.md) for reusable command patterns and [AGENT_STANDARDS.md](../AGENT_STANDARDS.md) for agent delegation.**

**File Discovery**: See [AGENT_STANDARDS.md - File Discovery & Exclusion](../AGENT_STANDARDS.md#file-discovery--exclusion)

**Step 0: Introduction** (See [COMMAND_PATTERNS.md - Pattern 1](../COMMAND_PATTERNS.md#pattern-1-step-0-introduction-and-confirmation))
- **What**: Identify performance bottlenecks (database, Docker, bundle, agents)
- **How**: Analyze → Measure → Select → Optimize → Report before/after
- **Time**: 10-30 minutes
- **Confirmation**: "Yes, start optimization" | "No, cancel"

---

**Interactive Mode**: See [COMMAND_PATTERNS.md - Pattern 2](../COMMAND_PATTERNS.md#pattern-2-category-selection-multi-select-with-all)

1. **Analyze First**: Run analysis (Grep N+1, check Docker size, count unused functions), measure real metrics
2. **Tab-Based Selection**: Infrastructure (All Infrastructure | Docker | Database | Bundle) + Advanced (All Advanced | Performance | Agents) + All (All Optimizations)
3. **Selection Summary**: Display selected categories, total count, warn about skipped categories
4. **Stage 2**: For each selected category, show specific optimizations (paginated if >4)
5. **Optimization Plan**: List skills, agent (Sonnet), specific changes per category, time estimate
6. **Confirm**: "Yes, start optimization" | "No, cancel"
7. **TodoWrite**: Track progress
8. **Launch Agent**: Task (general-purpose, Sonnet) with skills per category (database/Docker/code/agents)

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

Agent/Model Usage:
- Model cost reduction: [REDUCTION]% (opus→haiku where appropriate)
- Parallelization efficiency: [IMPROVEMENT]% (sequential→parallel)
- Execution time: [BEFORE] → [AFTER] ([IMPROVEMENT]% faster)

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

# Optimize agent/model usage (with cost savings)
/cco-optimize --agents

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

## Agent Error Handling

**If optimization agent execution fails:**

AskUserQuestion({
  questions: [{
    question: "optimize-agent (Sonnet) failed: {error_message}. How to proceed?",
    header: "optimize-agent (Sonnet) Error",
    multiSelect: false,
    options: [
      {label: "Retry", description: "Run agent again with same parameters"},
      {label: "Retry with different model", description: "Try Sonnet/Haiku/Opus"},
      {label: "Manual optimization", description: "Guide manual optimization process"},
      {label: "Skip this optimization", description: "Continue with next optimization"},
      {label: "Cancel", description: "Stop entire command"}
    ]
  }]
})

**Model selection if user chooses "Retry with different model":**

AskUserQuestion({
  questions: [{
    question: "Which model to try?",
    header: "Model Selection",
    multiSelect: false,
    options: [
      {label: "Sonnet", description: "Balanced performance and cost (recommended)"},
      {label: "Haiku", description: "Faster, more affordable"},
      {label: "Opus", description: "Most capable, higher cost"}
    ]
  }]
})
