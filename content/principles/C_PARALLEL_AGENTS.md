---
id: C_PARALLEL_AGENTS
title: Use Parallel Agents for Performance
category: claude-guidelines
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_PARALLEL_AGENTS: Use Parallel Agents for Performance 🔴

**Severity**: High

Launch multiple Claude agents in parallel (single message) for 2-5x speedup on independent tasks.

**Enforcement**: SHOULD

**Project Types**: all
**Languages**: all

---

## Why

### The Problem
- **Sequential bottlenecks** - Waiting for agent1 before starting agent2
- **Wasted parallelism** - Multiple independent tasks run one-by-one
- **Slow execution** - 15 minutes sequential vs 3 minutes parallel
- **Resource underutilization** - API can handle concurrent requests
- **Poor user experience** - Long waits for simple multi-task operations

### Business Value
- **3-5x faster execution** - Parallel agents vs sequential
- **Better developer experience** - Rapid feedback on complex tasks
- **Higher throughput** - More work completed per session
- **Cost efficiency** - Faster completion = fewer context switches
- **Improved productivity** - No waiting for sequential operations

### Technical Benefits
- **True parallelism** - Multiple agents execute simultaneously
- **Independent progress** - One agent failure doesn't block others
- **Scalable workflows** - Easily add more parallel agents
- **Efficient resource usage** - Maximize API throughput
- **Faster iteration** - Quick feedback loops

### Industry Evidence
- **MapReduce** - Parallel data processing (Google)
- **Kubernetes** - Parallel pod deployments
- **CI/CD pipelines** - Parallel test execution (GitHub Actions, GitLab CI)
- **Multicore processors** - Parallel thread execution
- **Async programming** - Concurrent I/O operations

---

## How

### Parallel Execution Strategy

**Critical Rule:** Launch ALL agents in a SINGLE message for true parallelism.

#### ❌ Wrong: Sequential Execution

```python
# Agent 1
Task("Analyze module A", model="sonnet")
# Wait for completion...

# Agent 2 (separate message)
Task("Analyze module B", model="sonnet")
# Wait for completion...

# Result: 10 minutes total (5 + 5 sequential)
```

#### ✅ Right: Parallel Execution

```python
# Single message with multiple Task() calls
Task("Analyze module A", model="sonnet")
Task("Analyze module B", model="sonnet")
Task("Analyze module C", model="sonnet")
# All execute simultaneously

# Result: 5 minutes total (parallel execution)
# Speedup: 3x faster!
```

---

## Implementation Patterns

### Pattern 1: Parallel Module Analysis

✅ **Good: Parallel Analysis**
```python
# Goal: Analyze 5 independent modules

# Single message with 5 parallel agents
Task("Analyze auth module for security issues",
     model="haiku",
     subagent_type="Audit")

Task("Analyze payment module for security issues",
     model="haiku",
     subagent_type="Audit")

Task("Analyze user module for security issues",
     model="haiku",
     subagent_type="Audit")

Task("Analyze product module for security issues",
     model="haiku",
     subagent_type="Audit")

Task("Analyze order module for security issues",
     model="haiku",
     subagent_type="Audit")

# Result: 5 agents run in parallel
# Time: ~2 minutes (vs 10 minutes sequential)
# Cost: 5 * $0.10 = $0.50 (same as sequential, but 5x faster!)
```

❌ **Bad: Sequential Analysis**
```python
# Message 1
Task("Analyze auth module", model="haiku")
# Wait... 2 minutes

# Message 2
Task("Analyze payment module", model="haiku")
# Wait... 2 minutes

# Message 3
Task("Analyze user module", model="haiku")
# Wait... 2 minutes

# Message 4
Task("Analyze product module", model="haiku")
# Wait... 2 minutes

# Message 5
Task("Analyze order module", model="haiku")
# Wait... 2 minutes

# Result: 10 minutes total (sequential)
```

### Pattern 2: Parallel File Updates

✅ **Good: Parallel Edits**
```python
# Goal: Update 10 configuration files

# Single message with 10 parallel agents
for config_file in [
    "frontend/config.ts",
    "backend/config.py",
    "api/settings.py",
    "database/config.json",
    "cache/redis.conf",
    "queue/rabbitmq.conf",
    "search/elasticsearch.yml",
    "logging/config.yaml",
    "monitoring/prometheus.yml",
    "nginx/nginx.conf"
]:
    Task(f"Update API endpoint in {config_file} from old.example.com to new.example.com",
         model="haiku",
         subagent_type="general-purpose")

# Result: All 10 files updated in parallel
# Time: ~1 minute (vs 10 minutes sequential)
```

### Pattern 3: Parallel Test Execution

✅ **Good: Parallel Testing**
```python
# Goal: Run tests for 4 microservices

# Single message with 4 parallel agents
Task("Run tests for auth-service and report results",
     model="sonnet",
     subagent_type="general-purpose")

Task("Run tests for payment-service and report results",
     model="sonnet",
     subagent_type="general-purpose")

Task("Run tests for user-service and report results",
     model="sonnet",
     subagent_type="general-purpose")

Task("Run tests for order-service and report results",
     model="sonnet",
     subagent_type="general-purpose")

# Result: All 4 test suites run in parallel
# Time: ~3 minutes (vs 12 minutes sequential)
# Speedup: 4x faster!
```

---

## When to Use Parallel Agents

### ✅ Good Candidates for Parallelization

**Independent modules:**
```python
# ✅ GOOD: Each module independent
Task("Refactor auth module")
Task("Refactor payment module")
Task("Refactor order module")
# No dependencies between modules
```

**Multiple file searches:**
```python
# ✅ GOOD: Searching different directories
Task("Find all TODO comments in src/frontend/")
Task("Find all TODO comments in src/backend/")
Task("Find all TODO comments in src/api/")
# Independent searches
```

**Parallel analysis:**
```python
# ✅ GOOD: Analyzing different aspects
Task("Check for security vulnerabilities")
Task("Check for performance issues")
Task("Check for code quality issues")
# Different analysis types, no dependencies
```

**Multi-service operations:**
```python
# ✅ GOOD: Independent services
Task("Deploy auth-service to staging")
Task("Deploy payment-service to staging")
Task("Deploy user-service to staging")
# Services deploy independently
```

### ❌ Bad Candidates (Must Be Sequential)

**Dependent operations:**
```python
# ❌ BAD: Can't parallelize dependencies
Task("Create database migrations")  # Must finish first
Task("Run migrations")               # Depends on migrations existing
Task("Seed test data")               # Depends on tables existing
# These MUST be sequential
```

**Shared state modifications:**
```python
# ❌ BAD: Both modify same file
Task("Add function A to utils.py")
Task("Add function B to utils.py")
# Race condition! Both agents edit same file
# Use single agent to modify same file
```

**Ordered execution:**
```python
# ❌ BAD: Order matters
Task("Build application")   # Must be first
Task("Run tests")            # Needs build artifacts
Task("Create Docker image")  # Needs successful tests
# These MUST be sequential
```

---

## Anti-Patterns

### ❌ Sequential Launch (Multiple Messages)

```python
# Message 1
Task("Analyze module1")
# Response arrives... then send Message 2

# Message 2
Task("Analyze module2")
# Response arrives... then send Message 3

# Message 3
Task("Analyze module3")

# Result: 3x slower than necessary!
```

### ❌ Forgetting to Parallelize

```python
# ❌ BAD: One agent doing multiple independent tasks
Task("""
Analyze these 10 modules for security issues:
- auth
- payment
- user
- product
- order
- inventory
- shipping
- notification
- analytics
- reporting
""", model="sonnet")

# Result: One agent does all 10 sequentially (30 minutes!)

# ✅ GOOD: 10 parallel agents
for module in ["auth", "payment", "user", ...]:
    Task(f"Analyze {module} for security issues", model="haiku")

# Result: All 10 in parallel (3 minutes)
```

### ❌ Parallelizing Dependent Tasks

```python
# ❌ BAD: These have dependencies!
Task("Create new API endpoint in api/users.py")
Task("Write tests for new API endpoint in tests/test_api.py")
Task("Update API documentation in docs/api.md")

# Problem: Tests/docs depend on endpoint implementation!
# Agents may fail or create inconsistent results

# ✅ GOOD: Sequential for dependencies
# 1. Create endpoint (one agent)
# 2. Then parallel: tests + docs (two agents)
```

---

## Optimal Agent Count

### 2-3 Agents: Ideal Sweet Spot

```python
# ✅ OPTIMAL: 2-3 parallel agents
Task("Analyze frontend for performance", model="haiku")
Task("Analyze backend for performance", model="haiku")
Task("Analyze database queries", model="haiku")

# Result: Good parallelism, manageable results
```

### 4-10 Agents: Diminishing Returns

```python
# ⚠️ CAUTION: 10 agents may be overkill for small tasks
for i in range(10):
    Task(f"Analyze module{i}", model="haiku")

# Result: Parallel execution, but:
# - 10 separate reports to review
# - Potential API rate limiting
# - Harder to synthesize results
```

### 10+ Agents: Coordination Overhead

```python
# ❌ TOO MANY: 20+ agents hard to manage
for file in all_files:  # 50 files
    Task(f"Analyze {file}", model="haiku")

# Problems:
# - 50 separate reports
# - Overwhelming to review
# - API rate limits may kick in
# - Coordination overhead

# ✅ BETTER: Batch into groups
# 10 agents, each handling 5 files
```

---

## Performance Comparison

### Scenario: Analyze 5 Microservices

**Sequential Execution (Bad):**
```
Agent 1: auth-service     → 5 minutes
Agent 2: payment-service  → 5 minutes
Agent 3: user-service     → 5 minutes
Agent 4: order-service    → 5 minutes
Agent 5: shipping-service → 5 minutes
Total: 25 minutes
```

**Parallel Execution (Good):**
```
All 5 agents launch simultaneously:
├─ Agent 1: auth-service     }
├─ Agent 2: payment-service  }  All complete
├─ Agent 3: user-service     }  in ~5 minutes
├─ Agent 4: order-service    }  (longest agent)
└─ Agent 5: shipping-service }

Total: 5 minutes (5x speedup!)
```

---

## Implementation Checklist

Before launching agents, verify:

- [ ] **Are tasks independent?** No shared state modifications
- [ ] **Can they run in parallel?** No dependencies between tasks
- [ ] **Launching in single message?** All Task() calls in one response
- [ ] **Appropriate model selected?** Haiku for simple, Sonnet for complex
- [ ] **Manageable agent count?** 2-10 agents is optimal
- [ ] **Clear task descriptions?** Each agent knows what to do
- [ ] **Results reviewable?** Can handle multiple reports

---

## Model Selection for Parallel Agents

### Haiku for High Parallelism (Cost-Effective)

```python
# ✅ GOOD: 10 Haiku agents in parallel
for module in ["mod1", "mod2", ..., "mod10"]:
    Task(f"Find unused imports in {module}", model="haiku")

# Cost: 10 * $0.05 = $0.50
# Time: ~2 minutes
```

### Sonnet for Balanced Tasks

```python
# ✅ GOOD: 3 Sonnet agents for complex analysis
Task("Analyze security vulnerabilities", model="sonnet")
Task("Analyze performance bottlenecks", model="sonnet")
Task("Analyze code quality issues", model="sonnet")

# Cost: 3 * $0.20 = $0.60
# Time: ~5 minutes
```

### Avoid Parallel Opus (Expensive)

```python
# ⚠️ CAUTION: Parallel Opus is expensive
Task("Design architecture for module A", model="opus")  # $1.50
Task("Design architecture for module B", model="opus")  # $1.50
Task("Design architecture for module C", model="opus")  # $1.50
# Total: $4.50 (consider if all three need Opus reasoning)
```

---

## Cross-References

**Related Principles:**
- **C_MODEL_SELECTION** - Choose appropriate model for parallel agents
- **C_AGENT_ORCHESTRATION_PATTERNS** - Detailed orchestration strategies
- **C_TOKEN_OPTIMIZATION** - Optimize context for parallel execution
- **C_CONTEXT_WINDOW_MGMT** - Manage context across multiple agents

---

## Summary

**Parallel Agents** means launching multiple independent Claude agents in a single message for 3-5x faster execution on complex multi-task operations.

**Core Rules:**
- **Single message** - All Task() calls in one response for true parallelism
- **Independent tasks** - No dependencies or shared state modifications
- **2-10 agents optimal** - Manageable parallelism without coordination overhead
- **Right model** - Haiku for simple, Sonnet for complex, avoid parallel Opus

**Remember**: "One message with many agents > many messages with one agent each."

**Impact**: 3-5x faster execution, better resource utilization, improved developer experience.
