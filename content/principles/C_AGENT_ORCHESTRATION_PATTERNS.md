---
id: C_AGENT_ORCHESTRATION_PATTERNS
title: Agent Orchestration Patterns
category: claude-guidelines
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_AGENT_ORCHESTRATION_PATTERNS: Agent Orchestration Patterns 🔴

**Severity**: High

Orchestrate multiple Claude agents efficiently through parallel execution, pipeline patterns, and appropriate model selection for optimal cost and performance.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Poor orchestration** - Agents launched randomly without strategy
- **Sequential bottlenecks** - No parallelization when possible
- **Wrong model choices** - Opus for grep, Haiku for architecture
- **No pipeline thinking** - Missing dependencies between agents
- **Resource waste** - Expensive agents for trivial tasks

### Business Value
- **5x faster execution** - Smart orchestration vs ad-hoc execution
- **60% cost reduction** - Right model for each agent
- **Higher quality** - Complex reasoning when needed
- **Better scalability** - Orchestration patterns scale to large tasks
- **Predictable performance** - Systematic approach vs trial-and-error

### Technical Benefits
- **Optimal parallelism** - Maximum concurrent execution
- **Pipeline efficiency** - Dependencies handled correctly
- **Resource optimization** - Right tool for each subtask
- **Fault isolation** - Agent failures don't cascade
- **Clear progress tracking** - Understand what's happening when

### Industry Evidence
- **Kubernetes orchestration** - Container management patterns
- **Apache Airflow** - Workflow orchestration DAGs
- **AWS Step Functions** - Serverless workflow coordination
- **MapReduce** - Data processing orchestration (Google)

---

## How

### Orchestration Patterns

#### Pattern 1: Parallel Fan-Out

**When**: Multiple independent tasks

```python
# ✅ GOOD: Parallel fan-out
# Task: Analyze 5 independent modules

Task("Analyze auth module", model="haiku")
Task("Analyze payment module", model="haiku")
Task("Analyze user module", model="haiku")
Task("Analyze product module", model="haiku")
Task("Analyze order module", model="haiku")

# Result: All 5 run in parallel
# Time: ~2 minutes (vs 10 minutes sequential)
# Cost: 5 * $0.10 = $0.50
```

#### Pattern 2: Sequential Pipeline

**When**: Tasks have dependencies

```python
# ✅ GOOD: Sequential pipeline
# Task: Build → Test → Deploy

# Step 1: Build (must finish first)
Task("Build application and verify success", model="sonnet")
# Wait for completion...

# Step 2: Test (depends on build)
Task("Run test suite on built artifacts", model="sonnet")
# Wait for completion...

# Step 3: Deploy (depends on tests passing)
Task("Deploy to staging environment", model="haiku")

# Result: Each step waits for previous completion
# Time: 15 minutes (unavoidable sequential dependencies)
```

#### Pattern 3: Hierarchical Decomposition

**When**: Complex task breaks into subtasks

```python
# ✅ GOOD: Hierarchical decomposition
# Task: Comprehensive codebase audit

# Level 1: High-level analysis (Opus for strategy)
Task("""Analyze codebase structure and identify:
- Major architectural issues
- High-risk areas
- Priority audit focus areas
Return list of top 5 critical modules to audit""",
model="opus",
subagent_type="Plan")

# Level 2: Detailed audits (parallel Sonnet for analysis)
# Based on Opus recommendations, launch parallel audits:
Task("Deep security audit of auth module", model="sonnet")
Task("Deep security audit of payment module", model="sonnet")
Task("Deep security audit of user module", model="sonnet")
Task("Deep security audit of order module", model="sonnet")
Task("Deep security audit of api module", model="sonnet")

# Result: Strategic planning (Opus) → Parallel execution (Sonnet)
# Time: 8 minutes (3 min Opus + 5 min parallel Sonnet)
# Cost: $1.50 (Opus) + $1.00 (5x Sonnet) = $2.50
```

#### Pattern 4: Scatter-Gather

**When**: Parallel work needs synthesis

```python
# ✅ GOOD: Scatter-Gather pattern
# Task: Multi-perspective code review

# Scatter: Parallel reviews from different angles
Task("Review for security vulnerabilities", model="sonnet")
Task("Review for performance issues", model="sonnet")
Task("Review for code quality", model="sonnet")
Task("Review for test coverage", model="haiku")
# Wait for all to complete...

# Gather: Synthesize results (Sonnet for synthesis)
Task("""Synthesize all review findings:
- Security: [findings from agent 1]
- Performance: [findings from agent 2]
- Quality: [findings from agent 3]
- Testing: [findings from agent 4]
Create prioritized action plan""",
model="sonnet")

# Result: Multiple perspectives → unified action plan
# Time: 5 min (parallel) + 2 min (synthesis) = 7 minutes
```

---

## Implementation Patterns

### Model Selection Strategy

#### Haiku: Data Gathering Layer

```python
# ✅ GOOD: Haiku for mechanical tasks
Task("Find all files with TODOs", model="haiku")
Task("Count lines of code per module", model="haiku")
Task("Extract all function signatures", model="haiku")
Task("List all API endpoints", model="haiku")

# Cost: 4 * $0.05 = $0.20
# Time: ~1 minute (parallel)
```

#### Sonnet: Analysis & Implementation Layer

```python
# ✅ GOOD: Sonnet for development work
Task("Implement user authentication", model="sonnet")
Task("Fix memory leak in cache", model="sonnet")
Task("Optimize database queries", model="sonnet")
Task("Write integration tests", model="sonnet")

# Cost: 4 * $0.20 = $0.80
# Time: ~5 minutes (parallel)
```

#### Opus: Strategic Planning Layer

```python
# ✅ GOOD: Opus for architecture
Task("Design microservices architecture", model="opus")
Task("Evaluate database technology options", model="opus")
Task("Create disaster recovery strategy", model="opus")

# Cost: 3 * $1.50 = $4.50
# Time: ~10 minutes (parallel or sequential based on dependencies)
```

---

## Orchestration Decision Tree

```
Complex Task?
├─ Can be parallelized?
│  ├─ YES → Pattern 1: Parallel Fan-Out
│  │  └─ Model: Haiku (mechanical) or Sonnet (complex)
│  └─ NO → Pattern 2: Sequential Pipeline
│     └─ Model: Based on each step's complexity
│
└─ Needs strategic planning first?
   ├─ YES → Pattern 3: Hierarchical Decomposition
   │  └─ Level 1: Opus (planning)
   │  └─ Level 2: Parallel Sonnet/Haiku (execution)
   │
   └─ Needs synthesis after parallel work?
      └─ YES → Pattern 4: Scatter-Gather
         └─ Scatter: Parallel agents (Sonnet/Haiku)
         └─ Gather: Synthesis agent (Sonnet)
```

---

## Anti-Patterns

### ❌ No Orchestration Strategy

```python
# ❌ BAD: Ad-hoc agent launches
Task("Do something with auth")
Task("Fix the payment thing")
Task("Check users")
Task("Whatever needs doing")

# Problems:
# - Unclear goals
# - No parallelization strategy
# - Wrong models
# - No dependency handling
```

### ❌ Over-Orchestration

```python
# ❌ BAD: Too many orchestration layers
# Task: Fix a simple bug

# Layer 1: Planning agent
Task("Analyze bug and create fix plan", model="opus")  # Overkill!

# Layer 2: Implementation agents
Task("Implement part 1 of fix", model="sonnet")
Task("Implement part 2 of fix", model="sonnet")

# Layer 3: Verification agents
Task("Verify part 1", model="haiku")
Task("Verify part 2", model="haiku")

# Layer 4: Synthesis
Task("Combine and test", model="sonnet")

# ✅ BETTER: Single agent for simple bug fix
Task("Fix null pointer in getUserProfile", model="sonnet")  # Done!
```

### ❌ Ignoring Dependencies

```python
# ❌ BAD: Parallel execution of dependent tasks
Task("Create database migrations")  # Creates SQL files
Task("Run migrations")               # Needs SQL files to exist
Task("Seed test data")               # Needs tables to exist

# All launched in parallel → WILL FAIL!

# ✅ GOOD: Respect dependencies
# Step 1
Task("Create database migrations", model="haiku")
# Wait...
# Step 2
Task("Run migrations", model="haiku")
# Wait...
# Step 3
Task("Seed test data", model="haiku")
```

---

## Cost Optimization Strategies

### Strategy 1: Haiku for Data, Sonnet for Logic

```python
# ❌ EXPENSIVE: All Opus
Task("Find all Python files", model="opus")       # $1.00
Task("Read config files", model="opus")           # $0.80
Task("Analyze architecture", model="opus")        # $1.50
Task("List dependencies", model="opus")           # $0.60
# Total: $3.90

# ✅ OPTIMIZED: Right model for each task
Task("Find all Python files", model="haiku")      # $0.05
Task("Read config files", model="haiku")          # $0.03
Task("Analyze architecture", model="opus")        # $1.50 (needs Opus!)
Task("List dependencies", model="haiku")          # $0.02
# Total: $1.60 (59% savings!)
```

### Strategy 2: Parallel Haiku > Sequential Opus

```python
# ❌ EXPENSIVE: One Opus doing everything
Task("""Analyze all 10 modules for:
- Security issues
- Performance problems
- Code quality
- Test coverage
""", model="opus")  # $3.00, 20 minutes

# ✅ OPTIMIZED: 10 parallel Haiku agents
for module in ["mod1", "mod2", ..., "mod10"]:
    Task(f"Quick analysis of {module}", model="haiku")
# Total: $0.50, 3 minutes (6x faster, 6x cheaper!)
```

### Strategy 3: Hybrid Orchestration

```python
# ✅ OPTIMAL: Opus planning + Haiku execution
# Step 1: Opus creates strategy
Task("Analyze codebase and identify top 5 critical issues",
     model="opus")  # $1.50
# Returns: [issue1, issue2, issue3, issue4, issue5]

# Step 2: Parallel Haiku fixes
Task(f"Fix {issue1}", model="haiku")  # $0.10
Task(f"Fix {issue2}", model="haiku")  # $0.10
Task(f"Fix {issue3}", model="haiku")  # $0.10
Task(f"Fix {issue4}", model="haiku")  # $0.10
Task(f"Fix {issue5}", model="haiku")  # $0.10

# Total: $2.00, 8 minutes
# Alternative (all Opus): $7.50, 25 minutes
# Savings: 73% cost, 68% time!
```

---

## Real-World Scenarios

### Scenario 1: Microservices Audit

**Goal**: Audit 5 microservices for security

**Orchestration**:
```python
# Parallel fan-out (independent services)
Task("Security audit of auth-service", model="sonnet")
Task("Security audit of payment-service", model="sonnet")
Task("Security audit of user-service", model="sonnet")
Task("Security audit of order-service", model="sonnet")
Task("Security audit of shipping-service", model="sonnet")

# Result: 5 services audited in parallel
# Time: 5 minutes (vs 25 minutes sequential)
# Cost: 5 * $0.20 = $1.00
```

### Scenario 2: Feature Implementation

**Goal**: Implement email notifications

**Orchestration**:
```python
# Sequential pipeline (dependencies)
# Step 1: Design
Task("Design email notification system", model="opus")
# Wait for completion... (3 min, $1.50)

# Step 2: Implementation (parallel)
Task("Implement email templates", model="sonnet")
Task("Implement send logic", model="sonnet")
Task("Implement queue system", model="sonnet")
# Wait for all... (5 min parallel, $0.60)

# Step 3: Testing
Task("Write comprehensive tests", model="sonnet")
# (3 min, $0.20)

# Total: 11 minutes, $2.30
```

### Scenario 3: Codebase Refactoring

**Goal**: Refactor to use TypeScript strict mode

**Orchestration**:
```python
# Hierarchical decomposition
# Level 1: Planning (Opus)
Task("""Analyze codebase and create TypeScript migration plan:
- Identify files needing most work
- Estimate effort per module
- Suggest migration order
""", model="opus")
# Result: Migration plan with priorities
# (5 min, $1.50)

# Level 2: Parallel migration (Sonnet)
for module in top_10_modules:
    Task(f"Migrate {module} to TypeScript strict mode",
         model="sonnet")
# (7 min parallel, $2.00)

# Level 3: Integration (Sonnet)
Task("Integrate all migrated modules and fix type errors",
     model="sonnet")
# (5 min, $0.20)

# Total: 17 minutes, $3.70
# Alternative (manual): 2-3 days
```

---

## Implementation Checklist

Before orchestrating agents:

- [ ] **Identified pattern?** (Fan-out/Pipeline/Hierarchical/Scatter-Gather)
- [ ] **Dependencies mapped?** Know what depends on what
- [ ] **Parallelization identified?** Max parallel execution
- [ ] **Models selected?** Right model for each agent
- [ ] **Cost estimated?** Total orchestration cost acceptable
- [ ] **Time estimated?** Expected completion time
- [ ] **Error handling planned?** What if an agent fails?

---

## Cross-References

**Related Principles:**
- **C_PARALLEL_AGENTS** - Detailed parallel execution patterns
- **C_MODEL_SELECTION** - Choosing appropriate model for each agent
- **C_TOKEN_OPTIMIZATION** - Optimizing context for agents
- **C_CONTEXT_WINDOW_MGMT** - Managing context across orchestration

---

## Summary

**Agent Orchestration Patterns** means systematically orchestrating multiple Claude agents through parallel fan-out, sequential pipelines, hierarchical decomposition, and scatter-gather patterns with appropriate model selection.

**Core Patterns:**
- **Fan-Out**: Parallel independent tasks (Haiku/Sonnet)
- **Pipeline**: Sequential dependencies (respect order)
- **Hierarchical**: Planning (Opus) → Execution (Sonnet/Haiku)
- **Scatter-Gather**: Parallel work → Synthesis

**Remember**: "Orchestrate strategically - parallel when possible, sequential when necessary, hierarchical for complexity."

**Impact**: 5x faster execution, 60% cost reduction, optimal resource utilization.
