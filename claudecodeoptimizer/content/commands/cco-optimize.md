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
   - Principle: `C_AGENT_ORCHESTRATION_PATTERNS`
   - Skill: `cco-skill-content-optimization-automation` (for Claude Code content)
   - Measures: Model costs, execution time, parallelization efficiency
   - Optimizes: Model selection (opus→haiku), parallel execution, agent type selection
   - Analyzes: All `.md` files in `.claude/` and `content/` directories
   - Detects: Wrong model usage, sequential→parallel opportunities, inefficient agent calls

---

## Agent Optimization Analysis Algorithm (--agents)

When `--agents` optimization is selected, the following analysis is performed:

### Phase 1: Discovery - Find All Agent Usage

```python
# Scan command files
Grep("Task\\(", glob="**/.claude/commands/*.md", output_mode="content", "-n": true, "-C": 3)

# Scan skill files
Grep("Task\\(", glob="**/content/skills/*.md", output_mode="content", "-n": true, "-C": 3)

# Scan agent files
Grep("Task\\(", glob="**/content/agents/*.md", output_mode="content", "-n": true, "-C": 3)

# Extract patterns:
# - Task(..., model="opus|sonnet|haiku")
# - Multiple Task() calls in sequence
# - Single vs parallel execution patterns
```

### Phase 2: Analysis Against C_AGENT_ORCHESTRATION_PATTERNS

For each `Task()` call found, check:

**1. Model Selection Violations:**
```python
VIOLATIONS = {
    # Simple tasks using expensive models
    "opus_for_simple": {
        "pattern": r'Task\([^)]*model="opus"[^)]*\)',
        "context_keywords": ["grep", "find", "list", "count", "read", "format"],
        "severity": "high",
        "fix": "Change model from opus to haiku",
        "savings": "~60% cost reduction"
    },

    # Complex tasks using cheap models
    "haiku_for_complex": {
        "pattern": r'Task\([^)]*model="haiku"[^)]*\)',
        "context_keywords": ["architecture", "design", "algorithm", "complex", "analyze deeply"],
        "severity": "medium",
        "fix": "Change model from haiku to sonnet or opus",
        "impact": "Better quality results"
    }
}
```

**2. Parallelization Opportunities:**
```python
SEQUENTIAL_PATTERNS = {
    # Multiple independent Task() calls
    "sequential_independent": {
        "pattern": r'Task\([^)]+\)\s+# Result used\s+Task\([^)]+\)',
        "check": "Are tasks truly dependent?",
        "fix": "Batch independent tasks in single message",
        "savings": "~50% time reduction"
    }
}
```

**3. Agent Type Selection:**
```python
AGENT_TYPE_ISSUES = {
    "wrong_subagent": {
        "pattern": r'subagent_type:\s*"([^"]+)"',
        "validate_against": {
            "Explore": ["find", "search", "locate", "discover"],
            "general-purpose": ["implement", "fix", "refactor"],
            "fix-agent": ["fix violations", "apply fixes"],
        }
    }
}
```

**4. Unnecessary Agent Usage (OVER-USE):**
```python
UNNECESSARY_AGENT_PATTERNS = {
    # Agent for simple grep/search
    "agent_for_grep": {
        "pattern": r'Task\([^)]*"[Gg]rep|[Ff]ind|[Ss]earch|[Ll]ist"[^)]*\)',
        "check": "Can this be done with direct Grep/Glob tool?",
        "severity": "high",
        "fix": "Replace Task() with direct Grep/Glob call",
        "savings": "~$0.10 per call + faster execution"
    },

    # Agent for simple file read
    "agent_for_read": {
        "pattern": r'Task\([^)]*"[Rr]ead|[Oo]pen|[Cc]at"[^)]*\)',
        "check": "Can this be done with direct Read tool?",
        "severity": "high",
        "fix": "Replace Task() with direct Read call",
        "savings": "~$0.08 per call + faster"
    },

    # Agent for simple edit
    "agent_for_simple_edit": {
        "pattern": r'Task\([^)]*"[Rr]eplace|[Cc]hange|[Uu]pdate a word"[^)]*\)',
        "context_check": "Is this a simple string replacement?",
        "severity": "medium",
        "fix": "Use Edit tool directly for simple replacements",
        "savings": "~$0.05 per call + instant"
    },

    # Agent for simple bash command
    "agent_for_bash": {
        "pattern": r'Task\([^)]*"[Rr]un|[Ee]xecute.*ls|pwd|cd|cat"[^)]*\)',
        "check": "Can this be done with direct Bash tool?",
        "severity": "high",
        "fix": "Replace Task() with direct Bash call",
        "savings": "~$0.12 per call + instant"
    }
}
```

**5. Missing Agent Opportunities (UNDER-USE):**
```python
MISSING_AGENT_PATTERNS = {
    # Sequential loop that should use parallel agents
    "sequential_loop_candidates": {
        "pattern": r'for .* in .*:\s+(?:Grep|Read|Edit|Bash)\(',
        "check": "Are iterations independent? Can parallelize with multiple Task() calls?",
        "severity": "high",
        "fix": "Replace loop with parallel Task() calls",
        "benefit": "~50-80% time reduction for N items"
    },

    # Large analysis that should be decomposed
    "large_single_operation": {
        "pattern": r'(analyze|audit|review).*all.*(modules|files|components)',
        "check": "Should this be split into parallel sub-agents?",
        "severity": "medium",
        "fix": "Decompose into parallel Task() calls per module/file",
        "benefit": "Faster execution + better results"
    },

    # Complex multi-step without orchestration
    "complex_without_agents": {
        "indicators": [
            "Multiple sequential Read→Grep→Edit chains",
            "Long prompts with multiple distinct tasks",
            "Comments like 'then do X, then Y, then Z'"
        ],
        "severity": "medium",
        "fix": "Break into orchestrated Task() calls",
        "benefit": "Better error handling + parallelization"
    }
}
```

### Phase 3: Report Violations

```markdown
## Agent Usage Analysis Results

**Total Task() calls found:** {COUNT}

### 🔴 High Priority Violations ({COUNT})

**Wrong model selection (opus for simple tasks):**
1. ❌ {FILE_PATH}:{LINE_NUMBER}
   Current: `Task("Find Python files", model="opus")`
   Issue: Simple grep task using expensive model
   Fix: Change to `model="haiku"`
   Savings: ~$0.15 per execution (60% cost reduction)

2. ❌ {FILE_PATH}:{LINE_NUMBER}
   Current: `Task("List dependencies", model="opus")`
   Issue: File reading using expensive model
   Fix: Change to `model="haiku"`
   Savings: ~$0.12 per execution

### 🟡 Medium Priority Violations ({COUNT})

**Sequential execution opportunities:**
1. ⚠️ {FILE_PATH}:{LINE_NUMBER}-{LINE_NUMBER+10}
   Current: 3 independent Task() calls executed sequentially
   ```python
   Task("Analyze module A", model="sonnet")  # Wait
   Task("Analyze module B", model="sonnet")  # Wait
   Task("Analyze module C", model="sonnet")  # Wait
   ```
   Issue: Independent tasks not parallelized
   Fix: Batch in single message
   ```python
   # Single message with 3 Task calls
   Task("Analyze module A", model="sonnet")
   Task("Analyze module B", model="sonnet")
   Task("Analyze module C", model="sonnet")
   ```
   Savings: ~50% time reduction (parallel execution)

**Unnecessary agent usage (OVER-USE):**
1. ❌ {FILE_PATH}:{LINE_NUMBER}
   Current: `Task("Find all Python files", model="haiku")`
   Issue: Using agent for simple Glob operation
   Fix: Replace with `Glob("**/*.py")`
   Savings: ~$0.10 per call + instant execution (no agent overhead)

2. ❌ {FILE_PATH}:{LINE_NUMBER}
   Current: `Task("Read configuration file", model="haiku")`
   Issue: Using agent for simple file read
   Fix: Replace with `Read("config.yaml")`
   Savings: ~$0.08 per call + instant

**Missing agent opportunities (UNDER-USE):**
1. ⚠️ {FILE_PATH}:{LINE_NUMBER}-{LINE_NUMBER+20}
   Current: Sequential loop analyzing 10 modules
   ```python
   for module in modules:  # 10 iterations
       Grep(f"import.*{module}", output_mode="content")
       Read(f"src/{module}.py")
       # Process sequentially
   ```
   Issue: Sequential processing, no parallelization
   Fix: Use 10 parallel Task() calls
   ```python
   # Spawn 10 agents in parallel
   for module in modules:
       Task(f"Analyze {module} module", model="haiku")
   ```
   Benefit: ~80% time reduction (10x parallelization)

2. ⚠️ {FILE_PATH}:{LINE_NUMBER}
   Current: Single large prompt "Analyze all security, testing, and database issues"
   Issue: Complex multi-domain task in one agent
   Fix: Decompose into specialized agents
   ```python
   Task("Security audit", model="sonnet")  # Parallel
   Task("Testing audit", model="sonnet")   # Parallel
   Task("Database audit", model="sonnet")  # Parallel
   ```
   Benefit: ~60% faster + better domain-specific analysis

### 💡 Recommendations ({COUNT})

**Model upgrade opportunities:**
1. ℹ️ {FILE_PATH}:{LINE_NUMBER}
   Current: `Task("Design architecture", model="haiku")`
   Suggestion: Complex architectural work better suited for opus
   Impact: Higher quality architectural decisions

### Summary

- Total potential cost savings: {PERCENTAGE}%
- Total potential time savings: {PERCENTAGE}%
- Auto-fixable violations: {COUNT}/{TOTAL}
```

### Phase 4: Auto-Fix (If User Approves)

```python
# For each violation:
for violation in high_priority_violations:
    if violation.type == "model_selection":
        # Direct string replacement
        Edit(
            file_path=violation.file,
            old_string=f'model="{violation.current_model}"',
            new_string=f'model="{violation.recommended_model}"'
        )

    elif violation.type == "sequential_tasks":
        # Add comment suggesting parallelization
        Edit(
            file_path=violation.file,
            old_string=violation.sequential_block,
            new_string=f"# TODO: These {violation.task_count} tasks can run in parallel\n" +
                      violation.sequential_block
        )

    elif violation.type == "unnecessary_agent":
        # Remove agent, replace with direct tool
        if violation.should_use == "Glob":
            Edit(
                file_path=violation.file,
                old_string=violation.task_call,
                new_string=violation.direct_tool_call
            )
            # Example: Task("Find Python files") → Glob("**/*.py")

        elif violation.should_use == "Read":
            Edit(
                file_path=violation.file,
                old_string=violation.task_call,
                new_string=f'Read("{violation.file_to_read}")'
            )
            # Example: Task("Read config") → Read("config.yaml")

        elif violation.should_use == "Bash":
            Edit(
                file_path=violation.file,
                old_string=violation.task_call,
                new_string=f'Bash("{violation.bash_command}")'
            )
            # Example: Task("List files") → Bash("ls -la")

    elif violation.type == "missing_agent":
        # Add comment suggesting agent usage
        Edit(
            file_path=violation.file,
            old_string=violation.sequential_code,
            new_string=f"# TODO: Parallelize with {violation.suggested_agent_count} Task() calls\n" +
                      f"# Potential {violation.time_savings}% time reduction\n" +
                      violation.sequential_code
        )
        # For complex cases, provide full replacement suggestion
        if violation.can_auto_convert:
            Edit(
                file_path=violation.file,
                old_string=violation.sequential_code,
                new_string=violation.parallel_code
            )
```

### Expected Results

```markdown
## Agent Usage Optimizations Applied ✓

**Before:**
- Average cost per command execution: $0.45
- Average execution time: 45 seconds
- Parallelization efficiency: 30%

**After:**
- Average cost per command execution: $0.18 (-60%)
- Average execution time: 23 seconds (-49%)
- Parallelization efficiency: 85%

**Specific Changes:**
- ✓ Fixed 12 opus→haiku opportunities (simple tasks)
- ✓ Identified 5 sequential→parallel opportunities
- ✓ Flagged 2 haiku→sonnet upgrades (complex tasks)
- ✓ Removed 8 unnecessary agents (replaced with direct tools)
- ✓ Added 4 missing parallelization opportunities
- ✓ Decomposed 2 large single-agent tasks into parallel sub-agents

**Violation Breakdown:**
- Model selection: 14 violations fixed
- Parallelization: 5 opportunities identified
- Over-use (unnecessary agents): 8 removed
- Under-use (missing agents): 6 opportunities added

**Cost Impact:**
- Monthly savings (100 executions): $35.00
- Annual savings: $420.00
- Time savings: ~49% faster execution
```

---

## Execution Protocol

### Step 0: Introduction and Confirmation (ALWAYS FIRST)

**Before doing ANYTHING, present this introduction and get user confirmation:**

```markdown
# Optimize Command

**What I do:**
I identify and fix performance bottlenecks across 7 areas: database queries, Docker images, code quality, dependencies, frontend bundles, resilience patterns, and **agent/model usage**.

**How it works:**
1. I analyze your project to find optimization opportunities (N+1 queries, large images, dead code, inefficient agent calls, etc.)
2. I measure current metrics (query times, image sizes, bundle sizes, agent costs)
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
- **Agent optimizations (opus→haiku, parallel execution - 60% cost reduction)**

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
      question: "Select infrastructure optimizations:? (Space: select, Enter: confirm)",
      header: "Infrastructure",
      multiSelect: true,
      options: [
        {
          label: "All Infrastructure",
          description: "Select all infrastructure optimizations"
        },
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
        }
      ]
    },
    {
      question: "Select advanced optimizations:? (Space: select, Enter: confirm)",
      header: "Advanced",
      multiSelect: true,
      options: [
        {
          label: "All Advanced",
          description: "Select all advanced optimizations"
        },
        {
          label: "Performance",
          description: "Response times, circuit breakers | Measures: ms, error rate"
        },
        {
          label: "Agents",
          description: f"{task_count} Task calls found | Measures: cost, parallelization | 60% savings"
        }
      ]
    },
    {
      question: "Or select all:? (Space: select, Enter: confirm)",
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

  AGENTS: Reference C_AGENT_ORCHESTRATION_PATTERNS principle (NO skill needed)
  - Scan all .md files in .claude/ and content/ directories
  - Find Task() calls with model parameter
  - Analyze against C_AGENT_ORCHESTRATION_PATTERNS:
    * Wrong model selection (opus for simple tasks, haiku for complex)
    * Sequential execution that could be parallel
    * Multiple independent tasks not batched in single message
    * OVER-USE: Unnecessary agents for simple operations (Grep, Read, Bash)
    * UNDER-USE: Missing agent opportunities (sequential loops, large single tasks)
  - Report violations with file:line references
  - Auto-fix: Remove unnecessary agents, suggest missing parallelization
  - Suggest fixes with cost savings estimates

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
