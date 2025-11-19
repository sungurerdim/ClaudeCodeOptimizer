---
name: agent-orchestration-patterns
description: Orchestrate multiple agents via parallel execution, pipelines, and appropriate model selection for optimal cost/performance
type: claude
severity: high
keywords: [orchestration, parallel execution, agent management, cost optimization, workflow]
category: [workflow, performance]
---

# C_AGENT_ORCHESTRATION_PATTERNS: Agent Orchestration Patterns

**Severity**: High

Orchestrate multiple agents via parallel execution, pipelines, and appropriate model selection for optimal cost/performance.

---

## Why

Poor orchestration wastes resources through sequential bottlenecks, wrong model choices (Opus for grep, Haiku for architecture), and lack of parallelization strategy.

---

## Patterns

### 1. Parallel Fan-Out
**When**: Independent tasks
```python
# 5 modules in parallel (significantly faster than sequential)
Task("Analyze auth module", model="haiku")
Task("Analyze payment module", model="haiku")
Task("Analyze user module", model="haiku")
Task("Analyze product module", model="haiku")
Task("Analyze order module", model="haiku")
# Cost-efficient parallel execution
```

### 2. Sequential Pipeline
**When**: Dependencies exist
```python
# Build → Test → Deploy
Task("Build application", model="sonnet")  # Wait
Task("Run test suite", model="sonnet")     # Wait
Task("Deploy to staging", model="haiku")
```

### 3. Hierarchical Decomposition
**When**: Complex task breaks into subtasks
```python
# Strategy (Opus) → Parallel execution (Sonnet)
Task("Identify top 5 critical modules", model="opus")  # Planning phase
# Then parallel:
Task("Audit auth module", model="sonnet")  # Execution phase
Task("Audit payment module", model="sonnet")
Task("Audit user module", model="sonnet")
# Faster execution with optimized cost
```

### 4. Scatter-Gather
**When**: Parallel work needs synthesis
```python
# Scatter: Parallel reviews
Task("Security review", model="sonnet")
Task("Performance review", model="sonnet")
Task("Quality review", model="sonnet")
# Gather: Synthesize
Task("Create action plan from reviews", model="sonnet")
```

---

## Model Selection

| Model | Speed | Cost | Use For |
|-------|-------|------|---------|
| **Haiku** | Fastest | Cheapest | Grep, format, read, simple edits |
| **Sonnet** | Balanced | Mid | Features, bugs, code review (default) |
| **Opus** | Slowest | Highest | Architecture, complex algorithms |

---

## Cost Optimization

```python
# ❌ EXPENSIVE: All Opus
Task("Find Python files", model="opus")    # Expensive for simple task
Task("Read configs", model="opus")         # Expensive for simple task
Task("Analyze architecture", model="opus") # Appropriate complexity
Task("List dependencies", model="opus")    # Expensive for simple task

# ✅ OPTIMIZED: Right model (significant savings)
Task("Find Python files", model="haiku")   # Cheap, fast
Task("Read configs", model="haiku")        # Cheap, fast
Task("Analyze architecture", model="opus") # Appropriate complexity
Task("List dependencies", model="haiku")   # Cheap, fast
```

---

## Checklist

- [ ] Pattern identified? (Fan-out/Pipeline/Hierarchical/Scatter-Gather)
- [ ] Dependencies mapped?
- [ ] Parallelization opportunities?
- [ ] Right model per agent?
- [ ] Cost estimated?
- [ ] Error handling planned?
